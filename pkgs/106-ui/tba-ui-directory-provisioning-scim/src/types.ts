export type ProvisioningConnection = {
  id: string; tenantSlug: string; name: string; vendorProfile: string; status: string;
  token: string; baseUrl: string; createdAt: string; lastSyncAt: string | null;
  errorRate: number; syncCount: number;
};
type ResourceMetadata = { resourceType: string; created: string; lastModified: string; location: string; version: string };
type SourceRecord = { id: string; externalId?: string; displayName: string; meta: ResourceMetadata;
  sourceConnectionId: string; sourceName: string };
type Contact = { value: string; type?: string; primary?: boolean };
export type ScimUser = SourceRecord & {
  userName: string; name: { givenName?: string; familyName?: string; formatted?: string };
  emails: Contact[]; phoneNumbers?: Contact[]; title?: string; department?: string;
  organization?: string; active: boolean;
};
export type ScimGroup = SourceRecord & { members: { value: string; display?: string; type?: string }[] };
export type MappingRule = {
  id: string; scimPath: string; canonicalPath: string; sourceAuthority: string;
  required: boolean; type: string; description: string;
};
export type SyncActivity = {
  id: string; tenantSlug: string; connectionId: string; connectionName: string; timestamp: string;
  method: string; url: string; status: number; requestBody: unknown; responseBody: unknown;
  result: "success" | "failure" | "quarantined"; latencyMs: number; correlationId: string;
  reasonCode?: string; resourceType?: string;
};
export type QuarantineItem = {
  id: string; activityId: string; connectionId: string; connectionName: string;
  resourceType: string; conflictType: string; reason: string;
  originalPayload: Partial<ScimUser> & { userName: string; schemas?: string[] };
  status: string; timestamp: string; resolvedAt?: string; resolutionNote?: string;
};
export type DashboardStats = {
  activeConnectionsCount: number; totalManagedUsers: number; totalManagedGroups: number;
  quarantinePendingCount: number; operations24h: number; failureRate24h: number;
  syncLatencyP95: number; leaverDeprovisioningSLA: string;
};
