import { describe, expect, it } from "vitest";
import { demoFixtures, journeySteps } from "./demoState";
import { surfaces } from "./surfaces";

describe("demo hub surface catalog", () => {
  it("covers every local frontdoor surface used by the demo stack", () => {
    expect(surfaces.map((surface) => surface.api)).toEqual([
      "tigrbl-auth-api-public",
      "tigrbl-auth-api-my-account",
      "tigrbl-auth-api-platform-admin",
      "tigrbl-auth-api-tenant-admin",
      "tigrbl-auth-api-developer",
      "tigrbl-auth-api-service-admin",
      "tigrbl-auth-api-resource-validation"
    ]);
  });

  it("makes every journey step executable with persona, action, proof, object, and launch metadata", () => {
    expect(journeySteps).toHaveLength(7);
    for (const step of journeySteps) {
      expect(step.persona).toBeTruthy();
      expect(step.action).toBeTruthy();
      expect(step.proof).toBeTruthy();
      expect(step.objectValue).toBeTruthy();
      expect(step.apiRequest.url).toBeTruthy();
      expect(step.apiRequest.expected).toBeTruthy();
      expect(surfaces.some((surface) => surface.id === step.surfaceId)).toBe(true);
    }
    expect(JSON.stringify(journeySteps)).toContain(demoFixtures.tenant.slug);
    expect(JSON.stringify(journeySteps)).toContain(demoFixtures.user.email);
  });
});
