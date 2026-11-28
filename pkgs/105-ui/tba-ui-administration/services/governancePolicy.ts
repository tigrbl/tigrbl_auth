import type { OAuthClient, Tenant } from '../types';
import { readLocal, storageKeyFor } from './persistence';

export type GovernancePlane = 'admin' | 'public';

export type ClientField = keyof OAuthClient;

export type DelegatedAdminScope = {
  subject: string;
  tenant_ids: string[];
  permissions: string[];
  visible_client_fields?: ClientField[];
  mutable_client_fields?: ClientField[];
};

export type ClientMutationAuthorization = {
  allowed: boolean;
  reason: string;
};

export type ComplianceSummary = {
  tenant_isolation: {
    enforced: boolean;
    visible_tenant_ids: string[];
  };
  delegated_admin: {
    active: boolean;
    subject: string | null;
    permission_count: number;
  };
  service_identities: {
    configured: number;
  };
  policy_engine: {
    role_count: number;
    policy_count: number;
    audit_event_count: number;
  };
  client_exposure: {
    plane: GovernancePlane;
    visible_fields: string[];
    redacted_fields: string[];
    client_count: number;
  };
};

export const PUBLIC_CLIENT_FIELDS: ClientField[] = ['name', 'client_id', 'redirect_uris', 'type'];
export const ADMIN_CLIENT_FIELDS: ClientField[] = [
  'id',
  'tenant_id',
  'name',
  'client_id',
  'client_secret',
  'redirect_uris',
  'type',
  'created_at',
];
export const DEFAULT_DELEGATED_VISIBLE_FIELDS: ClientField[] = [
  'id',
  'tenant_id',
  'name',
  'client_id',
  'redirect_uris',
  'type',
  'created_at',
];
export const DEFAULT_DELEGATED_MUTABLE_FIELDS: ClientField[] = ['name', 'redirect_uris', 'type'];

const DELEGATED_SCOPE_STORAGE_KEY = storageKeyFor('delegated-admin-scope');

const hasPermission = (grants: string[], requiredPermission: string): boolean => {
  return grants.some((grant) => {
    if (grant === '*' || grant === requiredPermission) {
      return true;
    }
    if (grant.endsWith('.*')) {
      const prefix = grant.slice(0, -2);
      return requiredPermission === prefix || requiredPermission.startsWith(`${prefix}.`);
    }
    return false;
  });
};

const visibleFieldsFor = (scope?: DelegatedAdminScope | null): ClientField[] => {
  if (!scope) {
    return ADMIN_CLIENT_FIELDS;
  }
  return scope.visible_client_fields?.length ? scope.visible_client_fields : DEFAULT_DELEGATED_VISIBLE_FIELDS;
};

const mutableFieldsFor = (scope?: DelegatedAdminScope | null): ClientField[] => {
  if (!scope) {
    return ADMIN_CLIENT_FIELDS;
  }
  return scope.mutable_client_fields?.length ? scope.mutable_client_fields : DEFAULT_DELEGATED_MUTABLE_FIELDS;
};

export const loadDelegatedAdminScope = (): DelegatedAdminScope | null => {
  return readLocal<DelegatedAdminScope | null>(DELEGATED_SCOPE_STORAGE_KEY, null);
};

export const filterVisibleTenants = (tenants: Tenant[], scope?: DelegatedAdminScope | null): Tenant[] => {
  if (!scope) {
    return tenants;
  }
  const visibleIds = new Set(scope.tenant_ids);
  return tenants.filter((tenant) => visibleIds.has(tenant.id));
};

export const exposeClientRecord = (
  client: OAuthClient,
  plane: GovernancePlane,
  scope?: DelegatedAdminScope | null,
): Partial<OAuthClient> => {
  const allowedFields = new Set<ClientField>(
    plane === 'public' ? PUBLIC_CLIENT_FIELDS : visibleFieldsFor(scope),
  );
  return Object.fromEntries(
    Object.entries(client).filter(([field]) => allowedFields.has(field as ClientField)),
  ) as Partial<OAuthClient>;
};

export const authorizeClientMutation = (
  tenantId: string,
  patch: Partial<OAuthClient>,
  scope?: DelegatedAdminScope | null,
  permission = 'client.update',
): ClientMutationAuthorization => {
  if (!scope) {
    return { allowed: true, reason: 'full admin scope' };
  }
  if (!scope.tenant_ids.includes(tenantId)) {
    return { allowed: false, reason: 'permission denied by delegated tenant scope' };
  }
  if (!hasPermission(scope.permissions, permission)) {
    return { allowed: false, reason: 'permission denied by delegated admin scope' };
  }
  const mutableFields = new Set(mutableFieldsFor(scope));
  const patchFields = Object.keys(patch) as ClientField[];
  if (!patchFields.every((field) => mutableFields.has(field))) {
    return { allowed: false, reason: 'permission denied by delegated client mutation scope' };
  }
  return { allowed: true, reason: 'permission granted by delegated admin scope' };
};

export const buildComplianceSummary = ({
  plane = 'admin',
  tenants,
  clients,
  scope,
  roleCount,
  policyCount,
  auditEventCount,
  serviceIdentityCount,
}: {
  plane?: GovernancePlane;
  tenants: Tenant[];
  clients: OAuthClient[];
  scope?: DelegatedAdminScope | null;
  roleCount: number;
  policyCount: number;
  auditEventCount: number;
  serviceIdentityCount: number;
}): ComplianceSummary => {
  const visibleFields = plane === 'public' ? PUBLIC_CLIENT_FIELDS : visibleFieldsFor(scope);
  const redactedFields = ADMIN_CLIENT_FIELDS.filter((field) => !visibleFields.includes(field));
  return {
    tenant_isolation: {
      enforced: true,
      visible_tenant_ids: filterVisibleTenants(tenants, scope).map((tenant) => tenant.id),
    },
    delegated_admin: {
      active: Boolean(scope),
      subject: scope?.subject ?? null,
      permission_count: scope?.permissions.length ?? 0,
    },
    service_identities: {
      configured: serviceIdentityCount,
    },
    policy_engine: {
      role_count: roleCount,
      policy_count: policyCount,
      audit_event_count: auditEventCount,
    },
    client_exposure: {
      plane,
      visible_fields: visibleFields,
      redacted_fields: redactedFields,
      client_count: clients.length,
    },
  };
};
