# SCIM 2.0 Focus

Research date: 2026-05-27

SCIM 2.0 is the provisioning protocol for moving identity lifecycle data across domains. It is not an OIDC login protocol and it is not an authorization-server surface. In product terms, SCIM is an inbound provisioning API used by enterprise IdPs and lifecycle-management systems to create, update, deactivate, and group users inside a service provider.

Normative anchors:

- [RFC 7643: SCIM Core Schema](https://www.rfc-editor.org/rfc/rfc7643)
- [RFC 7644: SCIM Protocol](https://www.rfc-editor.org/rfc/rfc7644)
- [IANA SCIM Schema URIs](https://www.iana.org/assignments/scim/scim.xhtml)

## Current `tigrbl_auth` State

| Area | Current state | Evidence | Interpretation |
|---|---|---|---|
| SSOT target | SCIM is tracked as `feat:f33-scim-provisioning` and covered by `adr:1052`, `spc:1068`, and `spc:1072`. | [ADR-1052](../.ssot/adr/ADR-1052-govern-access-governance-compliance-reporting-and-delegated-administration.yaml), [SPEC-1068](../.ssot/specs/SPEC-1068-federation-provisioning-and-cross-cloud-trust-requirements.yaml), [SPEC-1072](../.ssot/specs/SPEC-1072-access-governance-compliance-and-delegated-administration-requirements.yaml) | SCIM is governed, but not implemented as a product API. |
| Certification boundary | SCIM is explicitly out of the default baseline. | [Target Reality Matrix](compliance/TARGET_REALITY_MATRIX.md) | Current conformance claims should not imply SCIM support. |
| Runtime helper | `ScimProvisioningPlane` exists under governance-extension code and supports schema registration, user provision, group provision, simple patch, tenant snapshots. | [`governance_extension.py`](../pkgs/tigrbl-authz-policy/src/tigrbl_authz_policy/governance_extension.py) | Useful prototype/behavior seed, not a SCIM protocol server. |
| Tests | Unit tests cover schema registration, required fields, user patch, group membership, tenant mismatch, unsupported patch op. | [`test_governance_extension_plane_phase5.py`](../tests/unit/test_governance_extension_plane_phase5.py), [`test_phase5_governance_extension_boundary.py`](../tests/unit/test_phase5_governance_extension_boundary.py) | Current proof is helper-level T1/T2 behavior, not RFC 7643/7644 endpoint conformance. |
| Storage | Canonical storage has `Tenant`, `User`, `Service`, `Client`, keys, sessions, tokens, audit, etc.; no canonical `Group`/SCIM mapping tables are present. | [`tigrbl_identity_storage.tables`](../pkgs/tigrbl-identity-storage/src/tigrbl_identity_storage/tables) | User mapping can start from existing tables; group, membership, externalId, schema metadata, and SCIM audit need storage work. |
| Frontdoor API | No `tigrbl-auth-api-scim` or `/scim/v2` frontdoor exists. | Repo path scan | SCIM should be a new provisioning frontdoor or a tightly scoped Management API slice. |

## SCIM 2.0 Roles

| SCIM role | Meaning | `tigrbl_auth` mapping |
|---|---|---|
| SCIM Client | External IdP or lifecycle tool that sends provisioning operations. Examples: Okta, Microsoft Entra ID, Auth0 inbound SCIM partner connection, HRIS/IGA tooling. | A registered service/workload client with provisioning scopes and tenant binding. |
| SCIM Service Provider | The application/service receiving SCIM requests and managing identities. | A new `tigrbl_auth` SCIM/provisioning API frontdoor backed by canonical identity storage. |
| Resource Owner / Subject | User or group being provisioned. | Canonical `User`, future canonical `Group`, membership, entitlement, and audit records. |
| Authorization Server | Issues tokens used by the SCIM Client to call the SCIM Service Provider. | Existing `public-api` token issuer or service-admin-issued API/service key material. |
| Resource Server | Validates bearer credentials and enforces tenant/scim scopes on SCIM requests. | SCIM API frontdoor plus `resource-validation-api`/resource-server verifier contracts. |

## Protocol Surface

| Endpoint family | Expected behavior | Baseline priority | Notes for `tigrbl_auth` |
|---|---|---|---|
| `GET /scim/v2/ServiceProviderConfig` | Advertise supported auth schemes, PATCH, bulk, filter, change password, sort, ETag. | Must-have | This is the product honesty endpoint. It should only advertise what is implemented. |
| `GET /scim/v2/ResourceTypes` and `GET /scim/v2/ResourceTypes/{type}` | Describe `User`, `Group`, and schema endpoint locations. | Must-have | Use canonical route metadata and schema definitions. |
| `GET /scim/v2/Schemas` and `GET /scim/v2/Schemas/{id}` | Publish core User, Group, Enterprise User extension, and any supported extension schemas. | Must-have | Start with RFC 7643 core User/Group; add Enterprise User once storage mapping exists. |
| `GET /scim/v2/Users` | List/search users with filter, pagination, sort, and attribute projection. | Must-have | Minimum filters: `userName eq`, `externalId eq`, `id eq`; then broaden. |
| `POST /scim/v2/Users` | Create user with SCIM response body, stable `id`, `externalId`, `meta`. | Must-have | Must map `userName`, `displayName`, `active`, emails, names, externalId. |
| `GET /scim/v2/Users/{id}` | Read user by SCIM id. | Must-have | Enforce tenant and authorization scope. |
| `PUT /scim/v2/Users/{id}` | Replace user resource. | Should-have | Enterprise IdPs often use PUT for full updates. |
| `PATCH /scim/v2/Users/{id}` | Apply SCIM PATCH operations. | Should-have | Current helper supports only `add`/`replace`; RFC behavior needs paths, multi-value filters, and `remove`. |
| `DELETE /scim/v2/Users/{id}` | Deprovision user. | Must-have | Product decision: default to soft delete/deactivate (`active=false`) with audit evidence. |
| `GET/POST /scim/v2/Groups` | List/create groups. | Must-have | Requires canonical group and membership storage. |
| `GET/PUT/PATCH/DELETE /scim/v2/Groups/{id}` | Read/update/mutate/deprovision groups and memberships. | Must-have | Group membership is usually the enterprise value point. |
| `POST /scim/v2/.search` and resource-specific `.search` | POST-based search request. | Should-have | Useful for IdPs and clients that avoid URL-length/filter limits. |
| `POST /scim/v2/Bulk` | Bulk operations. | Later | Optional; high blast radius. Add only after single-resource semantics are stable. |
| `/scim/v2/Me` | Self-resource alias. | Later / likely out-of-scope | This is less relevant for inbound enterprise provisioning; account self-service should be its own product lane. |

## Data Model Requirements

| Model area | Required fields / behaviors | Current repo fit |
|---|---|---|
| SCIM User identity | `id`, `externalId`, `userName`, `active`, `name`, `displayName`, `emails`, `phoneNumbers`, `addresses`, `groups`, `meta`. | Existing `User` likely covers only part of this; needs SCIM profile/mapping layer. |
| SCIM Group | `id`, `externalId`, `displayName`, `members`, `meta`. | Missing canonical group/membership table. |
| Enterprise User extension | `employeeNumber`, `costCenter`, `organization`, `division`, `department`, `manager`. | Missing; should be optional and extension-backed. |
| Schema metadata | `schemas`, `ResourceType`, schema attributes, mutability, returned, uniqueness, canonical values. | Missing as runtime protocol metadata. |
| Versioning | `meta.version` / ETag-like optimistic concurrency. | Missing. Needed for robust PUT/PATCH. |
| Idempotency and correlation | `externalId`, source IdP connection, tenant, request id, audit event id. | Partial via tenant and audit primitives; needs explicit SCIM import state. |
| Error model | SCIM Error schema, HTTP statuses, `scimType`, fail-closed validation. | Missing at protocol level. |
| Tenant boundary | Tenant-scoped base URL or tenant-specific host; every resource and token must bind to tenant. | Existing tenant model helps; API shape needs decision. |

## Vendor Surface Comparison

| Vendor | SCIM stance | Product shape | Notes |
|---|---|---|---|
| Auth0 | Present as inbound SCIM for enterprise/B2B connections. | Enterprise connection provisioning surface plus Management API/user logs. | Auth0 frames SCIM as enterprise connection provisioning, not public login. See [Configure Inbound SCIM](https://auth0.com/docs/authenticate/protocols/scim/configure-inbound-scim/). |
| Okta | Strong SCIM client/integration stance; supports building SCIM-compliant app servers and OIN integrations. | Okta lifecycle provisioning and SCIM 2.0 integration guides. | Okta is often the SCIM client pushing users/groups into apps. See [Okta SCIM 2.0](https://developer.okta.com/docs/api/openapi/okta-scim/guides/scim-20/) and [Understanding SCIM](https://developer.okta.com/docs/concepts/scim/). |
| Keycloak | Emerging/experimental core SCIM Realm API in 26.6; historically extension-based. | Realm SCIM API and community extensions. | Treat as experimental, not mature long-standing core parity. See [Keycloak SCIM experimental feature](https://www.keycloak.org/2026/04/scim-as-experimental-feature). |
| FusionAuth | Present as SCIM API for users/groups. | Dedicated SCIM API endpoints under FusionAuth API catalog. | FusionAuth exposes SCIM as user/group provisioning API. See [FusionAuth SCIM APIs](https://fusionauth.io/docs/apis/scim). |
| Amazon Cognito | Cognito User Pools do not appear to expose a first-class SCIM user-pool API; AWS IAM Identity Center does support SCIM for its own identity-center product. | Cognito uses User Pools APIs/managed login; IAM Identity Center has separate SCIM provisioning. | Do not treat Cognito User Pools as SCIM-equivalent. See [Cognito User Pools API](https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/Welcome.html) and [IAM Identity Center SCIM provisioning](https://docs.aws.amazon.com/singlesignon/latest/userguide/provision-automatically.html). |

## Recommended `tigrbl_auth` Target Architecture

| Decision | Recommendation | Reason |
|---|---|---|
| Product lane | Treat SCIM as `Provisioning API`, not as public login, tenant-admin CRUD, or OIDC OP behavior. | Competitors expose SCIM as enterprise provisioning/lifecycle surface. |
| Backend package | Add `tigrbl-identity-scim` only when implementation begins. | Keeps RFC 7643/7644 schemas, filters, PATCH semantics, SCIM errors, and mapping logic isolated from generic admin CRUD. |
| Frontdoor package | Add `tigrbl-auth-api-scim` or `tigrbl-auth-api-provisioning` with `/scim/v2`. | SCIM clients expect a clean protocol base URL and standard resource paths. |
| Storage | Extend `tigrbl-identity-storage` with canonical `Group`, membership, SCIM external identity mapping, schema/connection metadata, and provisioning audit records. | SCIM must not duplicate identity tables or bypass canonical storage. |
| Authn/authz | Protect SCIM with bearer tokens or service keys bound to tenant + SCIM scopes. | SCIM is a protected resource server surface. The SCIM API should consume tokens, not issue them. |
| Tenant routing | Prefer tenant-scoped base URL: `/tenants/{tenant_slug}/scim/v2` for local/dev, with host-based tenant routing allowed later. | Enterprise IdPs configure one SCIM base URL per application/tenant. |
| Admin UIX | Put SCIM connection setup and status in tenant-admin/platform-admin UIX, not public UIX. | Admins configure provisioning; end users do not interact with SCIM directly. |
| Evidence | Keep SCIM out of current certification until endpoint-level conformance exists. | Current helper tests are not RFC 7643/7644 conformance evidence. |

## Minimum Viable SCIM Slice

| Slice | Deliverable | Tests |
|---|---|---|
| SCIM contracts | Pydantic/dataclass models for ListResponse, Error, User, Group, PatchOp, ServiceProviderConfig, ResourceType, Schema. | Unit tests against RFC-shaped examples and required fields. |
| Storage migration | Canonical group, group membership, SCIM external mapping, and provisioning audit tables. | Migration up/down and storage symbol tests. |
| Protocol engine | Filter parser subset, pagination, attributes/excludedAttributes projection, PATCH operation evaluator, SCIM error mapper. | Unit/negative tests for filters, pagination, unknown attributes, unsupported operations, tenant mismatch. |
| Frontdoor API | `/scim/v2/ServiceProviderConfig`, `/ResourceTypes`, `/Schemas`, `/Users`, `/Groups`. | OpenAPI route tests, behavior tests, fail-closed auth tests. |
| IdP interop profile | Okta-compatible inbound provisioning profile first. | Scripted fixture sequence: create user, query by `userName`, update, deactivate, create group, add/remove member. |
| Audit/evidence | Provisioning audit events with source client, tenant, externalId, operation, resource id, result. | Evidence JSON and regression tests. |

## Proposed Product Boundary

SCIM should become a new provisioning surface, not a feature hidden inside `/admin/identity`.

The clean target is:

```text
tigrbl-identity-scim                 # RFC 7643/7644 schemas, protocol logic, filters, PATCH, errors
tigrbl-auth-api-scim                 # Deployable SCIM v2 frontdoor
@tigrbl-auth/tenant-admin-uix        # SCIM connection setup/status UI
tigrbl-identity-storage              # Canonical users, groups, memberships, mappings, audit
tigrbl-authz-resource-server      # Token/scope validation integration for SCIM API
```

This keeps the split consistent with the repo's current direction: canonical storage owns tables, protocol packages own protocol semantics, and frontdoor APIs own route composition and product filtering.

