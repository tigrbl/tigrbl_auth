export type SdkDescriptor = {
  sdk_id: string;
  language: string;
  version: string;
  compatible_runtime_range: [string, string];
  generated_contracts: Record<string, string>;
  auth_helpers: string[];
};

export type PluginDescriptor = {
  plugin_id: string;
  extension_points: string[];
  lifecycle_hooks: string[];
  isolation_mode: string;
  enabled: boolean;
  operator_controls: string[];
  last_outcome?: 'succeeded' | 'failed';
};

export type ScimProvisioningRecord = {
  tenant_id: string;
  users: number;
  groups: number;
  schemas: string[];
};

export type EntitlementGrant = {
  assignment_id: string;
  tenant_id: string;
  subject_id: string;
  entitlement_id: string;
  active: boolean;
  expires_at?: string | null;
};

export type AccessReviewRecord = {
  campaign_id: string;
  tenant_id: string;
  status: 'open' | 'closed';
  pending_items: number;
  escalated_items: number;
  revoked_items: number;
};

export type Phase5WorkflowSummary = {
  sdk_ecosystem: {
    compatible_sdk_ids: string[];
    aligned_sdk_ids: string[];
    languages: string[];
  };
  extensibility: {
    enabled_plugin_ids: string[];
    failing_plugin_ids: string[];
    isolation_modes: string[];
  };
  governance: {
    scim_tenants: string[];
    managed_user_count: number;
    managed_group_count: number;
    active_entitlement_count: number;
    open_campaign_count: number;
    escalated_item_count: number;
    revoked_item_count: number;
  };
};

const semverKey = (value: string): [number, number, number] => {
  const [head] = value.trim().replace(/^v/, '').split('-', 1);
  const parts = head.split('.').filter(Boolean).slice(0, 3);
  const normalized = [...parts.map((part) => Number.parseInt(part.replace(/\D+/g, '') || '0', 10))];
  while (normalized.length < 3) {
    normalized.push(0);
  }
  return [normalized[0] ?? 0, normalized[1] ?? 0, normalized[2] ?? 0];
};

const compareSemver = (left: [number, number, number], right: [number, number, number]): number => {
  for (let index = 0; index < 3; index += 1) {
    const delta = (left[index] ?? 0) - (right[index] ?? 0);
    if (delta !== 0) {
      return delta;
    }
  }
  return 0;
};

const versionInRange = (version: string, [lower, upper]: [string, string]): boolean => {
  const value = semverKey(version);
  const min = semverKey(lower);
  const max = semverKey(upper);
  return compareSemver(value, min) >= 0 && compareSemver(value, max) <= 0;
};

export const summarizeSdkEcosystem = ({
  runtimeVersion,
  expectedContracts,
  sdks,
}: {
  runtimeVersion: string;
  expectedContracts: Record<string, string>;
  sdks: SdkDescriptor[];
}) => {
  const compatible = sdks.filter((sdk) => versionInRange(runtimeVersion, sdk.compatible_runtime_range));
  const aligned = compatible.filter((sdk) =>
    Object.entries(expectedContracts).every(([kind, expectedVersion]) => sdk.generated_contracts[kind] === expectedVersion),
  );
  return {
    compatible_sdk_ids: compatible.map((sdk) => sdk.sdk_id).sort(),
    aligned_sdk_ids: aligned.map((sdk) => sdk.sdk_id).sort(),
    languages: [...new Set(sdks.map((sdk) => sdk.language))].sort(),
  };
};

export const summarizePluginRuntime = (plugins: PluginDescriptor[]) => {
  return {
    enabled_plugin_ids: plugins.filter((plugin) => plugin.enabled).map((plugin) => plugin.plugin_id).sort(),
    failing_plugin_ids: plugins.filter((plugin) => plugin.last_outcome === 'failed').map((plugin) => plugin.plugin_id).sort(),
    isolation_modes: [...new Set(plugins.map((plugin) => plugin.isolation_mode))].sort(),
  };
};

export const summarizeGovernanceWorkflows = ({
  scim,
  entitlements,
  reviews,
}: {
  scim: ScimProvisioningRecord[];
  entitlements: EntitlementGrant[];
  reviews: AccessReviewRecord[];
}) => {
  return {
    scim_tenants: scim.map((record) => record.tenant_id).sort(),
    managed_user_count: scim.reduce((total, record) => total + record.users, 0),
    managed_group_count: scim.reduce((total, record) => total + record.groups, 0),
    active_entitlement_count: entitlements.filter((grant) => grant.active).length,
    open_campaign_count: reviews.filter((review) => review.status === 'open').length,
    escalated_item_count: reviews.reduce((total, review) => total + review.escalated_items, 0),
    revoked_item_count: reviews.reduce((total, review) => total + review.revoked_items, 0),
  };
};

export const buildPhase5WorkflowSummary = ({
  runtimeVersion,
  expectedContracts,
  sdks,
  plugins,
  scim,
  entitlements,
  reviews,
}: {
  runtimeVersion: string;
  expectedContracts: Record<string, string>;
  sdks: SdkDescriptor[];
  plugins: PluginDescriptor[];
  scim: ScimProvisioningRecord[];
  entitlements: EntitlementGrant[];
  reviews: AccessReviewRecord[];
}): Phase5WorkflowSummary => {
  return {
    sdk_ecosystem: summarizeSdkEcosystem({ runtimeVersion, expectedContracts, sdks }),
    extensibility: summarizePluginRuntime(plugins),
    governance: summarizeGovernanceWorkflows({ scim, entitlements, reviews }),
  };
};
