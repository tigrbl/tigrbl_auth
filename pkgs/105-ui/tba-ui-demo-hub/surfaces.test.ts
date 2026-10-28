import { describe, expect, it } from "vitest";
import { demoFixtures, journeySteps } from "./demoState";
import { surfaces } from "./surfaces";

describe("demo hub surface catalog", () => {
  it("covers every local frontdoor surface used by the demo stack", () => {
    expect(surfaces.map((surface) => surface.api)).toEqual([
      "tba-app-backend-public",
      "tba-app-backend-my-account",
      "tba-app-backend-platform-admin",
      "tba-app-backend-tenant-admin",
      "tba-app-backend-developer",
      "tba-app-backend-service-admin",
      "tba-app-backend-resource-validation"
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
