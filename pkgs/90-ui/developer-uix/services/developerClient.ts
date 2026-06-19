import { API_BASE_URL, apiUrl } from "./backendSurface";
import type { ClientRegistration, CreateClientRegistrationInput, DeveloperApplication, IssuerMetadata, UpdateClientRegistrationInput } from "../types";

type Fetcher = typeof fetch;

const defaultFetcher: Fetcher = (input, init) => globalThis.fetch(input, init);

function pathSegment(value: string) {
  return encodeURIComponent(value);
}

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

  application(clientId: string) {
    return this.request<DeveloperApplication>(`/client/${pathSegment(clientId)}`);
  }

  updateApplication(clientId: string, payload: UpdateClientRegistrationInput) {
    return this.request<DeveloperApplication>(`/client/${pathSegment(clientId)}`, {
      method: "PATCH",
      body: JSON.stringify(payload)
    });
  }

  deleteApplication(clientId: string) {
    return this.request<DeveloperApplication>(`/client/${pathSegment(clientId)}`, { method: "DELETE" });
  }

  clientRegistrations() {
    return this.request<ClientRegistration[]>("/clientregistration");
  }

  clientRegistration(registrationId: string) {
    return this.request<ClientRegistration>(`/clientregistration/${pathSegment(registrationId)}`);
  }

  updateClientRegistration(registrationId: string, payload: UpdateClientRegistrationInput) {
    return this.request<ClientRegistration>(`/clientregistration/${pathSegment(registrationId)}`, {
      method: "PATCH",
      body: JSON.stringify(payload)
    });
  }

  deleteClientRegistration(registrationId: string) {
    return this.request<ClientRegistration>(`/clientregistration/${pathSegment(registrationId)}`, { method: "DELETE" });
  }

  discovery() {
    return this.request<IssuerMetadata>("/.well-known/openid-configuration");
  }

  registerClient(payload: CreateClientRegistrationInput) {
    return this.request<ClientRegistration>("/register", {
      method: "POST",
      body: JSON.stringify(payload)
    });
  }
}

export const developerClient = new DeveloperClient();
