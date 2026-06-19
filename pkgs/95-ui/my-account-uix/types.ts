export type AccountProfile = {
  id: string;
  tenant_id: string;
  username: string;
  email: string;
  is_active: boolean;
  must_change_password: boolean;
  roles: string[];
};

export type AccountSession = {
  id: string;
  tenant_id: string;
  user_id: string;
  username: string;
  client_id?: string | null;
  state: string;
  auth_time?: string | null;
  last_seen_at?: string | null;
  expires_at?: string | null;
  ended_at?: string | null;
};

export type AuthorizedApp = {
  client_id: string;
  tenant_id: string;
  scope: string;
  consent_state: string;
  granted_at?: string | null;
  revoked_at?: string | null;
};

export type Consent = {
  id: string;
  tenant_id: string;
  user_id: string;
  client_id: string;
  scope: string;
  state: string;
  granted_at?: string | null;
  revoked_at?: string | null;
};
