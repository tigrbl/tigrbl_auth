import { gateway_rpc } from './jsonRpcService';
import type { Alert, OAuthClient, PolicyGate, Tenant, TelemetryData, TenantJwksKeyInput, TenantJwksPublicationKey, TenantJwksPublicationView, User } from '../types';
import { UserStatus } from '../types';

const toError = (error: unknown): Error => {
  if (error instanceof Error) {
    return error;
  }
  return new Error('Unknown backend error');
};

async function rpcResult<T>(method: string, params: unknown = {}): Promise<T> {
  try {
    const response = await gateway_rpc.call<T>(method, params);
    if (response.error) {
      throw new Error(response.error.message);
    }
    return response.result as T;
  } catch (error) {
    throw toError(error);
  }
}

async function supportedRpcResult<T>(method: string, params: unknown, fallback: T): Promise<T> {
  const supported = await gateway_rpc.hasMethod(method);
  if (!supported) {
    return fallback;
  }
  return rpcResult<T>(method, params);
}

async function restJson<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(path, {
    headers: {
      Accept: 'application/json',
      ...(init?.headers ?? {}),
    },
    ...init,
  });
  const contentType = response.headers.get('content-type') ?? '';
  const expectsJson = contentType.toLowerCase().includes('application/json');
  if (!expectsJson) {
    const preview = await response.text().catch(() => '');
    const suffix = preview ? ` Body starts with: ${preview.slice(0, 80)}` : '';
    throw new Error(`Expected JSON response from ${path}, received ${contentType || 'unknown content type'}.${suffix}`);
  }
  let payload: any;
  try {
    payload = await response.json();
  } catch (error) {
    throw new Error(`Expected JSON response from ${path}, but the JSON payload could not be parsed.`);
  }
  if (!response.ok) {
    throw new Error(String(payload?.detail || payload?.error || `HTTP ${response.status}`));
  }
  return payload as T;
}

function normalizeUser(user: any): User {
  return {
    id: String(user.id),
    tenant_id: String(user.tenant_id),
    username: String(user.username ?? user.email ?? user.id),
    email: String(user.email ?? ''),
    roles: Array.isArray(user.roles) ? user.roles.map(String) : [],
    status: user.is_active === false ? UserStatus.SUSPENDED : (user.must_change_password ? UserStatus.PENDING : UserStatus.ACTIVE),
    last_login: user.updated_at ?? user.created_at ?? '',
    is_admin: Boolean(user.is_admin),
    is_superuser: Boolean(user.is_superuser),
    must_change_password: Boolean(user.must_change_password),
    created_at: user.created_at,
    updated_at: user.updated_at,
  };
}

type OpenIdTenantDiscovery = {
  issuer: string;
  jwks_uri: string;
};

const lifecycleOrder: Record<string, number> = {
  active: 0,
  next: 1,
  retired: 2,
};

function sameTenant(record: any, tenant: Tenant): boolean {
  const scopedTenant = record?.tenant_slug ?? record?.tenant ?? record?.tenant_id ?? record?.metadata?.tenant_slug ?? record?.metadata?.tenant ?? record?.metadata?.tenant_id;
  return scopedTenant === tenant.slug || scopedTenant === tenant.id;
}

function normalizePublicJwk(key: any): TenantJwksPublicationKey | null {
  const kid = key?.kid;
  if (!kid) {
    return null;
  }
  return {
    kid: String(kid),
    alg: String(key?.alg ?? ''),
    kty: String(key?.kty ?? ''),
    use: String(key?.use ?? ''),
    crv: key?.crv ? String(key.crv) : undefined,
    lifecycle: String(key?.status ?? key?.publication_status ?? 'active').toLowerCase(),
    public: true,
  };
}

function normalizeInventoryKey(record: any, tenant: Tenant, publicKids: Set<string>): TenantJwksPublicationKey | null {
  if (!sameTenant(record, tenant)) {
    return null;
  }
  const data = record?.data ?? record?.metadata ?? {};
  const kid = data?.kid ?? record?.kid ?? record?.id;
  if (!kid) {
    return null;
  }
  return {
    kid: String(kid),
    alg: String(data?.alg ?? record?.alg ?? ''),
    kty: String(data?.kty ?? record?.kty ?? ''),
    use: String(data?.use ?? record?.use ?? ''),
    crv: data?.crv || data?.curve ? String(data?.crv ?? data?.curve) : undefined,
    lifecycle: String(data?.publication_status ?? record?.status ?? data?.status ?? 'active').toLowerCase(),
    public: publicKids.has(String(kid)),
    created_at: record?.created_at ? String(record.created_at) : undefined,
    updated_at: record?.updated_at ? String(record.updated_at) : undefined,
    rotated_at: data?.rotated_at ? String(data.rotated_at) : undefined,
    retired_at: data?.retired_at ? String(data.retired_at) : undefined,
  };
}

export function normalizeTenantJwksPublication(
  tenant: Tenant,
  discovery: OpenIdTenantDiscovery,
  jwks: { keys?: any[] },
  keyInventory: any[] = [],
): TenantJwksPublicationView {
  const publicKeys = (Array.isArray(jwks.keys) ? jwks.keys : [])
    .map(normalizePublicJwk)
    .filter((key): key is TenantJwksPublicationKey => key !== null);
  const rows = new Map(publicKeys.map((key) => [key.kid, key]));
  const publicKids = new Set(publicKeys.map((key) => key.kid));

  keyInventory
    .map((record) => normalizeInventoryKey(record, tenant, publicKids))
    .filter((key): key is TenantJwksPublicationKey => key !== null)
    .forEach((key) => {
      if (key.lifecycle === 'retired' || !rows.has(key.kid)) {
        rows.set(key.kid, key);
      }
    });

  const keys = Array.from(rows.values()).sort((left, right) => {
    const leftOrder = lifecycleOrder[left.lifecycle] ?? 3;
    const rightOrder = lifecycleOrder[right.lifecycle] ?? 3;
    return leftOrder - rightOrder || left.kid.localeCompare(right.kid);
  });
  const keys_by_lifecycle = keys.reduce<Record<string, TenantJwksPublicationKey[]>>((grouped, key) => {
    grouped[key.lifecycle] = [...(grouped[key.lifecycle] ?? []), key];
    return grouped;
  }, { active: [], next: [], retired: [] });

  return {
    tenant_slug: tenant.slug,
    issuer: discovery.issuer,
    jwks_uri: discovery.jwks_uri,
    publication_status: publicKeys.length > 0 ? 'published' : 'not_published',
    parity_indicator: `Matches GET /tenants/${tenant.slug}/.well-known/jwks.json`,
    keys,
    keys_by_lifecycle,
  };
}

export const backendService = {
  async getTenants(): Promise<Tenant[]> {
    const tenants = await restJson<any[]>('/admin/tenants');
    return tenants.map((tenant) => ({
      id: String(tenant.id ?? tenant.tenant_id ?? tenant.slug ?? tenant.name),
      name: String(tenant.name ?? tenant.title ?? tenant.tenant_id ?? tenant.id),
      slug: String(tenant.slug ?? tenant.tenant_id ?? tenant.id),
      email: tenant.email ? String(tenant.email) : undefined,
      description: tenant.description,
      created_at: tenant.created_at,
    }));
  },

  async createTenant(tenant: Pick<Tenant, 'name' | 'slug' | 'email'>): Promise<Tenant> {
    const created = await restJson<any>('/admin/tenants', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(tenant),
    });
    return {
      id: String(created.id ?? created.slug),
      name: String(created.name ?? tenant.name),
      slug: String(created.slug ?? tenant.slug),
      email: created.email ? String(created.email) : tenant.email,
      description: created.description,
      created_at: created.created_at,
    };
  },

  async deleteTenant(id: string): Promise<void> {
    await restJson(`/admin/tenants/${encodeURIComponent(id)}`, {
      method: 'DELETE',
    });
  },

  async getUsers(tenantId: string): Promise<User[]> {
    const users = await restJson<any[]>(`/admin/identities?tenant_id=${encodeURIComponent(tenantId)}`);
    return users.map(normalizeUser);
  },

  async createUser(
    payload: Pick<User, 'tenant_id' | 'username' | 'email'> & {
      password: string;
      is_admin?: boolean;
      is_superuser?: boolean;
      must_change_password?: boolean;
    },
  ): Promise<User> {
    const user = await restJson<any>('/admin/identities', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return normalizeUser(user);
  },

  async updateUser(
    id: string,
    payload: Partial<Pick<User, 'username' | 'email' | 'is_admin' | 'is_superuser' | 'must_change_password'>> & {
      is_active?: boolean;
      password?: string;
    },
  ): Promise<User> {
    const user = await restJson<any>(`/admin/identities/${encodeURIComponent(id)}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return normalizeUser(user);
  },

  async deleteUser(id: string): Promise<void> {
    await restJson(`/admin/identities/${encodeURIComponent(id)}`, {
      method: 'DELETE',
    });
  },

  async getClients(tenantId: string): Promise<OAuthClient[]> {
    const clients = await supportedRpcResult<any[]>('client.list', { tenant_id: tenantId }, []);
    return clients
      .map((client) => ({ ...client, tenant_id: client.tenant_id }))
      .filter((client) => client.tenant_id === tenantId);
  },

  async createClient(client: OAuthClient): Promise<OAuthClient> {
    return supportedRpcResult<OAuthClient>('client.create', client, client);
  },

  async updateClient(client: OAuthClient): Promise<OAuthClient> {
    return supportedRpcResult<OAuthClient>('client.update', client, client);
  },

  async deleteClient(id: string): Promise<void> {
    await supportedRpcResult('client.delete', { id }, undefined);
  },

  async getPolicies(tenantId: string): Promise<PolicyGate[]> {
    const policies = await supportedRpcResult<any[]>('policy.list', { tenant_id: tenantId }, []);
    return policies
      .map((policy) => ({ ...policy, tenant_id: policy.tenant_id }))
      .filter((policy) => policy.tenant_id === tenantId);
  },

  async syncPolicy(policy: PolicyGate): Promise<void> {
    await supportedRpcResult('policy.sync', { policy }, undefined);
  },

  async removePolicy(policyId: string): Promise<void> {
    await supportedRpcResult('policy.remove', { policy_id: policyId }, undefined);
  },

  async getTelemetry(): Promise<TelemetryData[]> {
    return supportedRpcResult<TelemetryData[]>('telemetry.list', {}, []);
  },

  async getAlerts(): Promise<Alert[]> {
    return supportedRpcResult<Alert[]>('alert.list', {}, []);
  },

  async getTenantJwksPublication(tenant: Tenant): Promise<TenantJwksPublicationView> {
    const discovery = await restJson<OpenIdTenantDiscovery>(`/tenants/${encodeURIComponent(tenant.slug)}/.well-known/openid-configuration`);
    const jwksPath = new URL(discovery.jwks_uri, window.location.origin).pathname;
    const jwks = await restJson<{ keys?: any[] }>(jwksPath);
    const inventory = await supportedRpcResult<any[]>('keys.list', { tenant: tenant.slug, tenant_id: tenant.id }, []);
    return normalizeTenantJwksPublication(tenant, discovery, jwks, inventory);
  },

  async seedTenantJwksKey(tenant: Tenant): Promise<void> {
    await supportedRpcResult('tenant.keys.seed', { tenant: tenant.slug, tenant_id: tenant.id }, undefined);
  },

  async createTenantJwksKey(tenant: Tenant, key: TenantJwksKeyInput): Promise<void> {
    await supportedRpcResult('tenant.keys.create', { tenant: tenant.slug, tenant_id: tenant.id, ...key }, undefined);
  },

  async updateTenantJwksKey(tenant: Tenant, key: TenantJwksKeyInput): Promise<void> {
    await supportedRpcResult('tenant.keys.update', { tenant: tenant.slug, tenant_id: tenant.id, ...key }, undefined);
  },

  async deleteTenantJwksKey(tenant: Tenant, kid: string): Promise<void> {
    await supportedRpcResult('tenant.keys.delete', { tenant: tenant.slug, tenant_id: tenant.id, kid }, undefined);
  },
};
