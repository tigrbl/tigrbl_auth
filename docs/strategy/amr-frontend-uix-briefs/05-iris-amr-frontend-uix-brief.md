# Iris AMR Frontend UIX Brief

- **AMR:** `iris`
- **Current delivery status:** Missing first-party iris verifier and lifecycle
- **Delivery target:** Complete first-party iris authenticator with specialized-device enrollment, liveness, verification, lifecycle, recovery, and deletion
- **Category:** Biometric method evidence
- **Primary rule:** Never infer iris scanning from generic WebAuthn or user-verification evidence
- **Platforms:** Federated/passkey web flows, native/specialized device integration, account/admin evidence surfaces

## UIX delivery priority

**P0 — Actual authentication UIX (ship first):** Iris method selection → specialized-device readiness → transaction-purpose confirmation → alignment/gaze guidance → fresh iris capture and liveness challenge → processing → quality retry/no-match/spoof/device-disconnect/blocked states → alternate method or recovery → success or next-factor result. Sign-in and step-up parity are required. This is the primary deliverable and release gate.

**P1 — Enrollment and user lifecycle:** consent, device preflight, enrollment capture, activation, backup method, detail, retraining/replacement, suspension, revocation, recovery, consent withdrawal, and template deletion.

**P2 — Administration and operations:** verifier/device configuration, biometric policy, privacy/retention, provider health, conformance, audit, and diagnostics.

Do not lead delivery with provider configuration. Iris becomes first class only after the complete P0 user authentication ceremony works on the specialized device and its web/native handoff.

**Release gate:** P0 must be interaction-complete and validated before P2 administration/configuration/management UIX is treated as delivery. P2 screens cannot be used to claim first-class authenticator support.

## 1. Mandate

Provide a complete first-party iris authenticator: eligibility, informed consent, specialized-device preflight, enrollment capture, quality and liveness, template activation, login/step-up verification, evidence, replacement, suspension, revocation, recovery, consent withdrawal, and template deletion. Trusted upstream evidence remains an adapter, not the core implementation.

## 2. Users and jobs

- Users authenticate through an approved device/provider and recover when it is unavailable.
- Account holders inspect validated iris evidence without exposure of biometric data.
- Administrators configure eligible providers, consent, freshness, fallback, and application scope.
- Platform operators manage trust, privacy, health, and conformance.
- Specialized native-device users complete capture/liveness entirely in the approved device boundary.

## 3. Screen inventory

| Screen | Type | Requirement |
|---|---|---|
| Eligibility and consent | Web/native | Confirm policy/device/region and record biometric privacy consent |
| Specialized-device preflight | Native/device | Verify sensor, calibration, positioning accessibility, connectivity, and verifier health |
| Enrollment introduction | Native/device | Explain positioning, gaze, lighting, liveness, samples, retries, and alternatives |
| Enrollment capture | Specialized device | Collect server-directed samples inside the verifier boundary |
| Enrollment quality/liveness | Specialized device | Provide safe alignment/quality feedback and presentation-attack checks |
| Enrollment review/activation | Web/native | Confirm safe metadata, consent, recovery, and lifecycle—not eye media |
| Method-aware login | Web/native | Offer the eligible first-party Iris authenticator plus distinctly labeled provider/device adapters |
| Redirect progress/callback | Web | Complete trusted federation and transformed evidence validation |
| Step-up chooser | Web/native | Offer iris-capable source only when eligible |
| Native-device handoff | Native/external | Enter approved sensor/liveness workflow |
| Capture/liveness ceremony | Specialized native device | Owned by native verifier, not generic web UI |
| First-party iris challenge | Specialized native device | Capture fresh challenge-bound sample and validate liveness/match |
| Result/next step | All | Show completion, insufficient evidence, or another required factor |
| Evidence detail | Web | Show accepted `iris`, provenance, freshness, consent profile, limitations |
| Session context | Web | Show how evidence contributed to assurance |
| Linked provider/device detail | Web | Manage link/status, not biometric templates |
| Iris authenticator detail | Web/native | Show status, verifier/device profile, consent, dates, and events |
| Retrain/replace | Specialized device | Enroll replacement before retiring prior template |
| Suspend/revoke/remove | Web/native | Stop use with recent-authentication and last-factor safeguards |
| Template deletion status | Web/native | Track pending/completed/failed/manual-review erasure |
| Recovery/fallback | Web/native | Select another factor or supervised path |
| Evidence/policy editor | Web | Configure trusted sources, scope, age, fallback, and rollout |
| Provider/privacy configuration | Web | Configure integration, retention projection, and regional controls |
| Health/conformance | Web | Monitor liveness/verifier outcomes and claim transformation |
| Redacted audit detail | Web | Investigate without displaying images/templates/scores |

## 4. End-to-end flows

### First-party enrollment

1. Eligibility verifies tenant policy, jurisdiction, verifier/device availability, user population constraints, and accessible alternatives.
2. Consent explains capture, template processing, retention, sharing, withdrawal, deletion, and consequences of declining.
3. Device preflight checks calibration, sensor, positioning, accessibility, lighting/environment, connectivity, and verifier health.
4. Explicit user action begins capture; samples remain inside the specialized device/verifier boundary.
5. Server-directed capture performs alignment, quality, liveness/presentation-attack, duplicate/cross-subject safeguards, and template creation.
6. Bounded safe guidance handles positioning, gaze, occlusion, lighting, and retry without exposing scores/thresholds.
7. Activation binds the template reference, tenant/subject, consent, verifier/device/profile, lifecycle, and recovery.
8. Review shows safe metadata and completion offers a backup authenticator.

### First-party authentication

1. Login/step-up offers the eligible first-party Iris method and transaction purpose.
2. Handoff connects to the approved specialized device and issues a fresh liveness challenge.
3. Device captures a fresh sample and returns a signed verifier result bound to the ceremony.
4. Server validates liveness, match, template/authenticator, tenant/subject, challenge, purpose, time, replay, device trust, and policy.
5. Success emits `iris`; quality retry, no match, spoof suspicion, device outage, cancellation, and block follow server-directed recovery.

### Lifecycle and deletion

1. Detail shows status, device/verifier/profile, consent, dates, re-enrollment deadline, and events.
2. Replacement runs a new enrollment and safely retires the prior template after activation.
3. Suspension/revocation blocks use immediately.
4. Recovery authorizes a fresh enrollment and never restores an old template.
5. Consent withdrawal/deletion submits an erasure job and displays pending/completed/failed/manual-review with audit reference.

### Federated evidence adapter

1. The server offers a trusted provider capable of returning normalized iris evidence.
2. Redirect progress preserves the transaction and approved branding.
3. Callback payload is processed server-side; raw claims are not rendered.
4. The server validates issuer, signature, nonce, time, trust profile, and evidence transformation.
5. Accepted evidence proceeds; stale/untrusted/absent iris evidence falls back or requires another factor.
6. Result and context views qualify the source and state that no iris image reached the application.

### Additional native/specialized-device adapter

1. The pre-handoff screen explains purpose, privacy, device requirement, and alternative methods.
2. Explicit action invokes the approved native verifier.
3. The device owns alignment, capture, quality, liveness, retry, and sensor feedback.
4. The app receives only a signed result bound to the ceremony.
5. Server validation determines success, retry, blocked, or alternate-factor response.
6. Resume/deep-link rejects stale, replayed, or mismatched results.

### Policy flow

1. Select approved providers/device profiles.
2. Set maximum evidence age, liveness requirement, app scope, fallback, consent, and regional availability.
3. Simulate valid, absent, stale, failed liveness, device unavailable, provider outage, and cross-region cases.
4. Review lockout/privacy impact and publish an auditable version.

## 5. Screen behavior

### Consent, preflight, and enrollment

- Consent is purpose-specific, versioned, and paired with an equivalent accessible alternative where required.
- Specialized-device preflight must finish before capture and expose safe calibration, connectivity, and accessibility recovery.
- Capture begins only after explicit action and has cancel, privacy, progress, bounded retry, and device-disconnect handling.
- Alignment and quality feedback have spoken, textual, haptic where supported, and non-color equivalents.
- Enrollment review never displays an iris image, template, feature vector, or match score.

### First-party challenge

- Show transaction purpose before device capture.
- Fresh liveness and ceremony binding are required for every authentication.
- No-match and spoof-suspected results do not reveal scores, thresholds, or whether another identity matched.
- Device unavailable or unsafe paths offer another method or recovery.

### Login and step-up

- Label the first-party method “Use iris recognition” with its approved specialized-device/verifier qualifier. Label external adapters by provider/device, with “supports iris verification” only when catalog evidence permits it.
- Never imply that ordinary passkeys use iris scanning.
- Provide explicit start, cancel/back, switch-method, expiry, and recovery behavior.

### Native handoff

- Never mimic sensor capture or ask for camera access in generic web UI.
- Provide approved external-device status: connecting, ready, user action required, processing, cancelled, unavailable, and returned.
- Map native error classes to safe, non-diagnostic user messages.

### Evidence detail

- Show source, verification time, freshness, trust profile, liveness requirement/result class, ceremony purpose, policy result, and audit reference.
- Do not show biometric images, templates, quality/match scores, sensor serials, or unrestricted device identifiers.
- Distinguish direct native evidence from transformed upstream evidence.

### Lifecycle, recovery, and deletion

- Detail distinguishes active, suspended, compromised, replacement-required, revoked, and deletion-pending.
- Retraining/replacement is a new enrollment.
- Last-factor removal is blocked until replacement/recovery exists.
- Deletion separates immediate authentication revocation from asynchronous template erasure.
- Recovery gives reduced assurance until fresh enrollment or stronger step-up succeeds.

### Configuration

- Require approved issuer/device profile; arbitrary `iris` claims are rejected.
- Configure consent, availability, fallback, maximum age, minimum evidence profile, fail behavior, and retention projection.
- Provider health separates outage, trust failure, liveness failure, stale response, and mapping rejection.

## 6. States

Implement eligibility, consent, device preflight/calibration, enrollment capture, quality retry, liveness failure, activation pending, active, first-party challenge, no match, spoof suspected, replacement, suspension, revocation, recovery, deletion pending/completed/failed/manual-review, redirecting, callback processing, awaiting device, cancelled, sensor unavailable, provider unavailable, stale/untrusted evidence, expired, blocked, policy changed, success, and requires-next-step.

Refresh never restarts external capture automatically.

## 7. Components

Reuse `CeremonyShell`, `ProviderButton`, `AuthenticatorMethodPicker`, `CeremonyProgress`, `MethodSwitchMenu`, `AuthenticationContextSummary`, `EvidenceFreshnessBadge`, `PolicyImpactPreview`, and shared result/failure states.

Add `BiometricConsentRecord`, `IrisDevicePreflight`, `IrisEnrollmentCapture`, `IrisAlignmentGuidance`, `ExternalBiometricHandoff`, `BiometricEvidenceQualifier`, `BiometricPrivacyNotice`, `LivenessEvidenceSummary`, `BiometricAuthenticatorLifecycle`, `BiometricDeletionStatus`, `EvidenceProvenancePanel`, and a native result adapter.

## 8. Data/API contract

The server returns eligibility, consent document/version/status, device/verifier/profile, preflight/calibration projection, enrollment/liveness state, template-reference projection, authenticator lifecycle, deletion job/status, ceremony state, provider/device display projection, normalized AMRs, provenance, evidence time/freshness, trust profile, policy satisfaction, allowed fallback, safe error, next step, and audit reference.

Biometric samples/templates, raw scores, raw upstream claims, sensor data, and unrestricted device identifiers never enter generic application payloads. Approved specialized-device capture handles samples only transiently inside the verifier boundary.

## 9. Responsive, accessibility, and non-web

- Web handoff screens work at narrow widths and 200% zoom.
- Native/external status is textual and does not depend on video, animation, sound, or color.
- Focus and announcements remain stable during device polling.
- Native apps bind results to the originating ceremony and provide an accessible cancel/fallback path.
- Specialized-device UI must meet equivalent keyboard/switch-control, contrast, language, and privacy requirements.

## 10. Security and privacy

- Bind evidence to tenant, subject, purpose, ceremony, provider/device, nonce, and time.
- Require explicit consent where applicable and disclose retention/data boundaries before handoff.
- Reject raw or untrusted iris claims.
- No biometric data in DOM, application storage, URLs, analytics, logs, screenshots, crash reports, or support exports.
- Require recent authentication for provider/device link changes and last-factor removal.
- Enforce liveness/presentation-attack detection, duplicate/cross-subject safeguards, encrypted template storage, signed verifier results, consent withdrawal, and deletion.

## 11. Analytics and audit

Analytics record eligibility, handoff, safe outcome class, fallback, and completion only. Audit records may identify accepted iris evidence with provenance, policy version, and trust decision but never biometric material or scores.

## 12. Tests

- Generic WebAuthn never renders `iris`.
- First-party consent, preflight, enrollment, quality retry, liveness, activation, login, and step-up pass end to end.
- No-match, spoof suspicion, calibration/sensor failure, disconnect, cancellation, timeout, block, and recovery are safe.
- Replacement, suspension, revocation, last-factor protection, consent withdrawal, and deletion states pass.
- Trusted native/upstream evidence renders qualified language.
- Missing, stale, failed-liveness, untrusted, mismatched, replayed, and cross-tenant evidence fails closed.
- Redirect/callback, external-device cancellation, outage, resume, expiry, and fallback work.
- Privacy leakage tests cover DOM, storage, URLs, logs, analytics, screenshots, and error reports.
- Accessibility, zoom, contrast, reduced-motion, and device-status announcements pass.

## 13. Acceptance criteria

- Login, handoff, callback, external ceremony, result, evidence, lifecycle link, recovery, policy, diagnostics, and audit paths are specified.
- No generic web UI collects iris data.
- A user can enroll, activate, authenticate, replace, suspend, revoke, recover, withdraw consent, and delete a first-party iris authenticator.
- `iris` is displayed only with accepted provenance.
- Every unavailable/failed path provides safe fallback or terminal guidance.
- Administrators can simulate and govern the integration without exposing biometric data.

## 14. Dependencies

- First-party specialized-device capture, liveness, matcher, signed-result, template, consent, and deletion contracts.
- Trusted federation evidence profile for the optional adapter.
- Liveness and consent contracts.
- Biometric privacy, retention, deletion, and regional policy.
- Signed native result and deep-link binding contract.

## References

- [AMR screen support matrix](../../amr-screen-support-matrix.md)
- [Universal authenticator ceremony brief](../uix-pairing-briefs/40-authenticator-ceremony-api-universal-authenticator-pages-uix.md)
- [Canonical AMR vocabulary](../../../pkgs/10-concrete/tigrbl-jose-concrete/src/tigrbl_jose_concrete/amr.py)
