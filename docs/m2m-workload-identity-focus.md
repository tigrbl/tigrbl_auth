# M2M and Workload Identity Focus

Research date: 2026-05-28

Machine-to-machine access is not just the OAuth `client_credentials` grant. The grant is the token issuance mechanism. The product lane is broader: service principals, workload principals, service accounts, app clients, API/resource servers, scopes, credentials, token posture, rotation, audit, and resource-server validation.

For `tigrbl_auth`, M2M should be a first-class product lane spanning the existing frontdoors and packages:

- `tigrbl-auth-api-public` issues OAuth tokens through `/token`.
- `tigrbl-auth-api-service-admin` owns service/workload lifecycle, service keys, API keys, and audit-oriented administration.
- `tigrbl-auth-api-developer` owns application/client registration and developer-facing client policy.
- `tigrbl-auth-api-resource-validation` owns token validation, JWKS, introspection, and protected-resource metadata.
- `tigrbl-identity-principals` owns service, workload, client, tenant, and identity-subject semantics.
- `tigrbl-authn-credentials` owns proof-of-control and credential lifecycle primitives.
- `tigrbl-auth-protocol-oauth` owns `client_credentials`, JWT assertion, mTLS, DPoP, resource indicators, and token-exchange protocol behavior.
- `tigrbl-identity-storage` owns canonical `Service`, `ServiceKey`, `ApiKey`, `Client`, `ClientRegistration`, token, key, and audit tables.

## Current `tigrbl_auth` State

| Area | Current state | Evidence | Interpretation |
|---|---|---|---|
| Product decision | M2M/workload identity is already drafted as a first-class product lane. | [ADR-1085](../.ssot/adr/ADR-1085-m2m-workload-identity-first-class-product-lane.yaml), [SPEC-1177](../.ssot/specs/SPEC-1177-m2m-workload-identity-product-surface-contract.yaml) | The right direction is already present, but the docs/tests/API shape still need to mature around it. |
| Service admin API | Service-admin API exposes services, service keys, API keys, token/audit inspection, and validation metadata. | [`tigrbl-auth-api-service-admin` README](../pkgs/tigrbl-auth-api-service-admin/README.md), [SPEC-1160](../.ssot/specs/SPEC-1160-service-admin-api-contract.yaml) | This should be the lifecycle control plane for M2M service/workload identities. |
| Principals | Principal package names users, services, clients, workloads, devices, and tenants as durable identity-subject context. | [`tigrbl-identity-principals` README](../pkgs/tigrbl-identity-principals/README.md) | M2M should use principal semantics, not treat machines as anonymous API keys. |
| Credentials | Credentials package covers API keys, auth adapters, session services, and token lifecycle helpers. | [`tigrbl-authn-credentials` README](../pkgs/tigrbl-authn-credentials/README.md) | Secret verification and key lifecycle should stay below frontdoor APIs. |
| OAuth token flow | `client_credentials` is implemented in token request flow and issues persisted token pairs for a client subject. | [`token.py`](../pkgs/tigrbl-auth-protocol-oauth/src/tigrbl_auth_protocol_oauth/ops/token.py), [`test_rfc6749_token_endpoint.py`](../tests/unit/test_rfc6749_token_endpoint.py) | Token issuance exists; product semantics around service/workload ownership need tightening. |
| Storage | Canonical storage has `Service`, `ServiceKey`, `ApiKey`, `Client`, `ClientRegistration`, token, revoked-token, key, and audit tables. | [`service.py`](../pkgs/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/service.py), [`service_key.py`](../pkgs/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/service_key.py), [`api_key.py`](../pkgs/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/api_key.py) | The table base is present; workload, resource server, scope grant, client grant, and credential rotation models need sharper contracts. |
| Service keys | Integration coverage proves service key creation, digest handling, read-time raw-key exclusion, validity windows, and request rejection for raw key/digest injection. | [`test_service_key_creation.py`](../tests/integration/test_service_key_creation.py) | Good credential hygiene exists at service-key level. It should be linked into M2M product tests. |
| Resource validation | Resource-validation API is the preferred validation and metadata surface. | [OAuth 2.x Vendor Coverage Matrix](oauth-2x-vendor-coverage-matrix.md), [SPEC-1165](../.ssot/specs/SPEC-1165-resource-validation-api-contract.yaml) | M2M is incomplete without resource-server verification and API/resource metadata. |

## M2M Is a Product Lane

| Concern | Token-flow view | Product-lane view |
|---|---|---|
| Subject | `client_id` authenticates to `/token`. | A durable service/workload principal belongs to a tenant/platform context and has lifecycle, owner, environment, and trust posture. |
| Credential | `client_secret`, `private_key_jwt`, mTLS, DPoP, or service key proves control. | Credentials are issued, rotated, revoked, labeled, scoped, audited, and policy-bound. |
| Authorization | Token contains scopes/audience/resource. | Admins grant a service access to APIs/resources, scopes, tenants/orgs, and sometimes delegated admin actions. |
| Resource | Token is presented to an API. | Resource servers have identifiers, metadata, JWKS/introspection validation posture, accepted token profiles, and audience/scope contracts. |
| Operations | Token endpoint returns an access token. | Operators need inventory, last-used telemetry, dormant credential detection, rotation, revocation, incident response, and audit export. |
| Developer experience | Developer registers a client. | Developer sees app/client credentials, allowed grants, callback-free M2M setup, API permissions, token examples, and validation docs. |
| Tenant model | Client is registered under an issuer. | M2M access may be platform-owned, tenant-owned, org-scoped, environment-scoped, or cross-tenant delegated. |

## Vendor Product Shape

| Vendor | Product framing | Credential posture | Authorization/resource model | Notes |
|---|---|---|---|---|
| Auth0 | M2M applications use Client Credentials Flow to call APIs. Docs: [Auth0 Client Credentials Flow](https://auth0.com/docs/flows/client-credentials-flow), [Call Your API Using Client Credentials](https://auth0.com/docs/get-started/authentication-and-authorization-flow/call-your-api-using-the-client-credentials-flow). | Client ID/secret for M2M apps; credentials-exchange Actions can customize behavior. See [Auth0 Machine to Machine Trigger](https://auth0.com/docs/customize/actions/explore-triggers/machine-to-machine-trigger). | Register API, define permissions/scopes, authorize M2M app to API; B2B org-scoped M2M exists. See [Auth0 M2M Access for Organizations](https://auth0.com/docs/manage-users/organizations/organizations-for-m2m-applications). | Strong product framing: M2M app, API, permissions, organization scoping, Actions hook. |
| Okta | OAuth service apps use Client Credentials for machine-to-machine access to Okta APIs. Docs: [Okta OAuth for service apps](https://developer.okta.com/docs/guides/implement-oauth-for-okta-serviceapp/), [Okta Client Credentials Flow](https://developer.okta.com/docs/guides/implement-grant-type/clientcreds/main/). | For Okta API scoped access, `private_key_jwt` is required. See [Okta client authentication methods](https://developer.okta.com/docs/api/openapi/okta-oauth/guides/client-auth/). | Service app gets OAuth scopes and admin roles for least privilege. | Strong security posture: private-key JWT, scopes, admin-role assignment. |
| Keycloak | Confidential clients with service accounts use client credentials and service-account roles. Docs: [Keycloak OIDC endpoint layers](https://www.keycloak.org/securing-apps/oidc-layers), [Keycloak Server Administration Guide](https://www.keycloak.org/docs/latest/server_admin/). | Client secret and other configured client auth methods; service-account roles bind permissions. | Realm/client roles, client scopes, Authorization Services, policy enforcer, service account role mappings. See [Keycloak Authorization Services](https://www.keycloak.org/docs/latest/authorization_services/). | Strong self-hosted model: client/service-account roles and resource-server policy can be rich, but product boundaries are less SaaS-packaged. |
| FusionAuth | M2M is modeled through Entity Management plus Client Credentials. Docs: [FusionAuth Machine To Machine Communication](https://fusionauth.io/docs/get-started/use-cases/machine-to-machine), [FusionAuth Entity Management](https://fusionauth.io/docs/get-started/core-concepts/entity-management). | Entities can authenticate using client credentials; API keys also exist for platform APIs. | Entity relationships and permissions model which entities can access other entities. See [FusionAuth Types and Relationships](https://fusionauth.io/docs/get-started/core-concepts/types-and-relationships). | Strongest conceptual match for "everything is an entity with permissions." |
| Amazon Cognito | User Pool M2M uses client credentials, app clients, resource servers, and custom scopes. Docs: [Cognito scopes, M2M, and resource servers](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-define-resource-servers.html), [Cognito OAuth grants](https://docs.aws.amazon.com/cognito/latest/developerguide/federation-endpoints-oauth-grants.html). | App client must have a secret and support client credentials only; token endpoint issues access tokens. See [Cognito token endpoint](https://docs.aws.amazon.com/cognito/latest/developerguide/token-endpoint.html). | Resource servers and custom scopes define API authorization; client metadata/context can influence M2M tokens. See [AWS M2M context announcement](https://aws.amazon.com/about-aws/whats-new/2025/04/amazon-cognito-context-machine-to-machine-flows/). | Strong API/resource-server orientation; less general workload identity than cloud IAM. |
| `tigrbl_auth` | Draft product lane exists; service-admin plus developer plus public token plus resource-validation form the lane. | Supports client credentials, shared secret, private-key JWT, mTLS, DPoP, service keys, API keys in pieces. | Needs explicit resource server, scope grant, workload principal, service ownership, and audit product model. | Best next move: make M2M a governed profile and product slice, not just CRUD plus token endpoint. |

## Capability Matrix

| Capability | Current / target in `tigrbl_auth` | Priority |
|---|---|---|
| Service principal lifecycle | Current `Service` table and service-admin API. Needs owner, environment, purpose, and status semantics. | P0 |
| Workload principal lifecycle | Planned by ADR/SPEC, but no obvious canonical workload table yet. Should model workloads separately from generic services where identity attachment is environment/runtime-specific. | P1 |
| OAuth client credentials | Current `/token` supports `grant_type=client_credentials`. Must bind to registered client, tenant, scopes, audience/resource, and credential posture. | P0 |
| Strong client authentication | Existing code supports `private_key_jwt`, mTLS, and DPoP-related validation in token flow. Must be policy-selectable for M2M profiles. | P0 |
| Service keys | Current `ServiceKey` table and integration coverage. Needs product mapping: bootstrap secrets, local service credentials, or non-OAuth API access. | P0 |
| API keys | Current `ApiKey` table for user-bound keys. Must distinguish user API keys from service/workload credentials. | P1 |
| Resource server model | Resource-validation exists; canonical resource server table/spec should declare resource identifiers, accepted issuers, audiences, scopes, and validation method. | P0 |
| Scope and permission grants | Current token can carry scope; product model needs grant records: client/service -> resource -> scopes/roles -> tenant/org boundary. | P0 |
| Rotation and revocation | Service keys have validity windows; OAuth token revocation exists. Need service/client credential rotation workflow, last-used telemetry, and emergency revoke. | P0 |
| Audit and evidence | Audit tables exist; M2M needs event taxonomy for credential created/used/rotated/revoked, token issued, token introspected, grant changed. | P0 |
| Tenant/org scoping | Draft docs mention tenant/platform context; need explicit tenant/org scoped M2M grants similar to Auth0 org-scoped M2M. | P1 |
| Token format/profile | JWT access token profile, DPoP, mTLS, resource indicators are tracked. Need one M2M profile deciding defaults. | P1 |
| SDK/operator examples | No strong M2M SDK story yet. Need CLI/curl/Python examples for token issue and resource validation. | P2 |

## Recommended Product Boundary

| Surface | Owns | Does not own |
|---|---|---|
| `tigrbl-auth-api-public` | OAuth `/token` issuance for `client_credentials`, assertion grants, token exchange, metadata. | Service inventory, credential rotation UI, grant administration. |
| `tigrbl-auth-api-service-admin` | Service/workload principal lifecycle, service keys, API keys where service-bound, credential rotation/revocation, M2M audit. | Human login, tenant lifecycle, public consent, developer catalog UX. |
| `tigrbl-auth-api-developer` | App/client registration, client type, allowed grants, redirect-free M2M client setup, developer-facing credentials. | Operational service ownership, production workload rotation, platform-wide policy. |
| `tigrbl-auth-api-resource-validation` | JWKS, introspection, protected-resource metadata, issuer/resource/audience validation contracts. | Token issuance and credential lifecycle. |
| `tigrbl-authz-resource-server` | Protected API integration package: validate tokens, scopes, audience/resource, DPoP/mTLS confirmation claims. | Authorization-server route composition. |
| `@tigrbl-auth/service-admin-uix` | Inventory, status, credential posture, rotation, revocation, audit, access grants. | Hosted login or end-user self-service. |

## Minimum Viable M2M Slice

| Slice | Deliverable | Tests |
|---|---|---|
| M2M profile | Profile declaring allowed grant `client_credentials`, allowed client auth methods, token lifetime, sender-constraint options, and metadata behavior. | Profile load, metadata, and fail-closed tests. |
| Resource server table/contract | Canonical resource server model with identifier, tenant, issuer, accepted audiences, scopes, validation mode. | Storage symbol tests, migration tests, CRUD route/product-surface tests. |
| Client/service grant model | Grant record connecting client or service principal to resource server scopes and tenant/org boundary. | Positive/negative grant authorization tests. |
| Token issuance | `/token` client credentials issues access token with correct `sub`, `client_id`, `tid`, `scope`, `aud`, resource, and optional `cnf`. | Unit/integration tests for shared secret, private-key JWT, mTLS/DPoP where enabled. |
| Resource validation | Resource-validation API and resource-server package validate M2M token issuer, audience, scope, expiry, revocation/introspection, sender constraint. | Resource-server verifier contract tests and negative tests. |
| Credential lifecycle | Service key/client secret create, rotate, revoke, last-used telemetry, raw secret one-time display. | Service key/client credential lifecycle tests and audit assertions. |
| Audit taxonomy | M2M audit events for principal created, credential issued, token minted, grant changed, token denied, credential rotated/revoked. | Audit event shape tests and evidence fixture. |
| Examples | Curl and Python examples for creating service/client, granting API scope, requesting token, calling protected API, validating token. | Docs example smoke tests. |

## Recommended Defaults

| Decision | Recommendation | Reason |
|---|---|---|
| Default client auth | Use `private_key_jwt` for high-assurance service apps; keep `client_secret_basic` for local/dev and compatibility. | Matches Okta's stronger service-app posture while preserving practical compatibility. |
| Token type | JWT access tokens for first-party resource servers; introspection for opaque/high-control deployments. | JWT is efficient; introspection gives centralized revocation and policy control. |
| Sender constraint | Support DPoP and mTLS as profile options; require for high-assurance M2M profiles. | Limits token replay after credential/token theft. |
| Scopes | Model scopes on resource servers, not as free text on clients. | Keeps API authorization comprehensible and auditable. |
| Grants | Store explicit service/client-to-resource grants. | Avoids hidden authorization via broad client metadata. |
| Tenant boundary | Every M2M principal, credential, grant, token, and audit event must be tenant/platform scoped. | Prevents cross-tenant leakage and supports org-scoped M2M later. |
| Secret display | Raw service/client secrets only once at create/rotate time; store only digests or public keys. | Current service key behavior already follows this pattern. |
| Rotation | Rotation should create a new credential, overlap if configured, then revoke old credential. | Avoids brittle instant-cutover deployments. |
| Audit | Treat M2M as security-event heavy. Audit every credential and grant mutation and every denied token issuance. | M2M incidents often involve stale credentials and overbroad grants. |

## Proposed SSOT Follow-Up

The repo already has draft `adr:1085` and `spc:1177`. The next SSOT work should not duplicate those; it should mature them and add testable slices.

| Entity type | Proposed work | Purpose |
|---|---|---|
| ADR update | Accept or revise `adr:1085` after agreeing product boundary. | Make first-class M2M/workload identity a real decision. |
| SPEC update | Expand `spc:1177` with resource server, grant, credential, token, and audit requirements. | Move from product framing to implementation contract. |
| SPEC link | Link `spc:1160`, `spc:1165`, developer API spec, and public API spec to `spc:1177`. | Make cross-frontdoor ownership explicit. |
| Feature | `feat:m2m-workload-identity-profile` | M2M runtime/profile defaults and fail-closed behavior. |
| Feature | `feat:m2m-resource-server-and-scope-grants` | Resource server and grant model. |
| Feature | `feat:m2m-credential-lifecycle-and-audit` | Secret/key lifecycle and audit taxonomy. |
| Feature | `feat:m2m-token-issuance-and-resource-validation` | End-to-end client credentials issuance and protected-resource validation. |
| Test | `tst:m2m-client-credentials-token-contract` | Token claims, audience/resource, scopes, tenant binding. |
| Test | `tst:m2m-resource-server-validation-contract` | Protected resource validation success/failure. |
| Test | `tst:m2m-credential-lifecycle-audit` | Create/rotate/revoke/last-used/audit coverage. |
| Test | `tst:m2m-product-surface-fail-closed` | Ensure public/developer/service/resource-validation surfaces expose only their M2M responsibilities. |

## Product Interpretation

The product should be named and framed as M2M / Workload Identity, with service-admin as one management frontdoor inside that product lane.

The clean target is:

```text
tigrbl-identity-principals          # Service, client, workload, tenant principal semantics
tigrbl-authn-credentials         # Credential proof, API keys, service keys, rotation helpers
tigrbl-auth-protocol-oauth               # client_credentials, private_key_jwt, mTLS, DPoP, resource indicators
tigrbl-identity-storage             # Canonical service/client/key/token/audit/resource/grant tables
tigrbl-auth-api-public              # Token issuance and issuer metadata
tigrbl-auth-api-service-admin       # Service/workload lifecycle, credential lifecycle, audit
tigrbl-auth-api-developer           # Developer client/app registration and M2M setup
tigrbl-auth-api-resource-validation # Resource validation, introspection, protected-resource metadata
tigrbl-authz-resource-server     # Protected API integration
@tigrbl-auth/service-admin-uix      # M2M inventory, grants, credential posture, rotation, audit
```

This is the same architecture pattern competitors use, even when their packaging names differ: M2M is a product lane made of authorization-server behavior, client/service lifecycle, resource/API authorization, credential lifecycle, and operational governance.
