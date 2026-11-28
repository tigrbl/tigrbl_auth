export interface TenantAdminSession {
  authenticated: boolean;
  session_id?: string | null;
  user_id?: string | null;
  tenant_id?: string | null;
  username?: string | null;
  email?: string | null;
  is_admin?: boolean;
  is_superuser?: boolean;
  roles?: string[];
}

export interface TenantIdentity {
  id: string;
  tenant_id?: string | null;
  username?: string | null;
  email?: string | null;
  is_active?: boolean;
  is_admin?: boolean;
  is_superuser?: boolean;
  must_change_password?: boolean;
  roles?: string[];
}

export interface CreateTenantIdentityInput {
  username: string;
  email: string;
  password: string;
  is_admin?: boolean;
  must_change_password?: boolean;
  roles?: string[];
}

export interface UpdateTenantIdentityInput {
  username?: string;
  email?: string;
  is_active?: boolean;
  is_admin?: boolean;
  must_change_password?: boolean;
  roles?: string[];
}

export interface TenantClient {
  id: string;
  client_id?: string | null;
  name?: string | null;
  redirect_uris?: string[];
  grant_types?: string[];
}

export interface CreateTenantClientInput {
  client_name: string;
  redirect_uris: string[];
  grant_types?: string[];
  scopes?: string[];
}

export interface UpdateTenantClientInput {
  client_name?: string;
  redirect_uris?: string[];
  grant_types?: string[];
  scopes?: string[];
}

export interface TenantConsent {
  id: string;
  client_id?: string | null;
  user_id?: string | null;
  scopes?: string[];
}

export interface KeyRotationEvent {
  id: string;
  tenant_id?: string | null;
  status?: string | null;
  created_at?: string | null;
}
