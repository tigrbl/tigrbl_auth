import { describe, expect, it } from 'vitest';

import {
  buildPhase5WorkflowSummary,
  summarizeGovernanceWorkflows,
  summarizePluginRuntime,
  summarizeSdkEcosystem,
  type AccessReviewRecord,
  type EntitlementGrant,
  type PluginDescriptor,
  type ScimProvisioningRecord,
  type SdkDescriptor,
} from './governanceWorkflow';

const sdks: SdkDescriptor[] = [
  {
    sdk_id: 'sdk-python',
    language: 'python',
    version: '0.3.4',
    compatible_runtime_range: ['0.3.0', '0.3.9'],
    generated_contracts: { openapi: '3.1.0', openrpc: '1.3.2' },
    auth_helpers: ['pkce', 'client_secret_basic'],
  },
  {
    sdk_id: 'sdk-ts',
    language: 'typescript',
    version: '0.3.4',
    compatible_runtime_range: ['0.3.0', '0.3.9'],
    generated_contracts: { openapi: '3.1.0', openrpc: '1.3.2' },
    auth_helpers: ['pkce', 'refresh_token'],
  },
];

const plugins: PluginDescriptor[] = [
  {
    plugin_id: 'plugin-audit-export',
    extension_points: ['audit.export'],
    lifecycle_hooks: ['before-export'],
    isolation_mode: 'process',
    enabled: true,
    operator_controls: ['audit', 'disable'],
    last_outcome: 'succeeded',
  },
  {
    plugin_id: 'plugin-faulty',
    extension_points: ['audit.export'],
    lifecycle_hooks: ['before-export'],
    isolation_mode: 'process',
    enabled: false,
    operator_controls: ['audit', 'disable'],
    last_outcome: 'failed',
  },
];

const scim: ScimProvisioningRecord[] = [
  {
    tenant_id: 'tenant-a',
    users: 2,
    groups: 1,
    schemas: ['urn:ietf:params:scim:schemas:core:2.0:User', 'urn:ietf:params:scim:schemas:core:2.0:Group'],
  },
];

const entitlements: EntitlementGrant[] = [
  {
    assignment_id: 'ent-1',
    tenant_id: 'tenant-a',
    subject_id: 'alice',
    entitlement_id: 'ent-admin-console',
    active: true,
  },
  {
    assignment_id: 'ent-2',
    tenant_id: 'tenant-a',
    subject_id: 'bob',
    entitlement_id: 'ent-audit-export',
    active: false,
  },
];

const reviews: AccessReviewRecord[] = [
  {
    campaign_id: 'campaign-q2',
    tenant_id: 'tenant-a',
    status: 'open',
    pending_items: 1,
    escalated_items: 1,
    revoked_items: 1,
  },
  {
    campaign_id: 'campaign-q1',
    tenant_id: 'tenant-a',
    status: 'closed',
    pending_items: 0,
    escalated_items: 0,
    revoked_items: 0,
  },
];

describe('governanceWorkflow', () => {
  it('summarizes SDK compatibility and contract alignment', () => {
    expect(
      summarizeSdkEcosystem({
        runtimeVersion: '0.3.4',
        expectedContracts: { openapi: '3.1.0', openrpc: '1.3.2' },
        sdks,
      }),
    ).toEqual({
      compatible_sdk_ids: ['sdk-python', 'sdk-ts'],
      aligned_sdk_ids: ['sdk-python', 'sdk-ts'],
      languages: ['python', 'typescript'],
    });
  });

  it('summarizes plugin runtime health and isolation posture', () => {
    expect(summarizePluginRuntime(plugins)).toEqual({
      enabled_plugin_ids: ['plugin-audit-export'],
      failing_plugin_ids: ['plugin-faulty'],
      isolation_modes: ['process'],
    });
  });

  it('summarizes SCIM, entitlement, and access review workflows', () => {
    expect(summarizeGovernanceWorkflows({ scim, entitlements, reviews })).toEqual({
      scim_tenants: ['tenant-a'],
      managed_user_count: 2,
      managed_group_count: 1,
      active_entitlement_count: 1,
      open_campaign_count: 1,
      escalated_item_count: 1,
      revoked_item_count: 1,
    });
  });

  it('builds the Phase 5 operator workflow summary', () => {
    const summary = buildPhase5WorkflowSummary({
      runtimeVersion: '0.3.4',
      expectedContracts: { openapi: '3.1.0', openrpc: '1.3.2' },
      sdks,
      plugins,
      scim,
      entitlements,
      reviews,
    });

    expect(summary.sdk_ecosystem.aligned_sdk_ids).toEqual(['sdk-python', 'sdk-ts']);
    expect(summary.extensibility.enabled_plugin_ids).toEqual(['plugin-audit-export']);
    expect(summary.governance.active_entitlement_count).toBe(1);
    expect(summary.governance.open_campaign_count).toBe(1);
  });
});
