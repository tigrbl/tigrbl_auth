# MFA Focus

Research date: 2026-05-28

MFA is not just a one-time-password check. A complete MFA product includes factor enrollment, challenge and verification, step-up policy, recovery, revocation, phishing-resistant authenticators, tenant/app policy, audit, UI, admin support, and token/session expression through `acr` and `amr`.

For `tigrbl_auth`, MFA should be treated as an advanced authentication product lane that spans:

- `tigrbl-authn-credentials` for factor credential material and proof verification.
- `tigrbl-authz-policy` for when MFA is required, optional, remembered, bypassed, or stepped up.
- `tigrbl-auth-protocol-oidc` and `tigrbl-identity-jose` for `acr` and `amr` expression in ID/access tokens.
- `tigrbl-auth-api-public` for user-facing enrollment/challenge/recovery flows.
- `tigrbl-auth-api-tenant-admin` for tenant MFA policy and user factor reset.
- `@tigrbl-auth/public-uix` for hosted login, enrollment, challenge, recovery, and profile factor management.

## Current `tigrbl_auth` State

| Area | Current state | Evidence | Interpretation |
| --- | --- | --- | --- |
| Governance | MFA is governed by advanced-authentication SSOT, but current implementation status is explicitly less than implemented. | [SPEC-1067](../.ssot/specs/SPEC-1067-advanced-authentication-and-adaptive-auth-requirements.yaml) | Do not claim production MFA support yet. |
| Credential primitive | `tigrbl-authn-credentials` has `CredentialKind.MFA_FACTOR`, `create_mfa_factor_credential`, credential verification, lifecycle, rotation, revocation, and audit primitives. | [`lifecycle.py`](../pkgs/30-capabilities/tigrbl-authn-credentials/src/tigrbl_authn_credentials/lifecycle.py), [`test_credentials_lifecycle_boundary.py`](../tests/unit/test_credentials_lifecycle_boundary.py) | Useful foundation, but not a complete factor protocol or public flow. |
| Passkey/WebAuthn primitive | `PASSKEY_WEBAUTHN` credential primitives and tests exist. | [`lifecycle.py`](../pkgs/30-capabilities/tigrbl-authn-credentials/src/tigrbl_authn_credentials/lifecycle.py), [`test_credentials_lifecycle_boundary.py`](../tests/unit/test_credentials_lifecycle_boundary.py) | Current behavior is proof-of-concept credential modeling, not full WebAuthn ceremony support. |
| Advanced auth registry | Phase 4 test scaffolds include `AdvancedAuthenticatorRegistry`, MFA enrollment, WebAuthn, passwordless, replay, anomaly, and adaptive contexts. | [`test_phase4_advanced_identity_boundary.py`](../tests/unit/test_phase4_advanced_identity_boundary.py) | Good conceptual boundary, but it is not yet productized through storage, routes, UI, and conformance tests. |
| Public UIX contract | Public UIX contract says MFA views belong in the public hosted-login surface. | [SPEC-1167](../.ssot/specs/SPEC-1167-public-uix-composition-contract.yaml) | MFA UX belongs with public login, not admin APIs. |
| Standards signal | JOSE package includes RFC 8176 `amr` validation. | [`rfc8176.py`](../pkgs/10-domain/tigrbl-identity-jose/src/tigrbl_identity_jose/standards/rfc8176.py) | Token expression of authentication method references is recognized. |

## Vendor Product Shape

| Vendor | Product framing | Factors / authenticators | Policy and step-up | API / admin surface | Notes |
| --- | --- | --- | --- | --- | --- |
| Auth0 | MFA is a secure-login product integrated with Universal Login, Guardian, Actions, Management API, and MFA API. Docs: [Auth0 MFA factors](https://auth0.com/docs/secure/multi-factor-authentication/multi-factor-authentication-factors), [Auth0 MFA API factor management](https://auth0.com/docs/secure/multi-factor-authentication/manage-mfa-auth0-apis/manage-authenticator-factors-mfa-api). | OTP, push/Guardian, email, SMS/voice, WebAuthn platform/roaming, recovery codes depending on tenant settings. | Actions can customize enrollment and challenge decisions; Universal Login can present contextual enrollment. | Management API Guardian factor endpoints and Authentication MFA API manage factors and enrollments. | Strong CIAM product framing: MFA is part of hosted login and tenant security posture. |
| Okta | MFA is part of authenticator assurance, Identity Engine policy, and Factors/Authenticators APIs. Docs: [Okta MFA concepts](https://developer.okta.com/docs/concepts/mfa/), [Okta User Factors API](https://developer.okta.com/docs/reference/api/factors/). | Okta Verify, Smart Card, YubiKey OTP, Google Authenticator, custom OTP, Duo, email, phone, SMS, voice, hardware/software OTP. | Strong policy posture with authenticators, app sign-on policy, account recovery use, phishing-resistant factors, and adaptive MFA. | Authentication API handles MFA enrollment/verification; Factors API manages user factors. | Strongest enterprise assurance model among this comparison. |
| Keycloak | MFA is modeled through authentication flows, required actions, OTP, WebAuthn, and recovery code authenticators. Docs: [Keycloak authentication flows](https://www.keycloak.org/docs/latest/server_admin/#_authentication-flows), [Keycloak WebAuthn](https://www.keycloak.org/docs/latest/server_admin/#_webauthn), [Keycloak recovery codes](https://www.keycloak.org/2025/10/recovery-codes). | OTP/TOTP, WebAuthn, passkeys/passwordless, recovery authentication codes, custom authenticators. | Highly configurable authentication flows with conditional 2FA and alternative authenticators. | Admin Console and Admin REST manage flows, credentials, required actions, and user credentials. | Powerful and flexible, but product UX depends heavily on flow configuration. |
| FusionAuth | MFA is a login and step-up product with Multi-Factor API and tenant/user settings. Docs: [FusionAuth MFA](https://fusionauth.io/docs/lifecycle/authenticate-users/multi-factor-authentication), [FusionAuth Multi-Factor API](https://fusionauth.io/docs/apis/two-factor). | TOTP, email, SMS/phone where plan supports it, recovery-style workflows through API design. | Supports MFA during login and step-up authentication before sensitive operations. | Multi-Factor API enables/disables and sends/validates MFA methods; User API stores user factor settings. | Clear app-developer integration model; TOTP is available broadly while email/phone can be plan-dependent. |
| Amazon Cognito | MFA is user-pool configuration integrated with managed login and auth challenge flows. Docs: [Cognito MFA](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-mfa.html), [Cognito TOTP MFA](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-mfa-totp.html). | SMS, email, TOTP; passkeys can satisfy MFA requirements with user verification in supported WebAuthn configuration. | User-pool MFA can be optional/required; app auth flows return MFA challenges and setup challenges. | User Pool APIs include software token association/verification and user MFA preference operations. | Strong managed-app baseline, but federated users delegate authentication to upstream IdP and Cognito does not add extra MFA for them. |
| `tigrbl_auth` | Planned advanced-authentication lane; current support is primitives and tests, not a complete MFA product. | Generic MFA factor credential plus passkey credential primitive; no mature TOTP/WebAuthn/SMS/email/push factor products yet. | Adaptive context and policy concepts exist in tests/specs, but no productized tenant/app policy surface. | Public UIX/API should own user challenge/enrollment; tenant-admin should own policy and reset; credentials package should own proof material. | Best next move: define MFA as a governed product slice before adding routes. |

## MFA Capability Matrix

| Capability | Current / target in `tigrbl_auth` | Priority |
| --- | --- | --- |
| Factor inventory | Current `MFA_FACTOR` credential kind is too generic. Add first-class factor metadata: type, channel, display name, tenant, subject, status, assurance, last-used, verified-at. | P0 |
| TOTP enrollment | Need otpauth URI generation, secret creation, QR payload, verification window, replay protection, and drift policy. | P0 |
| MFA challenge and verification | Need challenge records with nonce/session binding, expiry, attempt limits, replay prevention, and audit. | P0 |
| Step-up policy | Need policy rules for login, sensitive operations, admin actions, app risk, tenant risk, device/network context, and explicit `acr` target. | P0 |
| Recovery codes | Need one-time recovery codes with create/download/display-once, consumption, rotation, revocation, and admin reset. | P0 |
| Factor reset / support workflow | Tenant admins need auditable reset and recovery workflows; public users need self-service factor management. | P0 |
| `amr` / `acr` token claims | Need stable token expression of MFA method and assurance level after successful challenge. | P1 |
| WebAuthn / passkeys as MFA | Existing passkey primitive needs full WebAuthn ceremonies, RP ID binding, challenge binding, authenticator metadata, user verification, and phishing-resistant assurance semantics. | P1 |
| SMS/email OTP | Useful for CIAM parity, but should be weaker assurance than TOTP/WebAuthn and require anti-abuse/rate-limit policy. | P1 |
| Push authenticator | Later product; requires device registration, push channel, signed approvals, number matching, and fraud controls. | P2 |
| Remembered device/session | Needs secure device binding, expiry, revocation, risk override, and tenant policy. | P2 |
| Adaptive MFA | Existing phase 4 concepts should mature after baseline factor enrollment/challenge works. | P2 |
| Audit taxonomy | Need events for factor enrolled, challenged, verified, failed, reset, recovered, revoked, bypassed, and policy changed. | P0 |

## Product Boundary

| Surface | Owns | Does not own |
| --- | --- | --- |
| `tigrbl-authn-credentials` | Factor credential material, verification helpers, lifecycle states, recovery-code material, credential audit primitives. | Route composition, tenant policy, hosted login UX. |
| `tigrbl-authz-policy` | MFA requirement decisions, step-up rules, factor assurance policy, bypass/remembered-device decisions. | Secret verification and WebAuthn cryptographic ceremony details. |
| `tigrbl-auth-protocol-oidc` / `tigrbl-identity-jose` | `acr` and `amr` claim rules, OIDC authentication context expression. | Factor enrollment and user support workflows. |
| `tigrbl-auth-api-public` | Login-time MFA challenge, enrollment prompt, recovery-code challenge, user factor management where safe. | Tenant-wide policy mutation and admin reset authority. |
| `tigrbl-auth-api-tenant-admin` | Tenant MFA policy, required factors, admin factor reset, user support audit. | End-user factor secret display or challenge responses. |
| `@tigrbl-auth/public-uix` | Enrollment screens, challenge screens, recovery-code display, factor management, remembered-device prompts. | Tenant policy administration. |
| `@tigrbl-auth/tenant-admin-uix` | Policy configuration, user factor support/reset, MFA posture reporting. | Hosted-login challenge UX. |

## Minimum Viable MFA Slice

| Slice | Deliverable | Tests |
| --- | --- | --- |
| Canonical factor model | Store factor records with type, subject, tenant, status, display metadata, verified state, and last-used. | Storage/facade symbol tests, migration tests, lifecycle tests. |
| TOTP factor | Enroll TOTP, verify first code, challenge later codes, prevent replay, enforce attempts/expiry. | Positive, bad-code, expired, replay, drift-window, tenant-boundary tests. |
| Challenge table | Store MFA challenge/session binding with expiry, attempts, success/failure state, and audit ID. | Challenge lifecycle tests and login-flow integration tests. |
| Public flow | Login returns MFA-required state when policy requires it; verification resumes authorization/token flow. | Public API integration tests and OpenAPI path tests. |
| Tenant policy | Tenant admin configures optional/required MFA and allowed factor types. | Policy CRUD tests and cross-tenant denial tests. |
| Recovery codes | Generate one-time codes, display once, consume once, rotate/revoke. | One-time display, consumption, replay denial, reset audit tests. |
| Token claims | Successful MFA adds correct `amr` and `acr` values to OIDC tokens. | Token claim tests with RFC 8176 validation. |
| UIX smoke | Public UIX renders enrollment/challenge/recovery views against public API only. | UIX route/API-boundary tests. |
| Audit | Emit events for enrollment, challenge, verify, fail, recover, revoke, reset, and policy change. | Audit event shape and authorization tests. |

## Recommended Defaults

| Decision | Recommendation | Reason |
| --- | --- | --- |
| First production factor | TOTP plus recovery codes. | Low external dependency, widely understood, suitable as baseline. |
| Strong factor target | WebAuthn/passkeys with user verification. | Phishing-resistant and strategically important. |
| Weak factors | SMS and email OTP should be optional and lower assurance. | They are useful for reach, but weaker and abuse-prone. |
| Challenge storage | Store challenge state server-side with session binding and expiry. | Prevents replay and avoids encoding sensitive state in browser-only flows. |
| Secret storage | Store only digests or encrypted secrets as appropriate; display setup/recovery secrets once. | Matches existing credential hygiene patterns. |
| Token expression | Emit `amr` values and an `acr` profile after MFA. | Lets RP/resource-server consumers reason about assurance. |
| Tenant boundary | Every factor, challenge, recovery code, policy, and audit event must be tenant-scoped. | Avoids cross-tenant security failure. |
| Admin reset | Tenant-admin reset must be auditable and should not reveal existing factor secrets. | Support workflows are high-risk. |

## Proposed SSOT Follow-Up

| Entity type | Proposed work | Purpose |
| --- | --- | --- |
| ADR update | Clarify MFA as an advanced-authentication product lane over credentials, policy, public API, tenant-admin, and public UIX. | Prevent MFA from being treated as a generic credential helper only. |
| SPEC update | Expand SPEC-1067 with factor records, challenge records, TOTP, recovery codes, token claims, tenant policy, and audit requirements. | Turn broad MFA language into implementable contract. |
| Feature | `feat:mfa-factor-lifecycle` | Canonical factor records and lifecycle semantics. |
| Feature | `feat:mfa-totp-public-flow` | TOTP enrollment/challenge/verification over public API and UIX. |
| Feature | `feat:mfa-recovery-codes` | One-time recovery code lifecycle. |
| Feature | `feat:mfa-tenant-policy-and-admin-reset` | Tenant policy and support operations. |
| Feature | `feat:mfa-token-assurance-claims` | `acr`/`amr` emission and tests. |
| Test | `tst:mfa-factor-lifecycle-and-storage` | Factor storage and lifecycle proof. |
| Test | `tst:mfa-public-login-challenge-flow` | Public login MFA behavior proof. |
| Test | `tst:mfa-recovery-code-replay-denial` | Recovery safety proof. |
| Test | `tst:mfa-tenant-policy-boundaries` | Tenant isolation and admin authority proof. |
| Test | `tst:mfa-amr-acr-token-claims` | Token assurance proof. |

## Bibliography

- Auth0: [Multi-Factor Authentication Factors](https://auth0.com/docs/secure/multi-factor-authentication/multi-factor-authentication-factors)
- Auth0: [Manage Authentication Factors with MFA API](https://auth0.com/docs/secure/multi-factor-authentication/manage-mfa-auth0-apis/manage-authenticator-factors-mfa-api)
- Auth0: [Customize MFA Enrollments for Universal Login](https://auth0.com/docs/secure/multi-factor-authentication/customize-mfa-enrollments)
- Okta: [Multifactor Authentication](https://developer.okta.com/docs/concepts/mfa/)
- Okta: [User Factors API](https://developer.okta.com/docs/reference/api/factors/)
- Okta: [Authentication API](https://developer.okta.com/docs/reference/api/authn/)
- Keycloak: [Authentication flows](https://www.keycloak.org/docs/latest/server_admin/#_authentication-flows)
- Keycloak: [WebAuthn](https://www.keycloak.org/docs/latest/server_admin/#_webauthn)
- Keycloak: [Recovery Authentication Codes](https://www.keycloak.org/2025/10/recovery-codes)
- FusionAuth: [Multi-Factor Authentication](https://fusionauth.io/docs/lifecycle/authenticate-users/multi-factor-authentication)
- FusionAuth: [Multi-Factor API](https://fusionauth.io/docs/apis/two-factor)
- Amazon Cognito: [Adding MFA to a user pool](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-mfa.html)
- Amazon Cognito: [TOTP software token MFA](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-mfa-totp.html)
- Amazon Cognito: [Authentication flows](https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-authentication-flow-methods.html)
