# One-Time Password AMR Frontend UIX Brief

- **AMR:** `otp`
- **Current delivery status:** Partial; provider and generic code screen exist, full TOTP product does not
- **Delivery target:** Complete first-party OTP/TOTP enrollment, verification, lifecycle, recovery, policy, and operations product
- **Category:** Possession factor
- **Primary profile:** TOTP; HOTP and delivered OTP require separate capability descriptors
- **Platforms:** Web, native, authenticator app, account/admin management

## UIX delivery priority

**P0 — Actual authentication UIX (ship first):** OTP method selection → challenge introduction → code entry with paste/autofill → submitting → invalid/replayed/expired/drift/rate-limited/attempts-exhausted states → resend only for delivered profiles → switch/fallback/recovery → success or next-factor result. Sign-in and step-up parity are the release gate.

**P1 — Enrollment and user lifecycle:** TOTP introduction, QR/manual-secret reveal, initial verification, naming, recovery confirmation, detail, replacement/rotation, suspension, revocation, reset, and recovery.

**P2 — Administration and operations:** OTP profile policy, replay/drift/attempt configuration, user posture/reset, provider health for delivered profiles, audit, and diagnostics.

Do not lead with QR enrollment or policy administration. The first-class authenticator is primarily the code challenge users encounter during actual authentication.

**Release gate:** P0 must be interaction-complete and validated before P2 administration/configuration/management UIX is treated as delivery. P2 screens cannot be used to claim first-class authenticator support.

## 1. Mandate

Deliver a complete OTP product covering enrollment, initial verification, sign-in, step-up, evidence, lifecycle, rotation, recovery, administration, native autofill, and audit. Replace copy that assumes every OTP is “sent to your device.” The server owns OTP profile, secret generation, digits, period/counter, algorithm, replay, drift, attempts, and expiry.

## 2. Required screens

| Screen | Purpose |
|---|---|
| Login/method chooser | Offer named OTP method when eligible |
| OTP challenge/MFA page | Enter server-described code |
| Step-up challenge | Reuse OTP adapter in bound sensitive-action ceremony |
| Enrollment introduction | Explain authenticator app, security, recovery, and prerequisites |
| QR/manual secret reveal | Display the seed once with privacy controls |
| Initial-code verification | Prove setup before activation |
| Authenticator naming | Assign a safe user-visible label |
| Recovery confirmation | Ensure another path exists |
| Enrollment completion | Show activation and next actions |
| Retry/drift/expiry/rate-limit | Handle challenge failure safely |
| Evidence detail | Show OTP profile, time, freshness, purpose, and result |
| Authenticator detail | Show status, created/last-used, label, replace/remove |
| Replace/rotate | Enroll replacement before invalidating prior secret |
| Suspend/revoke/remove | Govern compromise and last-factor handling |
| Recovery reset | Recover without revealing or reusing the old seed |
| Tenant OTP policy | Configure profiles, attempts, replay, grace, and fallback |
| User posture/admin reset | Govern help-desk reset/re-enrollment |
| Audit/diagnostics | Show redacted challenge, replay, drift, and lockout outcomes |
| Authenticator-app screen | External app stores seed and generates codes |
| Native OTP entry/autofill | Secure entry and OS one-time-code integration |

## 3. Enrollment flow

1. User selects TOTP from Add Authenticator after recent-authentication checks.
2. Introduction states that codes are generated in an authenticator app and are not messages sent by TIGRBL.
3. Server creates a bound, expiring enrollment and returns QR/manual secret exactly once.
4. UI provides QR, manual key, issuer/account labels, copy control, and explicit exposure warning.
5. User enters an initial code; server validates window, replay, and enrollment binding.
6. User names the authenticator and confirms recovery.
7. Activation invalidates seed-display access and clears all frontend copies.
8. Completion offers another factor and recovery-code setup.

## 4. Challenge flow

1. Server returns digit count, input mode, expiry, attempts, and safe method label.
2. OTP input supports full-code paste and platform autofill.
3. Submission locks duplicate actions and clears code after the response as policy requires.
4. Generic invalid response does not reveal drift or near-match initially.
5. Safe clock guidance may appear only after configured failure thresholds.
6. Replay, expired code, rate limit, attempts exhausted, and suspended factor map to distinct safe states.
7. Success produces `otp` evidence and continues or requests another factor.

## 5. Screen behavior

### Secret reveal

- Treat QR and manual secret as equivalent secrets.
- Blur/cover on background, print, screen sharing, and inactivity where platform support permits.
- Clear on acknowledgment, timeout, navigation, refresh, error boundary, and unmount.
- Never put secret data in URLs, analytics, logs, DOM attributes, hidden content, or support capture.
- Do not allow re-reveal after activation; replacement creates a new enrollment.

### OTP input

- Persistent visible label; segmented visual inputs may use one semantic input.
- Server descriptor controls six/eight digits and accepted character set.
- Allow paste, autofill, keyboard entry, correction, and screen readers.
- Avoid countdown announcements every second.

### Lifecycle

- Detail shows label, status, profile, created, verified, last used, and event history—never seed.
- Replacement uses overlap only until the new factor is verified, then explicitly retires the old one.
- Removing the last usable factor is blocked or requires governed recovery.

### Administration

- Configure allowed OTP profiles, algorithms, digits, periods/windows, attempts, rate limits, replay store, grace, app scope, recovery, and enrollment requirements.
- Simulation covers clock drift, replay, provider/storage outage, no recovery, and mass re-enrollment.

## 6. States

Support not enrolled, enrollment pending, secret displayed, verification pending, active, suspended, compromised, replacement required, revoked, challenge ready, submitting, invalid, replayed, expired, rate limited, attempts exhausted, clock mismatch guidance, cancelled, policy changed, recovery only, success, and requires-next-step.

## 7. Components

Reuse `CeremonyShell`, `OtpInput`, `QrEnrollmentPanel`, `ManualSecretField`, `OneTimeSecretReveal`, `ChallengeCountdown`, `AuthenticatorDetailPanel`, `RecoveryImpactNotice`, and policy/audit primitives.

Add `OtpProfileSummary`, `SecretExposureShield`, `OtpEnrollmentProgress`, `OtpDriftGuidance`, and secure native autofill adapter.

## 8. Data/API expectations

The server owns enrollment/challenge IDs, secret issuance, QR/manual projection, profile, digits, algorithm, period/counter, attempts, expiry, drift/replay decisions, lifecycle, policy, next step, safe errors, and audit reference. The frontend never persists the seed or determines validity.

## 9. Responsive, accessibility, and non-web

- QR and manual key stack cleanly; manual setup remains usable when camera scanning is unavailable.
- At 200% zoom the secret, warning, copy action, and acknowledgment remain in logical order.
- Authenticator-app deep links are optional and must not expose the seed to unapproved handlers.
- Native apps use secure fields, one-time-code autofill, app-switcher privacy, and ceremony-bound resume.
- Screen readers receive one labeled code input and concise status announcements.

## 10. Security

- Seed is display-once, short-lived, tenant/subject/enrollment bound, and never recoverable after activation.
- Prevent replay, race conditions, brute force, enrollment fixation, cross-account binding, and clock-oracle leakage.
- Require recent authentication for add/replace/remove/reset.
- Notify factor changes and invalidate affected sessions according to policy.

## 11. Analytics and audit

Analytics record stage, safe error class, autofill/paste capability if privacy-approved, fallback, and completion—never codes or seeds. Audit enrollment, verification, replay rejection, challenge outcome, suspension, replacement, removal, recovery, reset, and policy changes.

## 12. Tests

- QR/manual enrollment, initial verification, naming, recovery confirmation, challenge, step-up, replacement, revoke, and reset pass.
- Secrets clear on every exit and never appear in telemetry/storage/URLs/snapshots.
- Replay, drift, window boundaries, duplicate submission, rate limit, concurrency, policy change, and cross-tenant cases fail safely.
- Paste, autofill, screen reader, mobile keyboard, zoom, and no-camera/manual setup pass.

## 13. Acceptance criteria

- All 20 screen types above are implemented or explicitly capability-gated.
- OTP copy accurately distinguishes generated versus delivered codes.
- Enrollment secrets are one-time and never recoverable from frontend state.
- Replay and attempts are server controlled.
- Users can recover, replace, and inspect OTP without seed exposure.
- Administrators can safely configure and simulate policy.

## 14. Dependencies

- TOTP secret issuer/verifier and replay store.
- Enrollment/challenge persistence and lifecycle APIs.
- Recovery, notification, and admin reset authority.
- Native autofill and approved authenticator-app handoff profiles.

## References

- [AMR screen support matrix](../../amr-screen-support-matrix.md)
- [Universal authenticator ceremony brief](../uix-pairing-briefs/40-authenticator-ceremony-api-universal-authenticator-pages-uix.md)
- [MFA product maturity](../../mfa-focus.md)
- [Canonical AMR vocabulary](../../../pkgs/10-concrete/tigrbl-jose-concrete/src/tigrbl_jose_concrete/amr.py)
