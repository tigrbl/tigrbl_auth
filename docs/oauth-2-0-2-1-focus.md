# OAuth 2.0 and OAuth 2.1 Focus

Research date: 2026-05-28

OAuth 2.0 is the standing standards base for the authorization server, client, resource server, and token ecosystem. OAuth 2.1 should be treated differently: as of this review, it is still an IETF draft, with latest observed revision `draft-ietf-oauth-v2-1-15` dated 2026-03-02. It is not a final RFC compliance target.

For `tigrbl_auth`, the right framing is:

- keep OAuth 2.0 plus extension RFCs as the broad compatibility and certification target;
- add OAuth 2.1 as a fail-closed runtime/profile alignment mode;
- do not market OAuth 2.1 as final RFC conformance until it is actually finalized;
- make OAuth 2.1 profile behavior stricter than the general OAuth 2.0 compatibility surface.

Normative anchors:

- [RFC 6749: OAuth 2.0 Authorization Framework](https://www.rfc-editor.org/rfc/rfc6749)
- [RFC 6750: Bearer Token Usage](https://www.rfc-editor.org/rfc/rfc6750)
- [RFC 7636: PKCE](https://www.rfc-editor.org/rfc/rfc7636)
- [RFC 9700: OAuth 2.0 Security Best Current Practice](https://www.rfc-editor.org/rfc/rfc9700)
- [IETF OAuth 2.1 draft](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1)
- [IETF OAuth 2.1 draft history](https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/history/)

## Current `tigrbl_auth` State

| Area | Current state | Evidence | Interpretation |
|---|---|---|---|
| OAuth protocol package | `tigrbl-identity-oauth` owns OAuth 2.x protocol behavior below route composition. | [`tigrbl-identity-oauth` README](../pkgs/tigrbl-identity-oauth/README.md) | This is the right package for OAuth 2.0 and OAuth 2.1 profile logic. |
| Public authorization-server frontdoor | `tigrbl-auth-api-public` exposes login, authorize, token, logout, registration, discovery, JWKS, and public OAuth/OIDC helpers. | [`tigrbl-auth-api-public` README](../pkgs/tigrbl-auth-api-public/README.md) | This is the deployable AS frontdoor for OAuth/OIDC protocol endpoints. |
| Resource validation frontdoor | `tigrbl-auth-api-resource-validation` exposes validation and metadata surfaces such as JWKS, introspection, and protected-resource metadata. | [`tigrbl-auth-api-resource-validation` README](../pkgs/tigrbl-auth-api-resource-validation/README.md), [Target Reality Matrix](compliance/TARGET_REALITY_MATRIX.md) | This is the protected-resource / resource-server integration surface. |
| Developer frontdoor | `tigrbl-auth-api-developer` owns developer-facing client registration and client management. | [`tigrbl-auth-api-developer` README](../pkgs/tigrbl-auth-api-developer/README.md) | OAuth client policy belongs here, while public protocol endpoints stay in public-api. |
| Service admin frontdoor | `tigrbl-auth-api-service-admin` owns service/workload identity administration. | [`tigrbl-auth-api-service-admin` README](../pkgs/tigrbl-auth-api-service-admin/README.md) | Client credentials, M2M, workload credentials, and service keys are product concerns here. |
| RP package | `tigrbl-identity-rp` is the app-side relying-party integration. | [`tigrbl-identity-rp` README](../pkgs/tigrbl-identity-rp/README.md) | Client/RP behavior should be tested separately from AS behavior. |
| OAuth 2.1 profile | Tracked only as alignment, not a final standard claim. | [Target Reality Matrix](compliance/TARGET_REALITY_MATRIX.md) | This is correct and should remain true until OAuth 2.1 exits draft state. |
| Password grant signal | A `PasswordGrantForm` contract exists today. | [`rest.py`](../pkgs/tigrbl-identity-contracts/src/tigrbl_identity_contracts/rest.py) | This must be explicitly excluded from any OAuth 2.1 profile, except tightly labeled dev/backcompat modes. |

## Standards Coverage Map

| Standard / profile | Status in repo direction | Owning surface | OAuth 2.1 relevance |
|---|---|---|---|
| RFC 6749 OAuth 2.0 | Baseline certifiable target. | `tigrbl-identity-oauth`, `tigrbl-auth-api-public` | Foundation that OAuth 2.1 consolidates and tightens. |
| RFC 6750 Bearer Tokens | Baseline certifiable target. | Public API, resource validation API, resource-server integrations | OAuth 2.1 posture should disallow bearer tokens in query transport. |
| RFC 7636 PKCE | Baseline certifiable target. | Public API authorize/token flow, RP package | Core OAuth 2.1 profile requirement for authorization-code clients. |
| RFC 7009 Token Revocation | Production-completion target. | Public API `/revoke` | Required for serious client/session lifecycle management. |
| RFC 7662 Token Introspection | Production-completion target. | Resource validation API, public protocol support where exposed | Required for opaque token and resource-server validation deployments. |
| RFC 8414 Authorization Server Metadata | Baseline certifiable target. | Public API `/.well-known/oauth-authorization-server` | Metadata must be profile-honest for OAuth 2.1 allowed grants and response types. |
| RFC 9207 Authorization Server Issuer Identification | Production-completion target. | Public API authorize/discovery | Important for mix-up attack mitigation and modern security posture. |
| RFC 7591 Dynamic Client Registration | Production-completion target. | Public API registration, developer API policy | OAuth 2.1 profile should reject insecure client metadata. |
| RFC 7592 Client Registration Management | Production-completion target. | Developer API / client management | Needed for lifecycle management of registered clients. |
| RFC 8252 Native Apps | Production-completion target. | Public API, developer API client policy, RP package | OAuth 2.1 redirect and PKCE behavior should align with native-app requirements. |
| RFC 8628 Device Authorization Grant | Hardening-completion target. | Public API device authorization | Useful for input-constrained clients; not OAuth 2.1 core. |
| RFC 8693 Token Exchange | Hardening-completion target. | Public API token exchange, service/admin policy | Useful for delegation and workload exchange patterns; not OAuth 2.1 core. |
| RFC 8705 mTLS | Hardening-completion target. | Public API token endpoints, service clients | Sender-constrained token option for confidential clients and high-assurance profiles. |
| RFC 8707 Resource Indicators | Hardening-completion target. | Public API authorize/token/device/PAR/token exchange | Important for API/resource-specific access tokens. |
| RFC 9101 JAR | Hardening-completion target. | Public API authorize/PAR | Useful for signed authorization requests and FAPI-style profiles. |
| RFC 9126 PAR | Hardening-completion target. | Public API `/par` | Strong modern pattern for reducing front-channel request exposure. |
| RFC 9396 RAR | Hardening-completion target. | Public API authorize/PAR | Useful for fine-grained authorization details. |
| RFC 9449 DPoP | Hardening-completion target. | Public API token endpoints, resource validation | Sender-constrained token option for public clients and API access. |
| RFC 9700 OAuth Security BCP | Hardening-completion target. | Public API, profile/runtime config, RP/resource-server integrations | Main source of modern OAuth 2.0 hardening that OAuth 2.1 incorporates. |
| RFC 9728 Protected Resource Metadata | Production-completion target. | Resource validation API | Important for resource servers advertising authorization metadata. |

## OAuth 2.0 vs OAuth 2.1 Deltas

| Topic | OAuth 2.0 compatibility posture | OAuth 2.1 alignment posture | `tigrbl_auth` action |
|---|---|---|---|
| Authorization code | Core grant. PKCE is an extension in RFC 7636. | Authorization code plus PKCE is the primary interactive flow. | Keep `/authorize` and `/token`; require PKCE in OAuth 2.1 profile, especially for public/browser/native clients. |
| Implicit grant | Present in RFC 6749 era compatibility. | Omitted from OAuth 2.1 draft. | Do not advertise `response_type=token` in OAuth 2.1 metadata; reject it fail-closed in OAuth 2.1 profile. |
| Resource Owner Password Credentials | Present in RFC 6749 era compatibility. | Omitted from OAuth 2.1 draft. | Treat password grant as dev/backcompat only; reject `grant_type=password` in OAuth 2.1 and production browser/native profiles. |
| Client credentials | Core grant for confidential clients and service clients. | Remains the M2M/workload lane, with modern client authentication expectations. | Keep in service-admin/developer policy; prefer strong client auth, service identity lifecycle, and scoped resource audiences. |
| Refresh tokens | Optional in OAuth 2.0. | Modern posture expects rotation or sender constraints for public clients. | Add/verify refresh-token rotation, reuse detection, and sender-constrained refresh-token policy per client type. |
| Redirect URI matching | OAuth 2.0 allowed more deployment variance. | Exact registered redirect URI matching, with the loopback port exception for native clients. | Enforce exact redirect matching in OAuth 2.1 profile; keep RFC 8252 native-app exception explicit and tested. |
| Bearer token transport | RFC 6750 defines header, form, and query methods. | Modern posture discourages or forbids query-token transport. | Disable `access_token` query transport in OAuth 2.1 profile and hardened production profiles. |
| Public clients | OAuth 2.0 left many details to extensions and guidance. | PKCE and redirect discipline become baseline behavior. | Developer API must record client type and enforce public-client policy at registration and token exchange. |
| Confidential clients | OAuth 2.0 supports client secrets and other auth methods. | Stronger posture favors private-key JWT, mTLS, DPoP, and audience/resource binding where appropriate. | Keep client-secret compatibility, but make stronger methods first-class in service/admin product lanes. |
| Metadata honesty | RFC 8414 and OIDC discovery are extensions to the original core. | Metadata must accurately reflect the active profile. | Profile-specific discovery must not list disabled grants, response types, auth methods, or token transports. |

## Product Surface Ownership

| Capability | Package / API owner | Route or product shape | Notes |
|---|---|---|---|
| Authorization endpoint | `tigrbl-auth-api-public`, backed by `tigrbl-identity-oauth` | `/authorize` | OAuth 2.1 profile should require PKCE and reject implicit. |
| Token endpoint | `tigrbl-auth-api-public`, backed by `tigrbl-identity-oauth` and credentials/JOSE/storage | `/token` | Must enforce grant allowlist by profile and client type. |
| Revocation | `tigrbl-auth-api-public` | `/revoke` | Also needs tenant/client scoping and audit. |
| Introspection | `tigrbl-auth-api-resource-validation` as preferred validation surface | `/introspect` where exposed | Resource validation should be the clean product surface for protected APIs. |
| Authorization server metadata | `tigrbl-auth-api-public` | `/.well-known/oauth-authorization-server` | Must be profile-specific and issuer-correct. |
| JWKS | `tigrbl-auth-api-resource-validation` and public issuer metadata | `/.well-known/jwks.json`, tenant JWKS | Signing-key metadata supports resource-server validation. |
| Dynamic registration | Public API for protocol endpoint, developer API for product lifecycle | `/register`, client-management routes | Developer API should own policy, lifecycle, UI-facing registration management. |
| M2M / client credentials | `tigrbl-auth-api-service-admin`, `tigrbl-auth-api-developer`, token endpoint | service clients, workload credentials, `/token` | Product lane needs explicit scopes, resources, rotation, and audit. |
| RP behavior | `tigrbl-identity-rp`, `@tigrbl-auth/rp` | SDK/client integration | Should verify metadata consumption, PKCE, state/nonce, token exchange, and logout behavior. |
| Resource server behavior | `tigrbl-identity-resource-server`, resource validation API | API middleware/integration | Should validate JWT/opaque tokens, issuer, audience/resource, scopes, DPoP/mTLS where enabled. |

## Competitor Surface Comparison

| Vendor | OAuth product / surface shape | OAuth 2.1 signal |
|---|---|---|
| Auth0 | Authentication API, Universal Login, Applications/clients, M2M applications. Docs: [Auth0 OAuth 2.0 Authorization Framework](https://auth0.com/docs/authenticate/protocols/oauth), [Auth0 Authorization Code Flow with PKCE](https://auth0.com/docs/flows/guides/auth-code-pkce/call-api-auth-code-pkce). | Frames product as OAuth 2.0/OIDC with modern PKCE guidance, not as a separate OAuth 2.1 product. |
| Okta | OIDC/OAuth API, API Access Management, applications, service apps. Docs: [Okta Authorization Code with PKCE](https://developer.okta.com/docs/guides/implement-grant-type/authcodepkce/main/), [Okta OAuth API access setup](https://developer.okta.com/docs/guides/set-up-oauth-api/main/). | Recommends authorization code with PKCE and exposes OAuth/OIDC APIs as product surfaces. |
| Keycloak | Realm OIDC/OAuth endpoints, client registration, service accounts, admin console/API. Docs: [Keycloak OIDC endpoint layers](https://www.keycloak.org/securing-apps/oidc-layers). | Product is protocol/provider-centered; OAuth 2.1 posture is a configuration/profile concern, not a separate product. |
| FusionAuth | OAuth endpoints, application configuration, JWT/API-key/service behavior. Docs: [FusionAuth OAuth guide](https://fusionauth.io/docs/lifecycle/authenticate-users/oauth/), [FusionAuth OAuth endpoints](https://fusionauth.io/docs/v1/tech/oauth/endpoints/). | Exposes OAuth 2.0 grants and PKCE configuration; OAuth 2.1 is best represented as stricter application policy. |
| Amazon Cognito | User pool authorization server, hosted UI, token endpoint, app clients, M2M client credentials. Docs: [Cognito OAuth grants](https://docs.aws.amazon.com/cognito/latest/developerguide/federation-endpoints-oauth-grants.html), [Cognito token endpoint](https://docs.aws.amazon.com/cognito/latest/developerguide/token-endpoint.html). | Supports PKCE and client credentials, but still documents implicit; OAuth 2.1-like behavior would be a stricter app-client policy. |
| `tigrbl_auth` | Protocol package plus thin product frontdoors: public AS, resource validation, developer client admin, service/workload admin, RP/resource-server packages. | Should add an explicit OAuth 2.1 alignment profile, while keeping OAuth 2.0 and extension RFC certification separate. |

## Recommended Target Architecture

| Decision | Recommendation | Reason |
|---|---|---|
| Standards claim | Keep OAuth 2.0 and extension RFCs as the certification target. | OAuth 2.1 remains draft-era alignment, not a final RFC claim. |
| Runtime profile | Add an explicit `oauth21` or `oauth2_1_alignment` profile. | Makes stricter behavior testable without breaking OAuth 2.0 compatibility modes. |
| Grant policy | Profile-gate grants by client type and runtime profile. | OAuth 2.1 profile must reject implicit and password grant while preserving controlled compatibility where necessary. |
| Metadata | Generate metadata from active profile and client-policy capabilities. | Discovery must not advertise unsupported or disallowed behavior. |
| Client registration | Make developer API registration enforce OAuth 2.1-safe defaults. | Many OAuth vulnerabilities start with permissive client metadata. |
| M2M lane | Treat client credentials as a service/workload product lane, not a side effect of generic client registration. | This aligns with planned service-admin and workload identity surfaces. |
| Token binding | Prefer DPoP and mTLS as optional sender-constrained hardening. | OAuth 2.1 posture benefits from sender-constrained tokens, especially for public and high-risk clients. |
| Backcompat | Label legacy OAuth 2.0 compatibility explicitly. | Operators need to know when they are enabling weaker historical behavior. |

## Minimum OAuth 2.1 Alignment Slice

| Slice | Deliverable | Tests |
|---|---|---|
| Profile definition | Runtime/profile config that activates OAuth 2.1 alignment. | Profile loader tests and metadata snapshot tests. |
| Grant allowlist | Authorization code, refresh token, and client credentials allowed according to client type; implicit and password grant rejected. | Negative tests for `response_type=token` and `grant_type=password`; positive tests for authorization code plus PKCE and client credentials. |
| PKCE enforcement | Require `code_challenge` at authorization time and `code_verifier` at token exchange for public clients and OAuth 2.1 profile clients. | Missing/invalid/verifier-mismatch tests and successful S256 flow. |
| Redirect matching | Exact redirect URI matching, with explicit RFC 8252 loopback port exception. | Exact-match negative tests, wildcard rejection, loopback positive/negative tests. |
| Bearer token transport | Disable bearer token in query transport for OAuth 2.1 and hardened production profiles. | Query-token rejection tests; Authorization-header positive tests. |
| Refresh-token safety | Rotation or sender-constrained refresh-token policy for public clients. | Reuse-detection and rotated-token tests. |
| Metadata honesty | Active-profile metadata omits disabled grant types, response types, and auth methods. | `/.well-known/oauth-authorization-server` profile-specific assertions. |
| Developer policy | Client registration rejects OAuth 2.1-incompatible metadata. | Developer API registration tests for implicit, password, wildcard redirects, missing PKCE policy. |
| RP/client behavior | RP SDK defaults to authorization code plus PKCE. | RP package tests for state, nonce, PKCE verifier, token exchange, issuer validation. |

## Proposed SSOT Follow-Up

Do not replace current OAuth 2.0 entities. Add a narrow profile contract and proof chain:

| Entity type | Proposed entity | Purpose |
|---|---|---|
| SPEC | `oauth-2-1-alignment-profile-contract` | Defines active-profile requirements while OAuth 2.1 is draft. |
| Feature | `feat:oauth21-alignment-profile` | Implements profile gating and metadata derivation. |
| Feature | `feat:oauth21-fail-closed-grant-policy` | Rejects implicit and password grant in OAuth 2.1 profile. |
| Feature | `feat:oauth21-pkce-and-redirect-policy` | Requires PKCE and exact redirect URI matching. |
| Feature | `feat:oauth21-bearer-transport-policy` | Disables bearer query transport in OAuth 2.1/hardened profiles. |
| Test | `tst:oauth21-profile-disallows-implicit-and-password-grants` | Negative proof for omitted legacy grants. |
| Test | `tst:oauth21-profile-requires-pkce` | Positive and negative PKCE proof. |
| Test | `tst:oauth21-profile-enforces-redirect-policy` | Exact-match and RFC 8252 loopback proof. |
| Test | `tst:oauth21-profile-metadata-honesty` | Discovery metadata proof. |
| Test | `tst:oauth21-profile-disallows-bearer-query` | Bearer transport proof. |

## Product Boundary

OAuth 2.1 should not force a new deployable API package. It should be a runtime/profile mode across existing packages:

```text
tigrbl-identity-oauth                    # OAuth 2.0 + extension RFC logic, OAuth 2.1 profile rules
tigrbl-auth-api-public                   # authorize/token/revoke/register/discovery/JWKS protocol frontdoor
tigrbl-auth-api-resource-validation      # introspection, JWKS, protected-resource metadata
tigrbl-auth-api-developer                # client registration, redirect/grant/client policy
tigrbl-auth-api-service-admin            # M2M/workload/service identity lifecycle
tigrbl-identity-rp / @tigrbl-auth/rp     # OAuth/OIDC client and RP behavior
tigrbl-identity-resource-server          # protected API token validation integration
```

The practical course is to keep OAuth 2.0 broad and interoperable, then add a stricter OAuth 2.1 alignment profile that operators can enable and tests can certify without overstating draft-standard status.
