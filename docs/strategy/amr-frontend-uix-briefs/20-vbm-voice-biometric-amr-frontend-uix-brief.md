# Voice Biometric AMR Frontend UIX Brief

- **AMR:** `vbm`
- **Current delivery status:** Missing; no voice-biometric verifier, liveness, consent, or template lifecycle exists
- **Delivery target:** Complete first-party voice-biometric enrollment, liveness, verification, lifecycle, recovery, consent, deletion, and operations product
- **Category:** Biometric method
- **Primary rule:** Voice biometric evidence is distinct from telephone-channel confirmation (`tel`)
- **Platforms:** Web/native microphone capture, specialized verifier, optional call channel, account/admin/privacy surfaces

## UIX delivery priority

**P0 — Actual authentication UIX (ship first):** Voice Biometric method selection → microphone/device readiness → transaction-purpose and randomized phrase → permission handoff → recording → liveness/match processing → noise/no-speech/quality-retry/spoof/no-match/permission-denied/blocked states → alternate method or recovery → success or next-factor result. Web/native capture parity is the release gate.

**P1 — Enrollment and user lifecycle:** informed consent, microphone preflight, enrollment samples, activation, detail, retraining/replacement, suspension, revocation, recovery, consent withdrawal, and template deletion.

**P2 — Administration and operations:** language/model/liveness policy, verifier/region configuration, retention/privacy operations, health/drift, fraud diagnostics, audit, and optional telephony profile.

Do not lead with model or consent administration. The first-class authenticator is the P0 live voice authentication ceremony and its accessible alternatives.

**Release gate:** P0 must be interaction-complete and validated before P2 administration/configuration/management UIX is treated as delivery. P2 screens cannot be used to claim first-class authenticator support.

## 1. Mandate

Specify the complete product required for voice-biometric enrollment and authentication: consent, microphone/device readiness, sample capture, liveness/anti-spoofing, verification, evidence, lifecycle, retraining/replacement, revocation, deletion, recovery, policy, provider health, diagnostics, accessibility alternatives, and privacy. Capability remains gated until every dependency is production-ready.

## 2. Required screens

| Screen | Purpose |
|---|---|
| Eligibility/method chooser | Offer voice biometric only where policy, language, device, and consent allow |
| Privacy/informed consent | Explain voice processing, storage, sharing, retention, deletion, and alternatives |
| Microphone/device preflight | Check permission, device, noise, input level, and compatibility |
| OS/browser microphone permission | Platform-owned consent prompt |
| Enrollment introduction | Explain phrases, environment, liveness, retries, and accessibility |
| Enrollment capture | Record required samples inside approved verifier boundary |
| Quality/liveness feedback | Provide safe corrective guidance without exposing thresholds |
| Enrollment review/activation | Confirm profile, consent, recovery, and safe metadata |
| Login/step-up voice ceremony | Capture prompted/randomized speech or approved passive profile |
| Processing/wait | Validate liveness and match through server/verifier |
| Retry/cancel/noise/spoof/blocked | Handle adverse states safely |
| Result/next-step | Show completion, reduced evidence, or another required factor |
| Evidence detail | Show `vbm`, source, time, freshness, liveness class, purpose, limitations |
| Voice authenticator detail | Show status, consent, created/last-used, retrain/revoke/delete |
| Retraining/replacement | Create new approved template before retiring old where allowed |
| Recovery/fallback | Use another factor; voice failure must not lock out users with speech/accessibility differences |
| Deletion/privacy request | Revoke and track template deletion |
| Voice-biometric policy | Configure languages, profiles, liveness, age, scope, fallback, retention |
| Verifier/provider configuration | Configure models, keys, regions, health, and fail behavior |
| Fraud/liveness diagnostics | Show redacted outcome classes and provider drift |
| Native capture | Equivalent secure microphone and app-resume flow |
| Optional call integration | Complete voice capture over approved telephony profile without conflating `tel` |

## 3. Enrollment flow

1. Server confirms eligibility and alternatives.
2. Consent records purpose/version and explains withdrawal/deletion.
3. Preflight asks for microphone permission only after explicit action and checks environment/device.
4. Verifier returns safe prompts and sample count; UI captures through approved adapter.
5. Quality and liveness feedback permits bounded retries without revealing matcher internals.
6. Server receives signed enrollment result/template reference, not raw samples in general app state.
7. Activation records consent, profile/model/version, region, recovery, and notification.

## 4. Authentication flow

1. User selects voice method or step-up requests it.
2. Preflight confirms permission/device/environment.
3. Server issues randomized or transaction-bound prompt where profile requires it.
4. Approved adapter captures and sends directly to verifier boundary.
5. Server validates liveness, match result, prompt/transaction binding, freshness, replay, and policy.
6. Success emits `vbm`; failures offer bounded retry, another factor, or recovery without disclosing scores.

## 5. Screen behavior

- Never use a static phrase where replay resistance requires randomized content.
- Show recording state, elapsed/remaining guidance, stop/cancel, and privacy status clearly.
- Provide a text/visual equivalent for auditory instructions.
- Do not display match, liveness, or confidence scores to ordinary users.
- Distinguish background noise, microphone denied/unavailable, speech not detected, quality retry, suspected replay/spoof, and policy block safely.
- Do not claim `tel` merely because capture occurred during a phone call.

## 6. Lifecycle and privacy

- Detail shows status, verifier/profile, language, consent version, created/last-used, re-enrollment date, and events—not recordings/templates.
- Retraining/replacement requires recent authentication and explicit consent.
- Revocation stops authentication immediately.
- Deletion tracks pending/completed/failed verifier deletion with reference and notification.
- Last-factor deletion requires replacement/recovery.

## 7. States

Support ineligible, consent required/declined/withdrawn, permission required/denied/permanently denied, no microphone, excessive noise, enrollment ready/recording/processing/quality retry/liveness failure/completed, active, suspended, retraining, revoked, deletion pending/completed/failed, challenge ready/recording/processing/invalid/spoof suspected/blocked, provider outage, network interruption, policy changed, expired, success, and requires-next-step.

## 8. Components

Reuse universal ceremony, privacy, compatibility, evidence, lifecycle, danger, policy, audit, and result components.

Add `MicrophonePreflight`, `VoiceConsentRecord`, `RecordingControl`, `InputLevelIndicator` with nonvisual equivalent, `VoicePrompt`, `CaptureQualityGuidance`, `LivenessEvidenceSummary`, `BiometricDeletionStatus`, and approved web/native verifier adapters.

## 9. Data/API expectations

Server returns eligibility, consent text/version/status, capture profile, prompt, limits, ceremony state, safe quality/liveness result, evidence/provenance/freshness, lifecycle/deletion state, fallback, policy version, and audit reference.

Raw recordings, templates, feature vectors, match/liveness scores, model internals, and unrestricted device telemetry never enter generic frontend state, analytics, or logs.

## 10. Responsive, accessibility, and non-web

- Recording controls remain usable at narrow widths and high zoom.
- All audio guidance has textual equivalents; all visual level/progress indicators have accessible status.
- Offer another method for users unable/unwilling to speak or use a microphone.
- Native apps use secure audio APIs, suppress app-switcher exposure, and bind resume/upload to ceremony.
- Call integration supports hearing/speech relay alternatives and keeps channel confirmation separate.

## 11. Security and privacy

- Complete biometric/privacy review, consent, minimization, encryption, retention, deletion, regional processing, and alternative-method policy before launch.
- Bind capture/result to tenant, subject, ceremony, randomized prompt, purpose, verifier, nonce, and time.
- Prevent replay, synthesis/deepfake, template substitution, cross-subject match, downgrade, and provider callback spoofing.
- No recordings/templates in DOM, browser storage, URLs, analytics, logs, crash reports, support exports, or generic audit.

## 12. Analytics and audit

Analytics records eligibility, permission, safe capture outcome, retry, fallback, and completion—not audio or scores. Audit consent, enrollment, profile/model version, liveness/match decision class, evidence, retraining, revoke, deletion, recovery, provider/policy changes, and operator action.

## 13. Tests

- Consent, permission, enrollment, liveness, authentication, step-up, retry, fallback, retrain, revoke, deletion, and recovery pass.
- Noise, no speech, denied permission, replayed recording, synthetic/spoof input, stale prompt, wrong subject/tenant, provider outage, and policy change fail safely.
- Audio/template leakage tests cover all client and operational surfaces.
- Accessibility covers speech/hearing disabilities, nonvisual controls, native, zoom, contrast, and reduced motion.

## 14. Acceptance criteria

- Every web, native, verifier, lifecycle, privacy, recovery, policy, and diagnostics screen is complete.
- Voice biometrics remain distinct from telephone confirmation.
- Users have meaningful consent, alternatives, revocation, and deletion.
- `vbm` is emitted only from verified liveness/match evidence.
- Raw biometric material never enters general frontend state.

## 15. Dependencies

- Approved voice verifier/model and signed-result protocol.
- Liveness/anti-spoofing, consent, template lifecycle, and deletion services.
- Privacy/legal/regional approval and accessible alternative.
- Secure web/native audio capture adapters and optional telephony profile.

## References

- [AMR screen support matrix](../../amr-screen-support-matrix.md)
- [Universal authenticator ceremony brief](../uix-pairing-briefs/40-authenticator-ceremony-api-universal-authenticator-pages-uix.md)
- [Canonical AMR vocabulary](../../../pkgs/10-concrete/tigrbl-jose-concrete/src/tigrbl_jose_concrete/amr.py)
