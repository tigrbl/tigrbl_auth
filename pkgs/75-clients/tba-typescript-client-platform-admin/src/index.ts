export type PlatformAdminTransport = <T>(method: string, path: string, body?: unknown) => Promise<T>;
export class PlatformAdminClient {
  constructor(private readonly transport: PlatformAdminTransport) {}
  listPolicies() { return this.transport("GET", "/v1/platform/authorization/policies"); }
  publishPolicy(id: string) { return this.transport("POST", `/v1/platform/authorization/policies/${id}/publish`); }
  decisionAudit() { return this.transport("GET", "/v1/platform/authorization/decisions"); }
  identityProviderClients() { return this.transport("GET", "/v1/platform/identity-provider/clients"); }
}
