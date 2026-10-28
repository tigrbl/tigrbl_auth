import { SURFACE_LINKS } from "./defaults";

export const surfaces = [
  {
    id: "public",
    title: "Public issuer",
    persona: "End user, browser client, relying party",
    api: "tba-app-backend-public",
    uix: "@tba/ui-public",
    objects: "issuer metadata, authorization requests, tokens, userinfo, hosted login",
    demoAction: "Start authentication through hosted login.",
    uixUrl: SURFACE_LINKS.publicUix,
    backendAppUrl: SURFACE_LINKS.publicApiDocs
  },
  {
    id: "my-account",
    title: "My Account",
    persona: "Signed-in end user",
    api: "tba-app-backend-my-account",
    uix: "@tba/ui-my-account",
    objects: "profile, sessions, password posture, authorized apps, consent grants",
    demoAction: "Review profile, sessions, and authorized applications.",
    uixUrl: SURFACE_LINKS.myAccountUix,
    backendAppUrl: SURFACE_LINKS.myAccountApiDocs
  },
  {
    id: "platform-admin",
    title: "Platform administration",
    persona: "Platform owner, operator, support engineer",
    api: "tba-app-backend-platform-administration",
    uix: "@tba/ui-platform-administration",
    objects: "tenants, platform identities, authority assignment, signing posture, audit",
    demoAction: "Provision tenant authority and review platform posture.",
    uixUrl: SURFACE_LINKS.platformAdminUix,
    backendAppUrl: SURFACE_LINKS.platformAdminApiDocs
  },
  {
    id: "tenant-admin",
    title: "Tenant administration",
    persona: "Tenant owner, tenant admin",
    api: "tba-app-backend-tenant-administration",
    uix: "@tba/ui-tenant-administration",
    objects: "tenant identities, roles, groups, tenant-scoped policy",
    demoAction: "Manage identities and delegated tenant authority.",
    uixUrl: SURFACE_LINKS.tenantAdminUix,
    backendAppUrl: SURFACE_LINKS.tenantAdminApiDocs
  },
  {
    id: "developer",
    title: "Developer platform",
    persona: "Application developer",
    api: "tba-app-backend-developer",
    uix: "@tba/ui-developer",
    objects: "applications, OAuth clients, redirect URIs, scopes, client credentials",
    demoAction: "Register an application client and inspect integration metadata.",
    uixUrl: SURFACE_LINKS.developerUix,
    backendAppUrl: SURFACE_LINKS.developerApiDocs
  },
  {
    id: "service-admin",
    title: "Service administration",
    persona: "Service owner, workload operator",
    api: "tba-app-backend-service-administration",
    uix: "@tba/ui-service-administration",
    objects: "workloads, service identities, service keys, M2M credentials",
    demoAction: "Create service credentials and review workload access posture.",
    uixUrl: SURFACE_LINKS.serviceAdminUix,
    backendAppUrl: SURFACE_LINKS.serviceAdminApiDocs
  },
  {
    id: "resource-validation",
    title: "Resource validation",
    persona: "Protected API owner, resource server integrator",
    api: "tba-app-backend-resource-validation",
    uix: "API-only surface",
    objects: "JWKS, introspection, issuer validation metadata, token validation inputs",
    demoAction: "Show how protected APIs consume issuer state.",
    uixUrl: "",
    backendAppUrl: SURFACE_LINKS.resourceValidationApiDocs
  }
] as const;
