export interface DeveloperSession {
  authenticated: boolean;
  developer_id: string;
  email: string;
  tenant_id: string;
  username: string;
  roles: string[];
}

export interface DeveloperApplication {
  id: string;
  client_id?: string | null;
  name?: string | null;
  redirect_uris?: string[];
  grant_types?: string[];
  scopes?: string[];
}

export interface ClientRegistration {
  id: string;
  client_id?: string | null;
  client_name?: string | null;
  redirect_uris?: string[];
  token_endpoint_auth_method?: string | null;
}

export interface CreateClientRegistrationInput {
  client_name?: string;
  redirect_uris?: string[];
  grant_types?: string[];
  response_types?: string[];
  scope?: string;
  token_endpoint_auth_method?: string;
}

export interface UpdateClientRegistrationInput {
  client_name?: string;
  redirect_uris?: string[];
  grant_types?: string[];
  scopes?: string[];
  token_endpoint_auth_method?: string;
}

export interface IssuerMetadata {
  issuer?: string;
  authorization_endpoint?: string;
  token_endpoint?: string;
  jwks_uri?: string;
  registration_endpoint?: string;
  scopes_supported?: string[];
  grant_types_supported?: string[];
  response_types_supported?: string[];
}
