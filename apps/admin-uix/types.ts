
export type UUID = string;

export type Tenant = {
  id: UUID;
  name: string;
  slug: string;
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

export type PolicyControlPlane = {
  bootstrap: (policies: PolicyGate[]) => void;
  syncPolicy: (policy: PolicyGate) => Promise<unknown>;
  removePolicy: (policy_id: string) => Promise<unknown>;
  bulkSync: (policies: PolicyGate[]) => Promise<unknown>;
  getPolicyStatus: (policy_id: string) => Promise<unknown>;
};
