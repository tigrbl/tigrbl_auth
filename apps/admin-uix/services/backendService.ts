import { gateway_rpc } from './jsonRpcService';
import type { Alert, OAuthClient, PolicyGate, Tenant, TelemetryData, User } from '../types';

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
    const users = await supportedRpcResult<any[]>('identity.list', { tenant_id: tenantId }, []);
    return users
      .map((user) => ({ ...user, tenant_id: user.tenant_id }))
      .filter((user) => user.tenant_id === tenantId);
  },

  async createUser(user: User): Promise<User> {
    return supportedRpcResult<User>('identity.create', user, user);
  },

  async updateUser(user: User): Promise<User> {
    return supportedRpcResult<User>('identity.update', user, user);
  },

  async deleteUser(id: string): Promise<void> {
    await supportedRpcResult('identity.delete', { id }, undefined);
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
