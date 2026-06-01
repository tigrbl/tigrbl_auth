import { API_BASE_URL, apiUrl } from "./backendSurface";
import type { AdminSession, CreateIdentityInput, CreateRealmInput, CreateTenantInput, Identity, Realm, Tenant, UpdateIdentityInput, UpdateRealmInput, UpdateTenantInput } from "../types";

type Fetcher = typeof fetch;

const defaultFetcher: Fetcher = (input, init) => globalThis.fetch(input, init);

function pathSegment(value: string) {
  return encodeURIComponent(value);
}

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

  realms() {
    return this.request<Realm[]>("/admin/realm");
  }

  createRealm(payload: CreateRealmInput) {
    return this.request<Realm>("/admin/realm", {
      method: "POST",
      body: JSON.stringify(payload)
    });
  }

  updateRealm(realmId: string, payload: UpdateRealmInput) {
    return this.request<Realm>(`/admin/realm/${pathSegment(realmId)}`, {
      method: "PATCH",
      body: JSON.stringify(payload)
    });
  }

  deleteRealm(realmId: string) {
    return this.request<Realm>(`/admin/realm/${pathSegment(realmId)}`, { method: "DELETE" });
  }

  realmTenants(realmId: string) {
    return this.request<Tenant[]>(`/admin/realm/${pathSegment(realmId)}/tenant`);
  }

  tenant(tenantId: string) {
    return this.request<Tenant>(`/admin/tenant/${pathSegment(tenantId)}`);
  }

  createTenant(payload: CreateTenantInput) {
    return this.request<Tenant>("/admin/tenant", {
      method: "POST",
      body: JSON.stringify(payload)
    });
  }

  updateTenant(tenantId: string, payload: UpdateTenantInput) {
    return this.request<Tenant>(`/admin/tenant/${pathSegment(tenantId)}`, {
      method: "PATCH",
      body: JSON.stringify(payload)
    });
  }

  enableTenant(tenantId: string) {
    return this.updateTenant(tenantId, { is_active: true });
  }

  disableTenant(tenantId: string) {
    return this.updateTenant(tenantId, { is_active: false });
  }

  deleteTenant(tenantId: string) {
    return this.request<Tenant>(`/admin/tenant/${pathSegment(tenantId)}`, { method: "DELETE" });
  }

  identities(tenantId: string) {
    const params = new URLSearchParams({ tenant_id: tenantId });
    return this.request<Identity[]>(`/admin/identity?${params.toString()}`);
  }

  createIdentity(payload: CreateIdentityInput) {
    return this.request<Identity>("/admin/identity", {
      method: "POST",
      body: JSON.stringify(payload)
    });
  }

  updateIdentity(identityId: string, payload: UpdateIdentityInput) {
    return this.request<Identity>(`/admin/identity/${pathSegment(identityId)}`, {
      method: "PATCH",
      body: JSON.stringify(payload)
    });
  }

  deleteIdentity(identityId: string) {
    return this.request<Identity>(`/admin/identity/${pathSegment(identityId)}`, { method: "DELETE" });
  }
}

export const platformAdminClient = new PlatformAdminClient();
