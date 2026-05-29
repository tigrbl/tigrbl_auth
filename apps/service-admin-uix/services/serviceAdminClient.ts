import { API_BASE_URL, apiUrl } from "./backendSurface";
import type { ApiKeyRecord, IntrospectionResult, ResourceMetadata, ServiceIdentity, ServiceKey, TokenRecord } from "../types";

type Fetcher = typeof fetch;

const defaultFetcher: Fetcher = (input, init) => globalThis.fetch(input, init);

export class ServiceAdminClient {
  constructor(private readonly fetcher: Fetcher = defaultFetcher) {}

  private async request<T>(path: string, init: RequestInit = {}): Promise<T> {
    const response = await this.fetcher(apiUrl(path), {
      credentials: "include",
      headers: {
        "content-type": "application/json",
        ...(init.headers || {})
      },
      ...init
    });

    if (!response.ok) {
      let detail = `${response.status} ${response.statusText}`.trim();
      try {
        const payload = await response.json();
        detail = payload.detail || payload.error || detail;
      } catch {
        // Keep HTTP status fallback.
      }
      throw new Error(detail);
    }

    return response.json() as Promise<T>;
  }

  baseUrl() {
    return API_BASE_URL;
  }

  services() {
    return this.request<ServiceIdentity[]>("/service");
  }

  serviceKeys() {
    return this.request<ServiceKey[]>("/servicekey");
  }

  apiKeys() {
    return this.request<ApiKeyRecord[]>("/apikey");
  }

  tokenRecords() {
    return this.request<TokenRecord[]>("/tokenrecord");
  }

  resourceMetadata() {
    return this.request<ResourceMetadata>("/.well-known/oauth-protected-resource");
  }

  introspect(token = "local-demo-token") {
    return this.request<IntrospectionResult>("/introspect", {
      method: "POST",
      body: JSON.stringify({ token })
    });
  }
}

export const serviceAdminClient = new ServiceAdminClient();
