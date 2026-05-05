
export interface User {
  id: string;
  email: string;
  name: string;
  picture?: string;
  provider: 'google' | 'github' | 'generic' | 'keycloak';
  isEmailVerified: boolean;
  mfaEnabled: boolean;
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
  authorizationEndpoint?: string;
  tokenEndpoint?: string;
  userinfoEndpoint?: string;
  endSessionEndpoint?: string;
}

export interface OidcDiscoveryMetadata {
  issuer: string;
  authorization_endpoint?: string;
  token_endpoint?: string;
  userinfo_endpoint?: string;
  registration_endpoint?: string;
  revocation_endpoint?: string;
  end_session_endpoint?: string;
  jwks_uri?: string;
  [key: string]: unknown;
}

export enum AuthProvider {
  GOOGLE = 'google',
  GITHUB = 'github',
  GENERIC = 'generic',
  KEYCLOAK = 'keycloak'
}
