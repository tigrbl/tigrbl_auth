# Telephone Confirmation AMR Frontend UIX Brief

- **AMR:** `tel`
- **Current delivery status:** Missing; no voice-call provider or verified telephone lifecycle exists
- **Delivery target:** Complete first-party phone enrollment, telephony/IVR verification, lifecycle, recovery, policy, fraud, accessibility, and operations product
- **Category:** Out-of-band telephone channel confirmation
- **Assurance posture:** Lower assurance; distinct from voice biometrics
- **Platforms:** Web, native, incoming phone call/IVR, tenant/platform administration, delivery/fraud diagnostics

## UIX delivery priority

**P0 — Actual authentication UIX (ship first):** Telephone method selection with masked destination → call confirmation → queued/ringing/connected wait → IVR transaction context and code/approval → callback correlation → busy/no-answer/voicemail/failed/invalid/expired/rate-limited states → bounded call-again → fallback/recovery → success or next-factor result. Web/native plus IVR interaction is the release gate.

**P1 — Enrollment and user lifecycle:** phone entry, ownership call, activation/naming, detail, replacement, suspension, removal, recovery, and accessible alternative setup.

**P2 — Administration and operations:** provider/routing/caller-ID/locale policy, IVR content, fraud/rate limits, regional/quiet-hours rules, health, cost, audit, and diagnostics.

Telephony administration is secondary. The first-class authenticator is the live P0 call and IVR authentication journey.

**Release gate:** P0 must be interaction-complete and validated before P2 administration/configuration/management UIX is treated as delivery. P2 screens cannot be used to claim first-class authenticator support.

## 1. Mandate

Deliver complete phone enrollment, ownership verification, call challenge, login/step-up, IVR interaction, evidence, lifecycle, replacement, recovery, provider configuration, fraud/rate-limit controls, accessibility, and audit. `tel` proves telephone-channel participation; it does not prove voice biometrics (`vbm`).

## 2. Required screens and interactions

| Screen/interaction | Purpose |
|---|---|
| Telephone method chooser | Offer only when enrolled, eligible, available, and allowed |
| Phone enrollment introduction | Explain call behavior, costs, accessibility, privacy, and alternatives |
| Phone entry/country selection | Collect normalized destination and consent |
| Ownership call confirmation | Verify number through a bound call |
| Enrollment completion/naming | Activate masked phone authenticator |
| Call challenge start | Confirm masked destination and initiate call |
| Calling/waiting screen | Show queue/ringing/connected/unknown state and expiry |
| IVR code or approval interaction | Complete confirmation on phone |
| Web/native code entry | Enter code heard during the call where profile requires it |
| Retry/callback/resend | Govern another call without abuse |
| Busy/no-answer/voicemail/failed | Offer safe retry or alternate method |
| Rate-limited/blocked/expired | Handle fraud and attempt controls |
| Step-up ceremony | Bind telephone confirmation to sensitive action |
| Evidence detail | Show channel, time, masked destination, provider, freshness, limitations |
| Phone authenticator detail | Show status, verified/last-used dates, replace/remove |
| Replacement/removal | Verify replacement and protect last-factor access |
| Recovery | Govern telephone recovery and reduced assurance |
| Telephone policy | Configure regions, purposes, IVR profile, attempts, fallback |
| Provider/routing configuration | Configure caller IDs, locale, routes, failover, templates |
| Call health/fraud diagnostics | Show queue, completion, abandonment, abuse, and cost |
| Native call-state handoff | Resume app ceremony after call interaction |

## 3. Enrollment flow

1. User selects telephone after recent-authentication checks.
2. Introduction explains incoming call, caller identity caveats, required interaction, accessibility options, and alternatives.
3. Phone entry validates region and displays normalized/masked confirmation.
4. Explicit action starts a bound enrollment call.
5. User completes IVR code/approval; server validates destination, ceremony, expiry, attempts, and replay.
6. Completion activates the phone, notifies existing channels, and recommends a stronger/recovery factor.

## 4. Authentication flow

1. Method chooser shows masked destination and availability.
2. Call-start screen describes transaction purpose and expiry.
3. Server initiates call; waiting screen reflects safe provider status.
4. Phone interaction states the transaction context and requires code/confirmation resistant to blind approval.
5. Server correlates provider callback and ceremony.
6. Success produces `tel`; failures offer bounded retry, alternate method, or recovery.

## 5. Screen and IVR behavior

- Never expose full phone number or account details.
- Do not treat voicemail delivery as successful confirmation.
- IVR supports language selection, repeat, slower playback, keypad alternatives, and accessible timing.
- Transaction confirmation includes purpose/context sufficient to resist approval confusion.
- Web waiting page does not require focus or rapid polling and supports cancel.
- Retry/call-again is server-controlled; changing destination requires a separate lifecycle flow.
- Copy never calls telephone confirmation voice biometric or phishing resistant.

## 6. Lifecycle and administration

- Detail shows safe label, masked number, region, verified/created/last-used dates, status, and events.
- Replacement verifies new number before retiring old; notify both where safe.
- Policy controls regions, purposes, call profiles, code/approval mode, attempts, duration, rate limits, quiet hours, fallback, recovery use, and assurance.
- Provider config controls approved caller IDs, locale/voice, routes, callback verification, failover, and outage behavior.

## 7. States

Support ineligible, unsupported region, consent required, call ready, queued, ringing, connected, IVR active, awaiting code/approval, completed, busy, no answer, voicemail, rejected, failed, callback delayed, invalid interaction, expired, replayed, rate limited, blocked, provider outage, active, suspended, replacement pending, revoked, recovery only, policy changed, success, and requires-next-step.

## 8. Components

Reuse `CeremonyShell`, `OtpInput` when applicable, `ChallengeCountdown`, `MaskedDestination`, `AuthenticatorDetailPanel`, policy/audit/result components.

Add `CallStartConfirmation`, `CallProgress`, `IvrInstructionSummary`, `CallAgainControl`, `TelephoneAssuranceNotice`, `CallProviderHealth`, and native call-state adapter.

## 9. Data/API expectations

Server owns normalized destination, mask, provider/routing, call content/profile, send/start, state, callback validation, code/approval, attempts, expiry, fraud decisions, lifecycle, and audit. Frontend never receives provider credentials, recordings, full destinations outside authorized enrollment, carrier/fraud internals, or callback secrets.

## 10. Responsive, accessibility, and non-web

- Waiting/status screens support screen readers without noisy polling.
- IVR works for users with hearing, speech, motor, cognitive, and language needs through repeat, keypad, text-relay/TDD or alternative-factor policy.
- Native apps resume the original ceremony after phone interaction and reject stale returns.
- Web code entry supports paste and accessible single-field semantics.

## 11. Security

- Bind calls/callbacks/interactions to tenant, subject, destination, ceremony, transaction purpose, nonce, and time.
- Verify provider callbacks and prevent replay, call pumping, enumeration, destination swap, voicemail acceptance, and blind approval.
- Rate limit across subject, destination, provider, tenant, network/device context, and ceremony.
- Do not expose full numbers, codes, recordings, or fraud data in telemetry/URLs/support UI.

## 12. Analytics and audit

Analytics records region class, call state/outcome, duration bucket, retry, fallback, and completion without full number. Audit enrollment, call start/callback, IVR outcome, replay/rate limit, replacement, removal, recovery, provider route, policy, and administrator action.

## 13. Tests

- Enrollment, ownership verification, login, step-up, IVR code/approval, retry, replacement, removal, recovery, and failover pass.
- Busy, no-answer, voicemail, delayed/spoofed callback, invalid/expired interaction, pumping, destination swap, and outage fail safely.
- Accessibility covers IVR alternatives and hearing/speech limitations.
- Full destinations, codes, callback secrets, and recordings never leak.

## 14. Acceptance criteria

- All web, native, IVR, lifecycle, policy, provider, and diagnostic interactions are complete.
- `tel` is clearly distinct from `sms` and `vbm`.
- Calls carry transaction context and never accept voicemail as proof.
- Users always have accessible retry/fallback/recovery paths.
- Provider callbacks and rate limits resist fraud and replay.

## 15. Dependencies

- Verified phone lifecycle and telephony provider abstraction.
- Accessible IVR content/profile and callback verification.
- Fraud/rate-limit, regional, consent, quiet-hours, and recovery policy.
- Native call-state and deep-link integration.

## References

- [AMR screen support matrix](../../amr-screen-support-matrix.md)
- [Universal authenticator ceremony brief](../uix-pairing-briefs/40-authenticator-ceremony-api-universal-authenticator-pages-uix.md)
- [Canonical AMR vocabulary](../../../pkgs/10-concrete/tigrbl-jose-concrete/src/tigrbl_jose_concrete/amr.py)
