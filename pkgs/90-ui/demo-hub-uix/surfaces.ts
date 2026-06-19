import { SURFACE_LINKS } from "./defaults";

export const surfaces = [
  {
    id: "public",
    title: "Public issuer",
    persona: "End user, browser client, relying party",
    api: "tigrbl-auth-api-public",
    uix: "@tigrbl-auth/public-uix",
    objects: "issuer metadata, authorization requests, tokens, userinfo, hosted login",
    demoAction: "Start authentication through hosted login.",
    uixUrl: SURFACE_LINKS.publicUix,
    apiUrl: SURFACE_LINKS.publicApiDocs
  },
  {
    id: "my-account",
    title: "My Account",
    persona: "Signed-in end user",
    api: "tigrbl-auth-api-my-account",
    uix: "@tigrbl-auth/my-account-uix",
    objects: "profile, sessions, password posture, authorized apps, consent grants",
    demoAction: "Review profile, sessions, and authorized applications.",
    uixUrl: SURFACE_LINKS.myAccountUix,
    apiUrl: SURFACE_LINKS.myAccountApiDocs
  },
  {
    id: "platform-admin",
    title: "Platform administration",
    persona: "Platform owner, operator, support engineer",
    api: "tigrbl-auth-api-platform-admin",
    uix: "@tigrbl-auth/platform-admin-uix",
    objects: "tenants, platform identities, authority assignment, signing posture, audit",
    demoAction: "Provision tenant authority and review platform posture.",
    uixUrl: SURFACE_LINKS.platformAdminUix,
    apiUrl: SURFACE_LINKS.platformAdminApiDocs
  },
  {
    id: "tenant-admin",
    title: "Tenant administration",
    persona: "Tenant owner, tenant admin",
    api: "tigrbl-auth-api-tenant-admin",
    uix: "@tigrbl-auth/tenant-admin-uix",
    objects: "tenant identities, roles, groups, tenant-scoped policy",
    demoAction: "Manage identities and delegated tenant authority.",
    uixUrl: SURFACE_LINKS.tenantAdminUix,
    apiUrl: SURFACE_LINKS.tenantAdminApiDocs
  },
  {
    id: "developer",
    title: "Developer platform",
    persona: "Application developer",
    api: "tigrbl-auth-api-developer",
    uix: "@tigrbl-auth/developer-uix",
    objects: "applications, OAuth clients, redirect URIs, scopes, client credentials",
    demoAction: "Register an application client and inspect integration metadata.",
    uixUrl: SURFACE_LINKS.developerUix,
    apiUrl: SURFACE_LINKS.developerApiDocs
  },
  {
    id: "service-admin",
    title: "Service administration",
    persona: "Service owner, workload operator",
    api: "tigrbl-auth-api-service-admin",
    uix: "@tigrbl-auth/service-admin-uix",
    objects: "workloads, service identities, service keys, M2M credentials",
    demoAction: "Create service credentials and review workload access posture.",
    uixUrl: SURFACE_LINKS.serviceAdminUix,
    apiUrl: SURFACE_LINKS.serviceAdminApiDocs
  },
  {
    id: "resource-validation",
    title: "Resource validation",
    persona: "Protected API owner, resource server integrator",
    api: "tigrbl-auth-api-resource-validation",
    uix: "API-only surface",
    objects: "JWKS, introspection, issuer validation metadata, token validation inputs",
    demoAction: "Show how protected APIs consume issuer state.",
    uixUrl: "",
    apiUrl: SURFACE_LINKS.resourceValidationApiDocs
  }
] as const;
