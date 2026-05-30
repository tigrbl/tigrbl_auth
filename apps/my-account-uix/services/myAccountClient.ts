import { API_BASE_URL } from "../defaults";
import type { AccountProfile, AccountSession, AuthorizedApp, Consent } from "../types";

type Fetcher = typeof fetch;

const defaultFetcher: Fetcher = (input, init) => globalThis.fetch(input, init);

export class MyAccountClient {
  constructor(private readonly baseUrl = API_BASE_URL, private readonly fetcher: Fetcher = defaultFetcher) {}

  private async request<T>(path: string, init: RequestInit = {}): Promise<T> {
    const response = await this.fetcher(`${this.baseUrl}${path}`, {
      credentials: "include",
      headers: {
        "content-type": "application/json",
        ...(init.headers || {})
      },
      ...init
    });
    if (!response.ok) {
      let detail = "";
      try {
        const payload = await response.json() as { detail?: unknown; message?: unknown };
        detail = String(payload.detail ?? payload.message ?? "");
      } catch {
        detail = "";
      }
      throw new Error([response.status, response.statusText, detail].filter(Boolean).join(" "));
    }
    if (response.status === 204) {
      return undefined as T;
    }
    return response.json() as Promise<T>;
  }

  profile() {
    return this.request<AccountProfile>("/account/profile");
  }

  updateProfile(payload: Partial<Pick<AccountProfile, "username" | "email">>) {
    return this.request<AccountProfile>("/account/profile", {
      method: "PATCH",
      body: JSON.stringify(payload)
    });
  }

  changePassword(currentPassword: string, newPassword: string) {
    return this.request<{ status: string; id?: string }>("/account/password/change", {
      method: "POST",
      body: JSON.stringify({ current_password: currentPassword, new_password: newPassword })
    });
  }

  sessions() {
    return this.request<AccountSession[]>("/account/sessions");
  }

  revokeSession(sessionId: string) {
    return this.request<{ status: string; id?: string }>(`/account/sessions/${sessionId}`, {
      method: "DELETE"
    });
  }

  authorizedApps() {
    return this.request<AuthorizedApp[]>("/account/authorized-apps");
  }

  revokeAuthorizedApp(clientId: string) {
    return this.request<{ status: string; id?: string }>(`/account/authorized-apps/${clientId}`, {
      method: "DELETE"
    });
  }

  consents() {
    return this.request<Consent[]>("/account/consents");
  }

  revokeConsent(consentId: string) {
    return this.request<{ status: string; id?: string }>(`/account/consents/${consentId}`, {
      method: "DELETE"
    });
  }
}

export const myAccountClient = new MyAccountClient();
