import type { DiscoveredIdentityProvider, OidcDiscoveryMetadata } from "../types";
import { resolveTrustedPublicEndpoint } from "./publicUxPolicy";

export interface PublicAdvancedAuthCapabilities {
  passwordless: boolean;
  mfa: boolean;
  webauthn: boolean;
  sso: boolean;
  social: boolean;
  federation: boolean;
  deviceIdentity: boolean;
  workloadIdentity: boolean;
  contextualStepUp: boolean;
}

export interface AdaptiveChallengeViewModel {
  riskLevel: "low" | "medium" | "high";
  stepUpRequired: boolean;
  preferredMethods: string[];
  reasons: string[];
}

export const readDiscoveredIdentityProviders = (
  discovery: OidcDiscoveryMetadata,
  publicBaseUrl: string,
): DiscoveredIdentityProvider[] => {
  const providers = Array.isArray(discovery.identity_providers) ? discovery.identity_providers : [];
  return providers
    .filter((provider): provider is DiscoveredIdentityProvider => {
      return Boolean(
        provider &&
        typeof provider.provider_id === "string" &&
        typeof provider.kind === "string" &&
        typeof provider.issuer === "string" &&
        typeof provider.authorization_endpoint === "string",
      );
    })
    .map((provider) => ({
      ...provider,
      authorization_endpoint: resolveTrustedPublicEndpoint(
        provider.authorization_endpoint,
        `${provider.kind}-authorize`,
        publicBaseUrl,
      ),
      display_name: provider.display_name || provider.provider_id,
      scopes: Array.isArray(provider.scopes) ? provider.scopes : [],
    }));
};

export const resolveAdvancedAuthCapabilities = (
  discovery: OidcDiscoveryMetadata,
  publicBaseUrl: string,
): PublicAdvancedAuthCapabilities => {
  const providers = readDiscoveredIdentityProviders(discovery, publicBaseUrl);
  const amrValues = Array.isArray(discovery.amr_values_supported) ? discovery.amr_values_supported : [];
  const acrValues = Array.isArray(discovery.acr_values_supported) ? discovery.acr_values_supported : [];
  return {
    passwordless: Boolean(
      discovery.passwordless_authentication_endpoint || discovery.webauthn_authentication_endpoint,
    ),
    mfa: Boolean(discovery.mfa_verification_endpoint),
    webauthn: Boolean(
      discovery.webauthn_registration_endpoint && discovery.webauthn_authentication_endpoint,
    ),
    sso: providers.some((provider) => provider.kind === "sso"),
    social: providers.some((provider) => provider.kind === "social"),
    federation: Boolean(
      discovery.trust_federation_endpoint || providers.some((provider) => provider.kind === "federation"),
    ),
    deviceIdentity: Boolean(discovery.device_identity_endpoint),
    workloadIdentity: Boolean(discovery.workload_identity_endpoint),
    contextualStepUp: amrValues.includes("mfa") || amrValues.includes("rba") || acrValues.length > 0,
  };
};

export const buildAdaptiveChallengeViewModel = ({
  riskScore,
  networkTrusted,
  deviceTrusted,
  localHour,
  anomalyDetected,
}: {
  riskScore: number;
  networkTrusted: boolean;
  deviceTrusted: boolean;
  localHour: number;
  anomalyDetected: boolean;
}): AdaptiveChallengeViewModel => {
  const reasons: string[] = [];
  let effectiveRiskScore = riskScore;

  if (!networkTrusted) {
    effectiveRiskScore += 1;
    reasons.push("Untrusted network context");
  }
  if (!deviceTrusted) {
    effectiveRiskScore += 2;
    reasons.push("Unknown or unhealthy device posture");
  }
  if (localHour < 6 || localHour > 22) {
    effectiveRiskScore += 1;
    reasons.push("Outside normal operating hours");
  }
  if (anomalyDetected) {
    effectiveRiskScore += 2;
    reasons.push("Upstream anomaly signal present");
  }

  if (effectiveRiskScore >= 5) {
    return {
      riskLevel: "high",
      stepUpRequired: true,
      preferredMethods: ["webauthn", "otp"],
      reasons,
    };
  }
  if (effectiveRiskScore >= 2) {
    return {
      riskLevel: "medium",
      stepUpRequired: true,
      preferredMethods: ["otp", "webauthn"],
      reasons,
    };
  }
  return {
    riskLevel: "low",
    stepUpRequired: false,
    preferredMethods: [],
    reasons: reasons.length ? reasons : ["Context accepted within bounded policy"],
  };
};
