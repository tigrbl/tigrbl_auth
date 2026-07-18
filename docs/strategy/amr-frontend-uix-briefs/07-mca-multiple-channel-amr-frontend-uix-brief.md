# Multiple-Channel Authentication AMR Frontend UIX Brief

- **AMR:** `mca`
- **Current delivery status:** Derived; no complete orchestration product exists
- **Delivery target:** Complete first-party multi-channel orchestration, evidence, recovery, policy, provider-health, and audit product
- **Category:** Orchestrated authentication evidence
- **Primary rule:** Emit `mca` only after the server proves that policy-defined independent channels completed
- **Platforms:** Web, native, external/OOB devices, administrative policy and evidence surfaces

## UIX delivery priority

**P0 — Actual authentication UIX (ship first):** multi-channel requirement introduction → channel/method chooser → channel-one ceremony → verified-step transition → channel-two/OOB handoff → external wait/callback → aggregate progress → retry/resend/channel-unavailable/substitution/expired/blocked states → policy-approved fallback → `mca` success or next requirement. This cross-channel authentication journey is the primary deliverable and release gate.

**P1 — Enrollment readiness and user lifecycle:** underlying-channel enrollment routing, independence readiness, destination/device replacement, recovery, and session/evidence review.

**P2 — Administration and operations:** independence policy, combination configuration, provider health, simulation, correlation diagnostics, audit, and channel operations.

Do not prioritize orchestration dashboards over the live ceremony. MCA is first class only when users can complete the full P0 multi-channel sequence across web, native, and OOB devices.

**Release gate:** P0 must be interaction-complete and validated before P2 administration/configuration/management UIX is treated as delivery. P2 screens cannot be used to claim first-class authenticator support.

## 1. Mandate

Deliver a universal multi-channel ceremony that coordinates two or more independently governed communication/authentication channels, survives handoffs and interruptions, prevents channel substitution, and presents achieved evidence accurately. `mca` must never appear in the add-authenticator catalog by itself.

### First-party enrollment applicability

`mca` has no standalone credential enrollment. The first-party product must orchestrate enrollment readiness for every underlying channel: verified phone/SMS/telephone destinations, TOTP, push device, passkey/security key, federation account, smart card, or another approved channel. An enrollment-readiness screen shows missing channels, independence conflicts, required recovery, and direct links into each underlying enrollment. The orchestration lifecycle covers draft policy, enrollment pending, ready, degraded, suspended, provider outage, recovery only, and retired combinations.

## 2. Users and jobs

- Users understand which channel is active, what remains, how long it lasts, and how to switch safely.
- Account holders inspect the channels used without exposing destination secrets.
- Administrators define channel independence, allowed combinations, sequence, fallback, and recovery.
- Operators monitor channel providers, correlation, replay, delivery, and fraud outcomes.
- Native users move among app, browser, phone, security key, or approved device without losing ceremony state.

## 3. Screen inventory

| Screen | Purpose |
|---|---|
| Login/method chooser | Start an eligible multi-channel path or underlying first method |
| MCA introduction | Explain required channels, privacy-safe destinations, expiry, and fallback |
| Channel progress | Show completed/current/pending steps without exposing secrets |
| Channel-specific ceremony adapter | Render OTP, push, passkey, call, smart card, or provider handoff |
| External-wait screen | Poll safely while an OOB channel is pending |
| Redirect/callback | Resume after an upstream channel |
| Channel switch/fallback | Use only policy-approved replacement channels |
| Retry/rate-limit/expired/blocked | Handle per-channel and aggregate ceremony failures |
| Completion/next step | Show whether MCA is achieved or another requirement remains |
| Evidence detail | Show channel classes, order, times, provenance, and independence decision |
| Session context | Explain how MCA contributed to authentication |
| Underlying authenticator lifecycle | Manage each authenticator separately |
| Recovery | Regain access without silently collapsing required channel independence |
| MCA policy editor | Define combinations, independence, ordering, age, and fallback |
| Policy simulator | Test availability, compromise, collision, and provider outage |
| Provider health dashboard | Show status for every channel provider |
| Correlation/audit diagnostics | Investigate redacted channel events and orchestration |
| Native handoff/resume | Preserve ceremony across app/device transitions |

## 4. End-to-end ceremony

1. Server evaluates policy and returns channel requirements plus eligible methods.
2. Introduction shows the number and general type of steps, safe destination hints, expiry, and alternatives.
3. User completes channel one through its dedicated adapter.
4. Server records verified channel evidence; the client cannot mark a step complete.
5. Ceremony advances to channel two or an external-wait state.
6. Correlation binds every callback/approval to the same tenant, subject, transaction, purpose, and ceremony.
7. If a channel fails, the server determines retry, alternative channel, restart, or terminal failure.
8. `mca` is emitted only when the independence evaluator accepts the completed set.
9. Result shows achieved context and redirects to the original action.

## 5. Screen behavior

### Introduction and progress

- Use ordered steps with text status: completed, current, waiting, unavailable, or required again.
- Do not disclose full phone/email destinations, risk rules, or channel-selection secrets.
- Back exits or pauses according to server policy; it cannot rewind verified server state.
- Refresh resumes current state and does not resend messages or reopen prompts.

### External wait

- Show approved destination/device hint, elapsed/remaining time, cancel, resend eligibility, and switch-method action.
- Poll with bounded backoff and accessible status updates.
- A late approval after cancellation/expiry is rejected server-side and shown as no longer valid.

### Fallback

- Explain when an alternative still satisfies MCA and when it reduces assurance.
- Never replace two required independent channels with two methods on the same compromised channel unless policy explicitly accepts it.
- Recovery that bypasses MCA must produce reduced/recovery assurance and post-recovery hardening steps.

### Evidence detail

- Show channel classes, underlying methods, completion times, provider/source, freshness, independence outcome, policy version, and audit reference.
- Redact destinations and device/provider identifiers.
- Do not infer MCA by counting AMR strings on the client.

## 6. States

Support eligibility loading, ready, channel one active, external wait, callback processing, channel complete, next channel, resend available/unavailable, channel unavailable, destination unreachable, retryable failure, rate limited, conflicting approval, replay, cancelled, expired, policy changed, aggregate blocked, recovery only, success, and requires-next-step.

## 7. Components

Reuse `CeremonyShell`, `CeremonyProgress`, `AuthenticatorMethodPicker`, `MethodSwitchMenu`, `ChallengeCountdown`, `CeremonyResult`, `AuthenticationContextSummary`, and all method adapters.

Add `ChannelSequence`, `ChannelStatusCard`, `ExternalApprovalWait`, `ChannelFallbackComparison`, `IndependenceEvidenceSummary`, and `ChannelProviderHealthGrid`.

## 8. Data/API expectations

The server owns channel requirements, independence rules, order, allowed methods, verified step state, destination projections, resend policy, expiry, attempts, callback binding, next action, aggregate result, and audit references.

Frontend events never establish completion, independence, or `mca`. Raw destinations, provider secrets, approval payloads, and risk internals are excluded.

## 9. Responsive, accessibility, and non-web

- Progress collapses into a semantic ordered list at narrow widths.
- Current action precedes completed-step detail in focus order.
- Polling announcements are throttled; countdown is not announced every second.
- Native deep links and app resumes restore the exact channel step.
- External devices show transaction context sufficient to prevent approval confusion.
- CLI/workload flows use explicit noninteractive channel adapters and machine-readable status, not browser scraping.

## 10. Security

- Bind all channel messages, approvals, callbacks, and proofs to the same ceremony and transaction.
- Prevent replay, approval fatigue, channel substitution, destination changes, cross-tenant correlation, and late completion.
- Rate limits apply per subject, destination, provider, tenant, and ceremony.
- Recovery/fallback cannot silently downgrade assurance.
- Sensitive destinations and correlation identifiers never enter analytics or URLs.

## 11. Analytics and audit

Analytics records channel class, step funnel, provider-safe status, fallback, duration, and completion. Audit records each channel proof, independence evaluation, policy version, resend, fallback, cancellation, expiry, provider outage, and administrative change with redacted destinations.

## 12. Tests

- Valid independent channels yield `mca`; duplicate/non-independent channels do not.
- Every ordering, callback, OOB approval, resend, timeout, fallback, policy change, and provider outage path is covered.
- Refresh does not duplicate challenges.
- Late/replayed/cross-tenant/cross-subject approvals fail.
- Recovery preserves reduced-assurance semantics.
- Keyboard, screen-reader, narrow-layout, native resume, and polling tests pass.

## 13. Acceptance criteria

- One orchestration supports all approved channel adapters end to end.
- The client never derives `mca` or channel independence.
- Users always know the current step and safe exit/fallback.
- Evidence, policy, provider health, recovery, audit, native handoff, and failure states are complete.
- No channel secret or full destination is exposed.

## 14. Dependencies

- Channel-independence evaluator and evidence contract.
- Underlying authenticator/channel adapters.
- OOB callback and correlation service.
- Policy simulation and provider-health aggregation.

## References

- [AMR screen support matrix](../../amr-screen-support-matrix.md)
- [Universal authenticator ceremony brief](../uix-pairing-briefs/40-authenticator-ceremony-api-universal-authenticator-pages-uix.md)
- [Canonical AMR vocabulary](../../../pkgs/10-concrete/tigrbl-jose-concrete/src/tigrbl_jose_concrete/amr.py)
