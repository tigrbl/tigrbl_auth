import { gateway_rpc } from './jsonRpcService';
import type { Alert, OAuthClient, PolicyGate, Tenant, TelemetryData, User } from '../types';
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
  const payload = await response.json().catch(() => ({}));
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

export const backendService = {
  async getTenants(): Promise<Tenant[]> {
    const tenants = await supportedRpcResult<any[]>('tenant.list', {}, []);
    return tenants.map((tenant) => ({
      id: String(tenant.id ?? tenant.tenant_id ?? tenant.slug ?? tenant.name),
      name: String(tenant.name ?? tenant.title ?? tenant.tenant_id ?? tenant.id),
      slug: String(tenant.slug ?? tenant.tenant_id ?? tenant.id),
      description: tenant.description,
      created_at: tenant.created_at,
    }));
  },

  async createTenant(tenant: Pick<Tenant, 'name' | 'slug' | 'description'>): Promise<Tenant> {
    return supportedRpcResult<Tenant>('tenant.create', tenant, {
      id: tenant.slug,
      name: tenant.name,
      slug: tenant.slug,
      description: tenant.description,
    });
  },

  async deleteTenant(id: string): Promise<void> {
    await supportedRpcResult('tenant.delete', { id }, undefined);
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
};
