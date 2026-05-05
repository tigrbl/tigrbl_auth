import type { PolicyGate } from '../types';
import { persistCollection, readLocal, storageKeyFor, writeLocal } from './persistence';

export interface JsonRpcRequest {
  jsonrpc: '2.0';
  method: string;
  params?: any;
  id: string;
}

export interface JsonRpcResponse<T = unknown> {
  jsonrpc: '2.0';
  result?: T;
  error?: {
    code: number;
    message: string;
    data?: unknown;
  };
  id: string | number | null;
}

export type RpcDiscoverResult = {
  methods?: string[];
  active_methods?: string[];
  method_names?: string[];
  registry?: Record<string, unknown>;
};

type JsonRpcHandler = (params: unknown) => Promise<JsonRpcResponse<unknown>> | JsonRpcResponse<unknown>;

type PolicySyncRecord = {
  id: string;
  realm_id: string;
  engine: PolicyGate['type'];
  version: number;
  status: 'synced' | 'removed';
  synced_at: string;
  content_hash: string;
};

type ControlPlanePolicy = {
  id: string;
  realm_id: string;
  name: string;
  type: PolicyGate['type'];
  content: string;
  version: number;
  synced_at: string;
};

const CONTROL_PLANE_KEY = storageKeyFor('policy-control-plane');
const SYNC_RECORDS_KEY = storageKeyFor('policy-sync');

const computeHash = (value: string): string => {
  let hash = 0;
  for (let i = 0; i < value.length; i += 1) {
    hash = (hash << 5) - hash + value.charCodeAt(i);
    hash |= 0;
  }
  return `h${(hash >>> 0).toString(16)}`;
};

const generate_uuid = (): string => {
  if (typeof crypto !== "undefined" && "randomUUID" in crypto) {
    return crypto.randomUUID();
  }
  const template = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx";
  return template.replace(/[xy]/g, (char) => {
    const rand = Math.floor(Math.random() * 16);
    const value = char === "x" ? rand : (rand % 4) + 8;
    return value.toString(16);
  });
};

export class JsonRpcService {
  private endpoint: string;
  private handlers: Map<string, JsonRpcHandler>;
  private methodCatalog: Set<string> | null;

  constructor(endpoint: string) {
    this.endpoint = endpoint.replace(/\/+$/, "") || "/rpc";
    this.handlers = new Map();
    this.methodCatalog = null;
  }

  registerHandler(method: string, handler: JsonRpcHandler): void {
    this.handlers.set(method, handler);
  }

  registerHandlers(handlers: Record<string, JsonRpcHandler>): void {
    Object.entries(handlers).forEach(([method, handler]) => {
      this.registerHandler(method, handler);
    });
  }

  clearHandlers(): void {
    this.handlers.clear();
  }

  async call<T = unknown>(method: string, params: unknown = {}): Promise<JsonRpcResponse<T>> {
    const request: JsonRpcRequest = {
      jsonrpc: '2.0',
      method,
      params,
      id: generate_uuid(),
    };

    const admin_token = this.getLocalToken() ?? this.getDevToken();

    console.debug(`[JSON-RPC] Request: ${method}`, params);

    try {
      const response = await this.requestJsonRpc(request, admin_token);

      if (!response.ok) {
        return {
          jsonrpc: "2.0",
          id: request.id,
          error: {
            code: response.status,
            message: `HTTP ${response.status}`,
          },
        };
      }

      const payload = (await response.json()) as JsonRpcResponse;
      return payload;
    } catch (error) {
      return {
        jsonrpc: "2.0",
        id: request.id,
        error: {
          code: -32000,
          message: error instanceof Error ? error.message : 'Network error',
        },
      };
    }
  }

  private getLocalToken(): string | null {
    if (typeof localStorage === 'undefined') {
      return null;
    }

    const value = localStorage.getItem('tigrbl_auth_admin_api_key');
    if (!value) {
      return null;
    }

    const token = value.trim();
    if (!token || token === 'null' || token === 'undefined') {
      return null;
    }

    return token;
  }

  private getDevToken(): string | null {
    const configured_token = import.meta.env.VITE_TIGRBL_AUTH_DEV_ADMIN_API_KEY;
    if (typeof configured_token === 'string' && configured_token.trim()) {
      return configured_token.trim();
    }
    return null;
  }

  private requestJsonRpc(request: JsonRpcRequest, token: string | null): Promise<Response> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };
    if (token) {
      headers['X-API-Key'] = token;
      headers.Authorization = `Bearer ${token}`;
    }
    return fetch(this.endpoint, {
      method: 'POST',
      headers,
      body: JSON.stringify(request),
    });
  }

  async discover(): Promise<Set<string>> {
    if (this.methodCatalog) {
      return this.methodCatalog;
    }
    const response = await this.call<RpcDiscoverResult>("rpc.discover", {});
    const result = response.result ?? {};
    const fromArrays = [
      ...(result.methods ?? []),
      ...(result.active_methods ?? []),
      ...(result.method_names ?? []),
    ];
    const fromRegistry = Object.keys(result.registry ?? {});
    this.methodCatalog = new Set([...fromArrays, ...fromRegistry]);
    return this.methodCatalog;
  }

  async hasMethod(method: string): Promise<boolean> {
    const catalog = await this.discover();
    return catalog.has(method);
  }

  bootstrap(policies: PolicyGate[]): void {
    const existing = readLocal<ControlPlanePolicy[]>(CONTROL_PLANE_KEY, []);
    if (existing.length === 0 && policies.length > 0) {
      policies.forEach((policy) => {
        void this.syncLocal(policy);
      });
    }
  }

  async syncPolicy(policy: PolicyGate): Promise<JsonRpcResponse<PolicySyncRecord>> {
    return this.call('Policy.sync', { policy });
  }

  async removePolicy(policy_id: string): Promise<JsonRpcResponse<PolicySyncRecord>> {
    return this.call('Policy.remove', { policy_id });
  }

  async bulkSync(policies: PolicyGate[]): Promise<JsonRpcResponse<PolicySyncRecord[]>> {
    return this.call('Policy.bulk_sync', { policies });
  }

  async getPolicyStatus(policy_id: string): Promise<JsonRpcResponse<PolicySyncRecord | null>> {
    return this.call('Policy.status', { policy_id });
  }

  private updateControlPlane(policies: ControlPlanePolicy[]): void {
    writeLocal(CONTROL_PLANE_KEY, policies);
    void persistCollection('policy_control_plane', policies);
  }

  private updateSyncRecords(records: PolicySyncRecord[]): void {
    writeLocal(SYNC_RECORDS_KEY, records);
    void persistCollection('policy_sync', records);
  }

  private syncLocal(policy: PolicyGate): PolicySyncRecord {
    const existingPolicies = readLocal<ControlPlanePolicy[]>(CONTROL_PLANE_KEY, []);
    const synced_at = new Date().toISOString();
    const controlPlanePolicy: ControlPlanePolicy = {
      id: policy.id,
      realm_id: policy.realm_id,
      name: policy.name,
      type: policy.type,
      content: policy.content,
      version: policy.version,
      synced_at,
    };

    const updatedPolicies = [
      ...existingPolicies.filter((entry) => entry.id !== policy.id),
      controlPlanePolicy,
    ];

    this.updateControlPlane(updatedPolicies);

    const record: PolicySyncRecord = {
      id: policy.id,
      realm_id: policy.realm_id,
      engine: policy.type,
      version: policy.version,
      status: 'synced',
      synced_at,
      content_hash: computeHash(policy.content),
    };

    this.updateSyncRecords(this.mergeSyncRecord(record));
    return record;
  }

  private removeLocal(policy_id: string): PolicySyncRecord {
    const existingPolicies = readLocal<ControlPlanePolicy[]>(CONTROL_PLANE_KEY, []);
    const existingPolicy = existingPolicies.find((entry) => entry.id === policy_id);
    const updatedPolicies = existingPolicies.filter((entry) => entry.id !== policy_id);
    this.updateControlPlane(updatedPolicies);

    const synced_at = new Date().toISOString();
    const record: PolicySyncRecord = {
      id: policy_id,
      realm_id: existingPolicy?.realm_id ?? 'unknown',
      engine: existingPolicy?.type ?? 'CEDAR',
      version: existingPolicy?.version ?? 0,
      status: 'removed',
      synced_at,
      content_hash: computeHash(`${policy_id}:${synced_at}`),
    };

    this.updateSyncRecords(this.mergeSyncRecord(record));
    return record;
  }

  private bulkSyncLocal(policies: PolicyGate[]): PolicySyncRecord[] {
    return policies.map((policy) => this.syncLocal(policy));
  }

  private getSyncStatus(policy_id: string): PolicySyncRecord | null {
    const records = readLocal<PolicySyncRecord[]>(SYNC_RECORDS_KEY, []);
    return records.find((record) => record.id === policy_id) ?? null;
  }

  private mergeSyncRecord(record: PolicySyncRecord): PolicySyncRecord[] {
    const records = readLocal<PolicySyncRecord[]>(SYNC_RECORDS_KEY, []);
    const next = [...records.filter((entry) => entry.id !== record.id), record];
    return next;
  }
}

export const tigrblAuthAdminRpc = new JsonRpcService(
  import.meta.env.VITE_TIGRBL_AUTH_ADMIN_RPC_URL || "/rpc",
);

export const gateway_rpc = tigrblAuthAdminRpc;
