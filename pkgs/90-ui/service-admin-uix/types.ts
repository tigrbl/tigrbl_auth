export interface ServiceAdminSession {
  authenticated: boolean;
  email: string;
  operator_id: string;
  tenant_id: string;
  username: string;
  roles: string[];
}

export interface ServiceIdentity {
  id: string;
  name?: string | null;
  tenant_id?: string | null;
  subject?: string | null;
  is_active?: boolean;
  created_at?: string | null;
}

export interface CreateServiceIdentityInput {
  name: string;
  tenant_id?: string;
  subject?: string;
  is_active?: boolean;
}

export interface UpdateServiceIdentityInput {
  name?: string;
  subject?: string;
  is_active?: boolean;
}

export interface ServiceKey {
  id: string;
  service_id?: string | null;
  kid?: string | null;
  status?: string | null;
  created_at?: string | null;
}

export interface CreateServiceKeyInput {
  service_id: string;
  kid?: string;
  algorithm?: string;
}

export interface ApiKeyRecord {
  id: string;
  service_id?: string | null;
  name?: string | null;
  scopes?: string[];
  status?: string | null;
}

export interface CreateApiKeyInput {
  service_id: string;
  name: string;
  scopes?: string[];
}

export interface UpdateApiKeyInput {
  name?: string;
  scopes?: string[];
  status?: string;
}

export interface TokenRecord {
  id: string;
  subject?: string | null;
  client_id?: string | null;
  scopes?: string[];
  status?: string | null;
  expires_at?: string | null;
}

export interface ResourceMetadata {
  resource?: string;
  authorization_servers?: string[];
  scopes_supported?: string[];
  bearer_methods_supported?: string[];
}

export interface IntrospectionResult {
  active?: boolean;
  sub?: string;
  client_id?: string;
  scope?: string;
  exp?: number;
}
