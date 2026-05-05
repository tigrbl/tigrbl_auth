import { gateway_rpc } from './jsonRpcService';
import type { Alert, OAuthClient, PolicyGate, Realm, TelemetryData, User } from '../types';

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
  async getRealms(): Promise<Realm[]> {
    const tenants = await supportedRpcResult<any[]>('tenant.list', {}, []);
    return tenants.map((tenant) => ({
      id: String(tenant.id ?? tenant.tenant_id ?? tenant.slug ?? tenant.name),
      name: String(tenant.name ?? tenant.title ?? tenant.tenant_id ?? tenant.id),
      slug: String(tenant.slug ?? tenant.tenant_id ?? tenant.id),
      description: tenant.description,
      created_at: tenant.created_at,
    }));
  },

  async createRealm(realm: Pick<Realm, 'name' | 'slug' | 'description'>): Promise<Realm> {
    return supportedRpcResult<Realm>('tenant.create', realm, {
      id: realm.slug,
      name: realm.name,
      slug: realm.slug,
      description: realm.description,
    });
  },

  async deleteRealm(id: string): Promise<void> {
    await supportedRpcResult('tenant.delete', { id }, undefined);
  },

  async getUsers(realmId: string): Promise<User[]> {
    const users = await supportedRpcResult<User[]>('identity.list', {}, []);
    return users.filter((user) => user.realm_id === realmId);
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

  async getClients(realmId: string): Promise<OAuthClient[]> {
    const clients = await supportedRpcResult<OAuthClient[]>('client.list', {}, []);
    return clients.filter((client) => client.realm_id === realmId);
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

  async getPolicies(realmId: string): Promise<PolicyGate[]> {
    const policies = await supportedRpcResult<PolicyGate[]>('policy.list', {}, []);
    return policies.filter((policy) => policy.realm_id === realmId);
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
