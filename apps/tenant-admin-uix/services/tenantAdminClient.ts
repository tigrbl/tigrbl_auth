import { API_BASE_URL, apiUrl } from "./backendSurface";
import type { KeyRotationEvent, TenantAdminSession, TenantClient, TenantConsent, TenantIdentity } from "../types";

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
    return this.request<TenantAdminSession>("/auth/admin/login", {
      method: "POST",
      body: JSON.stringify({ identifier, password })
    });
  }

  session() {
    return this.request<TenantAdminSession>("/auth/admin/session");
  }

  logout() {
    return this.request<TenantAdminSession>("/auth/admin/logout", { method: "POST" });
  }

  identities() {
    return this.request<TenantIdentity[]>("/user");
  }

  clients() {
    return this.request<TenantClient[]>("/client");
  }

  consents() {
    return this.request<TenantConsent[]>("/consent");
  }

  keyEvents() {
    return this.request<KeyRotationEvent[]>("/keyrotationevent");
  }
}

export const tenantAdminClient = new TenantAdminClient();
