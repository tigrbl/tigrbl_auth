# Product Provenance Lineage

This table orders the backend packages, deployable API front doors, UIX apps,
consumer integrations, and support tooling by provenance. Foundation packages
come first, followed by shared protocol/runtime layers, provider surfaces, edge
clients, consumer integrations, and support packages.

| Order | Package / app | Kind | Provenance role |
| --- | --- | --- | --- |
| 1 | `tigrbl-identity-core` | Backend package | Root primitives and shared identity foundation. |
| 2 | `tigrbl-identity-contracts` | Backend package | Shared wire models and API contracts. |
| 3 | `tigrbl-identity-principals` | Backend package | Tenants, users, services, clients, workloads, identity subjects. |
| 4 | `tigrbl-identity-credentials` | Backend package | Passwords, keys, API keys, service keys, credential proof/lifecycle. |
| 5 | `tigrbl-identity-jose` | Backend package | JWT, JWK, JWKS, signing, key material, token crypto. |
| 6 | `tigrbl-identity-policy` | Backend package | Authorization, RBAC/ABAC/delegation/governance decisions. |
| 7 | `tigrbl-identity-oauth` | Backend package | OAuth protocol flows. |
| 8 | `tigrbl-identity-oidc` | Backend package | OIDC behavior layered on OAuth. |
| 9 | `tigrbl-identity-admin` | Backend package | Shared administrative/control-plane services. |
| 10 | `tigrbl-identity-storage` | Backend package | Persistence backing for identity/admin/runtime state. |
| 11 | `tigrbl-identity-server` | Backend package | Provider app assembly. |
| 12 | `tigrbl-identity-runtime` | Backend package | Runtime/profile/runner configuration. |
| 13 | `tigrbl-auth-api-public` | API front door | First deployable public identity/provider surface. |
| 14 | `tigrbl-auth-api-resource-validation` | API front door | Read-only validation/metadata surface derived from public issuer state. |
| 15 | `tigrbl-auth-api-platform-admin` | API front door | Platform control plane: creates tenants and assigns authority. |
| 16 | `tigrbl-auth-api-tenant-admin` | API front door | Tenant-scoped administration derived from platform-created tenants. |
| 17 | `tigrbl-auth-api-developer` | API front door | Developer app/client registration inside a tenant context. |
| 18 | `tigrbl-auth-api-service-admin` | API front door | Service/workload identity administration inside a tenant/platform context. |
| 19 | `@tigrbl-auth/public-uix` | UIX app | Public hosted-login UI over `public-api`. |
| 20 | `@tigrbl-auth/platform-admin-uix` | UIX app | Platform owner/admin/operator UI over `platform-admin-api`. |
| 21 | `@tigrbl-auth/tenant-admin-uix` | UIX app | Tenant owner/admin UI over `tenant-admin-api`. |
| 22 | `@tigrbl-auth/developer-uix` | UIX app | Tenant developer UI over `developer-api`. |
| 23 | `@tigrbl-auth/service-admin-uix` | UIX app | Service/workload admin UI over `service-admin-api`. |
| 24 | `tigrbl-identity-rp` | Consumer package | App-side relying-party integration consuming the public issuer. |
| 25 | `@tigrbl-auth/rp` | Consumer UI/package | Browser/client RP integration consuming public issuer behavior. |
| 26 | `tigrbl-identity-resource-server` | Consumer package | Protected API token-validation integration consuming resource-validation metadata. |
| 27 | `tigrbl-identity-operator` | Tooling package | Operational tooling over assembled deployments. |
| 28 | `tigrbl-identity-testkit` | Test package | Cross-cutting fixtures, conformance, and integration harnesses. |
| 29 | `@tigrbl-auth/admin-uix` | Legacy UIX app | Temporary ancestor/extraction source, not a final product surface. |
