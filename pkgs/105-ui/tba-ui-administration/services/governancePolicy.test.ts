import { describe, expect, it } from 'vitest';

import type { OAuthClient, Tenant } from '../types';
import {
  ADMIN_CLIENT_FIELDS,
  authorizeClientMutation,
  buildComplianceSummary,
  DEFAULT_DELEGATED_MUTABLE_FIELDS,
  DEFAULT_DELEGATED_VISIBLE_FIELDS,
  exposeClientRecord,
  filterVisibleTenants,
  PUBLIC_CLIENT_FIELDS,
  type DelegatedAdminScope,
} from './governancePolicy';

const scope: DelegatedAdminScope = {
  subject: 'operator:tenant-a',
  tenant_ids: ['tenant-a'],
  permissions: ['client.read', 'client.update'],
};

const tenants: Tenant[] = [
  { id: 'tenant-a', name: 'Tenant A', slug: 'tenant-a' },
  { id: 'tenant-b', name: 'Tenant B', slug: 'tenant-b' },
];

const client: OAuthClient = {
  id: 'client-1',
  tenant_id: 'tenant-a',
  name: 'Portal',
  client_id: '9f4f0fc7-fce0-4d67-a6b4-8f8bd7cdca5e',
  client_secret: 'sk_live_secret',
  redirect_uris: ['https://portal.example/callback'],
  type: 'confidential',
  created_at: '2026-05-05T00:00:00+00:00',
};

describe('governancePolicy', () => {
  it('filters visible tenants for delegated administration', () => {
    expect(filterVisibleTenants(tenants, scope).map((tenant) => tenant.id)).toEqual(['tenant-a']);
    expect(filterVisibleTenants(tenants).map((tenant) => tenant.id)).toEqual(['tenant-a', 'tenant-b']);
  });

  it('redacts client records for delegated and public planes', () => {
    expect(exposeClientRecord(client, 'admin', scope)).toEqual({
      id: 'client-1',
      tenant_id: 'tenant-a',
      name: 'Portal',
      client_id: '9f4f0fc7-fce0-4d67-a6b4-8f8bd7cdca5e',
      redirect_uris: ['https://portal.example/callback'],
      type: 'confidential',
      created_at: '2026-05-05T00:00:00+00:00',
    });

    expect(exposeClientRecord(client, 'public')).toEqual({
      name: 'Portal',
      client_id: '9f4f0fc7-fce0-4d67-a6b4-8f8bd7cdca5e',
      redirect_uris: ['https://portal.example/callback'],
      type: 'confidential',
    });
  });

  it('enforces delegated client mutation authority', () => {
    expect(authorizeClientMutation('tenant-a', { name: 'Portal 2' }, scope)).toEqual({
      allowed: true,
      reason: 'permission granted by delegated admin scope',
    });

    expect(authorizeClientMutation('tenant-b', { name: 'Portal 2' }, scope)).toEqual({
      allowed: false,
      reason: 'permission denied by delegated tenant scope',
    });

    expect(authorizeClientMutation('tenant-a', { client_secret: 'rotated' }, scope)).toEqual({
      allowed: false,
      reason: 'permission denied by delegated client mutation scope',
    });
  });

  it('builds a compliance summary for delegated admin visibility', () => {
    const summary = buildComplianceSummary({
      tenants,
      clients: [client],
      scope,
      roleCount: 3,
      policyCount: 4,
      auditEventCount: 5,
      serviceIdentityCount: 2,
    });

    expect(summary.tenant_isolation).toEqual({
      enforced: true,
      visible_tenant_ids: ['tenant-a'],
    });
    expect(summary.delegated_admin).toEqual({
      active: true,
      subject: 'operator:tenant-a',
      permission_count: 2,
    });
    expect(summary.client_exposure.visible_fields).toEqual(DEFAULT_DELEGATED_VISIBLE_FIELDS);
    expect(summary.client_exposure.redacted_fields).toEqual(
      ADMIN_CLIENT_FIELDS.filter((field) => !DEFAULT_DELEGATED_VISIBLE_FIELDS.includes(field)),
    );
    expect(summary.service_identities.configured).toBe(2);
    expect(summary.policy_engine.audit_event_count).toBe(5);
  });

  it('documents the default field contracts for delegated and public planes', () => {
    expect(DEFAULT_DELEGATED_MUTABLE_FIELDS).toEqual(['name', 'redirect_uris', 'type']);
    expect(PUBLIC_CLIENT_FIELDS).toEqual(['name', 'client_id', 'redirect_uris', 'type']);
  });
});
