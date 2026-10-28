export type DecisionRequest = { principal: unknown; action: string; resource: unknown; authentication?: unknown };
export type Decision = { allowed: boolean; reason_code: string; obligations: string[]; matched_policy_versions: string[] };
export class PolicyDecisionClient {
  constructor(private readonly decideTransport: (request: DecisionRequest) => Promise<Decision>) {}
  decide(request: DecisionRequest) { return this.decideTransport(request); }
}
