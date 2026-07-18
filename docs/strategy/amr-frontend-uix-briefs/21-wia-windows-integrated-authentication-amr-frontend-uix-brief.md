# Windows Integrated Authentication AMR Frontend UIX Brief

- **AMR:** `wia`
- **Current delivery status:** Missing; no first-party Kerberos/Negotiate provider exists
- **Delivery target:** Complete first-party Windows Integrated Authentication provider, negotiation, federation fallback, lifecycle, policy, diagnostics, and operations product
- **Category:** Enterprise integrated authentication
- **Platforms:** Managed Windows browser, native desktop, enterprise federation, tenant/platform administration, developer compatibility, CLI diagnostics

## UIX delivery priority

**P0 — Actual authentication UIX (ship first):** enterprise/WIA method discovery → “Use your work account” selection or approved bounded automatic attempt → negotiation progress → OS Windows session/credential handoff → result mapping → unsupported/unmanaged/no-session/domain-mismatch/ambiguous/account-denied/clock/SPN/trust/provider-timeout states → federation/local fallback → success or next-factor result. Managed browser and native desktop parity are the release gate.

**P1 — Enrollment and user lifecycle:** first successful identity mapping/link confirmation, enterprise-account detail, link/unlink, mapping review, recovery/fallback, and session evidence.

**P2 — Administration and operations:** domains, providers, SPNs, service identities, trust, browser/device policy, application compatibility, keys, health, audit, and Kerberos diagnostics.

WIA is not first class merely because domains and SPNs can be configured. The P0 negotiation and fallback experience must work for real workforce users first.

**Release gate:** P0 must be interaction-complete and validated before P2 administration/configuration/management UIX is treated as delivery. P2 screens cannot be used to claim first-class authenticator support.

## 1. Mandate

Deliver complete Windows Integrated Authentication across enterprise method discovery, browser/native negotiation, Kerberos/Negotiate handoff, federation fallback, evidence, linked-account lifecycle, domain/provider policy, application compatibility, health, diagnostics, recovery, and audit. The experience must avoid credential prompts that imitate Windows and must fail safely outside managed environments.

### First-party enrollment semantics

WIA enrollment is an enterprise registration flow rather than creation of a user secret. Platform operators register the Kerberos/Negotiate provider, service identities/SPNs, keys, realm/domain trust, channel protections, browser/native profiles, and health checks. Tenant administrators verify domains, configure identity mappings and applications, and stage user eligibility. A user's first successful mapped negotiation creates or confirms the linked enterprise identity only after tenant/subject and takeover checks; explicit linking is required for ambiguity. Enrollment lifecycle covers pending verification, active, degraded, suspended, key rotation, mapping review, revoked, and retired provider/domain/application bindings.

## 2. Users and jobs

- Workforce users sign in using their current managed Windows session with minimal interaction.
- Remote/unmanaged users fall back to approved enterprise or local methods.
- Account holders inspect and unlink enterprise identities safely.
- Tenant administrators configure domains, provider assignment, browser/device eligibility, assurance, and fallback.
- Developers test application compatibility and redirect/Negotiate behavior.
- Platform operators manage provider trust, SPNs, delegation boundaries, keys, health, and conformance.
- Support/security teams diagnose Kerberos failures without seeing tickets or credentials.

## 3. Required screens and non-web interactions

| Screen/interaction | Purpose |
|---|---|
| Enterprise method discovery | Determine managed domain/device/browser eligibility |
| Login method chooser | Offer “Use your work account” or configured provider label |
| Integrated-auth introduction | Explain automatic sign-in, account used, privacy, and fallback |
| Negotiation progress | Show bounded processing while browser/native stack negotiates |
| OS Windows credential/session prompt | System-owned authentication when required |
| Negotiate result handler | Resume server ceremony after HTTP/native negotiation |
| Federation redirect/callback | Provide approved enterprise fallback or brokered WIA evidence |
| Domain/account mismatch | Prevent unintended identity linking or tenant confusion |
| Unmanaged/unsupported environment | Offer configuration help or another method |
| Step-up/recent authentication | Re-negotiate or use stronger approved method when required |
| Result/next-step | Complete sign-in or request another factor |
| Evidence detail | Show `wia`, domain/provider, time, freshness, authentication profile, limitations |
| Linked enterprise-account detail | Show safe identity projection, status, link/unlink, events |
| Account-link confirmation | Require recent authentication and takeover protections |
| Recovery/fallback | Route to provider recovery, supervised recovery, or local method |
| Tenant domain/provider config | Configure verified domains, providers, assignment, fallback, app scope |
| Browser/device policy | Configure managed environment and zone/profile requirements |
| SPN/service/delegation config | Platform-controlled enterprise integration configuration |
| Application compatibility/test | Test origins, redirects, browser policy, and authentication result |
| Provider/domain health | Monitor directory/KDC/federation, key, clock, DNS, and trust status |
| Kerberos/Negotiate diagnostics | Redacted structured failure analysis |
| Native desktop sign-in | Use OS APIs and current Windows session |
| CLI diagnostic tooling | Test DNS/SPN/KDC/time/profile without exposing tickets/secrets |

## 4. Managed browser flow

1. Server identifies a tenant/application eligible for WIA and returns a configured enterprise method.
2. Introduction appears on first use or when policy requires explicit choice; silent attempts are bounded and never loop.
3. Browser performs Negotiate according to approved enterprise browser policy.
4. Server validates token, SPN/audience, channel/protocol protections, domain/realm trust, time, replay, and identity mapping.
5. If one safe identity matches, sign-in continues; ambiguity/mismatch requires explicit account-link or fallback.
6. Accepted evidence emits `wia`; unsupported/unmanaged/private-browsing/proxy failures route to approved alternatives.

## 5. Native desktop flow

1. Native app requests integrated authentication through approved OS APIs.
2. System may use current session or show its own Windows credential UI.
3. App receives a bound result/token and returns it to the server ceremony.
4. Server performs the same trust, mapping, replay, and policy validation.
5. App resume, cancellation, account switch, and workstation lock/unlock cannot detach the result from the original ceremony.

## 6. Federation fallback and account linking

1. When direct WIA is unavailable, method chooser may redirect to an enterprise IdP capable of returning trusted normalized evidence.
2. Callback processing hides raw claims/tokens.
3. Existing-account linking requires recent authentication, explicit identity projection, tenant match, and takeover-risk checks.
4. Unlink warns about last-login-method and enterprise access effects.

## 7. Screen behavior

- Label by organization/provider, not protocol jargon, on user screens.
- Never render an HTML imitation of a Windows credential prompt.
- Negotiation progress has a short bounded timeout and visible “Use another method.”
- Error states distinguish unsupported environment, browser policy, domain trust, clock, provider outage, ambiguous mapping, and access policy using safe copy.
- Do not expose SPNs, realm topology, delegation details, ticket content, or exact trust failures to ordinary users.
- Evidence detail shows safe domain/provider, account projection, method/profile, time, freshness, policy result, and audit reference.

## 8. Administrative configuration

- Tenant controls verified domains, provider assignment, eligible apps, user mapping, managed browser/device requirements, assurance, MFA/step-up, fallback, and recovery.
- Platform controls SPNs, keys, service identities, realm/domain trust, delegation prohibition/allowlist, protocol/channel protection, clock tolerance, DNS discovery, provider health, and conformance.
- Simulation covers managed/unmanaged browser, wrong tenant/domain, ambiguous account, expired key, clock skew, KDC/provider outage, proxy stripping, federation fallback, and last-method unlink.

## 9. States

Support discovering, eligible/ineligible, ready, negotiating, OS prompt external, submitting, success, requires-next-step, unsupported browser/device, unmanaged environment, private-mode restriction, no current session, account choice, domain mismatch, ambiguous mapping, access denied, clock/trust/SPN safe failure, provider/KDC unavailable, timeout, cancelled, policy changed, federation fallback, recovery, and blocked.

## 10. Components

Reuse `CeremonyShell`, `AuthenticatorMethodPicker`, `ProviderButton`, `CompatibilityNotice`, `AuthenticationContextSummary`, `AuthenticatorEventTimeline`, `PolicyImpactPreview`, and shared callback/failure/result components.

Add `EnterpriseMethodCard`, `IntegratedAuthProgress`, `ManagedEnvironmentNotice`, `EnterpriseIdentityProjection`, `AccountLinkRiskGate`, `DomainProviderConfig`, `BrowserCompatibilityMatrix`, `EnterpriseHealthSummary`, and native/CLI adapters.

## 11. Data/API expectations

Server projection includes eligible enterprise method, safe organization/provider/domain label, negotiation state, normalized identity mapping, AMR/provenance, authentication time/freshness, account-link state, required next step, fallback, safe error, policy version, health projection, and audit reference.

Kerberos tickets/tokens, passwords, keys, unrestricted directory attributes, SPN topology, delegation internals, raw federation claims, and diagnostic secrets never enter ordinary frontend payloads.

## 12. Responsive, accessibility, and non-web

- Progress and fallback remain visible at narrow widths and high zoom.
- Status updates are announced once per material change.
- OS prompts remain system owned; focus returns predictably after cancellation/completion.
- Native desktop supports keyboard/screen reader/high contrast and Windows accessibility conventions.
- CLI emits redacted structured diagnostics, uses current credential context/key-store references, and never prints tickets or asks for passwords as command arguments.

## 13. Security

- Bind results to tenant, subject mapping, client/application, SPN/audience, ceremony, purpose, channel, nonce, and time.
- Prevent replay, reflection, issuer/realm confusion, account-link takeover, cross-tenant mapping, delegation abuse, downgrade, and unsafe fallback.
- Require verified domains and explicit mapping rules.
- Recent authentication is required for linking/unlinking and sensitive configuration.
- Redact directory/account and infrastructure data in UI, telemetry, logs, URLs, and support exports.

## 14. Analytics and audit

Analytics records method eligibility, environment class, negotiation stage, safe failure class, fallback, and completion. Audit normalized identity, domain/provider, trust/profile, evidence, mapping/link changes, fallback, provider health incident, policy/config changes, and operator identity with strict redaction.

## 15. Tests

- Managed browser/native success, current-session and OS-prompt paths, step-up, federation fallback, link/unlink, and recovery pass.
- Unmanaged/unsupported/private-mode, ambiguous mapping, wrong tenant/domain, replay, reflection, clock skew, SPN/trust failure, proxy behavior, KDC/provider outage, and policy change fail safely.
- No tickets, tokens, passwords, directory secrets, or topology leak.
- Accessibility, responsive, Windows high-contrast, native resume, CLI redaction, and last-method safeguards pass.

## 16. Acceptance criteria

- Direct, native, and federated enterprise flows are complete end to end.
- Users always have a bounded fallback and never encounter a fake credential prompt.
- `wia` is emitted only from trusted normalized evidence.
- Linking/mapping prevents tenant and account takeover.
- Administrators can configure, simulate, monitor, and diagnose the enterprise integration safely.

## 17. Dependencies

- Kerberos/Negotiate provider and normalized evidence contract.
- Verified-domain, identity-mapping, and enterprise account-link services.
- Browser/native support policy and OS adapters.
- SPN/trust/key/KDC health, secure diagnostics, and federation fallback.

## References

- [AMR screen support matrix](../../amr-screen-support-matrix.md)
- [Universal authenticator ceremony brief](../uix-pairing-briefs/40-authenticator-ceremony-api-universal-authenticator-pages-uix.md)
- [Canonical AMR vocabulary](../../../pkgs/10-concrete/tigrbl-jose-concrete/src/tigrbl_jose_concrete/amr.py)
