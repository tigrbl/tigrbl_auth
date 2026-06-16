
export type OidcClaimSet = Record<string, unknown>;

export interface OidcSessionContext {
  id_token: OidcClaimSet;
  access_token: OidcClaimSet;
  userinfo: OidcClaimSet;
  client: {
    provider: 'generic';
    client_id: string;
    issuer: string;
    scope: string;
    token_type?: string;
  };
  authorization_request: {
    nonce?: string;
    redirect_uri: string;
  };
}

export interface User {
  id: string;
  email: string;
  name: string;
  picture?: string;
  provider: 'generic';
  isEmailVerified: boolean;
  mfaEnabled: boolean;
  oidcContext?: OidcSessionContext;
}

export interface PlatformConfig {
  // Brand Identity
  name: string;
  logoLetter: string;

  // Visual Tokens (CSS Variables)
  primaryColor: string;
  secondaryColor: string;
  backgroundColor: string;
  borderRadius: string; // e.g. "12px"

  // Navigation & URLs
  postLoginRedirectUri: string; // Dynamic landing/callback page

  // Content Labels
  loginTitle: string;
  loginSubtitle: string;
  registerTitle: string;
  registerSubtitle: string;
  footerText: string;
  supportEmail: string;

  // Embed Metadata
  embedTitle: string;
  embedDescription: string;
  embedImage: string;
  embedUrl: string;

  // Feature Flags
  enableBrandingSettings: boolean;
  enableAdapterSettings: boolean;
}

export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  resetRequestSent?: boolean;
  mfaPending?: boolean;
  verificationEmailSent?: boolean;
}

export interface OidcConfig {
  clientId: string;
  redirectUri: string;
  scope: string;
  authority: string;
  responseType?: string;
  loginEndpoint?: string;
  authorizationEndpoint?: string;
  tokenEndpoint?: string;
  userinfoEndpoint?: string;
  endSessionEndpoint?: string;
}

export interface DiscoveredIdentityProvider {
  provider_id: string;
  kind: "social" | "sso" | "federation";
  issuer: string;
  authorization_endpoint: string;
  display_name?: string;
  logout_supported?: boolean;
  scopes?: string[];
  tenant_id?: string;
}

export interface OidcDiscoveryMetadata {
  issuer: string;
  authorization_endpoint?: string;
  token_endpoint?: string;
  userinfo_endpoint?: string;
  registration_endpoint?: string;
  password_recovery_endpoint?: string;
  password_reset_endpoint?: string;
  mfa_verification_endpoint?: string;
  email_verification_endpoint?: string;
  email_verification_resend_endpoint?: string;
  revocation_endpoint?: string;
  end_session_endpoint?: string;
  passwordless_authentication_endpoint?: string;
  webauthn_registration_endpoint?: string;
  webauthn_authentication_endpoint?: string;
  device_identity_endpoint?: string;
  workload_identity_endpoint?: string;
  trust_federation_endpoint?: string;
  amr_values_supported?: string[];
  acr_values_supported?: string[];
  identity_providers?: DiscoveredIdentityProvider[];
  terms_of_service_uri?: string;
  jwks_uri?: string;
  [key: string]: unknown;
}

export enum AuthProvider {
  GENERIC = 'generic'
}
