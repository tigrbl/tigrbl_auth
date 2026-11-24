export type AppConnectionPermissionStatus =
  | "requested"
  | "available_to_request"
  | "unavailable_for_account"
  | "unavailable_for_bot";

export interface AppConnectionPermission {
  id: string;
  label: string;
  status: AppConnectionPermissionStatus;
  explicit?: boolean;
}

export interface AppConnectionBot {
  id: string;
  name: string;
  permissions: readonly AppConnectionPermission[];
}

export interface AppConnectionConsent {
  clientId: string;
  clientName: string;
  resource: string;
  permissions: readonly AppConnectionPermission[];
  bots: readonly AppConnectionBot[];
}

export interface AppConnection {
  id: string;
  clientName: string;
  botId: string | null;
  scopes: readonly string[];
}

export interface AppConnectionDecision {
  approved: boolean;
  botId: string | null;
  scopes: readonly string[];
}

export interface AppConnectionDecisionResult {
  redirectUrl: string;
}

export interface AppConnectionResponse<T> {
  path: string;
  read(body: unknown): T;
}

export interface AppConnectionsProtocol<
  Request,
  Consent extends AppConnectionConsent = AppConnectionConsent,
  Connection extends AppConnection = AppConnection,
> {
  getConsent(request: Request): AppConnectionResponse<Consent>;
  decideConsent(
    request: Request,
    decision: AppConnectionDecision,
  ): AppConnectionResponse<AppConnectionDecisionResult> & { body: unknown };
  listConnections(): AppConnectionResponse<readonly Connection[]>;
  revokeConnection(id: string): AppConnectionResponse<boolean>;
}

export interface AppConnectionsRequest {
  path: string;
  method: "GET" | "POST" | "DELETE";
  body?: unknown;
  signal?: AbortSignal;
}

export type AppConnectionsTransport = (request: AppConnectionsRequest) => Promise<unknown>;

export function createAppConnectionsClient<
  Request,
  Consent extends AppConnectionConsent,
  Connection extends AppConnection,
>(
  protocol: AppConnectionsProtocol<Request, Consent, Connection>,
  transport: AppConnectionsTransport,
) {
  async function send<T>(
    response: AppConnectionResponse<T>,
    request: Omit<AppConnectionsRequest, "path">,
  ): Promise<T> {
    return response.read(await transport({ ...request, path: response.path }));
  }

  return {
    getConsent(request: Request, signal?: AbortSignal): Promise<Consent> {
      return send(protocol.getConsent(request), { method: "GET", signal });
    },
    decideConsent(
      request: Request,
      decision: AppConnectionDecision,
      signal?: AbortSignal,
    ): Promise<AppConnectionDecisionResult> {
      const response = protocol.decideConsent(request, decision);
      return send(response, { method: "POST", body: response.body, signal });
    },
    listConnections(signal?: AbortSignal): Promise<readonly Connection[]> {
      return send(protocol.listConnections(), { method: "GET", signal });
    },
    revokeConnection(id: string, signal?: AbortSignal): Promise<boolean> {
      return send(protocol.revokeConnection(id), { method: "DELETE", signal });
    },
  };
}

export class AppConnectionsHttpError extends Error {
  constructor(readonly status: number, message: string) {
    super(message);
    this.name = "AppConnectionsHttpError";
  }
}

export interface JsonTransportOptions {
  baseUrl?: string;
  credentials?: RequestCredentials;
  getHeaders?: () => HeadersInit | Promise<HeadersInit>;
  fetch?: typeof globalThis.fetch;
}

function responseMessage(body: unknown, status: number): string {
  if (body && typeof body === "object") {
    if ("detail" in body && typeof body.detail === "string") return body.detail;
    if ("error_description" in body && typeof body.error_description === "string") {
      return body.error_description;
    }
  }
  return `Request failed (${status}).`;
}

export function createJsonAppConnectionsTransport({
  baseUrl = "",
  credentials = "same-origin",
  getHeaders,
  fetch: fetchRequest = globalThis.fetch,
}: JsonTransportOptions = {}): AppConnectionsTransport {
  const base = baseUrl.replace(/\/+$/, "");

  return async ({ path, method, body, signal }) => {
    if (!path.startsWith("/") || /^\/[\/\\]/.test(path) || /[\r\n\t]/.test(path)) {
      throw new TypeError("App connection paths must be absolute paths within the configured API.");
    }
    const headers = new Headers(await getHeaders?.());
    headers.set("accept", "application/json");
    if (body !== undefined) headers.set("content-type", "application/json");
    const response = await fetchRequest(base + path, {
      method,
      body: body === undefined ? undefined : JSON.stringify(body),
      headers,
      signal,
      credentials,
      cache: "no-store",
      redirect: "error",
    });
    if (!response.ok) {
      const errorBody: unknown = await response.json().catch(() => undefined);
      throw new AppConnectionsHttpError(response.status, responseMessage(errorBody, response.status));
    }
    return response.status === 204 ? undefined : response.json();
  };
}
