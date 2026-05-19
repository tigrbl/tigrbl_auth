# Identity Market Roadmap

This document captures the market-driven product strategy for the planned
identity package suite. It is a planning artifact, not a certification claim.
The current repository still treats final package-level certification as blocked
until the validated execution, clean-room, migration, and peer-evidence gates are
complete.

## Positioning

The repo should not be positioned as only IAM. IAM is one addressed market, but
the planned package suite also covers identity-provider infrastructure, API
access security, workload and machine identity, credential lifecycle, policy,
runtime assembly, operator workflows, and consumer SDKs.

Recommended positioning:

```text
Developer-first identity infrastructure for API and workload security.
```

Expanded positioning:

```text
An identity-provider and access-management platform for Tigrbl-native systems,
covering OAuth/OIDC, API authorization, workload identity, credentials, policy,
runtime assembly, operator control, and conformance-governed delivery.
```

## Market Reports

The following market reports are directional inputs for priority setting. The
markets overlap, so these values must not be summed into one total addressable
market.

| Rank | Market | CAGR | Forecast period | Reported size / forecast | Source |
|---:|---|---:|---|---|---|
| 1 | API Security | 32.2% | 2025-2034 | USD 751.05M in 2024 to USD 12.2457B by 2034 | [Market.us API Security Market](https://market.us/report/api-security-market/) |
| 2 | Workload Identity Security | 27.8% | 2025-2034 | USD 2.35B in 2024 to USD 27.31B by 2034 | [Market.us Workload Identity Security Market](https://market.us/report/workload-identity-security-market/) |
| 3 | Identity-as-a-Service | 24.7% | 2024-2030 | USD 7.21B in 2023 to USD 33.51B by 2030 | [Grand View Research IDaaS Market](https://www.grandviewresearch.com/industry-analysis/identity-as-a-service-market) |
| 4 | Privileged Access Management | 19.7% | 2025-2030 | USD 3.2857B in 2024 to USD 9.3856B by 2030 | [Grand View Research PAM Outlook](https://www.grandviewresearch.com/horizon/outlook/privileged-access-management-market-size/global) |
| 5 | Privileged Access Management | 18.0% | 2026-2032 | USD 3.6B in 2024 to USD 28B by 2032 | [Verified Market Research PAM Market](https://www.verifiedmarketresearch.com/product/privileged-access-management-market/) |
| 6 | Customer IAM | 17.4% | 2024-2030 | USD 8.12B in 2023 to USD 26.72B by 2030 | [Grand View Research CIAM Market](https://www.grandviewresearch.com/industry-analysis/customer-identity-access-management-market-report) |
| 7 | Machine Identity and Credential Management | 15.2% | 2026-2033 | USD 1.2B in 2024 to USD 3.8B by 2033 | [Verified Market Reports Machine Identity and Credential Management Market](https://www.verifiedmarketreports.com/product/machine-identity-and-credential-management-market/) |
| 8 | Identity and Access Management | 15.1% | 2024-2031 | USD 20.86B in 2024 to USD 58.2B by 2031 | [Verified Market Research IAM Market](https://www.verifiedmarketresearch.com/product/global-identity-access-management-market-size-and-forecast) |
| 9 | Identity Governance and Administration | 14.9% | 2025-2033 | USD 7.95B in 2024 to USD 27.11B by 2033 | [Grand View Research IGA Market](https://www.grandviewresearch.com/industry-analysis/identity-governance-administration-market-report) |
| 10 | API Security | 14.8% | 2024-2034 | USD 3.2B in 2024 to USD 12.8B by 2034 | [Emergen Research API Security Market](https://www.emergenresearch.com/industry-report/api-security-market) |
| 11 | Identity and Access Management | 11.3% | 2026-2033 | USD 26.77B in 2025 to USD 62.90B by 2033 | [Grand View Research IAM Market](https://www.grandviewresearch.com/industry-analysis/identity-and-access-management-iam) |
| 12 | Identity and Access Management | 10.4% | 2025-2030 | USD 25.96B in 2025 to USD 42.61B by 2030 | [MarketsandMarkets IAM Market](https://www.marketsandmarkets.com/Market-Reports/identity-access-management-iam-market-1168.html) |
| 13 | Customer IAM | 9.7% | 2025-2030 | USD 14.12B in 2025 to USD 22.47B by 2030 | [MarketsandMarkets CIAM report excerpt](https://www.prnewswire.com/) |

## Market-Driven Priority

The highest-growth signals point away from generic IAM-first sequencing and
toward API access security, workload identity, and developer-first IDaaS.

| Priority | Market driver | Repo / product focus |
|---:|---|---|
| 1 | API Security | Resource-server SDK, token validation, JWKS cache, introspection fallback, audience checks, scope checks, DPoP proof checks, mTLS binding checks, protected API middleware. |
| 2 | Workload Identity Security | Workload principals, service principals, machine principals, workload attestation, JWT assertions, mTLS credentials, DPoP keys, service keys, proof binding. |
| 3 | IDaaS | Runtime assembly, deployment profiles, feature flags, config precedence, tenant bootstrap, hosted provider shape, health and diagnostics, operator deploy flows. |
| 4 | PAM-adjacent Admin Authority | Admin, owner, tenant owner, superuser, delegated admin, break-glass semantics, privileged sessions, admin audit, credential mutation authorization. |
| 5 | CIAM | Relying-party SDK, user login, signup or invitation, password reset, MFA, passkeys, sessions, logout, consent, userinfo. |
| 6 | Machine Identity and Credential Management | App, client, service, API key, service key, rotation, last-used tracking, revocation, client-credential hardening. |
| 7 | IGA / Policy Governance | RBAC, ABAC, membership, entitlement review, policy registry, authorization traces, audit and provenance. |
| 8 | Core IAM | Users, groups, roles, permissions, tenant membership, basic admin CRUD. |

## Planned Product Lines

The planned package boundaries let the repo deliver a product line instead of a
single monolithic auth package.

| Product line | Package focus | Market tie |
|---|---|---|
| Identity Provider | server, runtime, storage, OAuth, OIDC, JOSE, admin | IAM, IDaaS, CIAM |
| API Access Security SDK | resource-server, JOSE, OAuth, policy, contracts | API Security |
| Workload Identity Suite | principals, credentials, policy, OAuth, JOSE | Workload Identity Security, Machine Identity |
| Credential Lifecycle | credentials, principals, policy, storage | Machine Identity, IAM, PAM-adjacent |
| Policy and Governance | policy, principals, contracts, admin | IGA, PAM-adjacent, IAM |
| Operator and Runtime Control | operator, runtime, server, storage | IDaaS, compliance automation |
| Relying Party SDK | rp, OIDC, OAuth, contracts, JOSE | CIAM, IDaaS |
| Testkit and Conformance | testkit, contracts, protocol fixtures | Developer infrastructure, compliance automation |

## Planned Package Priority

The market priority changes the implementation order. The provider still needs
core rails early, but the first visible product wedge should be API and workload
identity security, not generic IAM.

| Priority | Package boundary | Why |
|---:|---|---|
| 1 | `core` | Shared primitives required by every other package. |
| 2 | `contracts` | Stable external schemas and public contracts. |
| 3 | `jose` | Token verification, signing, JWKS, JWT, DPoP, and key material are foundational for API security and workload identity. |
| 4 | `principals` | Principal taxonomy must represent users, clients, apps, services, devices, machines, workloads, groups, roles, aliases, and tenants. |
| 5 | `credentials` | API keys, service keys, client secrets, passkeys, passwords, mTLS certs, JWT assertions, sessions, and lifecycle controls. |
| 6 | `policy` | Authorization decisions for scopes, tenants, RBAC, ABAC, delegation, credential use, and admin authority. |
| 7 | `resource-server` | Highest-growth API security wedge: token validation, audience/scope enforcement, JWKS cache, introspection fallback, proof checks. |
| 8 | `oauth` | Authorization server and token protocol state machines, including client credentials, device flow, token exchange, DPoP, mTLS, PAR, JAR, RAR. |
| 9 | `runtime` | Assembly, profile loading, config precedence, feature flags, deployment profiles, health, diagnostics, middleware enablement. |
| 10 | `operator` | CLI, bootstrap, migrations, import/export, certification reports, release gates, clean-room evidence, key/resource lifecycle. |
| 11 | `storage` | Durable Tigrbl/SQLAlchemy tables, migrations, repositories, SQLite/Postgres portability. SQLAlchemy is the default implementation substrate, not part of the tracked package name. |
| 12 | `server` | Tigrbl app/gateway/plugin composition, route binding, REST/RPC projection, public/admin surface wiring. |
| 13 | `oidc` | OIDC provider behavior, discovery, ID token, userinfo, logout, sessions, federated/social identity projection. |
| 14 | `admin` | Tenant/user/client/app/service/key/session/token/policy administration after policy and credential foundations are clear. |
| 15 | `rp` | Relying-party client SDK for login, callback handling, session establishment, logout, and userinfo mapping. |
| 16 | `testkit` | Fixtures, fake providers, fake repositories, fake key stores, conformance harnesses, protocol vectors. |
| 17 | `tigrbl-auth` facade | Compatibility and product facade over the split packages. |

## Delivery Waves

### Wave 1: API Access Security Foundation

Goal: create the fastest-growth wedge first.

Scope:

```text
core
contracts
jose
principals
credentials
policy
resource-server
```

Deliverables:

- Access-token claim models.
- JWKS cache and token validator.
- Audience and resource checks.
- Scope and permission checks.
- Introspection fallback client.
- DPoP proof validation.
- mTLS certificate binding validation.
- ASGI protected API middleware.
- Testkit token fixtures for protected APIs.

### Wave 2: Workload and Machine Identity

Goal: make non-human identity first-class.

Scope:

```text
principals
credentials
policy
jose
oauth
storage
```

Deliverables:

- Service principals.
- Machine principals.
- Workload principals.
- App and client principal relationships.
- API key and service key lifecycle.
- Client secret lifecycle.
- JWT bearer assertions.
- mTLS and DPoP proof binding.
- Workload attestation model.
- Rotation, revocation, redaction, and last-used tracking.

### Wave 3: IDaaS Runtime and Operator

Goal: make the provider deployable and operable as a product.

Scope:

```text
runtime
server
storage
operator
tigrbl-auth facade
```

Deliverables:

- Runtime assembly.
- Profile loading.
- Config precedence.
- Feature flag resolution.
- Deployment profiles.
- Runner selection.
- Lifecycle hooks.
- Health and diagnostics.
- Bootstrap and migration commands.
- Import/export workflows.
- Certification and evidence reports.

### Wave 4: CIAM and Relying Party Experience

Goal: support user-facing app identity flows after the provider and verifier
surfaces are stable.

Scope:

```text
oidc
rp
admin
credentials
policy
```

Deliverables:

- OIDC discovery client.
- Authorization URL builder.
- PKCE login flow.
- Callback validation.
- Token exchange client.
- ID token validation.
- RP session model.
- Userinfo client.
- Logout client behavior.
- Password reset and forgot-password flows.
- MFA and passkey support.
- Consent policy.

### Wave 5: Governance Depth

Goal: add deeper IAM, IGA, PAM-adjacent, and compliance workflows once the
high-growth access and workload foundations are in place.

Scope:

```text
policy
admin
principals
operator
testkit
```

Deliverables:

- Delegated admin policy.
- Tenant owner and superuser authority.
- Privileged admin sessions.
- Admin operation authorization.
- Entitlement and role review flows.
- Authorization traces.
- Audit provenance.
- Policy versioning.
- Release and conformance evidence linkage.

## Product Sequencing

First visible product:

```text
API and workload identity security for Tigrbl-native systems.
```

Second visible product:

```text
Deployable Tigrbl-native identity provider and operator runtime.
```

Third visible product:

```text
Consumer SDKs for protected APIs and relying-party applications.
```

The resulting product stack is:

| Product | Primary buyers / users |
|---|---|
| API Access Security SDK | API platform teams, service teams, backend developers. |
| Workload Identity Suite | Platform engineering, infrastructure, DevSecOps. |
| Identity Provider Runtime | Platform teams, SaaS builders, internal developer platforms. |
| Operator CLI | Operators, release engineers, compliance engineers. |
| Relying Party SDK | Application developers. |
| Policy and Governance Layer | Security engineering, IAM governance, tenant admins. |
| Testkit and Conformance Harness | Developers, auditors, certification maintainers. |

## Implications

- Do not lead with generic IAM CRUD as the first product wedge.
- Make API verification and workload identity first-class package boundaries,
  not later examples.
- Keep `resource-server` and `rp` as consumer packages so downstream apps do
  not inherit provider runtime, storage, or operator dependencies.
- Keep runtime assembly as a separate package because deployment profiles,
  feature flags, config precedence, lifecycle hooks, health checks, and
  middleware enablement are product surfaces.
- Keep operator workflows separate from request-path runtime behavior.
- Keep `tigrbl-auth` as the facade and compatibility product while the
  identity suite becomes the implementation and distribution layer.
