> [!WARNING]
> Archived historical reference. This document is retained for audit history only and is **not** an authoritative current-state artifact.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` for the current source of truth.

# tigrbl_auth — AuthN/Z Matrices

## Scope and assumptions

This document combines:

- the revised standards matrix from `tigrbl_auth_standards_compliance_matrix_v2`, and
- the currently uploaded `tigrbl_auth` package state.

### Current package signal

The current package already shows meaningful auth-server intent:

- `runtime_cfg.py` exposes a large set of RFC feature toggles as environment-backed settings,
- `app.py` mounts `surface_api`, OIDC discovery, RFC 8693, RFC 7009, RFC 8414, and an `rfc8932` hook,
- the package exposes `/login` and `/authorize` surfaces,
- the test suite covers many OAuth/OIDC/JOSE RFCs,
- there is **no first-class CLI surface** yet; the CLI rows below are therefore a **proposed CLI contract** built on top of the current settings model.

### Terminology used below

- **RFC targets** = normative IETF targets.
- **Specifications** = non-RFC but still normative/important specs, such as OIDC, MCP, A2A, OpenAPI, OpenRPC.
- **CLI flag groups** = top-level command namespaces for the future `tigrbl-auth` CLI.
- **CLI flag features** = concrete switches or subcommands.
- **Operationals** = non-protocol runtime controls.
- **Interops** = external systems, flows, or clients that should work with the capability.

---

## Matrix 1 — Capability × RFC / Spec / CLI / Operational / Interop

| Capability slice | RFC target(s) | Feature(s) | Specification(s) | CLI flag group(s) | CLI flag feature(s) | Operational(s) | Interop(s) | Current package signal | Gap / next action |
|---|---|---|---|---|---|---|---|---|---|
| Core authorization server | RFC 6749, RFC 6750, RFC 7636, RFC 9700 | authorization endpoint, token endpoint, bearer token handling, PKCE, redirect validation, error model | OAuth 2.0; OAuth 2.1 alignment profile | `serve`, `oauth-core`, `security` | `--enable-rfc6749`, `--enable-rfc6750`, `--enable-rfc7636`, `--require-tls`, `--exact-redirect-match` | issuer config, redirect registry, rate limits, CSRF/state validation | browser RPs, SPAs, confidential clients, resource servers | runtime flags exist; `/authorize` and auth flow routes exist; token tests exist | make OAuth 2.1 alignment explicit; wire RFC 9700 controls into release gates |
| Discovery and well-known metadata | RFC 8414, RFC 8615, RFC 9207 | AS metadata, issuer discovery, well-known endpoints, issuer identification | OIDC Discovery 1.0 | `discovery`, `serve` | `--enable-rfc8414`, `--enable-rfc9207`, `--issuer`, `--public-base-url` | deterministic metadata emission, hostname/issuer consistency, cache headers | OIDC clients, MCP clients, gateways, SDK generators | OIDC discovery and RFC 8414 are mounted | switch well-known target to RFC 8615 in docs and claims; add strict issuer validation evidence |
| OIDC identity provider surface | RFC 7519, RFC 7517, RFC 7518, RFC 7515, RFC 7516 | ID tokens, UserInfo, nonce handling, claims issuance, optional ID-token encryption | OpenID Connect Core 1.0; UserInfo; Discovery | `oidc`, `tokens`, `discovery` | `--enable-oidc`, `--enable-userinfo`, `--enable-id-token-encryption`, `--id-token-alg`, `--id-token-enc` | claim templates, audience rules, key rollover, consent UX | OIDC RPs, mobile clients, browser clients | `oidc_id_token.py`, `oidc_userinfo.py`, discovery code, JOSE flags | add full OIDC conformance mapping and claim policy ADR |
| Sessions, cookies, and logout | RFC 6265, RFC 7009 | browser sessions, cookie policy, logout, revocation, session invalidation | OIDC RP-Initiated Logout; OIDC Session Mgmt; Front-Channel Logout; Back-Channel Logout | `sessions`, `logout`, `tokens` | `--session-mode=cookie|token`, `--session-cookie-secure`, `--session-cookie-samesite`, `--enable-rp-logout`, `--enable-frontchannel-logout`, `--enable-backchannel-logout` | session store, purge jobs, replay resistance, logout propagation | browser apps, multi-app SSO, account portals | `/logout` surface exists; revocation support exists; auth session table exists | OIDC logout family not yet a clearly surfaced certifiable boundary |
| Dynamic client registration and management | RFC 7591, RFC 7592 | register client, rotate registration access tokens, manage/update/delete clients | OIDC Dynamic Client Registration profile | `clients`, `policies` | `--enable-rfc7591`, `--enable-rfc7592`, `register-client`, `update-client`, `delete-client`, `--allow-anonymous-dcr` | anti-abuse controls, trusted-host policy, registration audit, approval flows | MCP clients, marketplaces, self-service developer onboarding, Keycloak-style DCR interop | runtime flags and tests exist | surface real HTTP endpoints and registration policies; gate anonymous DCR behind policy |
| Token lifecycle and resource-server support | RFC 7009, RFC 7662, RFC 9068, RFC 6750 | revocation, introspection, JWT access token profile, bearer methods | OAuth token lifecycle; resource server verification profile | `tokens`, `resource-server` | `--enable-rfc7009`, `--enable-rfc7662`, `--enable-rfc9068`, `--access-token-format=jwt|opaque`, `--allow-query-bearer`, `--allow-form-bearer` | revocation store, introspection cache TTL, token TTL policy, gateway integration | API gateways, MCP servers, resource servers, service meshes | revocation and introspection code/tests exist; JWT profile helpers exist | make JWT-vs-opaque mode explicit and publish RS validation guidance |
| Device and CLI login | RFC 8628, RFC 8252 | device authorization, user code verification, native redirect safety | OAuth 2.0 Device Authorization Grant; native-app profile | `device`, `clients` | `--enable-rfc8628`, `device authorize`, `device verify`, `--device-code-ttl`, `--user-code-length`, `--poll-interval-seconds`, `--enforce-rfc8252` | polling limits, user code entropy, verification UX, abuse protection | CLI apps, TVs/devices, terminal tools | runtime flag and tests exist | mount and certify full device endpoints; add CLI UX contract |
| Token exchange and delegation | RFC 8693, RFC 8707 | subject token exchange, delegation, impersonation, audience/resource rebinding | OAuth Token Exchange | `exchange`, `tokens`, `policy` | `--enable-rfc8693`, `exchange-token`, `--allow-impersonation`, `--allow-delegation`, `--default-audience-policy` | policy approval, audit trail, limited scope derivation, tenant controls | service-to-service, backend-for-frontend, chained API calls | RFC 8693 include hook is mounted | add policy engine and claim/evidence rules for delegation vs impersonation |
| Authorization-request hardening | RFC 9101, RFC 9126, RFC 9396 | JAR, PAR, rich authorization requests, structured authorization details | OAuth hardening profile | `hardening`, `oauth-core`, `policy` | `--enable-rfc9101`, `--enable-rfc9126`, `--enable-rfc9396`, `--require-par`, `--require-request-object`, `--allow-authorization-details` | request object validation, nonce/state rules, storage/expiry for PAR objects | high-security clients, MCP-adjacent flows, regulated deployments | helper code/tests and PAR model signal exist | surface certifiable endpoints and enforce mode switches |
| Sender-constrained tokens | RFC 9449, RFC 8705, RFC 7800 | DPoP proof verification, mTLS client auth, cnf handling, token binding | DPoP profile; mTLS profile | `proof`, `trust`, `clients` | `--enable-rfc9449`, `--enable-rfc8705`, `--require-dpop`, `--require-mtls`, `--bind-refresh-tokens`, `--accept-client-cert` | certificate handling, replay cache, proof clock skew, thumbprint tracking | high-security APIs, financial-grade patterns, Keycloak-style DPoP interop | flags and helper code/tests exist | move from helper-level support to enforced end-to-end proof validation |
| Trust and protected-resource metadata | RFC 9728, RFC 8414, RFC 7517, RFC 9700 | protected resource metadata, auth-server metadata, JWKS, signed metadata, trust anchors | MCP Authorization; OIDC Discovery | `trust`, `discovery`, `keys` | `--enable-rfc9728`, `--signed-metadata`, `--jwks-rotation-seconds`, `--trusted-issuer`, `--trusted-jwks` | trust-store management, metadata signing, issuer pinning, rotation runbooks | MCP clients and servers, gateways, zero-config discovery | current package has AS metadata and JWKS, but not explicit RFC 9728 surface | add `/.well-known/oauth-protected-resource` and tie it to MCP profile claims |
| JOSE, keys, and crypto policy | RFC 7515, RFC 7516, RFC 7517, RFC 7518, RFC 7519, RFC 7638, RFC 8037, RFC 8725 | JWS, JWE, JWK, JWT, thumbprints, EdDSA, algorithm allowlists, `none` rejection | JOSE stack; JWT BCP | `keys`, `tokens`, `hardening` | `--enable-rfc7515`, `--enable-rfc7516`, `--enable-rfc7517`, `--enable-rfc7518`, `--enable-rfc7519`, `--enable-rfc7638`, `--enable-rfc8037`, `--enable-rfc8725`, `--jws-alg-allowlist` | HSM/KMS integration, key generation, rotation policy, signing/encryption separation | OIDC RPs, gateways, language SDKs | strong helper coverage and tests exist | formalize key lifecycle and algorithm policy as ADR + release gate |
| Contracts and machine-readable descriptions | RFC 9110 (HTTP semantics), RFC 8615 | published OpenAPI and OpenRPC contracts; discovery documents; stable method/operation names | OpenAPI 3.1.x; OpenRPC 1.4.x | `contracts`, `rpc`, `docs` | `--emit-openapi`, `--emit-openrpc`, `--openapi-version`, `--rpc-discover`, `--spec-output-dir` | spec generation, drift detection, versioning, linting | SDK generators, doc portals, admin automation | OpenAPI tests exist; no first-class CLI or contract emission pipeline yet | publish spec artifacts on every release and gate diff drift |
| Certification, evidence, and peer claims | RFC 9700, RFC 9728 (where claimed), RFC 9449 / 8705 / 9126 / 9101 (where claimed) | release gates, evidence bundles, wire captures, peer-reviewed claim packs | internal certification tier model; independent peer-claim discipline | `gates`, `evidence`, `certify` | `--gate-`, `--gate-tier`, `--require-evidence`, `--require-peer-review`, `collect-evidence`, `verify-claims` | CI gates, artifact retention, waivers, attestation signing | external auditors, peer review, cross-stack interop testing | standards matrix exists, but package repo lacks gate/evidence structure | add compliance plane and block Tier 3/4 claims without artifacts |
| Advanced federation and trust expansion | RFC 5280, RFC 9525, RFC 8446; optionally RFC 8705 / future SPIFFE drafts | external IdP trust, x509-based client trust, service identity, future federation | OpenID Federation 1.0; SPIFFE/SPIRE ecosystem | `federation`, `trust` | `--enable-openid-federation`, `--enable-client-assertions`, `--truststore-path`, `--allow-spiffe` | truststore ops, certificate lifecycle, federation metadata policy | Keycloak-class federation, mesh/workload identities | currently out of scope or helper-level only | keep out of core baseline until core AS/OP boundary is certifiable |

---

## Matrix 2 — Proposed CLI flag groups

> The current package is environment-variable driven. The table below defines the **recommended CLI contract** that should sit on top of the existing `Settings` model.

| CLI flag group | Scope | Example flag features | Maps cleanly to current package? | Operational intent | Interop intent |
|---|---|---|---|---|---|
| `serve` | process and network identity | `--host`, `--port`, `--issuer`, `--public-base-url`, `--require-tls`, `--trust-proxy` | yes | stable deployment identity and safe edge deployment | consistent issuer/discovery for OIDC, MCP, gateways |
| `oauth-core` | core AS behavior | `--enable-rfc6749`, `--enable-rfc6750`, `--enable-rfc7636`, `--allow-query-bearer`, `--allow-form-bearer` | yes | control bearer semantics and core OAuth surface | browser, SPA, confidential-client compatibility |
| `oidc` | OP behavior | `--enable-oidc`, `--enable-userinfo`, `--enable-id-token-encryption`, `--enable-rp-logout`, `--enable-frontchannel-logout`, `--enable-backchannel-logout` | partial | explicit OIDC surface and session/logout behavior | RP interoperability and OIDC certification prep |
| `clients` | client registration and policy | `--enable-rfc7591`, `--enable-rfc7592`, `--allow-public-clients`, `--allow-anonymous-dcr`, `--require-pkce` | partial | safe client onboarding and DCR policy | MCP, marketplaces, developer portals |
| `tokens` | token issuance and validation | `--enable-rfc7009`, `--enable-rfc7662`, `--enable-rfc9068`, `--access-token-format=jwt|opaque`, `--access-token-ttl`, `--refresh-rotation` | partial | govern token lifecycle and revocation | resource servers, gateways, machine clients |
| `device` | device and terminal flows | `--enable-rfc8628`, `--device-code-ttl`, `--user-code-length`, `--poll-interval-seconds` | yes | safe CLI/device UX and abuse control | CLI tools, TV/device apps |
| `exchange` | delegation and impersonation | `--enable-rfc8693`, `--allow-impersonation`, `--allow-delegation`, `--exchange-audience-policy` | partial | controlled service-to-service delegation | backend chains, zero-trust API fabrics |
| `hardening` | request-channel and redirect hardening | `--enable-rfc9101`, `--enable-rfc9126`, `--enable-rfc9396`, `--exact-redirect-match`, `--forbid-implicit` | partial | enforce high-security deployment posture | regulated or high-assurance clients |
| `proof` | sender-constrained tokens | `--enable-rfc9449`, `--require-dpop`, `--enable-rfc8705`, `--require-mtls`, `--bind-refresh-tokens` | partial | proof validation, certificate binding, replay protection | DPoP/mTLS capable clients and APIs |
| `trust` | discovery and trust anchors | `--enable-rfc8414`, `--enable-rfc9728`, `--trusted-issuer`, `--trusted-jwks`, `--signed-metadata` | partial | trust bootstrap and metadata signing | MCP discovery, external RPs, gateways |
| `keys` | signing/encryption material | `--jwks-rotation-seconds`, `--jws-alg-allowlist`, `--jwe-alg-allowlist`, `--kms-uri`, `--active-kid` | partial | cryptographic safety and rotation | JOSE consumers, RP/RS verification |
| `contracts` | spec generation | `--emit-openapi`, `--emit-openrpc`, `--openapi-version`, `--rpc-discover`, `--spec-output-dir` | no | prevent contract drift | SDKs, docs, admin tooling |
| `gates` | release policy | `--gate-`, `--gate-tier`, `--waiver-file`, `--require-evidence`, `--require-peer-review` | no | enforce release gates and certification discipline | peer review and external validation |
| `evidence` | claim artifact generation | `collect-evidence`, `verify-claims`, `bundle-peer-pack`, `publish-attestation` | no | preserve certifiable proof of conformance | Tier 3 and Tier 4 claimability |

---

## Matrix 3 — Protocol / peer boundary matrix

| System | Boundary relative to `tigrbl_auth` | AuthN/AuthZ features that matter | RFC / spec signal | Operational emphasis | Interop implication for `tigrbl_auth` |
|---|---|---|---|---|---|
| A2A | protocol consumer, not an IdP | HTTPS, TLS identity validation, Agent Card auth discovery, HTTP header credentials, implementation-specific authz by skills/actions/scopes | A2A spec; HTTP auth; TLS | Agent Card publication, challenge semantics, least privilege | `tigrbl_auth` should provide transport auth + discovery, not A2A task orchestration |
| MCP | protected-resource and auth discovery profile | OAuth 2.1-style auth, PKCE, protected resource metadata, AS discovery, refresh rotation, exact redirects | MCP Authorization; RFC 9728; RFC 8414; OIDC Discovery | resource metadata, secure token storage, short-lived tokens | `tigrbl_auth` must add RFC 9728 and MCP-ready discovery if it wants first-class MCP support |
| Firebase Auth | app-centric CIAM | email/password, phone, federated IdPs, anonymous auth, custom claims, session cookies; Identity Platform adds MFA, SAML/OIDC, multitenancy | Firebase Auth; OAuth 2.0 / OIDC use | hosted UX, SDK-first integration, session cookies | stronger app UX benchmark, but weaker standards-transparency benchmark |
| Supabase Auth | auth + data-plane authorization platform | password, magic link, OTP, phone, social login, MFA, JWTs, AAL claims, RLS integration; OAuth 2.1/OIDC AS supports auth-code+PKCE and refresh only | Supabase Auth; OAuth 2.1/OIDC profile | DB-centric authz, self-hosting, RLS | `tigrbl_auth` should not copy RLS; it should beat Supabase on standards conformance evidence |
| Clerk | developer-centric CIAM + OAuth provider | sessions, organizations, roles/permissions, OAuth apps, DCR, consent, public clients + PKCE, JWT or opaque tokens, machine auth, API keys | Clerk OAuth docs; OIDC/OAuth metadata | polished DX, session tooling, org authz | strong benchmark for app-facing developer ergonomics and DCR policy |
| FastAPI Users | app library, not AS/IdP | register/login/logout, verify/reset flows, cookie or bearer transport, JWT/database/Redis strategy, OAuth association | FastAPI Users docs | app embedding and route generation | `tigrbl_auth` boundary is broader: AS/OP + trust plane, not just app-local auth |
| Django auth | framework-local auth subsystem | users, groups, permissions, pluggable backends, password hashing, sessions; missing built-in OAuth, throttling, object perms | Django auth docs | session middleware, admin integration | `tigrbl_auth` should integrate with frameworks, not reduce itself to framework-local auth |
| Keycloak | closest full-stack peer | OIDC, OAuth2, SAML, identity brokering, user federation, sessions, token mappers, device grant, DPoP, dynamic client registration, standard token exchange | Keycloak admin docs | large IAM boundary, broker/federation, admin control plane | strongest peer for standards breadth; `tigrbl_auth` must be narrower but cleaner and more certifiable |

---

## Matrix 4 — Missing targets and concrete gaps

| Gap | Missing RFC target(s) / spec(s) | Missing feature(s) | CLI flag group(s) | CLI flag feature(s) | Operational blocker | Interop blocker | Priority |
|---|---|---|---|---|---|---|---:|
| Protected resource metadata | RFC 9728 | `/.well-known/oauth-protected-resource`, `authorization_servers`, `resource_metadata` challenge path | `trust` | `--enable-rfc9728`, `--resource-metadata-url` | no MCP-ready resource metadata plane | blocks full MCP authorization discovery | 1 |
| Well-known claim cleanup | RFC 8615 | stop claiming RFC 5785 as current target; align all docs/specs to RFC 8615 | `discovery` | `--well-known-profile=current` | stale or obsolete claim language | weakens standards precision | 1 |
| Security BCP as hard gate | RFC 9700 | exact redirect match, open-redirect defense, implicit-off posture, refresh rotation, stronger defaults | `hardening`, `gates` | `--forbid-implicit`, `--exact-redirect-match`, `--refresh-rotation`, `--gate-tier=3` | no formal hardening gate | weakens certifiable production posture | 1 |
| OIDC logout suite | OIDC RP-Initiated Logout, Front-Channel Logout, Back-Channel Logout | full logout endpoints and propagation | `oidc`, `sessions` | `--enable-rp-logout`, `--enable-frontchannel-logout`, `--enable-backchannel-logout` | incomplete browser session semantics | partial RP interop | 1 |
| Client registration surfacing | RFC 7591, RFC 7592 | first-class DCR + management endpoints with policy controls | `clients` | `--enable-rfc7591`, `--enable-rfc7592`, `--allow-anonymous-dcr` | unsafe or absent self-service onboarding | blocks MCP optional DCR and marketplace onboarding | 1 |
| PAR/JAR/RAR enforcement | RFC 9126, RFC 9101, RFC 9396 | enforced request-object and PAR flow, rich authorization details | `hardening`, `policy` | `--require-par`, `--require-request-object`, `--allow-authorization-details` | insufficient high-assurance flow control | weak interop with security-sensitive clients | 2 |
| Sender-constrained enforcement | RFC 9449, RFC 8705 | end-to-end DPoP/mTLS issuance + verification, not just helpers | `proof` | `--require-dpop`, `--require-mtls`, `--bind-refresh-tokens` | replay/certificate handling missing as release gate | blocks higher-assurance API interop | 2 |
| JWT access token profile claim | RFC 9068 | explicit JWT AT profile mode and RS documentation | `tokens` | `--enable-rfc9068`, `--access-token-format=jwt` | RS validation ambiguity | weak gateway and resource-server predictability | 2 |
| OpenAPI security completeness | OpenAPI 3.1.x | complete security schemes for bearer, oauth2, openIdConnect, mutualTLS, cookie/API key where used | `contracts` | `--emit-openapi`, `--openapi-version=3.1.2` | no contract gate | weak SDK/doc interop | 2 |
| OpenRPC admin-only boundary | OpenRPC 1.4.x | explicit admin/control-plane JSON-RPC contract + `rpc.discover` | `contracts`, `rpc` | `--emit-openrpc`, `--rpc-discover` | no stable RPC contract | weak automation/admin-tool interoperability | 3 |
| Certification plane | internal tier model + peer claims discipline | release gates, evidence bundle, waivers, attestation output | `gates`, `evidence` | `--gate-`, `--gate-tier`, `collect-evidence`, `publish-attestation` | cannot prove Tier 3/4 claims | blocks independent peer validation | 1 |
| Trust/federation expansion | OpenID Federation 1.0; optional SPIFFE-related future work | federation metadata and workload/client trust | `federation`, `trust` | `--enable-openid-federation`, `--allow-spiffe` | trust-store and policy complexity | only needed for advanced trust topologies | 4 |
| Mis-scoped auth-core targets | RFC 8932 is not an auth-server core target | remove DNS privacy guidance from auth-core claim plane | `gates`, `claims` | `verify-claims --strict-core` | misleading standards boundary | weakens credibility of compliance claims | 1 |

---

## Matrix 5 — Boundary of `tigrbl_auth`

| In scope | Out of scope | Why |
|---|---|---|
| OAuth authorization server endpoints | A2A task execution semantics | A2A consumes auth; it is not an IdP/AS replacement |
| OIDC provider endpoints and metadata | MCP tool/runtime semantics | MCP consumes auth discovery and tokens |
| sessions, cookies, logout, revocation, introspection | generic app-local auth scaffolding | frameworks like Django/FastAPI already do this locally |
| client registration, device flow, token exchange, PAR/JAR/RAR | product entitlements / business permissions engine | that is higher-level product policy, not core AS/OP behavior |
| sender-constrained tokens, JOSE/JWT/JWKS, trust metadata | Firebase-style hosted app UX surface | not the differentiator for a certifiable standards package |
| OpenAPI/OpenRPC contracts for REST/admin RPC | database-native authz like Supabase RLS | `tigrbl_auth` should integrate with RLS, not become RLS |
| certification evidence, release gates, peer-claim bundles | full Keycloak-sized LDAP/Kerberos/IdP-broker platform in baseline | too large for the initial certifiable boundary |

---

## Recommended package-level CLI layout

```text
tigrbl-auth
├── serve
├── discovery
├── oauth-core
├── oidc
├── clients
├── tokens
├── sessions
├── device
├── exchange
├── hardening
├── proof
├── trust
├── a2a
├── contracts
├── gates
└── evidence
```

### Example CLI feature slices

```text
tigrbl-auth serve --issuer https://auth.example.com --require-tls

tigrbl-auth discovery --enable-rfc8414 --enable-rfc9728 --signed-metadata

tigrbl-auth oauth-core --enable-rfc6749 --enable-rfc6750 --enable-rfc7636

tigrbl-auth oidc --enable-userinfo --enable-rp-logout --enable-id-token-encryption

tigrbl-auth clients --enable-rfc7591 --enable-rfc7592 --require-pkce

tigrbl-auth tokens --enable-rfc7009 --enable-rfc7662 --enable-rfc9068 --access-token-format jwt

tigrbl-auth device --enable-rfc8628 --device-code-ttl 900

tigrbl-auth exchange --enable-rfc8693 --allow-delegation

tigrbl-auth hardening --enable-rfc9101 --enable-rfc9126 --forbid-implicit

tigrbl-auth proof --enable-rfc9449 --require-dpop

tigrbl-auth contracts --emit-openapi --emit-openrpc

tigrbl-auth gates --gate-production-readiness --gate-tier 3 --require-evidence
```

---

## Bottom line

The package should be treated as a **Tigrbl-native IdP / authorization server / trust plane** with five coordinated planes:

1. **runtime plane** — AS/OP, tokens, sessions, keys, policy,
2. **discovery plane** — OIDC, AS metadata, protected resource metadata, A2A publication,
3. **contract plane** — OpenAPI and OpenRPC,
4. **operations plane** — CLI, runbooks, key rotation, audit, release gates,
5. **certification plane** — claims, evidence, peer-review bundles.

That is the shape that makes the RFC/spec matrix, CLI design, operations model, and interop story coherent.

---

## Source set used for the peer/protocol rows

- Agent2Agent Protocol (A2A) specification
- Model Context Protocol authorization specification
- Firebase Authentication documentation
- Supabase Auth documentation
- Clerk OAuth and organization documentation
- FastAPI Users documentation
- Django authentication documentation
- Keycloak server administration and client registration documentation
- OpenAPI 3.1 specification
- OpenRPC specification
- RFC Editor pages for RFC 8615, RFC 9700, RFC 9728, and RFC 8932
