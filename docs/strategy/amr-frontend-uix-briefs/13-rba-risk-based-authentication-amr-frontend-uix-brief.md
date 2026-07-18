# Risk-Based Authentication AMR Frontend UIX Brief

- **AMR:** `rba`
- **Current delivery status:** Derived/contextual; adaptive scaffolding exists but is not productized
- **Delivery target:** Complete first-party risk-signal, decision, step-up, review, recovery, policy, simulation, and operations product
- **Category:** Authentication decision evidence
- **Primary rule:** Risk changes the required ceremony; it is not offered as an authenticator
- **Platforms:** Web/native login and step-up, account context, tenant/platform administration, security operations

## UIX delivery priority

**P0 — Actual adaptive-authentication UIX (ship first):** context evaluation → safe decision loading → continue or risk-triggered step-up introduction → eligible-method chooser → authenticator ceremony → reevaluation → review/deny/recovery/provider-unavailable/policy-changed states → success and return to the original transaction. This user-visible adaptive sequence is the release gate.

**P1 — User lifecycle and response:** session context, unfamiliar-activity reporting, session revocation, managed-signal consent/enrollment, review outcome, and governed recovery.

**P2 — Administration and operations:** signal/provider registration, risk rules, simulation, versioning, rollout, detector health, security investigation, audit, and diagnostics.

RBA is not delivered merely because an administrator can configure rules. It becomes first class when the P0 adaptive journey safely guides real users through additional authentication or recovery.

**Release gate:** P0 must be interaction-complete and validated before P2 administration/configuration/management UIX is treated as delivery. P2 screens cannot be used to claim first-class authenticator support.

## 1. Mandate

Deliver a complete adaptive-authentication experience that evaluates approved risk signals, requests proportionate verification, presents safe explanations, supports recovery and review, and records policy/evidence provenance. Never expose exact scores, thresholds, detector rules, or bypass hints to users.

### First-party enrollment and lifecycle applicability

`rba` has no user credential enrollment. The first-party enrollment surface registers and approves signal providers, device/posture collectors, detector/rule versions, review queues, and response policies. Each source and policy has draft, testing, active, degraded, suspended, superseded, rolled-back, and retired lifecycle states. Users may enroll managed-device posture or consented signals through the owning source flow and may review/revoke permitted grants. Recovery means restoring account access through a governed review or stronger authenticator, never deleting the risk event.

## 2. Required screens

| Screen | Purpose |
|---|---|
| Login context evaluation | Hold or continue while the server evaluates risk |
| Risk-triggered step-up introduction | Explain that another verification step is required |
| Eligible-method chooser | Offer methods satisfying the server's adaptive decision |
| Universal step-up ceremony | Complete selected authenticator(s) |
| Device/OS attestation handoff | Obtain approved posture evidence when needed |
| External approval/wait | Support governed approval or OOB confirmation |
| Retry/blocked/review state | Handle elevated risk without revealing detector internals |
| Completion/return | Continue the bound transaction after sufficient evidence |
| Session context | Show safe risk-decision category, time, signals class, and authentication response |
| Authentication-event detail | Show redacted evidence, decision, policy, and audit reference |
| User unfamiliar-activity report | Revoke session and initiate account protection |
| Risk-policy editor | Define signals, decisions, step-up, deny/review, and fallback |
| Policy simulator | Test representative, boundary, stale, conflicting, and unavailable cases |
| Version/impact/rollout | Approve, stage, monitor, and roll back policy |
| Signal-provider configuration | Configure sources, freshness, trust, privacy, and fail behavior |
| Provider/detector health | Show latency, errors, drift, freshness, and outage posture |
| Security investigation | Correlate redacted decisions and actions |
| Native risk/step-up | Present equivalent decision and native method adapters |

## 3. End-to-end decision flow

1. Login/action starts a server-bound transaction.
2. Server gathers approved context and evaluates a versioned risk policy.
3. UI receives only a safe decision: continue, step up, review, deny, or recover.
4. Step-up screen explains the outcome generically and offers eligible methods.
5. User completes required ceremony; server reevaluates with new evidence.
6. Success returns to the original action; deny/review/recovery states preserve audit and notification.
7. Session context records the safe decision class and achieved response, including `rba` where policy defines it.

## 4. Administrative flow

1. Configure signal sources and privacy classification.
2. Build policy from named conditions and responses—not opaque UI-only logic.
3. Define freshness, confidence, source conflict, provider outage, and fail behavior.
4. Simulate known-good, new device, impossible travel, compromised session, missing signal, stale signal, source disagreement, and mass-provider outage.
5. Preview affected users/apps and lockout/support impact.
6. Approve/version/stage rollout; monitor safe aggregate outcomes; roll back if necessary.

## 5. Screen behavior

### User-facing decision

- Use “We need another verification step” instead of “Your risk score is 87.”
- Provide methods, expiry, cancel/back, switch, recovery, and support according to server state.
- Denied/review states give a reference ID and account-protection action without revealing rule details.
- Do not label a device “trusted” without a defined trust grant and expiry.

### Context/evidence detail

- Show decision category, evaluation time, policy version, broad signal classes, achieved methods, freshness, and audit reference.
- Redact precise location, IP/device fingerprints, behavioral features, model internals, and third-party scores.
- Permit session revocation and unfamiliar-event reporting.

### Policy and health

- Separate signal configuration, policy decisions, rollout, and outcomes.
- Every rule includes scope, response, fallback, expiry/freshness, and missing-signal behavior.
- Health distinguishes source outage, data staleness, evaluation error, latency, and model/rule version drift.

## 6. States

Support evaluating, continue, step-up required, method unavailable, awaiting device/provider, additional evidence received, reevaluating, review pending, denied, recovery required, provider unavailable, conflicting/stale/missing signals, policy changed, cancelled, expired, blocked, success, and success requiring another action.

## 7. Components

Reuse `CeremonyShell`, `AuthenticatorMethodPicker`, `AuthenticationContextSummary`, `PolicyImpactPreview`, `AuditReference`, `BlockedCeremonyState`, and method adapters.

Add `AdaptiveDecisionNotice`, `RiskSignalClassSummary`, `SafeDecisionReason`, `RiskPolicyBuilder`, `RiskSimulationWorkbench`, `SignalProviderHealth`, and `UnfamiliarActivityAction`.

## 8. Data/API expectations

The server owns signals, models/rules, scores, thresholds, policy version, decision, eligible response methods, reevaluation, and audit. Frontend receives safe reason, broad signal classes, freshness, required action, allowed recovery, provider health projection, and audit reference—not raw features or bypass logic.

## 9. Responsive, accessibility, and native

- The required action remains primary at narrow widths; help and context are secondary.
- Status updates during evaluation are announced without repetitive polling noise.
- Native device/posture prompts use platform APIs and bind resume to the ceremony.
- Review/deny references are selectable and screen-reader labeled.
- Policy builder supports keyboard, zoom, non-color semantics, and a complete textual rule representation.

## 10. Security and privacy

- Minimize and classify signals; enforce purpose, retention, regional, and access controls.
- Bind decisions and new evidence to tenant, subject, transaction, ceremony, time, and policy version.
- Prevent replay, downgrade, signal spoofing, policy confusion, and cross-tenant evidence.
- Never expose precise signals or decision internals through analytics, logs, URLs, DOM, errors, or support UI.
- Recovery/override is governed, time-bound, notified, and audited.

## 11. Analytics and audit

Analytics records safe decision class, step-up method, completion, fallback, review/deny aggregate, provider availability, and duration. Audit policy version, signal-source classes, freshness, decision, evidence response, overrides, reviews, session actions, and administrative changes with strict redaction.

## 12. Tests

- Continue, step-up, review, deny, recovery, and return-to-action flows pass.
- Missing/stale/conflicting/spoofed signals and provider outages follow explicit policy.
- UI never reveals scores, thresholds, rules, precise signals, or bypass hints.
- Policy simulation, staged rollout, rollback, concurrency, policy-change, and cross-tenant cases pass.
- Native resume, accessibility, zoom, responsive, and security-redaction tests pass.

## 13. Acceptance criteria

- RBA drives a complete adaptive ceremony but never appears as an addable authenticator.
- Users get clear required actions and safe recovery without detector disclosure.
- Account holders can inspect and respond to suspicious sessions.
- Administrators can configure, simulate, version, deploy, monitor, and roll back policy.
- Every decision is explainable through approved safe projections and auditable provenance.

## 14. Dependencies

- Canonical risk-signal, decision, safe-reason, and provenance contracts.
- Versioned policy evaluator and simulator.
- Signal-provider registry/health and privacy classification.
- Step-up, review, recovery, notification, and override authorities.

## References

- [AMR screen support matrix](../../amr-screen-support-matrix.md)
- [Universal authenticator ceremony brief](../uix-pairing-briefs/40-authenticator-ceremony-api-universal-authenticator-pages-uix.md)
- [Canonical AMR vocabulary](../../../pkgs/10-concrete/tigrbl-jose-concrete/src/tigrbl_jose_concrete/amr.py)
