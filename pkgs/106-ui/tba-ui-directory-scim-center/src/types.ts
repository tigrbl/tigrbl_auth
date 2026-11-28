export type ScimConnection = {
  connectionId: string; name: string; sourceProfile: string; lifecycleState: string;
  tokenSecretHash: string; tokenSecret?: string; createdAt: string; lastUsed: string;
  totalManagedUsers: number; totalManagedGroups: number; errorRate: number; baseScimUrl: string;
  attributeMappings: { sourcePath: string; targetField: string; ownership: string }[]; precedencePolicy: string;
};
export type UserRecord = {
  id: string; userName: string; displayName: string; emails: { value: string; type?: string; primary?: boolean }[];
  active: boolean; title?: string; department?: string; organization?: string; employeeNumber?: string;
  createdAt: string; updatedAt: string; sourceConnectionId: string; externalId?: string; scimId: string;
  sourceStatus: string; originalPayloadDigest?: string;
};
export type GroupRecord = {
  id: string; displayName: string; externalId?: string; scimId: string; sourceConnectionId: string;
  members: { value: string; display?: string }[]; mappedRoles: string[]; mappedEntitlements: string[];
  createdAt: string; updatedAt: string;
};
export type QuarantineRecord = {
  id: string; connectionId: string; connectionName: string; resourceType: string; scimId: string;
  externalId?: string; payload: Record<string, unknown> & { userName?: string;
    name?: { formatted?: string; givenName?: string; familyName?: string };
    displayName?: string; title?: string; department?: string }; reason: string; conflictWithId?: string;
  conflictField?: string; conflictValue?: string; timestamp: string;
};
export type SyncEvent = {
  id: string; timestamp: string; connectionId: string; connectionName: string; clientIp: string;
  operation: string; resourceType: string; resourceId?: string; status: string; responseCode: number;
  rawRequest: string; rawResponse: string; latencyMs: number; correlationId: string; summary: string;
};
export type OverviewMetrics = {
  totalConnections: number; totalUsers: number; totalGroups: number; quarantinedCount: number;
  avgLatencyMs: number; syncSuccessRate: number; recentFailuresCount: number;
};
