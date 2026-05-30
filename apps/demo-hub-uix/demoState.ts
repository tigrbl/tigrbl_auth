import { surfaces } from "./surfaces";

export const demoFixtures = {
  tenant: {
    id: "tenant_acme_demo",
    name: "Acme Demo",
    slug: "acme-demo"
  },
  user: {
    id: "usr_alex_demo",
    email: "alex@acme.example",
    role: "tenant-admin"
  },
  app: {
    clientId: "client_acme_dashboard",
    name: "Acme Dashboard",
    redirectUri: "http://localhost:5173/callback",
    scopes: "openid profile email offline_access"
  },
  service: {
    id: "svc_acme_worker",
    name: "Acme Worker",
    credential: "svc-key-acme-worker-local"
  },
  resource: {
    id: "api_acme_orders",
    name: "Acme Orders API",
    audience: "https://api.acme.example/orders"
  }
} as const;

type SurfaceId = (typeof surfaces)[number]["id"];

export type JourneyStep = {
  id: string;
  order: number;
  surfaceId: SurfaceId;
  persona: string;
  goal: string;
  action: string;
  proof: string;
  objectLabel: string;
  objectValue: string;
  apiRequest: {
    label: string;
    method: "GET" | "POST" | "PATCH" | "DELETE";
    url: string;
    body?: Record<string, unknown>;
    expected: string;
  };
};

export const journeySteps: JourneyStep[] = [
  {
    id: "platform-provision-tenant",
    order: 1,
    surfaceId: "platform-admin",
    persona: "Platform operator",
    goal: "Create the SaaS tenant and assign platform authority.",
    action: `Provision ${demoFixtures.tenant.name} from the platform control plane.`,
    proof: `${demoFixtures.tenant.slug} is visible as a platform-created tenant.`,
    objectLabel: "Tenant",
    objectValue: `${demoFixtures.tenant.name} (${demoFixtures.tenant.slug})`,
    apiRequest: {
      label: "List platform tenants",
      method: "GET",
      url: "/api/platform-admin/admin/tenant",
      expected: "Returns tenant rows when an admin session/API key is present; otherwise proves auth boundary."
    }
  },
  {
    id: "tenant-manage-identity",
    order: 2,
    surfaceId: "tenant-admin",
    persona: "Tenant admin",
    goal: "Manage the tenant-scoped identity and role posture.",
    action: `Review ${demoFixtures.user.email} and assign tenant role ${demoFixtures.user.role}.`,
    proof: `${demoFixtures.user.email} has tenant-scoped access inside ${demoFixtures.tenant.slug}.`,
    objectLabel: "Identity",
    objectValue: `${demoFixtures.user.email} (${demoFixtures.user.role})`,
    apiRequest: {
      label: "List tenant identities",
      method: "GET",
      url: "/api/tenant-admin/admin/identities",
      expected: "Returns tenant-scoped identities when a tenant admin session is present; otherwise proves auth boundary."
    }
  },
  {
    id: "developer-register-client",
    order: 3,
    surfaceId: "developer",
    persona: "Application developer",
    goal: "Register the browser application that will consume the issuer.",
    action: `Register ${demoFixtures.app.name} with redirect URI ${demoFixtures.app.redirectUri}.`,
    proof: `${demoFixtures.app.clientId} exists with scopes ${demoFixtures.app.scopes}.`,
    objectLabel: "OAuth client",
    objectValue: demoFixtures.app.clientId,
    apiRequest: {
      label: "Read developer issuer metadata",
      method: "GET",
      url: "/api/developer/.well-known/openid-configuration",
      expected: "Returns issuer metadata consumed by developer-created applications."
    }
  },
  {
    id: "public-authenticate-user",
    order: 4,
    surfaceId: "public",
    persona: "End user",
    goal: "Authenticate through the hosted issuer surface.",
    action: `Sign in as ${demoFixtures.user.email}.`,
    proof: "The public issuer establishes a browser account session.",
    objectLabel: "Issuer session",
    objectValue: demoFixtures.user.email,
    apiRequest: {
      label: "Read public issuer metadata",
      method: "GET",
      url: "/api/public/.well-known/openid-configuration",
      expected: "Returns public OAuth/OIDC issuer metadata."
    }
  },
  {
    id: "account-review-consents",
    order: 5,
    surfaceId: "my-account",
    persona: "Signed-in end user",
    goal: "Review profile, sessions, authorized apps, and consent grants.",
    action: `Open My Account and inspect ${demoFixtures.app.name} authorization state.`,
    proof: "Profile, session, authorized app, and consent data are subject-scoped.",
    objectLabel: "Account",
    objectValue: `${demoFixtures.user.email} self-service`,
    apiRequest: {
      label: "Read current account profile",
      method: "GET",
      url: "/api/my-account/account/profile",
      expected: "Returns the current subject profile when an account session is present; otherwise proves subject boundary."
    }
  },
  {
    id: "service-configure-workload",
    order: 6,
    surfaceId: "service-admin",
    persona: "Service owner",
    goal: "Create workload identity for machine-to-machine access.",
    action: `Configure ${demoFixtures.service.name} credentials.`,
    proof: `${demoFixtures.service.credential} is visible for workload authentication.`,
    objectLabel: "Workload",
    objectValue: demoFixtures.service.id,
    apiRequest: {
      label: "List service identities",
      method: "GET",
      url: "/api/service-admin/service",
      expected: "Returns workload/service identities when service-admin authority is present; otherwise proves auth boundary."
    }
  },
  {
    id: "resource-validate-token",
    order: 7,
    surfaceId: "resource-validation",
    persona: "Protected API owner",
    goal: "Validate issuer metadata for a downstream protected API.",
    action: `Open resource-validation docs for ${demoFixtures.resource.name}.`,
    proof: "JWKS and validation metadata are available to resource servers.",
    objectLabel: "Resource API",
    objectValue: `${demoFixtures.resource.name} (${demoFixtures.resource.audience})`,
    apiRequest: {
      label: "Read validation JWKS",
      method: "GET",
      url: "/api/resource-validation/.well-known/jwks.json",
      expected: "Returns signing-key metadata consumed by protected resource servers."
    }
  }
];

export function getSurfaceForStep(step: JourneyStep) {
  return surfaces.find((surface) => surface.id === step.surfaceId);
}
