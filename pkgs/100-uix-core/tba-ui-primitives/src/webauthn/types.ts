export interface WebAuthnTransport {
  fetch(input: RequestInfo | URL, init?: RequestInit): Promise<Response>;
}

export interface RegistrationIdentity {
  userName: string;
  displayName: string;
}

export interface AuthenticationIdentity {
  userName?: string;
  conditional?: boolean;
}

export interface WebAuthnResult {
  ok: boolean;
  [key: string]: unknown;
}
