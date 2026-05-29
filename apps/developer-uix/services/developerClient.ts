import { API_BASE_URL, apiUrl } from "./backendSurface";
import type { ClientRegistration, DeveloperApplication, IssuerMetadata } from "../types";

type Fetcher = typeof fetch;

const defaultFetcher: Fetcher = (input, init) => globalThis.fetch(input, init);

export class DeveloperClient {
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

  applications() {
    return this.request<DeveloperApplication[]>("/client");
  }

  clientRegistrations() {
    return this.request<ClientRegistration[]>("/clientregistration");
  }

  discovery() {
    return this.request<IssuerMetadata>("/.well-known/openid-configuration");
  }

  registerClient(payload: Partial<ClientRegistration>) {
    return this.request<ClientRegistration>("/register", {
      method: "POST",
      body: JSON.stringify(payload)
    });
  }
}

export const developerClient = new DeveloperClient();
