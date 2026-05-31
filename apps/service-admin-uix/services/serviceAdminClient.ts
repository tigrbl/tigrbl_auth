import { API_BASE_URL, apiUrl } from "./backendSurface";
import type {
  ApiKeyRecord,
  CreateApiKeyInput,
  CreateServiceIdentityInput,
  CreateServiceKeyInput,
  IntrospectionResult,
  ResourceMetadata,
  ServiceIdentity,
  ServiceKey,
  TokenRecord,
  UpdateApiKeyInput,
  UpdateServiceIdentityInput
} from "../types";

type Fetcher = typeof fetch;

const defaultFetcher: Fetcher = (input, init) => globalThis.fetch(input, init);

function pathSegment(value: string) {
  return encodeURIComponent(value);
}

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

  createService(payload: CreateServiceIdentityInput) {
    return this.request<ServiceIdentity>("/service", {
      method: "POST",
      body: JSON.stringify(payload)
    });
  }

  updateService(serviceId: string, payload: UpdateServiceIdentityInput) {
    return this.request<ServiceIdentity>(`/service/${pathSegment(serviceId)}`, {
      method: "PATCH",
      body: JSON.stringify(payload)
    });
  }

  deleteService(serviceId: string) {
    return this.request<ServiceIdentity>(`/service/${pathSegment(serviceId)}`, { method: "DELETE" });
  }

  serviceKeys() {
    return this.request<ServiceKey[]>("/servicekey");
  }

  createServiceKey(payload: CreateServiceKeyInput) {
    return this.request<ServiceKey>("/servicekey", {
      method: "POST",
      body: JSON.stringify(payload)
    });
  }

  revokeServiceKey(keyId: string) {
    return this.request<ServiceKey>(`/servicekey/${pathSegment(keyId)}`, { method: "DELETE" });
  }

  apiKeys() {
    return this.request<ApiKeyRecord[]>("/apikey");
  }

  createApiKey(payload: CreateApiKeyInput) {
    return this.request<ApiKeyRecord>("/apikey", {
      method: "POST",
      body: JSON.stringify(payload)
    });
  }

  updateApiKey(apiKeyId: string, payload: UpdateApiKeyInput) {
    return this.request<ApiKeyRecord>(`/apikey/${pathSegment(apiKeyId)}`, {
      method: "PATCH",
      body: JSON.stringify(payload)
    });
  }

  revokeApiKey(apiKeyId: string) {
    return this.request<ApiKeyRecord>(`/apikey/${pathSegment(apiKeyId)}`, { method: "DELETE" });
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
