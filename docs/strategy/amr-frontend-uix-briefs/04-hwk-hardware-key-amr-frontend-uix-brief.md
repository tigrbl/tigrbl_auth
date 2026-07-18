# Hardware-Secured Key AMR Frontend UIX Brief

- **AMR:** `hwk`
- **Current delivery status:** Partial; WebAuthn metadata defaults to `hwk` without evidence-driven classification
- **Delivery target:** Complete first-party hardware-secured key product for human, client, and workload authentication
- **Category:** Possession/key-protection evidence
- **Primary implementation rule:** Show `hwk` only when accepted attestation or key-origin evidence proves hardware protection
- **Platforms:** Web, native, browser/OS WebAuthn, roaming security keys, client/workload configuration, CLI diagnostics

## UIX delivery priority

**P0 — Actual authentication UIX (ship first):** passkey/security-key method selection → compatibility state → transaction-purpose confirmation → browser/OS/device handoff → insert/select/touch/unlock guidance → assertion/proof processing → cancelled/timeout/transport/untrusted-hardware/policy-insufficient states → fallback/recovery → success or next-factor result. Human sign-in/step-up and machine proof execution are the release-gating experiences.

**P1 — Enrollment and lifecycle:** platform/roaming key enrollment, attestation result, naming, backup/recovery, authenticator detail, replacement, overlap, revocation, and compromised-key response.

**P2 — Administration and operations:** attestation/algorithm policy, client/workload registration configuration, trust metadata, provider health, validation workbench, and audit.

Hardware-key configuration is secondary. The authenticator is first class only when the P0 assertion/proof ceremony is complete across browser, native, and external-key devices.

**Release gate:** P0 must be interaction-complete and validated before P2 administration/configuration/management UIX is treated as delivery. P2 screens cannot be used to claim first-class authenticator support.

## 1. Mandate

Deliver complete human, client, and workload experiences for enrolling, authenticating with, managing, inspecting, and governing hardware-secured keys. The UI must distinguish platform passkeys, roaming security keys, hardware client keys, certificates, and workload keys while keeping key material and assurance claims accurate.

## 2. Users and jobs

- Users enroll and use a platform or roaming authenticator and recover from loss safely.
- Account holders name, inspect, replace, suspend, and remove hardware-backed authenticators.
- Administrators require approved attestation, algorithms, user verification, and fallback.
- Developers bind hardware-backed public keys/certificates without uploading private keys.
- Service operators rotate workload keys and inspect proof evidence.
- Platform operators manage attestation roots, metadata, algorithms, health, and conformance.

## 3. Required screens

| Screen | Platform | Purpose |
|---|---|---|
| Login method chooser | Web/native | Offer passkey/security key when eligible |
| Passkey/security-key assertion | Web/native + OS/device | Complete WebAuthn or profile-specific proof |
| Step-up chooser/ceremony | Web/native | Require approved hardware evidence |
| Enrollment introduction | Web/native | Explain platform versus roaming options and policy |
| Compatibility/preflight | Web/native | Check browser, OS, transport, and policy support |
| Registration prompt/handoff | Browser/OS | Create the credential through the platform |
| Cross-device handoff | Web/native/external | Complete hybrid flow when supported |
| Naming and metadata review | Web | Save safe display metadata |
| Authenticator detail | Web | Show verified backing, transports, status, dates, and evidence |
| Replace/revoke/remove | Web | Protect lifecycle and last-authenticator cases |
| Recovery center | Web | Manage backup methods and lost-key recovery |
| Attestation/algorithm policy | Web | Configure trust, hardware requirements, and rollout |
| Client/workload key registration | Web | Register public key, JWKS, CSR, or certificate |
| Rotation/overlap page | Web | Activate replacement before retiring prior key |
| Evidence detail | Web | Show attestation/key-origin provenance and freshness |
| Validation diagnostics | Web/CLI | Test synthetic proof and public metadata |
| Device prompts | OS/external | Insert, touch, unlock, select transport, or enter device PIN |

## 4. Human enrollment flow

1. Add-authenticator displays “Passkey” and “Security key” according to policy—not a blanket “hardware key.”
2. Introduction explains device compatibility, portability, backup state, recovery, and verified hardware requirements.
3. Preflight obtains server options and checks browser capability without starting registration.
4. Explicit action launches WebAuthn registration.
5. The OS/device owns biometric, PIN, insertion, touch, and transport prompts.
6. The server validates challenge, RP, attestation, algorithms, UV, and policy.
7. If hardware evidence is accepted, naming/review shows `hwk`; otherwise policy either accepts a lower classification or rejects registration.
8. Completion requires recovery guidance and provides a second-authenticator action.

## 5. Authentication and step-up flow

1. Server returns eligible credentials and policy requirements.
2. The UI supports conditional mediation where allowed or explicit selection otherwise.
3. Assertion handoff handles platform, roaming, cross-device, cancellation, timeout, and unsupported transport.
4. Server validates assertion and returns evidence-derived properties.
5. Success shows achieved context; insufficient hardware evidence can require another method without claiming authentication failure.
6. Refresh resumes but never automatically relaunches WebAuthn.

## 6. Client/workload flow

1. Choose an approved key/certificate authentication profile.
2. Register public material only: JWK/JWKS, certificate, CSR information, or attested public key.
3. Validate algorithm, use, identifier, chain/profile, attestation, and ownership proof.
4. Show fingerprint/thumbprint, key ID, hardware-evidence source, expiry, and binding.
5. Test with synthetic/redacted requests.
6. Rotate with overlap; activate replacement; verify traffic; retire/revoke prior key.
7. Audit every lifecycle transition.

## 7. Screen behavior

### Method chooser and compatibility

- Separate platform passkey, roaming security key, and managed hardware key only when the server catalog supports the distinction.
- Never promise hardware backing before registration/assertion evidence is accepted.
- Unsupported browser, missing transport, disabled platform authenticator, and policy incompatibility have distinct actions.

### Device handoff

- Launch only from explicit user action.
- Do not imitate system biometric/PIN/security-key dialogs.
- Provide insertion/touch guidance outside the prompt without obscuring it.
- Map `NotAllowedError`, cancellation, timeout, invalid state, duplicate credential, transport failure, and policy rejection safely.

### Authenticator/evidence detail

- Show credential name, type, created/last-used dates, status, backup eligibility/state, verified hardware classification, attestation trust profile, transports, and audit reference.
- Do not show raw credential IDs, attestation objects, certificates beyond approved public projections, or device fingerprints.
- Distinguish verified hardware-backed, unverified backing, and evidence unavailable.

### Policy

- Controls include required hardware evidence, accepted attestation roots/formats, algorithms, UV, discoverability, transports, backup policy, app scope, grace, fallback, and recovery.
- Simulation covers missing/untrusted attestation, synced passkey, roaming key, provider outage, metadata staleness, and last-factor lockout.

## 8. Ceremony states

Support eligibility loading, ready, registering/asserting, awaiting OS/device, cross-device pending, submitting, duplicate, cancellation, timeout, unsupported environment, untrusted attestation, policy rejection, stale metadata, transport failure, retryable/terminal error, blocked, expired, success, and requires-next-step.

## 9. Components

Reuse `CeremonyShell`, `PasskeyPrompt`, `SecurityKeyPrompt`, `CrossDeviceHandoff`, `CompatibilityNotice`, `AuthenticatorInventory`, `AuthenticatorDetailPanel`, `AssuranceSummary`, `CertificateUploader`, `CertificateFingerprint`, `PublicKeySummary`, `JwksEditor`, `OneTimeSecretReveal`, and policy/audit primitives.

Add:

- `KeyBackingBadge` with verified/unverified/unavailable states;
- `AttestationSummary`;
- `AuthenticatorTransportList`;
- `HardwareKeyCompatibilityCheck`;
- `KeyRotationTimeline`;
- browser/native WebAuthn and hardware-key adapters.

## 10. Data/API expectations

The server supplies ceremony state/options, credential projection, verified backing classification, attestation trust result, algorithms, transports, UV/UP, backup eligibility/state, policy satisfaction, lifecycle actions, next step, safe errors, and audit reference.

Private keys, WebAuthn secrets, raw attestation unless explicitly authorized, unrestricted device identifiers, and hidden policy logic never enter frontend state.

## 11. Responsive and non-web requirements

- Enrollment and assertion work at narrow widths, 200% zoom, and mobile browser viewport changes caused by OS handoff.
- Cross-device QR/handoff has a textual alternative and expires visibly.
- Native apps bind app-resume callbacks to the ceremony.
- External-key screens cover insert, touch, unlock/PIN, retry, blocked device, and removal.
- CLI tooling accepts public material or synthetic proofs, never requests private-key upload, and produces redacted diagnostics.

## 12. Accessibility

- Device instructions do not depend on animation, color, or sound.
- Countdown is announced sparingly; focus stays stable during polling.
- All controls have visible focus and 44px-equivalent touch targets where touch is expected.
- Error summaries link to corrective actions.
- Cross-device, forced colors, screen reader, keyboard, reduced motion, and cancellation paths are tested.

## 13. Security

- Bind challenges to origin/RP or client/workload profile, tenant, subject, purpose, and ceremony.
- Prevent replay, duplicate enrollment, cross-account credential binding, downgrade, and unsafe fallback.
- Require recent authentication for destructive lifecycle actions.
- Prevent removal of the last usable authenticator without a governed recovery path.
- Never accept client-asserted `hwk`; derive it from verified server evidence.

## 14. Analytics and audit

Analytics: method eligibility, preflight result class, handoff, safe failure, fallback, completion, and lifecycle funnel. Exclude credential IDs, attestation payloads, public-key material, and device details.

Audit registration, attestation decision, assertion, policy version, evidence classification, rename, replacement, suspension, revocation, removal, client/workload binding, rotation, and administrator changes.

## 15. Tests

- Synced or unverified passkeys do not automatically receive `hwk`.
- Accepted attestation/key-origin evidence produces `hwk` with provenance.
- Platform/roaming/cross-device enrollment and assertion succeed.
- Cancellation, duplicate, timeout, transport failure, blocked key, stale metadata, untrusted attestation, and policy changes recover safely.
- Rotation overlap prevents outage; last-factor deletion is blocked.
- No private material leaks to DOM, logs, URLs, analytics, or error reports.
- Cross-tenant, origin/RP, replay, algorithm downgrade, accessibility, and responsive tests pass.

## 16. Acceptance criteria

- Human and machine flows cover enrollment, proof, evidence, lifecycle, rotation, recovery, policy, diagnostics, and audit.
- `hwk` is evidence-derived, never method-name-derived.
- System/device prompts remain system owned.
- Every unavailable or failed hardware path offers safe retry/fallback/recovery.
- Administrators can safely simulate and roll out hardware-key requirements.

## 17. Dependencies

- Attestation trust and metadata provider.
- Evidence-driven WebAuthn AMR classification.
- Client/workload public-key ownership-proof contracts.
- Recovery and lifecycle APIs for human and machine keys.

## References

- [AMR screen support matrix](../../amr-screen-support-matrix.md)
- [Universal authenticator ceremony brief](../uix-pairing-briefs/40-authenticator-ceremony-api-universal-authenticator-pages-uix.md)
- [Canonical AMR vocabulary](../../../pkgs/10-concrete/tigrbl-jose-concrete/src/tigrbl_jose_concrete/amr.py)
