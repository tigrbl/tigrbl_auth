export type PublicBoundaryTier = "T0" | "T1" | "T2";

export interface PublicBoundaryFeature {
  featureId: string;
  surface: "public-uix";
  category: "shell" | "flow" | "session" | "contract" | "browser-security";
  route: string;
  requiresAuthenticatedSession: boolean;
  browserStorage: "none" | "session";
  tokenDisclosure: "none" | "memory-only";
  csrfRequired: boolean;
  safeErrorDisclosure: boolean;
  redirectConstrained: boolean;
}

export const PUBLIC_UIX_BOUNDARY_FEATURES: readonly PublicBoundaryFeature[] = [
  {
    featureId: "feat:uix-public-shell",
    surface: "public-uix",
    category: "shell",
    route: "#/",
    requiresAuthenticatedSession: false,
    browserStorage: "none",
    tokenDisclosure: "none",
    csrfRequired: false,
    safeErrorDisclosure: true,
    redirectConstrained: true,
  },
  {
    featureId: "feat:uix-public-auth-session",
    surface: "public-uix",
    category: "session",
    route: "#/callback",
    requiresAuthenticatedSession: false,
    browserStorage: "session",
    tokenDisclosure: "memory-only",
    csrfRequired: true,
    safeErrorDisclosure: true,
    redirectConstrained: true,
  },
  {
    featureId: "feat:uix-public-login-view",
    surface: "public-uix",
    category: "flow",
    route: "#/login",
    requiresAuthenticatedSession: false,
    browserStorage: "none",
    tokenDisclosure: "none",
    csrfRequired: true,
    safeErrorDisclosure: true,
    redirectConstrained: true,
  },
  {
    featureId: "feat:uix-public-logout-view",
    surface: "public-uix",
    category: "flow",
    route: "#/login",
    requiresAuthenticatedSession: true,
    browserStorage: "session",
    tokenDisclosure: "none",
    csrfRequired: true,
    safeErrorDisclosure: true,
    redirectConstrained: true,
  },
  {
    featureId: "feat:uix-public-registration-view",
    surface: "public-uix",
    category: "flow",
    route: "#/register",
    requiresAuthenticatedSession: false,
    browserStorage: "none",
    tokenDisclosure: "none",
    csrfRequired: true,
    safeErrorDisclosure: true,
    redirectConstrained: true,
  },
  {
    featureId: "feat:uix-public-recovery-view",
    surface: "public-uix",
    category: "flow",
    route: "#/forgot-password",
    requiresAuthenticatedSession: false,
    browserStorage: "none",
    tokenDisclosure: "none",
    csrfRequired: true,
    safeErrorDisclosure: true,
    redirectConstrained: true,
  },
  {
    featureId: "feat:uix-public-session-continuity",
    surface: "public-uix",
    category: "session",
    route: "#/profile",
    requiresAuthenticatedSession: true,
    browserStorage: "session",
    tokenDisclosure: "memory-only",
    csrfRequired: true,
    safeErrorDisclosure: true,
    redirectConstrained: true,
  },
  {
    featureId: "feat:uix-public-openapi-contract-consumption",
    surface: "public-uix",
    category: "contract",
    route: "#/",
    requiresAuthenticatedSession: false,
    browserStorage: "none",
    tokenDisclosure: "none",
    csrfRequired: false,
    safeErrorDisclosure: true,
    redirectConstrained: true,
  },
  {
    featureId: "feat:uix-public-browser-token-handling",
    surface: "public-uix",
    category: "browser-security",
    route: "#/callback",
    requiresAuthenticatedSession: false,
    browserStorage: "session",
    tokenDisclosure: "memory-only",
    csrfRequired: true,
    safeErrorDisclosure: true,
    redirectConstrained: true,
  },
  {
    featureId: "feat:uix-public-problem-details-rendering",
    surface: "public-uix",
    category: "contract",
    route: "#/login",
    requiresAuthenticatedSession: false,
    browserStorage: "none",
    tokenDisclosure: "none",
    csrfRequired: false,
    safeErrorDisclosure: true,
    redirectConstrained: true,
  },
  {
    featureId: "feat:uix-public-safe-error-disclosure",
    surface: "public-uix",
    category: "browser-security",
    route: "#/login",
    requiresAuthenticatedSession: false,
    browserStorage: "none",
    tokenDisclosure: "none",
    csrfRequired: false,
    safeErrorDisclosure: true,
    redirectConstrained: true,
  },
  {
    featureId: "feat:uix-public-consent-view",
    surface: "public-uix",
    category: "flow",
    route: "#/consent",
    requiresAuthenticatedSession: false,
    browserStorage: "none",
    tokenDisclosure: "none",
    csrfRequired: true,
    safeErrorDisclosure: true,
    redirectConstrained: true,
  },
  {
    featureId: "feat:uix-public-cookie-session-model",
    surface: "public-uix",
    category: "session",
    route: "#/profile",
    requiresAuthenticatedSession: true,
    browserStorage: "session",
    tokenDisclosure: "memory-only",
    csrfRequired: true,
    safeErrorDisclosure: true,
    redirectConstrained: true,
  },
  {
    featureId: "feat:uix-public-csrf-protection",
    surface: "public-uix",
    category: "browser-security",
    route: "#/",
    requiresAuthenticatedSession: false,
    browserStorage: "session",
    tokenDisclosure: "none",
    csrfRequired: true,
    safeErrorDisclosure: true,
    redirectConstrained: true,
  },
  {
    featureId: "feat:uix-public-origin-and-redirect-constraints",
    surface: "public-uix",
    category: "browser-security",
    route: "#/",
    requiresAuthenticatedSession: false,
    browserStorage: "none",
    tokenDisclosure: "none",
    csrfRequired: false,
    safeErrorDisclosure: true,
    redirectConstrained: true,
  },
];

export const publicUixBoundaryManifest = (): Record<string, PublicBoundaryFeature> =>
  Object.fromEntries(PUBLIC_UIX_BOUNDARY_FEATURES.map((feature) => [feature.featureId, feature]));

export const publicUixBoundaryIntegrity = () => {
  const manifest = publicUixBoundaryManifest();
  const rows = Object.values(manifest);
  const unsafeTokenRows = rows.filter(
    (row) => row.tokenDisclosure !== "none" && row.tokenDisclosure !== "memory-only",
  );
  const unsafeErrorRows = rows.filter((row) => !row.safeErrorDisclosure);
  const unconstrainedRedirectRows = rows.filter((row) => !row.redirectConstrained);
  const csrfPostRows = rows.filter(
    (row) => ["flow", "session", "browser-security"].includes(row.category) && row.csrfRequired,
  );

  return {
    featureCount: rows.length,
    csrfProtectedCount: csrfPostRows.length,
    unsafeTokenFeatureIds: unsafeTokenRows.map((row) => row.featureId),
    unsafeErrorFeatureIds: unsafeErrorRows.map((row) => row.featureId),
    unconstrainedRedirectFeatureIds: unconstrainedRedirectRows.map((row) => row.featureId),
    passed:
      rows.length === 15
      && unsafeTokenRows.length === 0
      && unsafeErrorRows.length === 0
      && unconstrainedRedirectRows.length === 0
      && csrfPostRows.length >= 8,
  };
};
