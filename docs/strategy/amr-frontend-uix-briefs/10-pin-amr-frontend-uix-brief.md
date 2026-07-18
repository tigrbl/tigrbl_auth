# PIN AMR Frontend UIX Brief

- **AMR:** `pin`
- **Current delivery status:** Missing first-party PIN credential/verifier lifecycle
- **Delivery target:** Complete first-party PIN authenticator plus platform, key, card, and upstream PIN evidence adapters
- **Category:** Knowledge method or local authenticator unlock
- **Primary rule:** Do not claim `pin` when WebAuthn reports only user verification
- **Platforms:** Web and native first-party PIN, browser/OS WebAuthn, external security keys/cards, native device authentication, and trusted upstream adapters

## UIX delivery priority

**P0 — Actual authentication UIX (ship first):** PIN method selection → transaction-purpose confirmation → secure account-PIN entry or external device/card PIN handoff → submitting/processing → generic invalid/rate-limited/locked/blocked/forgotten states → fallback or reset/recovery handoff → success or next-factor result. First-party account PIN, native, security-key, and smart-card modes must remain clearly distinct. This is the release gate.

**P1 — Enrollment and user lifecycle:** first-party PIN creation/confirmation/activation, change/replacement, detail, suspension, compromise, removal, forgot/reset, and recovery; underlying external-device lifecycle stays with its owning authenticator.

**P2 — Administration and operations:** PIN policy, external evidence-source policy, administrative forced reset, device/provider health, audit, and diagnostics.

A PIN settings page is not sufficient. First-class delivery requires the complete P0 challenge and secure handoff experience before management tooling.

**Release gate:** P0 must be interaction-complete and validated before P2 administration/configuration/management UIX is treated as delivery. P2 screens cannot be used to claim first-class authenticator support.

## 1. Mandate

Deliver a complete first-party account PIN authenticator covering creation, confirmation, login, step-up, evidence, change, replacement, suspension, compromise, removal, reset, recovery, policy, audit, and native secure entry. Also support platform passkeys, roaming security keys, smart cards, native device unlock, and trusted federation without collecting their device/card PINs in application UI.

## 2. Modes

1. **Device-local PIN:** OS/platform unlock; app receives only authentication result.
2. **Authenticator PIN:** security key or smart-card middleware owns entry.
3. **Trusted upstream PIN:** accepted only through normalized provider evidence.
4. **First-party account PIN:** TIGRBL-owned credential, verifier, lifecycle, recovery, and policy defined by this brief.

## 3. Required screens

| Screen | Purpose |
|---|---|
| Passkey/security-key login | Start underlying authentication without promising PIN |
| Step-up chooser | Offer eligible key/card/native method |
| WebAuthn/device handoff | Invoke system-controlled prompt |
| Security-key/card instructions | Explain insert, touch, unlock, retry, and blocked device |
| Native device-auth screen | Invoke platform authentication API |
| Result/next-step | Show “User verified” unless `pin` provenance is trusted |
| Evidence detail | Show accepted PIN evidence source and limitations |
| Authenticator/key/card detail | Manage the underlying authenticator, not its PIN |
| Recovery/fallback | Use alternate method after forgotten/blocked device PIN |
| User-verification policy | Configure requirements without forcing modality claims |
| Device/provider configuration | Configure supported key/card/native profiles |
| Audit/diagnostics | Show redacted result/error class, never PIN or attempt oracle |
| First-party PIN introduction | Explain account scope, assurance limitations, policy, recovery, and alternatives |
| First-party PIN creation/confirmation | Create and verify a TIGRBL-owned account PIN securely |
| First-party PIN login/step-up | Challenge the server-owned PIN verifier |
| First-party PIN detail/change/replace | Manage status and replace without exposing verifier data |
| First-party PIN suspend/revoke/remove | Stop use with recent-authentication and last-factor safeguards |
| First-party PIN forgot/reset/recovery | Recover without disclosing or restoring the old PIN |
| First-party PIN policy/admin reset | Configure and govern PIN lifecycle without administrators viewing PINs |

## 4. End-to-end device/key flow

1. Server offers passkey, security key, card, or native-device authentication.
2. Pre-handoff copy says the device may request a PIN, biometric, touch, or another unlock method.
3. Explicit user action invokes WebAuthn/native/middleware.
4. The OS/device owns PIN entry, retries, lockout, and reset.
5. The application submits only the signed proof/result.
6. Server evidence determines whether the result supports `pin`, generic user verification, or insufficient evidence.
7. Forgotten/blocked PIN routes to device-vendor guidance plus an application-approved alternate method; the app never resets the device PIN.

## 5. First-party PIN flow

The first-party PIN authenticator requires all of the following:

1. Introduction explaining limited assurance and device/account scope.
2. PIN creation with server-defined length/format and confirmation.
3. Initial verification and recovery setup.
4. Challenge with enumeration-safe errors, attempt limits, rate limiting, and secure input.
5. Detail, change, replacement, suspension, compromise, removal, and reset.
6. Administrative policy, audit, notification, and last-factor safeguards.

PIN data uses a dedicated verifier contract and is never stored or validated in frontend code.

### First-party enrollment

1. Recent-authentication and eligibility checks open the introduction.
2. Server returns length/format, disallowed-pattern, attempt, reset, and app/purpose policy projections.
3. User creates and confirms the PIN through secure labeled inputs supporting paste where policy permits.
4. Client checks only confirmation equality; server owns acceptance, blocklists, sequence/repetition checks, history, and verifier creation.
5. Initial verification activates the credential and clears all fields.
6. Completion confirms recovery and sends a notification.

### First-party authentication

1. Server returns a bound PIN challenge with purpose, attempts, expiry, and safe fallback.
2. User submits through a secure field; duplicate submission is disabled.
3. Server verifies, rate limits, updates attempts, and returns generic invalid/locked/compromised/success state.
4. Success emits `pin` evidence and advances or completes the ceremony.

### Change, reset, and recovery

1. Change requires current PIN or policy-approved recent stronger authentication.
2. Replacement verifies and activates the new PIN before retiring the old verifier atomically.
3. Forgot/reset uses a bound recovery ceremony and never returns the old PIN.
4. Administrative reset creates a forced-reset state; administrators cannot choose or see a permanent PIN.
5. Removing the final usable authenticator is blocked without replacement/recovery.

## 6. Screen behavior

### Handoff and prompts

- Never render a fake OS, security-key, or smart-card PIN dialog.
- Do not request a device PIN in HTML fields.
- Provide textual device guidance that remains accurate across vendors.
- Map cancellation, PIN required, invalid PIN, retries low, blocked, device removed, middleware unavailable, and timeout to safe actions without exposing exact security counters unless the device UI owns them.

### Evidence detail

- Show `pin` for successful first-party PIN verification or trusted native/upstream evidence, with provenance.
- Otherwise show “User verified; verification method not disclosed.”
- Include provider/authenticator, time, freshness, purpose, policy result, and audit reference.
- Never show PIN length, value, retries, or device reset secrets.

### Policy

- Configure first-party PIN length/format, disallowed patterns, attempts, rate limits, lockout, compromise, history, reset, recovery, permitted apps/actions, freshness, and fallback.
- Configure trusted external PIN sources and blocked-device response separately.
- Simulation includes confirmation mismatch, invalid/forgotten/compromised PIN, attempts exhausted, reset artifact replay, modality unknown, blocked key/card, provider outage, and no fallback.

## 7. States

Support first-party not-enrolled, introduction, creation, confirmation mismatch, verification pending, active, invalid, rate limited, attempts exhausted, locked, compromised, change/replace pending, suspended, revoked, removed, reset requested/artifact invalid/expired/used, forced reset, recovery, policy changed, success, and requires-next-step. Also support awaiting system/device, PIN requested externally, cancellation, invalid/blocked externally, device unavailable/removed, middleware unavailable, timeout, modality unknown, and stale/untrusted external evidence.

## 8. Components

Reuse `CeremonyShell`, `PasskeyPrompt`, `SecurityKeyPrompt`, `CompatibilityNotice`, `AuthenticationContextSummary`, `EvidenceFreshnessBadge`, `MethodSwitchMenu`, and lifecycle/policy components.

Add `SecurePinField`, `PinRequirements`, `PinCreationConfirmation`, `PinResetArtifactState`, `PinLifecyclePanel`, `ExternalPinGuidance`, `VerificationMethodQualifier`, `DeviceBlockedHelp`, and native/middleware adapter error mapping.

## 9. Data/API expectations

The server returns first-party PIN credential status, policy projection, challenge/reset ceremony state, attempts/lockout projection, normalized AMR/provenance, underlying external method, user-verification result, device/provider projection, safe error, policy satisfaction, allowed fallback, and audit reference. The client never receives verifier/hash/history data, validates a PIN, or receives a device/authenticator PIN.

## 10. Responsive, accessibility, and non-web

- Guidance fits narrow screens and high zoom without obscuring system prompts.
- Focus returns from external prompts to a clear result/error heading.
- Device instructions support keyboard, screen reader, switch control, forced colors, and reduced motion.
- Native apps use secure platform authentication APIs and bind resume to the ceremony.
- CLI diagnostics test device/provider availability and public proof only; they never accept PIN values as command arguments.

## 11. Security

- First-party account PIN entry exists transiently in the secure application field until submission and is verified only by the server credential boundary; device/card PIN entry remains inside the external device boundary.
- Prevent prompt spoofing, replay, downgrade to generic password fields, cross-account binding, and unsafe fallback.
- Do not expose retry counters or device identifiers beyond approved projections.
- Require recent authentication for underlying authenticator removal/replacement.
- No PINs in persistent DOM/debug markup, storage, URLs, clipboard telemetry, analytics, logs, screenshots, crash reports, or support exports; secure fields clear on submit result, navigation, timeout, and unmount.

## 12. Analytics and audit

Analytics records handoff, device/provider class, safe outcome, fallback, and completion. Audit accepted evidence, provenance, blocked-device result, underlying authenticator lifecycle, policy version, and administrative changes—never PIN values.

First-party audit also covers creation, activation, verification outcome, lockout, change, replacement, suspension, compromise, removal, reset, recovery, and administrator-forced reset.

## 13. Tests

- Generic WebAuthn UV does not render `pin`.
- First-party creation, confirmation, initial verification, login, step-up, change, replacement, suspend, revoke, remove, forgot/reset, forced reset, and recovery pass end to end.
- Invalid PIN, attempts/rate-limit/lockout, compromise, reset replay/expiry/use, concurrent replacement, last-factor removal, and policy change fail safely.
- Trusted native/upstream evidence does.
- App UI never captures security-key/card/device PIN.
- Cancel, invalid/blocked external PIN, device removal, middleware outage, timeout, fallback, and resume work.
- Spoofing, replay, cross-tenant, policy change, and telemetry leakage tests pass.
- Native, browser, accessibility, zoom, and device-instruction tests pass.

## 14. Acceptance criteria

- All first-party enrollment, authentication, evidence, lifecycle, reset, recovery, policy, administration, and native screens are complete, alongside device/key/card adapters.
- PIN modality is never guessed.
- Device PIN reset remains outside application UI.
- First-party PIN is fully implemented rather than deferred behind an optional future scope.

## 15. Dependencies

- Evidence source capable of distinguishing PIN from generic user verification.
- WebAuthn/native/card middleware adapters.
- Approved external-device help content.
- First-party PIN credential, verifier, policy, attempts/lockout, lifecycle, reset, recovery, notification, and audit contracts.

## References

- [AMR screen support matrix](../../amr-screen-support-matrix.md)
- [Universal authenticator ceremony brief](../uix-pairing-briefs/40-authenticator-ceremony-api-universal-authenticator-pages-uix.md)
- [Canonical AMR vocabulary](../../../pkgs/10-concrete/tigrbl-jose-concrete/src/tigrbl_jose_concrete/amr.py)
