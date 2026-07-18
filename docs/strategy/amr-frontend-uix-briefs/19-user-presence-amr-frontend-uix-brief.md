# User-Presence AMR Frontend UIX Brief

- **AMR:** `user`
- **Current delivery status:** Partial; WebAuthn advertises user presence statically rather than per-ceremony evidence
- **Delivery target:** Complete first-party user-presence ceremony, evidence, lifecycle integration, policy, device guidance, and diagnostics product
- **Category:** Authenticator interaction evidence
- **Primary rule:** User presence must come from a verified ceremony flag/result, never from authenticator type alone
- **Platforms:** WebAuthn web/native, roaming security keys, managed hardware keys, evidence/admin/diagnostic screens

## UIX delivery priority

**P0 — Actual authentication UIX (ship first):** presence-capable method selection → transaction-purpose confirmation → browser/OS/device handoff → insert/touch/presence guidance → assertion processing → presence-absent/UV-additionally-required/cancelled/timeout/device-removed/transport-failure states → fallback/recovery → success or next-factor result. This actual physical-interaction ceremony is the release gate.

**P1 — Enrollment and user lifecycle:** underlying passkey/security-key/managed-key enrollment, authenticator detail, replacement, removal, and alternate-method recovery.

**P2 — Administration and operations:** presence-versus-verification policy, managed-key profiles, device capability, audit, conformance, and diagnostics.

Presence policy and evidence pages are secondary. `user` becomes first class only when the P0 physical interaction and all failure states work across browser, native, and external devices.

**Release gate:** P0 must be interaction-complete and validated before P2 administration/configuration/management UIX is treated as delivery. P2 screens cannot be used to claim first-class authenticator support.

## 1. Mandate

Deliver complete user-presence experiences for passkeys, security keys, managed hardware keys, and trusted upstream/native evidence. The UI must guide required physical interaction, handle cancellation/device failures, display evidence freshness, and govern policy without claiming user verification, biometrics, identity proofing, or hardware backing solely from presence.

## 2. Required screens

| Screen | Purpose |
|---|---|
| Passkey/security-key login | Start an eligible assertion |
| Step-up chooser | Offer presence-capable methods when policy requires them |
| Compatibility/preflight | Check browser/platform/transport support |
| Enrollment ceremony | Register underlying authenticator and verify supported behavior |
| Presence assertion ceremony | Invoke OS/device proof requiring presence |
| Insert/touch guidance | Explain external-key physical interaction |
| Native platform prompt | Perform system-owned interaction |
| Retry/cancel/timeout/device removed | Recover safely from physical/device states |
| Result/next-step | Show completion or additional user-verification/factor requirement |
| Evidence detail | Show presence result, time, freshness, authenticator, purpose, provenance |
| Authenticator detail | Manage underlying key/passkey lifecycle |
| Recovery/fallback | Use another authenticator if presence cannot be completed |
| Presence/UV policy | Configure when presence is sufficient versus verification required |
| Managed-key profile | Configure applicable client/workload human-presence requirements |
| Ceremony diagnostics | Show flag/result classes, transport, timeout, and safe device errors |
| Native/CLI device test | Validate supported public interaction profiles without secrets |

## 3. Enrollment flow

1. User selects passkey/security key/managed key.
2. Introduction explains required touch/presence and distinguishes it from user verification.
3. Explicit action invokes platform/device registration.
4. Device owns touch, insertion, PIN/biometric, and transport prompts.
5. Server validates registration and records supported/verified evidence projections.
6. Completion manages the authenticator as a key/passkey; `user` is emitted only on qualifying authentication ceremonies, not enrollment naming alone.

## 4. Authentication flow

1. Server supplies assertion options and presence policy.
2. UI gives safe device-specific guidance from the capability descriptor.
3. Browser/native/device performs assertion after explicit action.
4. Server validates UP flag/result, challenge, origin/RP/profile, signature, counter/replay, and policy.
5. Accepted evidence emits `user`; missing presence can retry, switch, or require another method.
6. If policy requires user verification, presence alone is shown as insufficient rather than failed identity.

## 5. Screen behavior

- “Touch your security key” is used only for a known compatible transport/device; otherwise use generic “Follow your device’s instructions.”
- Do not say “biometric verified,” “PIN verified,” or “identity verified” from presence alone.
- Do not automatically relaunch prompts after cancel, refresh, or timeout.
- External-device guidance supports insertion, touch, keep connected, removal, blocked, and unsupported states.
- Result/evidence distinguishes user present, user verified, modality unknown, and evidence unavailable.

## 6. Policy and evidence

- Evidence detail shows authenticator/profile, ceremony purpose, presence result, authentication time, freshness, UP/UV distinction, properties, policy result, and audit reference.
- Policy editor separates presence required, user verification required, phishing resistance, hardware backing, authentication age, app/action scope, fallback, and recovery.
- Simulation covers presence absent, UV present, device cancellation, transport failure, stale evidence, and provider outage.

## 7. States

Support eligibility loading, ready, awaiting OS/device, insert, touch, processing, presence absent, user verification additionally required, cancelled, timeout, device removed, transport unavailable, unsupported environment, invalid assertion, replay, policy changed, expired, blocked, success, and requires-next-step.

## 8. Components

Reuse `CeremonyShell`, `PasskeyPrompt`, `SecurityKeyPrompt`, `CompatibilityNotice`, `AuthenticatorDetailPanel`, `AuthenticationContextSummary`, `EvidenceFreshnessBadge`, and shared result/failure components.

Add `PresenceRequirementNotice`, `PhysicalInteractionGuide`, `PresenceEvidenceSummary`, `UpUvComparison`, and browser/native/device adapter result mapping.

## 9. Data/API expectations

Server returns underlying authenticator/profile, ceremony state, presence requirement/result, user-verification result, transport guidance projection, evidence time/freshness, policy satisfaction, fallback, safe errors, and audit reference. The client cannot set presence flags or derive `user` from method type.

## 10. Responsive, accessibility, and non-web

- Instructions use text plus optional approved imagery and work without motion/sound/color.
- Focus returns from OS prompts and status changes are announced sparingly.
- External-key steps support motor and visual accessibility and adequate time.
- Native apps use platform APIs and bind app resume to ceremony.
- CLI/device tests report public capability and redacted outcomes, not private proofs or PINs.

## 11. Security

- Bind assertion to tenant, subject, credential, challenge, origin/RP/profile, purpose, ceremony, and time.
- Prevent replay, cross-account binding, downgrade from UV to UP, transport confusion, and synthetic client presence claims.
- Require explicit interaction before prompts.
- Do not log raw assertions, credential IDs, device identifiers, or private material.

## 12. Analytics and audit

Analytics records prompt, transport class, safe outcome, fallback, and completion. Audit accepted/rejected presence, UP/UV result, authenticator/profile, policy version, ceremony purpose, replay rejection, lifecycle and admin changes.

## 13. Tests

- `user` appears only when validated presence evidence is true.
- Authenticator type alone never emits/displays it.
- UP and UV are presented and governed separately.
- Insert/touch/cancel/timeout/device removal/transport failure/replay/policy change recover safely.
- Accessibility, external-device, browser/native resume, cross-tenant, and prompt-loop tests pass.

## 14. Acceptance criteria

- All login, step-up, enrollment, external-device, evidence, lifecycle, recovery, policy, and diagnostic screens are complete.
- Presence is evidence-derived per ceremony.
- Copy never overclaims biometric modality, user verification, hardware backing, or identity proof.
- Users can complete or safely exit every physical interaction state.

## 15. Dependencies

- Evidence-driven WebAuthn/managed-key UP and UV contracts.
- Browser/native/device adapters and capability descriptors.
- Presence-versus-verification policy model.
- Authenticator lifecycle and fallback/recovery APIs.

## References

- [AMR screen support matrix](../../amr-screen-support-matrix.md)
- [Universal authenticator ceremony brief](../uix-pairing-briefs/40-authenticator-ceremony-api-universal-authenticator-pages-uix.md)
- [Canonical AMR vocabulary](../../../pkgs/10-concrete/tigrbl-jose-concrete/src/tigrbl_jose_concrete/amr.py)
