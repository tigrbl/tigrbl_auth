# Retina AMR Frontend UIX Brief

- **AMR:** `retina`
- **Current delivery status:** Missing; no first-party retina verifier exists
- **Delivery target:** Complete first-party retina enrollment, liveness, verification, lifecycle, recovery, consent, deletion, and device-operations product
- **Category:** Specialized biometric method
- **Primary rule:** Retina evidence requires a dedicated approved verifier and must never be inferred from WebAuthn
- **Platforms:** Specialized native/device UI, federated web handoff, evidence/account/admin web

## UIX delivery priority

**P0 — Actual authentication UIX (ship first):** Retina method selection → specialized-device readiness → transaction-purpose confirmation → positioning/alignment guidance → retinal capture and fresh liveness challenge → processing → quality retry/no-match/spoof/device-failure/blocked states → fallback or supervised recovery → success or next-factor result. Sign-in and step-up are the release gate.

**P1 — Enrollment and user lifecycle:** informed consent, device preflight, enrollment capture, activation, detail, replacement/re-enrollment, suspension, revocation, recovery, consent withdrawal, and template deletion.

**P2 — Administration and operations:** device/verifier configuration, biometric policy, consent/retention administration, fleet health, conformance, audit, and incident diagnostics.

The specialized-device P0 ceremony—not the policy or device dashboard—is the first-class authenticator deliverable.

**Release gate:** P0 must be interaction-complete and validated before P2 administration/configuration/management UIX is treated as delivery. P2 screens cannot be used to claim first-class authenticator support.

## 1. Mandate

Specify the complete experience required before retinal scanning can be supported: eligibility, informed consent, device compatibility, enrollment, capture, liveness, verification, evidence, lifecycle, deletion, recovery, administration, provider health, audit, and non-web device interaction. Generic browser UI must not access camera/sensor data or imitate a retinal scanner.

## 2. Users and jobs

- Eligible users understand why retina verification is requested and can choose an alternative.
- Enrolled users complete a specialized-device ceremony and recover from sensor/device failure.
- Account holders inspect, suspend, retrain/replace, revoke, and delete the authenticator.
- Administrators govern consent, liveness, devices, assurance, geography, fallback, and retention.
- Platform operators manage verifier trust, device fleet, privacy, health, and conformance.

## 3. Required screens

| Screen | Purpose |
|---|---|
| Eligibility/method chooser | Offer retina only to approved users/devices/locations |
| Privacy and informed consent | Explain biometric processing, purpose, retention, sharing, deletion, alternatives |
| Device compatibility/preflight | Confirm approved sensor, calibration, environment, and connectivity |
| Enrollment introduction | Explain positioning, liveness, retries, and recovery |
| Native/device enrollment capture | Collect approved samples entirely inside verifier boundary |
| Enrollment quality/liveness feedback | Give safe actionable guidance without exposing thresholds |
| Enrollment review/activation | Confirm authenticator/device projection and consent record |
| Login/step-up handoff | Transfer to native/specialized verifier |
| Verification capture/liveness | Complete bound proof on device |
| Retry/cancel/unavailable/blocked | Handle quality, liveness, device, network, and policy failures |
| Federation redirect/callback | Consume trusted upstream retina evidence if supported |
| Result/next-step | Show success, reduced evidence, or another factor |
| Evidence detail | Show provenance, time, freshness, liveness class, device profile, limitations |
| Authenticator lifecycle | Suspend, replace/re-enroll, revoke, delete, inspect events |
| Recovery/fallback | Use another factor or supervised recovery |
| Biometric policy/consent admin | Configure eligibility, assurance, retention, fallback, and region |
| Device/verifier configuration | Manage trusted devices, keys, versions, health, and outage |
| Privacy request/deletion status | Track template deletion without exposing template data |
| Audit/incident diagnostics | Show redacted verifier/device outcomes |

## 4. Enrollment flow

1. Server verifies eligibility and returns approved verifier/device plus alternatives.
2. Consent screen records versioned, purpose-specific consent; declining exits to fallback without penalty beyond policy.
3. Preflight checks device, software, calibration, connectivity, and environmental readiness.
4. Explicit action starts native/device capture.
5. Device owns positioning, sample capture, quality, liveness, retry, and template construction.
6. Server receives a signed enrollment result, not raw images/templates.
7. Activation records device/verifier projection, consent, lifecycle, and recovery readiness.
8. Completion offers another method and privacy/deletion information.

## 5. Authentication flow

1. User selects approved retina method or policy requests it.
2. Web/native handoff displays purpose, device, expiry, and fallback.
3. Device performs capture/liveness and returns a signed ceremony-bound result.
4. Server validates device trust, signature, liveness, match result, time, replay, subject binding, and policy.
5. Safe retry may be allowed; repeated liveness/match failures become blocked/recovery without revealing thresholds.
6. Accepted evidence emits `retina`; result continues or requests another factor.

## 6. Lifecycle and deletion

- Detail shows status, enrollment date, verifier/device profile, consent version, last use, expiry/re-enrollment, and event history.
- Replacement creates a new enrollment before retiring the old template where policy permits.
- Revocation blocks use immediately.
- Deletion screen explains consequences, requires recent authentication, submits a verifier deletion job, and shows pending/completed/failed status with audit reference.
- Last-factor deletion requires an approved replacement or supervised recovery.

## 7. States

Support ineligible, consent required/declined/withdrawn, device unavailable, incompatible, calibration required, enrollment ready/capturing/quality retry/liveness failure/completed, active, suspended, replacement required, revoked, deletion pending/completed/failed, verification ready/capturing/processing/retry/blocked, provider outage, network interruption, stale/untrusted result, replay, policy changed, expired, success, and requires-next-step.

## 8. Components

Reuse universal ceremony, method chooser, compatibility, privacy, evidence, lifecycle, danger, policy, audit, and failure components.

Add `BiometricConsentRecord`, `SpecializedDevicePreflight`, `RetinaDeviceHandoff`, `CaptureGuidanceFrame` for native/device implementations only, `LivenessResultSummary`, `BiometricDeletionStatus`, and `VerifierDeviceHealth`.

## 9. Data/API expectations

Server projection includes eligibility, approved device/verifier, consent text/version/status, ceremony state, safe native instructions, signed-result status, liveness class, evidence provenance/freshness, lifecycle/deletion state, fallback, policy version, and audit reference.

Raw eye images, templates, feature vectors, match/quality thresholds, unrestricted scores, and sensor telemetry never enter generic web/native application payloads.

## 10. Responsive, accessibility, and device UI

- Web consent/handoff/evidence screens support reflow, zoom, keyboard, screen reader, contrast, and reduced motion.
- Native/device capture supports spoken and nonvisual guidance, physical accessibility alternatives, language selection, and operator-assisted modes where governed.
- Guidance must not depend only on color, animation, or sound.
- Device disconnection/resume remains bound to the original ceremony.

## 11. Security and privacy

- Complete biometric privacy, data-protection impact, consent/alternative, retention, deletion, and regional review before activation.
- Samples/templates stay in approved verifier/device boundaries and are encrypted with separation of duties.
- Bind enrollment/results to tenant, subject, ceremony, purpose, verifier/device, nonce, and time.
- Prevent replay, template substitution, cross-subject matching, downgrade, spoofing, and operator misuse.
- No biometric data in URLs, logs, analytics, browser storage, screenshots, crash reports, support exports, or generic audit.

## 12. Analytics and audit

Analytics records eligibility, consent outcome, device availability, safe capture outcome class, fallback, and completion. Audit consent, enrollment, verifier/device, liveness/match decision class, evidence, lifecycle, deletion job, recovery, policy/provider changes, and operator action without biometric material.

## 13. Tests

- Consent accept/decline/withdraw, enrollment, quality retry, liveness failure, authentication, fallback, replacement, revoke, deletion, and recovery pass.
- Device outage/disconnect, replay, stale result, wrong subject/tenant, policy change, and provider compromise fail safely.
- No biometric data crosses the verifier boundary.
- Accessibility includes nonvisual guidance and users unable to position/use the device.
- Generic WebAuthn never renders `retina`.

## 14. Acceptance criteria

- No retina capability appears before provider, privacy, consent, lifecycle, and deletion contracts are production-ready.
- All web and specialized-device screens are implemented end to end.
- Alternatives are available wherever policy permits and consent is meaningful.
- `retina` is emitted only from verified signed evidence.
- Users can revoke and obtain proof of deletion without exposing biometric material.

## 15. Dependencies

- Approved retina verifier/device and signed-result protocol.
- Liveness, consent, template lifecycle, and deletion services.
- Legal/privacy/regional approval and accessibility alternative.
- Device fleet, health, calibration, and conformance management.

## References

- [AMR screen support matrix](../../amr-screen-support-matrix.md)
- [Universal authenticator ceremony brief](../uix-pairing-briefs/40-authenticator-ceremony-api-universal-authenticator-pages-uix.md)
- [Canonical AMR vocabulary](../../../pkgs/10-concrete/tigrbl-jose-concrete/src/tigrbl_jose_concrete/amr.py)
