import { API_BASE_URL, apiUrl } from "./backendSurface";
import type {
  CreateTenantClientInput,
  CreateTenantIdentityInput,
  KeyRotationEvent,
  TenantAdminSession,
  TenantClient,
  TenantConsent,
  TenantIdentity,
  UpdateTenantClientInput,
  UpdateTenantIdentityInput
} from "../types";

type Fetcher = typeof fetch;

const defaultFetcher: Fetcher = (input, init) => globalThis.fetch(input, init);

export class TenantAdminClient {
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

  login(identifier: string, password: string) {
    return this.request<TenantAdminSession>("/admin/auth/login", {
      method: "POST",
      body: JSON.stringify({ identifier, password })
    });
  }

  session() {
    return this.request<TenantAdminSession>("/admin/auth/session");
  }

  logout() {
    return this.request<TenantAdminSession>("/admin/auth/logout", { method: "POST" });
  }

  identities() {
    return this.request<TenantIdentity[]>("/user");
  }

  createIdentity(payload: CreateTenantIdentityInput) {
    return this.request<TenantIdentity>("/user", {
      method: "POST",
      body: JSON.stringify(payload)
    });
  }

  updateIdentity(identityId: string, payload: UpdateTenantIdentityInput) {
    return this.request<TenantIdentity>(`/user/${identityId}`, {
      method: "PATCH",
      body: JSON.stringify(payload)
    });
  }

  lockIdentity(identityId: string) {
    return this.updateIdentity(identityId, { is_active: false });
  }

  unlockIdentity(identityId: string) {
    return this.updateIdentity(identityId, { is_active: true });
  }

  deleteIdentity(identityId: string) {
    return this.request<TenantIdentity>(`/user/${identityId}`, { method: "DELETE" });
  }

  clients() {
    return this.request<TenantClient[]>("/client");
  }

  createClient(payload: CreateTenantClientInput) {
    return this.request<TenantClient>("/client", {
      method: "POST",
      body: JSON.stringify(payload)
    });
  }

  updateClient(clientId: string, payload: UpdateTenantClientInput) {
    return this.request<TenantClient>(`/client/${clientId}`, {
      method: "PATCH",
      body: JSON.stringify(payload)
    });
  }

  deleteClient(clientId: string) {
    return this.request<TenantClient>(`/client/${clientId}`, { method: "DELETE" });
  }

  consents() {
    return this.request<TenantConsent[]>("/consent");
  }

  revokeConsent(consentId: string) {
    return this.request<TenantConsent>(`/consent/${consentId}`, { method: "DELETE" });
  }

  keyEvents() {
    return this.request<KeyRotationEvent[]>("/keyrotationevent");
  }

  triggerKeyRotation(payload: { tenant_id?: string; reason?: string }) {
    return this.request<KeyRotationEvent>("/keyrotationevent", {
      method: "POST",
      body: JSON.stringify(payload)
    });
  }
}

export const tenantAdminClient = new TenantAdminClient();
