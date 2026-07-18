# Multi-Factor Authentication AMR Frontend UIX Brief

- **AMR:** `mfa`
- **Current delivery status:** Derived; current generic `MfaPage` is insufficient
- **Delivery target:** Complete first-party MFA orchestration, enrollment, step-up, recovery, lifecycle, policy, support, and operations product
- **Category:** Orchestrated assurance evidence
- **Primary rule:** The server emits `mfa` only after independent factor classes satisfy policy
- **Platforms:** Public web, native apps, account management, tenant/platform policy, external authenticators

## UIX delivery priority

**P0 — Actual authentication UIX (ship first):** MFA requirement introduction → eligible-factor chooser → first factor challenge → verified progress → next-factor challenge or OOB callback → retry/switch/provider-unavailable/rate-limited/expired/blocked states → recovery with reduced assurance where allowed → `mfa` success and return to the original transaction. Sign-in and step-up are release-gating flows.

**P1 — Enrollment and user lifecycle:** enrollment-required gate, method-specific enrollment, factor inventory/detail, replacement/removal, backup/recovery, and session assurance review.

**P2 — Administration and operations:** factor-class policy, grace/remembered-device/support reset, simulation, rollout, provider capability/health, audit, and diagnostics.

The generic `MfaPage` is not the product. MFA becomes first class only when the P0 multi-factor ceremony is complete for every supported adapter and adverse state.

**Release gate:** P0 must be interaction-complete and validated before P2 administration/configuration/management UIX is treated as delivery. P2 screens cannot be used to claim first-class authenticator support.

## 1. Mandate

Replace the single-code mental model with a universal, method-aware MFA and step-up experience. Support enrollment, factor selection, sequential or conditional challenges, recovery, evidence, lifecycle, policy, administrative reset, native handoffs, and audit without treating `mfa` as an addable authenticator.

## 2. Users and jobs

- Users enroll resilient factors and complete MFA/step-up with clear progress and fallback.
- Account holders manage factors and understand session assurance.
- Tenant administrators define factor-class combinations, grace, remembered-device behavior, recovery, and rollout.
- Support agents perform governed factor reset/re-enrollment.
- Platform operators manage provider capability, health, and conformance.
- Developers understand whether an application/request requires MFA and how completion returns.

## 3. Required screens

| Screen | Purpose |
|---|---|
| Method-aware login | Start authentication and preserve the original application transaction |
| MFA requirement introduction | Explain why another factor is needed and available choices |
| Factor chooser | List eligible enrolled methods with safe status and fallback |
| Enrollment-required gate | Route users who lack an eligible factor into governed enrollment |
| Method-specific enrollment | TOTP, passkey, security key, recovery, or future provider adapter |
| Multi-step ceremony progress | Show achieved/current/remaining requirements |
| Method-specific challenge | Render OTP, WebAuthn, recovery, push, federation, or other adapter |
| External wait/callback | Resume OOB or federated methods |
| Switch method | Change only within policy-approved equivalent choices |
| Retry/rate-limit/expired/blocked | Handle method and aggregate failures |
| MFA completion/next step | Show achieved context or remaining policy obligation |
| Recovery ceremony | Use recovery with reduced assurance and post-recovery steps |
| My Authenticators inventory | Add, name, replace, suspend, remove, and inspect factors |
| Factor detail/event history | Show lifecycle, assurance, last use, and evidence |
| Session context | Show factors/classes, time, freshness, and `mfa` result |
| Tenant MFA policy | Configure apps, actions, factor classes, age, grace, fallback |
| Policy simulation/versioning | Test enrollment and lockout impact before rollout |
| User enrollment posture/admin reset | Govern help-desk recovery and re-enrollment |
| Provider capability/health | Show maturity, outage, and supported ceremony modes |
| Audit/diagnostics | Correlate factors, ceremonies, policy, and failures |
| Native factor chooser/ceremony | Match web semantics using platform-native adapters |

## 4. Critical flows

### Sign-in and step-up

1. Server returns required factor classes, achieved evidence, eligible methods, and transaction purpose.
2. Requirement screen uses safe, outcome-oriented copy and offers a factor chooser when more than one method is eligible.
3. User completes the selected adapter; server records evidence.
4. Progress updates from server state and either completes, requests another factor, or offers policy-approved fallback.
5. `mfa` is emitted only after the independence evaluator accepts the achieved set.
6. Completion returns to the original authorization/action with a bound callback.

### Enrollment during authentication

1. If policy requires MFA but no eligible factor exists, server chooses enrollment-required, grace, recovery, or block behavior.
2. Enrollment explains method, privacy, recovery, and effect on the current transaction.
3. Complete method-specific setup and initial verification.
4. Confirm recovery and return to the original MFA ceremony without creating duplicate transactions.

### Account management

1. Inventory shows active, suspended, recovery-only, replacement-required, and unavailable methods.
2. Add/replace uses method-specific enrollment and recent-authentication gates.
3. Removing the last eligible factor is blocked or requires an approved replacement/recovery plan.
4. Changes invalidate affected sessions/remembered-device grants according to policy.

### Administration

1. Define required factor classes and allowed methods per app/action/risk context.
2. Configure authentication age, grace, recovery, remembered-device, bypass approval, and enrollment deadlines.
3. Simulate representative users, no-factor populations, provider outage, last-factor removal, and recovery.
4. Preview impact, version, approve, roll out, monitor, and roll back safely.

## 5. Screen behavior

### Factor chooser

- Show method name, device/account hint, availability, last-used context, and recommended status.
- Do not rank weaker methods as equivalent to phishing-resistant methods.
- Disabled methods explain policy, outage, incompatibility, or enrollment state safely.

### Progress and challenge

- Use “Step 1 of 2” only when the server confirms a fixed sequence; adaptive flows use achieved/current language.
- Persist no secrets between adapters.
- Refresh resumes current server step without resending or reopening prompts.
- Back/cancel follows transaction policy; switch method never resets achieved evidence without server direction.

### Evidence and context

- Show underlying methods, factor classes, authentication times, freshness, properties, policy version, recovery/reduced assurance, and audit reference.
- Never infer MFA by counting AMRs client-side.

### Recovery

- Clearly label reduced assurance and required account-hardening actions.
- Recovered sessions cannot perform sensitive operations until policy-approved step-up.
- Notify and audit recovery, reset, bypass, and re-enrollment.

## 6. States

Support eligible/ineligible, no enrollment, enrollment pending, grace period, factor chooser, method active, external wait, challenge invalid, retryable, rate limited, attempts exhausted, provider unavailable, device unsupported, policy changed, factor suspended/revoked, recovery only, cancelled, expired, blocked, success, and requires-next-step.

## 7. Components

Reuse every universal ceremony, inventory, method-adapter, evidence, policy, safety, and result component defined by the shared design system.

Add `FactorRequirementSummary`, `FactorClassBadge`, `MfaProgress`, `EligibleFactorList`, `EnrollmentRequiredGate`, `AssuranceComparison`, `RecoveryAssuranceWarning`, and `EnrollmentPostureTable`.

The existing `MfaPage` becomes a route adapter into `CeremonyShell`; it must not retain code-specific business logic.

## 8. Data/API expectations

Server fields include required/achieved factor classes, eligible methods, independence result, ceremony purpose/state, current adapter descriptor, attempts, expiry, method-switch eligibility, enrollment requirement, grace/recovery state, next action, context result, policy version, safe reason, and audit reference.

The client cannot assert completion, independence, `mfa`, bypass, remembered-device trust, or assurance level.

## 9. Responsive, accessibility, and native

- Chooser and progress reflow to a single semantic list at narrow widths.
- Current action comes before completed-detail content in focus order.
- Errors and changing steps receive managed focus and restrained live announcements.
- Native apps use shared state contracts with native WebAuthn, OTP autofill, push, deep link, and device adapters.
- External approvals show transaction context to prevent approval fatigue/confusion.

## 10. Security

- Bind every factor to tenant, subject, transaction, purpose, ceremony, and policy version.
- Enforce independence, replay protection, rate limits, expiry, downgrade resistance, and safe fallback server-side.
- Prevent factor deletion/replacement from bypassing recent-authentication requirements.
- Recovery and support bypass produce explicit reduced-assurance evidence and notifications.
- No secrets, raw proofs, full destinations, or risk internals in telemetry or URLs.

## 11. Analytics and audit

Analytics captures requirement shown, chooser selection, adapter funnel, safe error class, fallback, recovery, and completion. Audit underlying factor evidence, independence evaluation, policy version, bypass/recovery, lifecycle changes, provider outage, and administrative actions.

## 12. Tests

- Independent factors yield `mfa`; duplicate factor classes or non-independent evidence do not.
- Login, enrollment-required, multi-step, adaptive, switch, fallback, recovery, and return-to-transaction flows pass.
- Refresh does not duplicate challenges; stale/replayed callbacks fail.
- No-factor, provider outage, last-factor removal, policy change, and support reset are safe.
- Accessibility, narrow layouts, native resume, external approval, cross-tenant, and cross-subject tests pass.

## 13. Acceptance criteria

- All enrollment, challenge, orchestration, recovery, inventory, evidence, policy, support, provider, diagnostics, and native screens are complete.
- `mfa` is server-derived from independent factors.
- The generic six-digit `MfaPage` assumption is removed.
- Users can always identify the current action, safe fallback, and outcome.
- Administrators can simulate and roll out policy without creating avoidable lockouts.

## 14. Dependencies

- Factor-class and independence evaluator.
- Production-ready method adapters and lifecycle APIs.
- Step-up/authorization transaction binding.
- Recovery, remembered-device, bypass, and support authority contracts.

## References

- [AMR screen support matrix](../../amr-screen-support-matrix.md)
- [Universal authenticator ceremony brief](../uix-pairing-briefs/40-authenticator-ceremony-api-universal-authenticator-pages-uix.md)
- [MFA product maturity](../../mfa-focus.md)
- [Canonical AMR vocabulary](../../../pkgs/10-concrete/tigrbl-jose-concrete/src/tigrbl_jose_concrete/amr.py)
