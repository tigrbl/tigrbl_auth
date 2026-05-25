import { extractApiErrorMessage, parseResponseBody } from './errorMessages';

export class RestService {
  private base_url: string;
  private routes: Map<string, RestHandler>;

  constructor(base_url: string) {
    this.base_url = base_url;
    this.routes = new Map();
  }

  registerRoute(method: string, path: string, handler: RestHandler): void {
    this.routes.set(`${method.toUpperCase()} ${path}`, handler);
  }

  clearRoutes(): void {
    this.routes.clear();
  }

  private async request<T>(path: string, options: RequestInit = {}): Promise<T> {
    const method = (options.method || 'GET').toUpperCase();
    const url = `${this.base_url}${path}`;
    const headers = {
      "Content-Type": "application/json",
      ...options.headers,
    };

    console.debug(`[REST] ${options.method || "GET"} ${url}`);

    const response = await fetch(url, {
      ...options,
      headers,
    });

    const parsed = await parseResponseBody(response);

    if (!response.ok) {
      throw new Error(extractApiErrorMessage(response, parsed.payload, { fallback: `HTTP ${response.status}` }));
    }

    if (response.status === 204 || parsed.payload === null) {
      return {} as T;
    }

    return parsed.payload as T;
  }

  async get<T>(path: string): Promise<T> {
    return this.request<T>(path, { method: "GET" });
  }

  async post<T>(path: string, body: unknown): Promise<T> {
    return this.request<T>(path, {
      method: "POST",
      body: JSON.stringify(body),
    });
  }

  async put<T>(path: string, body: unknown): Promise<T> {
    return this.request<T>(path, {
      method: "PUT",
      body: JSON.stringify(body),
    });
  }

  async delete<T>(path: string): Promise<T> {
    return this.request<T>(path, { method: "DELETE" });
  }
}

export const gateway_rest = new RestService('/');
