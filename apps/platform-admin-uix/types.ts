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

export interface CreateTenantInput {
  slug: string;
  name: string;
  email: string;
}

export interface UpdateTenantInput {
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
