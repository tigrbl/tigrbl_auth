export type TenantAdminTransport = <T>(method: string, path: string, body?: unknown) => Promise<T>;
export class TenantAdminClient {
  constructor(private readonly transport: TenantAdminTransport) {}
  listMembers(tenantId: string) { return this.transport("GET", `/v1/tenants/${tenantId}/members`); }
  listRoles(tenantId: string) { return this.transport("GET", `/v1/tenants/${tenantId}/authorization/roles`); }
  createGrant(tenantId: string, grant: unknown) { return this.transport("POST", `/v1/tenants/${tenantId}/authorization/grants`, grant); }
  effectiveAccess(tenantId: string, principalId: string) { return this.transport("GET", `/v1/tenants/${tenantId}/authorization/effective-access/${principalId}`); }
}
