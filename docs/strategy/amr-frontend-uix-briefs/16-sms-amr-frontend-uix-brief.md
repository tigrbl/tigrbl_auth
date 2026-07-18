# SMS AMR Frontend UIX Brief

- **AMR:** `sms`
- **Current delivery status:** Missing; no mature SMS provider, phone lifecycle, or anti-abuse flow
- **Delivery target:** Complete first-party phone enrollment, SMS delivery, OTP verification, lifecycle, recovery, policy, fraud, and operations product
- **Category:** Delivered OTP/channel confirmation
- **Assurance posture:** Lower assurance; not phishing resistant
- **Platforms:** Web, native mobile, phone messaging app, tenant/platform administration, provider diagnostics

## UIX delivery priority

**P0 — Actual authentication UIX (ship first):** SMS method selection with masked destination → send confirmation → queued/delivery-wait state → code entry with paste/autofill → submitting → delayed/failed/invalid/replayed/expired/rate-limited/blocked states → bounded resend → switch/fallback/recovery → success or next-factor result. Sign-in and step-up are the release gate.

**P1 — Enrollment and user lifecycle:** phone entry/normalization, ownership verification, activation/naming, detail, replacement, suspension, removal, recovery, and stronger-factor guidance.

**P2 — Administration and operations:** regional/provider/routing policy, templates, anti-abuse/fraud controls, delivery health/failover, cost, audit, and diagnostics.

Provider dashboards and phone management are secondary. The first-class authenticator is the P0 send/wait/code/failure authentication experience.

**Release gate:** P0 must be interaction-complete and validated before P2 administration/configuration/management UIX is treated as delivery. P2 screens cannot be used to claim first-class authenticator support.

## 1. Mandate

Deliver complete phone enrollment, ownership verification, SMS challenge, sign-in/step-up, evidence, lifecycle, replacement, recovery, policy, provider health, fraud controls, audit, native autofill, and delivery-state experiences. Distinguish the `sms` channel from the `otp` code method; successful SMS OTP may legitimately emit both when server evidence supports it.

## 2. Required screens

| Screen | Purpose |
|---|---|
| SMS method option | Offer only when enrolled, eligible, available, and policy-approved |
| Phone enrollment introduction | Explain assurance, messaging costs, privacy, recovery, and alternatives |
| Phone entry/country selection | Collect normalized destination with clear region handling |
| Ownership-verification send | Confirm masked destination before delivery |
| Enrollment code challenge | Verify phone ownership |
| Enrollment completion/naming | Activate safe phone label and recovery guidance |
| SMS login/MFA challenge | Send and enter code for authentication |
| Resend/change destination | Enforce server timers and prevent unsafe destination mutation |
| Delivery delayed/failed | Offer retry, alternate provider/method, or support |
| Invalid/expired/rate-limited/blocked | Handle code and abuse controls safely |
| Step-up ceremony | Use SMS only when policy permits its assurance |
| Evidence detail | Show channel, time, freshness, masked destination, provider class, limitations |
| Phone authenticator detail | Show masked number, status, verified/last-used dates, replace/remove |
| Phone replacement | Verify new number before retiring old one |
| Recovery | Govern phone recovery and reduced-assurance outcomes |
| Tenant SMS policy | Configure countries, apps, purposes, attempts, resend, fallback, assurance |
| Provider configuration | Configure sender, routing, templates, regional providers, failover |
| Provider health/delivery diagnostics | Monitor queue, receipts, latency, failures, fraud, cost |
| Abuse/security event detail | Show redacted sends, failures, velocity, and block actions |
| Native OTP autofill | Consume platform SMS-code APIs safely |
| Phone messaging screen | External receipt and code viewing |

## 3. Enrollment flow

1. User selects SMS after recent-authentication and policy checks.
2. Introduction states SMS risks and recommends stronger methods.
3. Phone entry uses explicit country/region, normalization preview, and consent/communication notice.
4. Server validates eligibility and returns masked destination plus send action.
5. Explicit send creates a bound, expiring code and server-controlled resend timer.
6. User enters code using paste/autofill; server verifies attempts, expiry, replay, and destination binding.
7. Completion activates the number, sends change notification, and prompts for recovery/stronger factor.

## 4. Authentication flow

1. Method chooser shows masked destination and provider availability.
2. Challenge screen confirms destination before explicit send unless policy pre-sends safely.
3. Waiting screen shows delivery in progress, resend eligibility, expiry, change-method, and cancel.
4. Code submission returns generic invalid, expired, replayed, rate-limited, or blocked state.
5. Success produces normalized `sms` and, where applicable, `otp` evidence.
6. Delivery failure/provider outage offers another method without exposing provider internals.

## 5. Screen behavior

- Mask numbers consistently and resist account enumeration.
- Do not let users change the destination inside an active authentication ceremony.
- Resend is server-controlled and clearly explains that prior codes may become invalid.
- Code input uses one semantic field with paste and `one-time-code` autofill.
- Copy does not call SMS secure or phishing resistant.
- Recovery through SMS is labeled reduced assurance where applicable.

## 6. Lifecycle and administration

- Detail shows safe label, masked number, region, verified/created/last-used dates, status, and event history.
- Replacement verifies the new number before retirement and notifies the old channel where safe.
- Removal requires recent authentication and last-factor safeguards.
- Policy controls countries/regions, provider routing, app/purpose scope, attempts, resend, rate limits, SIM-change/porting signals if available, fallback, recovery use, and assurance.
- Provider health separates accepted, queued, delivered, undelivered, rejected, delayed, and unknown states.

## 7. States

Support ineligible, unsupported country, invalid number, consent required, verification pending, send ready, queued, delivered/unknown, delayed, failed, code ready, invalid, expired, replayed, rate limited, resend unavailable/available, destination blocked, provider outage, active, suspended, compromised, replacement pending, revoked, recovery only, policy changed, success, and requires-next-step.

## 8. Components

Reuse `CeremonyShell`, `OtpInput`, `ChallengeCountdown`, `AuthenticatorMethodPicker`, `AuthenticatorDetailPanel`, `RecoveryImpactNotice`, and policy/audit components.

Add `PhoneNumberField`, `CountryAvailabilityNotice`, `MaskedDestination`, `SmsSendConfirmation`, `DeliveryStatus`, `ResendControl`, `SmsAssuranceNotice`, and native autofill adapter.

## 9. Data/API expectations

The server owns normalized destination, masking projection, provider routing, templates, send, code, attempts, resend, expiry, delivery status, fraud/risk decisions, lifecycle, policy, and audit. Frontend never receives provider credentials, full destinations outside authorized enrollment, code hashes, carrier intelligence, or fraud internals.

## 10. Responsive, accessibility, and non-web

- Country and phone fields remain labeled and usable at high zoom.
- Code input supports mobile numeric keyboard without preventing desktop paste.
- Delivery polling uses restrained announcements.
- Native apps use approved SMS retrieval/autofill APIs and bind the code to the current app/ceremony where supported.
- Messaging-app content contains no sensitive account detail and clearly identifies purpose/expiry without clickable phishing-prone links unless governed.

## 11. Security

- Bind codes to tenant, subject, destination, ceremony, purpose, time, and transaction.
- Rate limit by tenant, subject, destination, IP/device context, provider, and ceremony.
- Protect against replay, SMS pumping, enumeration, destination swapping, SIM-swap/porting risk where signals exist, and provider callback spoofing.
- Never place codes/full numbers in analytics, URLs, logs, screenshots, or support exports.

## 12. Analytics and audit

Analytics records enrollment/challenge stage, region class, safe delivery outcome, resend, fallback, and completion without full number/code. Audit destination changes, verification, sends, delivery status, challenge outcome, replay/rate limit, replacement, removal, recovery, provider routing, policy, and administrator actions.

## 13. Tests

- Enrollment, send, autofill/paste, verification, login, step-up, resend, replacement, removal, recovery, and provider failover pass.
- Invalid/expired/replayed codes, delayed/failed delivery, unsupported region, pumping, enumeration, destination swap, callback spoof, and policy change fail safely.
- Full numbers/codes never leak.
- Accessibility, localization, phone formatting, narrow layout, native autofill, and last-factor tests pass.

## 14. Acceptance criteria

- Every enrollment, challenge, delivery, lifecycle, recovery, policy, provider, audit, and native screen is complete.
- SMS is accurately presented as a channel with lower assurance.
- Destination and resend are server controlled during ceremonies.
- Provider outages and delivery uncertainty have clear fallback.
- Product analytics and UI never expose full numbers or codes.

## 15. Dependencies

- Verified phone lifecycle and SMS delivery/provider abstraction.
- OTP verifier/replay/rate-limit service.
- Delivery receipt validation and provider health.
- Regional, consent, anti-abuse, recovery, and notification policy.

## References

- [AMR screen support matrix](../../amr-screen-support-matrix.md)
- [Universal authenticator ceremony brief](../uix-pairing-briefs/40-authenticator-ceremony-api-universal-authenticator-pages-uix.md)
- [MFA product maturity](../../mfa-focus.md)
- [Canonical AMR vocabulary](../../../pkgs/10-concrete/tigrbl-jose-concrete/src/tigrbl_jose_concrete/amr.py)
