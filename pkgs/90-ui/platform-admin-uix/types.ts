export interface AdminSession {
  authenticated: boolean;
  session_id?: string | null;
  user_id?: string | null;
  tenant_id?: string | null;
  username?: string | null;
  email?: string | null;
  is_admin: boolean;
  is_superuser: boolean;
  must_change_password: boolean;
  roles: string[];
}

export interface Tenant {
  id: string;
  realm_id?: string | null;
  slug: string;
  name: string;
  email: string;
  is_active?: boolean;
  created_at?: string | null;
  updated_at?: string | null;
}

export interface Identity {
  id: string;
  tenant_id: string;
  username: string;
  email: string;
  is_active: boolean;
  is_admin: boolean;
  is_superuser: boolean;
  must_change_password: boolean;
  roles: string[];
  created_at?: string | null;
  updated_at?: string | null;
}

export interface Realm {
  id: string;
  slug: string;
  name: string;
  issuer_path: string;
  description?: string | null;
  created_at?: string | null;
  updated_at?: string | null;
}

export interface CreateTenantInput {
  realm_id?: string | null;
  slug: string;
  name: string;
  email: string;
}

export interface CreateRealmInput {
  slug: string;
  name: string;
  issuer_path?: string | null;
  description?: string | null;
}

export interface UpdateRealmInput {
  slug?: string;
  name?: string;
  issuer_path?: string | null;
  description?: string | null;
}

export interface UpdateTenantInput {
  realm_id?: string | null;
  slug?: string;
  name?: string;
  email?: string;
  is_active?: boolean;
}

export interface CreateIdentityInput {
  tenant_id: string;
  username: string;
  email: string;
  password: string;
  is_admin: boolean;
  is_superuser: boolean;
  must_change_password: boolean;
}

export interface UpdateIdentityInput {
  username?: string;
  email?: string;
  is_active?: boolean;
  is_admin?: boolean;
  is_superuser?: boolean;
  must_change_password?: boolean;
  roles?: string[];
}
