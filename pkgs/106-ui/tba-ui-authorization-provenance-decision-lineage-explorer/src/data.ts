import { createHash } from "node:crypto";
import { EvaluationOutcome, type Step } from "./types";

export function calculateSimpleHash(value: string) {
  return createHash("sha256").update(value).digest("hex");
}

export function generateStableKey(subject: string, resource: string, action: string, policy: string) {
  return calculateSimpleHash(JSON.stringify([subject, resource, action, policy]));
}

export const MockPolicyEngine = {
  evaluate(roles: string[], classification: string, deviceScore: number, mfa: boolean,
    ipAddress: string, destination: string, emergency: boolean, policyVersion: string,
    _substitutions?: Record<string, string>) {
    const restricted = classification === "restricted" || classification === "confidential";
    const checks: [string, boolean, string][] = [
      ["demo-policy-version", policyVersion === "1.0.0", "Only the sample policy version is available."],
      ["assigned-role", roles.includes("employee") || roles.includes("auditor"), "A sample employee or auditor role is required."],
      ["trusted-device", Number.isFinite(deviceScore) && deviceScore >= 70, "Device trust score must be at least 70."],
      ["restricted-resource", !restricted || mfa, "Restricted resources require MFA."],
      ["destination", !destination || destination === "us-east1", "This sample permits only its home region."],
      ["request-context", Boolean(ipAddress) && !emergency, "Emergency or incomplete requests are denied."],
    ];
    const steps: Step[] = checks.map(([ruleName, passed, reason]) => ({
      ruleName, outcome: passed ? EvaluationOutcome.PERMIT : EvaluationOutcome.DENY,
      reason: passed ? "Check passed." : reason,
    }));
    const failed = steps.find(step => step.outcome === EvaluationOutcome.DENY);
    return failed ? { effect: EvaluationOutcome.DENY, reason: failed.reason, obligations: [], steps } :
      { effect: EvaluationOutcome.PERMIT, reason: "All sample policy checks passed.", obligations: ["audit"], steps };
  },
};
