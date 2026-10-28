# Product Provenance Lineage

This table orders the backend packages, deployable API front doors, UIX apps,
consumer integrations, and support tooling by provenance. Foundation packages
come first, followed by shared protocol/runtime layers, provider surfaces, edge
clients, consumer integrations, and support packages.

The current package taxonomy uses `identity` for neutral identity records,
`authn` for credential proof, `authz` for policy/enforcement, `auth-protocol`
for OAuth/OIDC/RP wire behavior, and `auth` for composed products/front doors.
The old renamed `tba-identity-*` package names remain compatibility packages
for one migration window.

| Order | Package / app | Kind | Provenance role |
| --- | --- | --- | --- |
| 1 | `tba-primitives-identity` | Backend package | Root primitives and shared identity foundation. |
| 2 | `tba-contracts-identity` | Backend package | Shared wire models and API contracts. |
| 3 | `tba-concrete-identity-principals` | Backend package | Tenants, users, services, clients, workloads, identity subjects. |
| 4 | `tba-credentials` | Backend package | Passwords, keys, API keys, service keys, credential proof/lifecycle. |
| 5 | `tba-provider-identity-jose` | Backend package | JWT, JWK, JWKS, signing, key material, token crypto. |
| 6 | `tba-runtime-authorization-policy` | Backend package | Authorization, RBAC/ABAC/delegation/governance decisions. |
| 7 | `tba-protocol-oauth` | Backend package | OAuth protocol flows. |
| 8 | `tba-protocol-oidc` | Backend package | OIDC behavior layered on OAuth. |
| 9 | `tba-runtime-identity-administration` | Backend package | Shared administrative/control-plane services. |
| 10 | `tba-storage-core` | Backend package | Persistence backing for identity/admin/runtime state. |
| 11 | `tba-server-identity` | Backend package | Provider app assembly. |
| 12 | `tba-runtime-identity` | Backend package | Runtime/profile/runner configuration. |
| 13 | `tba-app-backend-public` | API front door | First deployable public identity/provider surface. |
| 14 | `tba-app-backend-resource-validation` | API front door | Read-only validation/metadata surface derived from public issuer state. |
| 15 | `tba-app-backend-platform-admin` | API front door | Platform control plane: creates tenants and assigns authority. |
| 16 | `tba-app-backend-tenant-admin` | API front door | Tenant-scoped administration derived from platform-created tenants. |
| 17 | `tba-app-backend-developer` | API front door | Developer app/client registration inside a tenant context. |
| 18 | `tba-app-backend-service-admin` | API front door | Service/workload identity administration inside a tenant/platform context. |
| 19 | `@tba/ui-public` | UIX app | Public hosted-login UI over `public-app`. |
| 20 | `@tba/ui-platform-admin` | UIX app | Platform owner/admin/operator UI over `platform-admin-app`. |
| 21 | `@tba/ui-tenant-admin` | UIX app | Tenant owner/admin UI over `tenant-admin-app`. |
| 22 | `@tba/ui-developer` | UIX app | Tenant developer UI over `developer-app`. |
| 23 | `@tba/ui-service-admin` | UIX app | Service/workload admin UI over `service-admin-app`. |
| 24 | `tba-protocol-oidc-relying-party` | Consumer package | App-side relying-party integration consuming the public issuer. |
| 25 | `@tba/client-oidc-relying-party` | Consumer UI/package | Browser/client RP integration consuming public issuer behavior. |
| 26 | `tba-protocol-authorization-resource-server` | Consumer package | Protected API token-validation integration consuming resource-validation metadata. |
| 27 | `tba-operator-identity` | Tooling package | Operational tooling over assembled deployments. |
| 28 | `tba-testkit-identity` | Test package | Cross-cutting fixtures, conformance, and integration harnesses. |
| 29 | `@tba/ui-admin` | Legacy UIX app | Temporary ancestor/extraction source, not a final product surface. |
