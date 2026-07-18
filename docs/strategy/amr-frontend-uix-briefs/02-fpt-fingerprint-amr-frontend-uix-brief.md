# Fingerprint AMR Frontend UIX Brief

- **AMR:** `fpt`
- **Current delivery status:** Missing first-party fingerprint verifier and lifecycle
- **Delivery target:** Complete first-party fingerprint authenticator with native enrollment, liveness, verification, lifecycle, recovery, and deletion
- **Category:** Biometric method evidence
- **Primary implementation rule:** A WebAuthn user-verification result is not proof that a fingerprint was used
- **Platforms:** Public web, account/admin web, native platform authentication, external fingerprint devices where separately integrated

## UIX delivery priority

**P0 — Actual authentication UIX (ship first):** Fingerprint method selection → transaction-purpose confirmation → sensor/permission readiness → native fingerprint capture → liveness and match processing → safe quality retry/no-match/spoof/blocked/sensor-unavailable states → alternate-method or recovery handoff → success or next-factor result. It must support both sign-in and step-up. This is the primary deliverable and release gate.

**P1 — Enrollment and user lifecycle:** biometric consent, finger/sensor enrollment, activation, recovery confirmation, authenticator detail, retraining/replacement, suspension, revocation, recovery, consent withdrawal, and template deletion.

**P2 — Administration and operations:** biometric evidence policy, verifier/sensor profiles, health, conformance, retention, audit, and diagnostics.

Do not begin with evidence dashboards. Fingerprint is first class only when a user can complete the P0 ceremony—including every adverse state—without relying on administrative tooling.

**Release gate:** P0 must be interaction-complete and validated before P2 administration/configuration/management UIX is treated as delivery. P2 screens cannot be used to claim first-class authenticator support.

## 1. Outcome

Provide a complete first-party fingerprint authenticator: informed consent, approved native sensor enrollment, presentation-attack detection, template creation, transaction-bound verification, evidence, replacement, suspension, revocation, recovery, consent withdrawal, and template deletion. Trusted passkey or federation evidence remains supported as an adapter but cannot substitute for the native product.

## 2. Users and jobs

- End users authenticate through their device or trusted provider and recover safely when the sensor is unavailable.
- Account holders inspect when and where fingerprint evidence was asserted.
- Tenant administrators define which evidence sources may satisfy fingerprint-specific policies.
- Platform operators configure provider trust, monitor transformations, and investigate rejected claims.
- Native-app users complete a platform prompt without the application handling fingerprint data.

## 3. Scope boundaries

Generic browser/application UI must not capture or retain fingerprint images/templates, infer `fpt` from WebAuthn UV, expose raw upstream claims, or promise liveness/hardware backing without separate verified properties. Approved native capture code may handle samples only transiently and directly inside the verifier transfer boundary.

## 4. Required screens

| Screen | Type | Required behavior |
|---|---|---|
| Eligibility and consent | Web/native | Explain biometric purpose, processing, retention, deletion, alternatives, and record versioned consent |
| Sensor/permission preflight | Native/OS | Verify approved sensor, driver, permission, verifier health, and accessibility |
| Enrollment introduction | Native | Explain finger selection, placement, repeated samples, liveness, retries, and recovery |
| Enrollment capture | Native/verifier | Collect server-directed samples inside approved boundary |
| Capture quality/liveness | Native/verifier | Provide safe placement/coverage feedback and anti-spoof checks |
| Enrollment review/activation | Web/native | Confirm safe metadata, consent, lifecycle, and recovery—not fingerprint media |
| Login/method chooser | Web/native | Offer the eligible first-party Fingerprint authenticator plus distinctly labeled passkey/provider adapters |
| Passkey assertion | Web/native | Handoff to WebAuthn/OS and submit assertion without modality inference |
| Federation redirect/callback | Web | Preserve transaction, validate server-transformed evidence, handle mismatch and outage |
| MFA/step-up chooser | Web/native | Offer eligible underlying method and show policy target without asserting modality early |
| Native fingerprint prompt | OS | System-owned capture and verification |
| First-party fingerprint challenge | Native/verifier | Capture fresh, challenge-bound sample and validate liveness/match |
| Result/next-step | Web/native | Show completion or another required factor |
| Evidence detail | Web | Show accepted `fpt`, source, time, freshness, trust profile, and limitations |
| Session context | Web | Explain how the current session received the evidence |
| Underlying authenticator detail | Web | Manage passkey or linked provider; never manage fingerprint templates |
| Fingerprint authenticator detail | Web/native | Show status, selected-finger label, verifier profile, consent, dates, and events |
| Retrain/replace | Native/verifier | Enroll replacement template before retiring prior one |
| Suspend/revoke/remove | Web/native | Stop use with recent-authentication and last-factor safeguards |
| Template deletion status | Web/native | Track pending/completed/failed/manual-review deletion |
| Recovery/re-enrollment | Web/native | Recover through another method and create a new template |
| Evidence policy editor | Web | Configure trusted sources, age, application scope, fallback, and rollout |
| Provider configuration/health | Web | Configure transformations and show rejection/outage posture |
| Authentication event detail | Web | Render redacted provenance and audit reference |
| Unsupported modality state | All | Explain that available evidence proves user verification but not fingerprint use |

## 5. Critical flows

### First-party enrollment

1. Eligibility verifies policy, jurisdiction, age/population constraints, device/sensor, verifier health, and accessible alternatives.
2. Consent explains processing boundary, template retention, sharing, withdrawal, deletion, and consequences of declining.
3. Explicit action invokes OS sensor permission and native preflight.
4. User chooses an allowed finger label without the server storing anatomical detail beyond the approved display projection.
5. Native capture collects multiple server-directed samples and streams them directly to the verifier.
6. Verifier evaluates coverage/quality, liveness/presentation attack, duplicate/cross-subject safeguards, and template creation.
7. Safe feedback guides lift/place/reposition/clean sensor without exposing scores or thresholds.
8. Activation binds template reference, subject, tenant, consent, verifier/profile, lifecycle, and recovery.
9. Completion notifies the user and encourages a backup authenticator.

### First-party authentication

1. Login/step-up returns an eligible fingerprint method and transaction purpose.
2. Explicit action opens the approved native capture surface.
3. Server/verifier issues a fresh challenge and liveness profile.
4. Native capture obtains a new sample within the verifier boundary.
5. Server validates liveness, match, template/authenticator, tenant/subject, challenge, purpose, verifier signature, time, replay, and policy.
6. Accepted result emits `fpt`; quality retry, no match, spoof suspicion, lockout, sensor failure, cancellation, and expiry route safely.

### Lifecycle and deletion

1. Detail presents status, finger label, verifier/profile, consent, created/last-used, re-enrollment deadline, and events.
2. Replacement runs a new enrollment and activates the new template before retiring the prior one where overlap is allowed.
3. Suspension/revocation blocks authentication immediately.
4. Recovery never restores an old template; it permits a fresh enrollment after approved proof.
5. Consent withdrawal/deletion submits a verifier erasure job and displays pending/completed/failed/manual-review states.

### Passkey authentication adapter

1. The server offers a passkey method.
2. Explicit user action launches the browser/OS prompt.
3. The user completes the system-controlled verification.
4. The assertion is submitted; client code does not inspect prompt copy or device heuristics.
5. Server evidence determines whether the UI may show `fpt` or only “User verified.”
6. Success continues to the target; cancellation, sensor lockout, timeout, and unsupported environments return to a resumable ceremony.

### Federated fingerprint evidence adapter

1. The user selects a configured provider.
2. Redirect and callback screens preserve server state and hide tokens/claims.
3. The server maps upstream evidence through an approved profile.
4. Trusted `fpt` appears as qualified evidence; untrusted or stale evidence cannot satisfy policy.
5. Identity mismatch or account-link risk blocks the flow with recovery guidance.

### Policy administration

1. Select fingerprint evidence as an allowed/required condition.
2. Select trusted issuers/integrations and maximum evidence age.
3. Choose fallbacks and applications.
4. Simulate absent, generic UV, accepted fingerprint, stale, conflicting, and provider-outage cases.
5. Review lockout impact, approve, publish, and audit the version.

## 6. Screen behavior

### Consent, preflight, and enrollment capture

- Consent is purpose-specific, versioned, separable from general terms, and offers an equivalent accessible alternative where required.
- Sensor permission is requested only after explicit consent action.
- Native preflight distinguishes no sensor, unsupported sensor, driver/service unavailable, permission denied, sensor dirty, verifier outage, and accessible-alternative required.
- Capture guidance has text, spoken, haptic where supported, and non-color equivalents.
- Raw samples clear from transient buffers after acknowledged transfer, retry replacement, cancellation, timeout, or crash recovery.
- Enrollment review never shows a fingerprint image or template.

### First-party challenge

- Show transaction purpose before capture.
- Bounded quality retries do not consume authentication attempts until server policy says so.
- No-match and spoof-suspected states do not expose scores, thresholds, or whether another identity matched.
- A blocked or unavailable sensor always offers policy-approved fallback/recovery.

### Login, step-up, and ceremony

- Label the first-party method “Use fingerprint” with its approved sensor/verifier qualifier. Label passkey, security-key, device, and provider adapters by their actual authenticator.
- Only adapter copy may say “Your device may ask for a fingerprint, face, PIN, or another unlock method”; the direct fingerprint method has its own consented first-party capture flow.
- Implement eligibility, consent, permission, preflight, enrollment capture, quality retry, liveness failure, activation pending, active, first-party challenge, no match, spoof suspected, sensor unavailable/dirty/blocked, replacement, suspension, revocation, recovery, deletion pending/completed/failed/manual-review, external prompt, submitting, cancelled, expired, provider outage, success, and requires-next-step states.
- Refresh resumes server state and never automatically reopens the system prompt.
- Switch-method remains visible whenever policy allows it.

### Evidence detail

- Heading: “Fingerprint evidence” only when the normalized evidence state is trusted.
- Show direct versus transformed source, provider/authenticator, authentication time, evidence age, ceremony purpose, policy result, and audit reference.
- State that the application did not receive or store fingerprint data.
- For generic UV, show “User verified; method not disclosed.”
- Allow reporting an unfamiliar event and navigating to the underlying authenticator/session lifecycle.

### Lifecycle, recovery, and deletion

- Detail distinguishes active, suspended, compromised, replacement-required, revoked, and deletion-pending.
- Replace/retrain is a new enrollment, not editing a template in app state.
- Last-factor removal is blocked until replacement/recovery exists.
- Deletion separates immediate authentication revocation from asynchronous verifier erasure and supplies an audit reference.
- Recovery yields reduced assurance until a new fingerprint or stronger method is activated.

### Configuration and diagnostics

- No “trust all upstream AMRs” option.
- Provider profiles define issuer, mapping rules, freshness, assurance constraints, and allowed tenants/apps.
- Health views separate provider outage, invalid signature, stale evidence, unsupported claim, and transformation failure.
- Diagnostics use synthetic/redacted payloads only.

## 7. State matrix

Support ineligible, consent required/declined/withdrawn/outdated, permission required/denied, sensor unavailable/unsupported/dirty/blocked, preflight degraded, enrollment ready/capturing/quality retry/liveness failure/activation pending, active, challenge ready/capturing/processing/no match/spoof suspected, submitting, external adapter pending, cancelled, timeout, rate limited, attempts exhausted, suspended, compromised, replacement required, revoked, recovery only, deletion pending/completed/failed/manual-review, provider outage, policy changed, success, and requires-next-step.

Refresh resumes server state and never restarts capture or creates another template automatically.

## 8. Components

Reuse `CeremonyShell`, `AuthenticatorMethodPicker`, `PasskeyPrompt`, `ProviderButton`, `MethodSwitchMenu`, `AuthenticationContextSummary`, `EvidenceFreshnessBadge`, `AuthenticatorEventTimeline`, `PolicyImpactPreview`, and shared failure states.

Add or extend:

- `BiometricEvidenceQualifier` with trusted, transformed, generic-UV, stale, and rejected modes;
- `BiometricPrivacyNotice`;
- `EvidenceProvenancePanel`;
- native handoff adapter result mapping for sensor unavailable, lockout, cancellation, and interruption.
- `BiometricConsentRecord`, `FingerprintSensorPreflight`, `FingerprintEnrollmentCapture`, `CaptureCoverageGuidance`, `LivenessChallengeStatus`, `BiometricAuthenticatorLifecycle`, and `BiometricDeletionStatus`.

## 9. Data contract

Presentation-safe server data must include eligibility, consent document/version/status, capture/verifier profile, sensor/preflight projection, enrollment/liveness state, template-reference projection, authenticator lifecycle, deletion job/status, ceremony state, underlying method/provider, normalized AMRs, evidence provenance, authentication time, freshness, trust profile, policy satisfaction, next step, safe error, allowed fallback, and audit reference.

Generic browser/application state must never receive fingerprint samples, templates, matching/liveness scores, unrestricted device identifiers, or raw upstream claims. Approved native capture handles samples only transiently in the verifier boundary.

## 10. Responsive, accessibility, and native requirements

- Stack ceremony content and actions on narrow layouts; keep the primary action visible without obscuring error text.
- Evidence uses semantic definition lists and wraps long provider names.
- All statuses have text equivalents, visible focus, 200% zoom support, forced-color support, and screen-reader announcements.
- OS prompts launch only from explicit actions and are never visually imitated.
- Native resume/deep-link handling must bind to the original ceremony and reject stale returns.

## 11. Security and privacy

- No biometric material outside the approved transient native/verifier boundary, including application state, DOM, URLs, logs, analytics, clipboard, screenshots, crash reports, or support exports.
- Enforce origin/RP, tenant, subject, transaction, provider, nonce, and callback binding server-side.
- Require recent authentication before provider linking/unlinking or removing the last usable authenticator.
- Reject unexpected `fpt` claims unless a configured evidence profile explicitly accepts them.
- Enforce liveness/presentation-attack detection, duplicate/cross-subject safeguards, encrypted template storage, separation of duties, signed verifier results, consent withdrawal, and deletion.

## 12. Analytics and audit

Product analytics may record offered method, handoff, safe error class, fallback, and completion. Only security audit records may identify accepted `fpt`, and those records must contain provenance—not biometric data.

Audit provider/profile changes, accepted/rejected evidence, freshness decisions, policy versions, account-link changes, and underlying authenticator/session revocation.

## 13. Test requirements

- Generic WebAuthn UV never renders `fpt`.
- First-party consent, permission, enrollment, quality retry, liveness, activation, login, and step-up pass end to end.
- No-match, spoof suspicion, sensor failure/dirty/blocked, cancellation, timeout, attempts exhaustion, and recovery are safe.
- Replacement, suspension, revocation, last-factor protection, consent withdrawal, and deletion-state tests pass.
- Accepted direct/transformed evidence renders qualified fingerprint language.
- Missing, untrusted, stale, conflicting, and replayed evidence fails closed.
- OS cancel, lockout, unavailable sensor, unsupported environment, timeout, refresh/resume, and fallback work.
- Federation callback mismatch, outage, takeover block, and replay are safe.
- No fingerprint material or raw claims reach browser/native telemetry or general application storage; native transient buffers clear correctly.
- Keyboard, screen reader, zoom, contrast, reduced-motion, cross-tenant, and cross-subject tests pass.

## 14. Acceptance criteria

- The flow is complete across login, step-up, callback, native handoff, result, evidence, policy, health, audit, and fallback.
- A user can enroll, activate, authenticate, replace, suspend, revoke, recover, withdraw consent, and delete a first-party fingerprint authenticator.
- Fingerprint language appears only from trusted server-normalized evidence.
- Every failure has a safe retry, switch, recovery, or terminal route.
- Users can inspect evidence without seeing sensitive biometric or raw-provider data.
- Administrators can simulate and safely roll out fingerprint-specific evidence policy.

## 15. Dependencies

- Trusted biometric-evidence and transformation profile.
- First-party native sensor capture, liveness, matcher, signed-result, template, consent, and deletion contracts.
- Biometric audit-retention and regional privacy policy.
- Evidence-driven WebAuthn AMR emission.

## References

- [AMR screen support matrix](../../amr-screen-support-matrix.md)
- [Universal authenticator ceremony brief](../uix-pairing-briefs/40-authenticator-ceremony-api-universal-authenticator-pages-uix.md)
- [Canonical AMR vocabulary](../../../pkgs/10-concrete/tigrbl-jose-concrete/src/tigrbl_jose_concrete/amr.py)
