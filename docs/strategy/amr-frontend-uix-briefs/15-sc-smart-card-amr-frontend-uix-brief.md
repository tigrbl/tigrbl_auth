# Smart Card AMR Frontend UIX Brief

- **AMR:** `sc`
- **Current delivery status:** Partial; certificate/mTLS foundations exist, PIV/CAC smart-card product is missing
- **Delivery target:** Complete first-party smart-card registration, authentication, lifecycle, recovery, trust, middleware, and operations product
- **Category:** Possession factor with certificate proof
- **Platforms:** Web, browser/OS certificate selector, card middleware, external reader/card, native desktop, developer/service mTLS, CLI diagnostics

## UIX delivery priority

**P0 — Actual authentication UIX (ship first):** Smart Card method selection → middleware/reader/card readiness → transaction-purpose confirmation → OS certificate selection → card-owned PIN/touch proof → handshake/processing → no-reader/no-card/wrong-certificate/PIN-blocked/expired/revoked/trust-outage states → fallback or recovery → success or next-factor result. Web, native desktop, and card-device handoff are release-gating.

**P1 — Enrollment and user lifecycle:** card/certificate registration, ownership proof, activation, detail, renewal/replacement, lost/stolen revocation, removal, and recovery.

**P2 — Administration and operations:** PIV/CAC trust policy, roots/profile/revocation configuration, mTLS client/service setup, middleware support, provider health, audit, and diagnostics.

Do not mistake certificate configuration for the authenticator. Smart Card is first class only when the P0 physical-card authentication ceremony works end to end.

**Release gate:** P0 must be interaction-complete and validated before P2 administration/configuration/management UIX is treated as delivery. P2 screens cannot be used to claim first-class authenticator support.

## 1. Mandate

Deliver complete PIV/CAC/smart-card authentication across card registration, certificate selection, login, step-up, evidence, lifecycle, expiry, replacement, revocation, recovery, trust policy, mTLS client/service configuration, middleware diagnostics, and non-web device prompts. PIN entry and private keys remain on the card/middleware boundary.

## 2. Required screens

| Screen | Purpose |
|---|---|
| Smart-card method chooser | Offer card authentication when browser/device/policy are compatible |
| Compatibility/middleware preflight | Detect approved browser/native bridge, reader, middleware, and certificate availability |
| Card registration | Bind approved public certificate/card identity to subject/client/service |
| Certificate selector handoff | Invoke OS/browser/middleware selection |
| Card PIN/touch handoff | Let middleware/card own unlock and proof |
| Login ceremony | Complete certificate challenge or approved mTLS flow |
| Step-up ceremony | Require card for sensitive actions |
| Insert/remove/reader guidance | Handle physical card/reader states |
| Retry/blocked/expired/revoked | Resolve PIN/card/certificate/middleware failures safely |
| Evidence detail | Show `sc`, certificate profile, trust, proof time, freshness, properties |
| Card/certificate detail | Show public identity, expiry, status, last use, issuer/profile |
| Replace/renew | Bind replacement before retiring expiring card where permitted |
| Revoke/remove | Handle lost/stolen/terminated card and dependent access |
| Recovery/fallback | Use alternate factor or supervised identity recovery |
| PIV/CAC trust policy | Configure issuers, roots, EKU, SAN/subject mapping, revocation, algorithms |
| User enrollment posture | Show missing/expiring/revoked card and re-enrollment actions |
| Developer/service mTLS config | Bind card/certificate-based client/service identities where applicable |
| Certificate validation diagnostics | Test chain, profile, revocation, clock, middleware, and proof |
| Provider/trust health | Monitor OCSP/CRL, trust anchors, middleware versions, and outages |
| Audit/incident detail | Investigate redacted card/certificate events |
| Native desktop/CLI tooling | Inspect public certificates and test connectivity without private-key export |

## 3. Registration flow

1. Recent-authentication/administrator authorization opens card registration.
2. Preflight verifies supported environment and gives installation/help routes without downloading unapproved software.
3. User inserts card and invokes system certificate selector.
4. Frontend receives approved public certificate projection only.
5. Server validates chain, trust anchor, profile, EKU, SAN/subject mapping, expiry, revocation, algorithms, tenant/subject, and duplicates.
6. Server challenges possession; middleware/card signs or completes handshake after its own PIN prompt.
7. Activation shows safe card label, public fingerprint, issuer/profile, expiry, status, recovery, and replacement guidance.

## 4. Authentication flow

1. Server offers smart card based on policy and compatibility.
2. UI explains insert/select/unlock sequence and fallback.
3. OS/browser/middleware owns certificate selection and PIN entry.
4. Proof is submitted or TLS handshake completes.
5. Server validates trust, revocation, proof, binding, freshness, and policy.
6. Success emits `sc` with supporting properties as verified; expired/revoked/blocked/untrusted outcomes route to replacement or recovery.

## 5. Lifecycle and recovery

- Detail shows card label, public certificate fingerprint, issuer/profile, subject projection, expiry, revocation status, created/last-used, and event history.
- Renewal/replacement supports overlap where identity policy permits.
- Lost/stolen revocation is immediate, warns about affected sessions/apps/services, and triggers notification.
- App cannot reset card PIN; blocked PIN routes to issuing authority/device workflow and alternate authentication.
- Removing the final eligible method requires supervised recovery or replacement.

## 6. Screen behavior

- Never render a fake certificate selector or PIN dialog.
- Do not ask users to upload private keys or export them from cards.
- Provide specific safe states: no reader, no card, multiple certificates, wrong profile, expired, revoked, chain failure, PIN blocked, middleware missing/outdated, and trust service unavailable.
- Certificate details use approved public fields; raw certificate download is permission controlled.
- Diagnostics use synthetic/public inputs and redact subject identifiers as required.

## 7. States

Support unsupported environment, middleware missing/outdated, reader missing, card absent/removed, certificate selection, multiple eligible/none eligible, ownership proof, active, expiring, expired, suspended, revoked, replacement required, PIN required externally, PIN blocked externally, chain/profile/EKU/SAN failure, revocation status unavailable, provider outage, cancelled, timeout, policy changed, success, and requires-next-step.

## 8. Components

Reuse `CeremonyShell`, `SecurityKeyPrompt`, `CompatibilityNotice`, `CertificateUploader` only for public certificate/CSR cases, `CertificateFingerprint`, `AuthenticatorDetailPanel`, `PolicyImpactPreview`, `DangerZone`, and audit/result components.

Add `SmartCardPreflight`, `CertificateSelectorHandoff`, `CardReaderStatus`, `CertificateProfileSummary`, `RevocationStatusBadge`, `CardReplacementTimeline`, and middleware/native adapters.

## 9. Data/API expectations

Server returns environment capability projection, approved certificate fields, trust/profile/revocation result, ownership status, ceremony state, evidence, lifecycle/actions, expiry, dependency impact, safe errors, policy version, and audit reference. PINs, private keys, card secrets, unrestricted subject data, and raw middleware diagnostics never enter normal frontend state.

## 10. Responsive, accessibility, and non-web

- Instructions work without images and remain usable at narrow widths/zoom.
- Reader/card state has text and accessible live updates without polling noise.
- Native desktop supports OS certificate APIs and secure middleware IPC.
- External reader/card prompts cover insertion, selection, touch, PIN, retry, blocked, and safe removal.
- CLI accepts certificate paths/public metadata and key-store references; private keys/PINs are not command arguments.

## 11. Security

- Bind card/certificate to tenant, subject/client/service, purpose, ceremony, trust profile, and proof.
- Enforce chain, EKU, SAN/subject mapping, revocation, time, algorithm, and replay policies server-side.
- Prevent certificate confusion, key substitution, cross-tenant binding, downgrade, and unsafe fallback.
- Require recent authentication/authority for registration, replacement, revocation, and removal.

## 12. Analytics and audit

Analytics records capability, handoff, safe failure class, replacement/recovery funnel, and completion. Audit certificate/card binding, proof, trust/revocation decision, login, expiry, replacement, revoke, lost/stolen event, recovery, policy/trust changes, and operator actions with redaction.

## 13. Tests

- Registration, certificate selection, ownership proof, login, step-up, evidence, renewal, overlap, revoke, removal, and recovery pass.
- No reader/card, multiple certificates, wrong profile, expiry, revocation, PIN blocked, middleware outage, and trust outage recover safely.
- Private keys/PINs never reach application UI or telemetry.
- Certificate confusion, replay, cross-tenant, policy change, OCSP/CRL, clock boundary, accessibility, native, and CLI tests pass.

## 14. Acceptance criteria

- Web and non-web card journeys are complete end to end.
- PIN and private-key operations stay inside card/middleware.
- Users can handle expiry, loss, blocking, replacement, and recovery safely.
- Developers/service operators can configure mTLS profiles without private-key upload.
- Administrators can govern and diagnose trust/revocation without exposing sensitive certificate data.

## 15. Dependencies

- PIV/CAC certificate profile and subject-mapping contracts.
- Browser/native middleware adapters and support policy.
- Trust anchors, OCSP/CRL/status services, and health.
- Card lifecycle, recovery, and administrative authority.

## References

- [AMR screen support matrix](../../amr-screen-support-matrix.md)
- [Universal authenticator ceremony brief](../uix-pairing-briefs/40-authenticator-ceremony-api-universal-authenticator-pages-uix.md)
- [Canonical AMR vocabulary](../../../pkgs/10-concrete/tigrbl-jose-concrete/src/tigrbl_jose_concrete/amr.py)
