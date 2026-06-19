
export type UUID = string;

export type Tenant = {
  id: UUID;
  name: string;
  slug: string;
  email?: string;
  created_at?: string;
  description?: string;
};

export enum UserStatus {
  ACTIVE = 'ACTIVE',
  PENDING = 'PENDING',
  SUSPENDED = 'SUSPENDED',
  REVOKED = 'REVOKED'
}

export type User = {
  id: UUID;
  tenant_id: UUID;
  username: string;
  email: string;
  roles: string[];
  status: UserStatus;
  last_login?: string;
  mfa_device?: string;
  bio?: string;
  mfa_enabled?: boolean;
  is_admin?: boolean;
  is_superuser?: boolean;
  must_change_password?: boolean;
  created_at?: string;
  updated_at?: string;
};

export type OAuthClient = {
  id: UUID;
  tenant_id: UUID;
  name: string;
  client_id: UUID;
  client_secret?: string;
  redirect_uris: string[];
  type: 'public' | 'confidential';
  created_at?: string;
};

export type PolicyType = 'CEDAR' | 'OPA';

export type PolicyGate = {
  id: UUID;
  tenant_id: UUID;
  name: string;
  type: PolicyType;
  content: string;
  is_active: boolean;
  version: number;
  last_updated?: string;
};

export type ServiceAccount = {
  id: UUID;
  name: string;
  api_key: string;
  scopes: string[];
};

export type Alert = {
  id: UUID;
  severity: 'low' | 'medium' | 'high';
  message: string;
  timestamp: string;
};

export type TelemetryData = {
  timestamp: string;
  requests: number;
  latency: number;
  errors: number;
};

export type JwksKeyLifecycle = 'active' | 'next' | 'retired' | string;

export type TenantJwksPublicationKey = {
  kid: string;
  alg: string;
  kty: string;
  use: string;
  crv?: string;
  lifecycle: JwksKeyLifecycle;
  public: boolean;
  created_at?: string;
  updated_at?: string;
  rotated_at?: string;
  retired_at?: string;
};

export type TenantJwksKeyInput = {
  kid: string;
  label?: string;
  status?: JwksKeyLifecycle;
  alg?: string;
  kty?: string;
  use?: string;
  crv?: string;
  x?: string;
  n?: string;
  e?: string;
  publish?: boolean;
};

export type TenantJwksPublicationView = {
  tenant_slug: string;
  issuer: string;
  jwks_uri: string;
  publication_status: 'published' | 'not_published';
  parity_indicator: string;
  keys: TenantJwksPublicationKey[];
  keys_by_lifecycle: Record<string, TenantJwksPublicationKey[]>;
};

export type PolicyControlPlane = {
  bootstrap: (policies: PolicyGate[]) => void;
  syncPolicy: (policy: PolicyGate) => Promise<unknown>;
  removePolicy: (policy_id: string) => Promise<unknown>;
  bulkSync: (policies: PolicyGate[]) => Promise<unknown>;
  getPolicyStatus: (policy_id: string) => Promise<unknown>;
};
