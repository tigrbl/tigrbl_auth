import { describe, expect, it } from "vitest";

import type { OidcDiscoveryMetadata } from "../types";
import {
  buildAdaptiveChallengeViewModel,
  readDiscoveredIdentityProviders,
  resolveAdvancedAuthCapabilities,
} from "./advancedIdentity";

const discovery: OidcDiscoveryMetadata = {
  issuer: "https://auth.example.com",
  authorization_endpoint: "https://auth.example.com/authorize",
  token_endpoint: "https://auth.example.com/token",
  mfa_verification_endpoint: "https://auth.example.com/mfa/verify",
  passwordless_authentication_endpoint: "https://auth.example.com/passwordless",
  webauthn_registration_endpoint: "https://auth.example.com/webauthn/register",
  webauthn_authentication_endpoint: "https://auth.example.com/webauthn/authenticate",
  device_identity_endpoint: "https://auth.example.com/device",
  workload_identity_endpoint: "https://auth.example.com/workload",
  trust_federation_endpoint: "https://auth.example.com/trust",
  amr_values_supported: ["pwd", "mfa", "rba"],
  identity_providers: [
    {
      provider_id: "github",
      kind: "social",
      issuer: "https://github.com/login/oauth",
      authorization_endpoint: "https://auth.example.com/providers/github/authorize",
      display_name: "GitHub",
      scopes: ["openid", "email"],
    },
    {
      provider_id: "corp-sso",
      kind: "sso",
      issuer: "https://login.example.com",
      authorization_endpoint: "https://auth.example.com/providers/corp-sso/authorize",
      logout_supported: true,
    },
    {
      provider_id: "partner-fed",
      kind: "federation",
      issuer: "https://partner.example.com",
      authorization_endpoint: "https://auth.example.com/providers/partner-fed/authorize",
    },
  ],
};

describe("advancedIdentity", () => {
  it("normalizes discovered identity providers through trusted public endpoints", () => {
    const providers = readDiscoveredIdentityProviders(discovery, "https://auth.example.com");

    expect(providers.map((provider) => provider.kind)).toEqual(["social", "sso", "federation"]);
    expect(providers[0].display_name).toBe("GitHub");
    expect(providers[1].logout_supported).toBe(true);
    expect(providers[2].authorization_endpoint).toBe(
      "https://auth.example.com/providers/partner-fed/authorize",
    );
  });

  it("derives the full advanced-auth capability surface from discovery metadata", () => {
    expect(resolveAdvancedAuthCapabilities(discovery, "https://auth.example.com")).toEqual({
      passwordless: true,
      mfa: true,
      webauthn: true,
      sso: true,
      social: true,
      federation: true,
      deviceIdentity: true,
      workloadIdentity: true,
      contextualStepUp: true,
    });
  });

  it("builds adaptive challenge prompts for medium and high risk sessions", () => {
    const medium = buildAdaptiveChallengeViewModel({
      riskScore: 0,
      networkTrusted: false,
      deviceTrusted: true,
      localHour: 23,
      anomalyDetected: false,
    });
    const high = buildAdaptiveChallengeViewModel({
      riskScore: 1,
      networkTrusted: false,
      deviceTrusted: false,
      localHour: 23,
      anomalyDetected: true,
    });

    expect(medium).toEqual({
      riskLevel: "medium",
      stepUpRequired: true,
      preferredMethods: ["otp", "webauthn"],
      reasons: ["Untrusted network context", "Outside normal operating hours"],
    });
    expect(high.riskLevel).toBe("high");
    expect(high.stepUpRequired).toBe(true);
    expect(high.preferredMethods).toEqual(["webauthn", "otp"]);
    expect(high.reasons).toContain("Upstream anomaly signal present");
  });
});
