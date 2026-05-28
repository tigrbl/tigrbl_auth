import { API_BASE_URL, apiUrl } from "./backendSurface";
import type { AdminSession, CreateIdentityInput, CreateTenantInput, Identity, Tenant } from "../types";

type Fetcher = typeof fetch;

const defaultFetcher: Fetcher = (input, init) => globalThis.fetch(input, init);

export class PlatformAdminClient {
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
        // Keep the HTTP status when the response is not JSON.
      }
      throw new Error(detail);
    }

    return response.json() as Promise<T>;
  }

  baseUrl() {
    return API_BASE_URL;
  }

  login(identifier: string, password: string) {
    return this.request<AdminSession>("/admin/auth/login", {
      method: "POST",
      body: JSON.stringify({ identifier, password })
    });
  }

  session() {
    return this.request<AdminSession>("/admin/auth/session");
  }

  logout() {
    return this.request<AdminSession>("/admin/auth/logout", { method: "POST" });
  }

  tenants() {
    return this.request<Tenant[]>("/admin/tenant");
  }

  createTenant(payload: CreateTenantInput) {
    return this.request<Tenant>("/admin/tenant", {
      method: "POST",
      body: JSON.stringify(payload)
    });
  }

  deleteTenant(tenantId: string) {
    return this.request<Tenant>(`/admin/tenant/${tenantId}`, { method: "DELETE" });
  }

  identities(tenantId: string) {
    const params = new URLSearchParams({ tenant_id: tenantId });
    return this.request<Identity[]>(`/admin/identities?${params.toString()}`);
  }

  createIdentity(payload: CreateIdentityInput) {
    return this.request<Identity>("/admin/identities", {
      method: "POST",
      body: JSON.stringify(payload)
    });
  }
}

export const platformAdminClient = new PlatformAdminClient();
