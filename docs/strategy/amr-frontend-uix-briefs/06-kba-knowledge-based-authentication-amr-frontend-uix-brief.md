# Knowledge-Based Authentication AMR Frontend UIX Brief

- **AMR:** `kba`
- **Current delivery status:** Missing; no first-party KBA provider or lifecycle exists
- **Delivery target:** Complete first-party KBA enrollment, verifier, challenge, lifecycle, recovery, policy, and operations product
- **Category:** Knowledge factor
- **Risk posture:** Lower-assurance, high social-engineering and data-breach exposure; disabled by default
- **Platforms:** Public web/native, account management, supervised recovery, tenant/platform administration

## UIX delivery priority

**P0 — Actual authentication UIX (ship first):** KBA method selection → lower-assurance notice → server-selected question challenge → secure answer entry → submitting → generic invalid/rate-limited/attempts-exhausted/expired/blocked states → fallback or recovery → success or next-factor result. The challenge must work for sign-in, step-up, and governed recovery without revealing answer correctness. This is the release gate.

**P1 — Enrollment and user lifecycle:** question selection where allowed, answer creation/confirmation, activation, detail, replacement, suspension, compromise response, removal, and recovery.

**P2 — Administration and operations:** KBA eligibility/prohibition policy, question/verifier provider configuration, abuse controls, health, support tooling, audit, and diagnostics.

A question catalog or admin policy page is not the authenticator. First-class delivery requires the complete P0 challenge and failure experience first.

**Release gate:** P0 must be interaction-complete and validated before P2 administration/configuration/management UIX is treated as delivery. P2 screens cannot be used to claim first-class authenticator support.

## 1. Mandate

Define the full product experience required if knowledge-based authentication is deliberately supported. The implementation must treat KBA as a constrained compatibility or recovery method, not a preferred authenticator. Questions, expected answers, scoring, and source data remain server/provider owned and must never leak through UI, analytics, logs, or support tooling.

## 2. Users and jobs

- Users enroll permitted questions, complete challenges, and recover from lockout without account enumeration.
- Account holders replace or remove KBA while preserving another usable authenticator.
- Support agents initiate governed recovery without viewing answers.
- Administrators prohibit or narrowly scope KBA, define attempt/freshness policy, and assess lockout impact.
- Platform operators configure approved question/verifier providers and monitor abuse.

## 3. Required screens

| Screen | Purpose |
|---|---|
| Login method chooser | Offer KBA only when eligible and policy-approved |
| KBA introduction/risk notice | Explain limitations and recommend stronger methods |
| Enrollment question selection | Select only server-approved questions where user-selected questions are allowed |
| Enrollment answer entry | Collect and confirm answers without exposing normalization rules |
| Enrollment review/completion | Confirm activation and stronger recovery method |
| KBA challenge | Present server-selected questions and attempt state |
| Retry/rate-limit/blocked/expired | Safely handle failures without revealing answer correctness |
| Step-up challenge | Use KBA only for policies that explicitly allow its assurance |
| Evidence detail | Show KBA use, time, provider, and reduced assurance—not questions/answers |
| Authenticator detail | Show status, dates, policy use, replace/remove actions |
| Replace/remove flow | Require recent stronger authentication and prevent last-factor lockout |
| Recovery flow | Govern KBA as a recovery input, never sole proof for sensitive resets unless policy explicitly allows it |
| Tenant KBA policy | Scope apps/purposes, attempts, question source, fallback, and prohibition |
| Provider configuration | Configure source/verifier, encryption boundary, health, and regional availability |
| Audit/abuse diagnostics | Show redacted attempts, velocity, lockout, and provider outcomes |
| Native challenge | Equivalent accessible screens for native clients |

## 4. End-to-end enrollment

1. Add-authenticator shows KBA only when capability maturity and tenant policy permit it.
2. Introduction clearly labels KBA as weaker than passkeys/TOTP and lists allowed uses.
3. The server returns approved question descriptors; the client never invents or stores questions.
4. Answers use labeled inputs with password-manager-safe behavior and optional show/hide where appropriate.
5. Confirmation detects mismatches client-side but server owns normalization, hashing/encryption, duplicate rules, and acceptance.
6. Completion requires another recovery method or displays an explicit reduced-resilience warning.
7. Secrets clear on submit, navigation, timeout, error boundary, and unmount.

## 5. Authentication and recovery

1. Server selects question set, ordering, required count, attempt budget, and expiry.
2. UI presents one question per step or an accessible grouped form according to server descriptor.
3. Submission returns only generic accepted/retry/blocked results; never identify which answer failed.
4. Retry preserves only fields policy allows and announces remaining safe attempt information.
5. Success produces `kba` evidence with provider, time, purpose, and assurance limitations.
6. Recovery cannot immediately weaken or replace stronger authenticators without a governed delay, notification, or additional proof.

## 6. Screen behavior

### Enrollment

- Do not permit free-form questions such as family names or public-profile facts unless explicitly governed.
- Explain that answers should not be reused passwords.
- Never display stored answers after activation.
- Back navigation invalidates or safely resumes the server enrollment ceremony without retaining answers.

### Challenge

- Prevent account enumeration through question wording, counts, timing, and error differences.
- Avoid revealing source-record data in question prompts.
- Support paste; do not disable password managers arbitrarily.
- Provide switch-method, recovery, cancel, expiry, and support actions according to server state.

### Lifecycle and administration

- Detail shows status, enrollment/last-used dates, provider, permitted purposes, and event timeline.
- Replace is a new enrollment followed by activation and retirement of the prior set.
- Policy simulation covers exposed-answer breach, provider outage, no fallback, attempts exhausted, and supervised recovery.

## 7. States

Support ineligible, not enrolled, enrollment pending, active, suspended, compromised, replacement required, revoked, challenge ready, submitting, generic invalid response, rate limited, attempts exhausted, expired, cancelled, provider unavailable, policy changed, recovery only, success, and requires-next-step.

## 8. Components

Reuse `CeremonyShell`, `AuthenticatorMethodPicker`, `RecentAuthenticationGate`, `AuthenticatorDetailPanel`, `AuthenticatorEventTimeline`, `PolicyImpactPreview`, `DangerZone`, and shared error/result states.

Add `KbaRiskNotice`, `KbaQuestionPicker`, `KbaAnswerField`, `KbaChallengeStep`, `AnswerSecretClearBoundary`, and `KbaPolicySummary`.

## 9. Data/API expectations

The server owns question descriptors, source, answer normalization/verifier, required count, ordering, attempts, expiry, rate limit, assurance, lifecycle, recovery restrictions, and audit references. Frontend payloads never contain stored answers, hashes, correctness per question, source-dataset records, or scoring internals.

## 10. Responsive, accessibility, and native

- One-column challenge at narrow widths; question and input remain adjacent at high zoom.
- Progress conveys step count without leaking adaptive question selection.
- Labels remain persistent; errors link to fields and are announced.
- Native clients use secure text controls, clear app-switcher snapshots where supported, and bind resume to ceremony state.
- Full keyboard, screen reader, contrast, forced-colors, reduced-motion, and 200% zoom support is mandatory.

## 11. Security and privacy

- TLS is insufficient by itself; server storage/verifier boundaries must protect answers.
- Never log, cache, persist, auto-save, analyze, or return answers.
- Enforce tenant/subject/ceremony binding, throttling, enumeration resistance, breach response, and notifications.
- KBA does not satisfy phishing-resistant or high-assurance policy.
- Require stronger recent authentication for lifecycle changes.

## 12. Analytics and audit

Analytics records funnel stage and safe error class only. Audit enrollment, challenge outcome, attempt exhaustion, rate limit, suspension, compromise, replacement, removal, recovery use, policy/provider changes, and support actions without questions or answers.

## 13. Tests

- Enrollment, confirmation, replacement, removal, challenge, step-up, and recovery complete end to end.
- Answer mismatch and failure do not reveal correctness or account existence.
- Secrets clear on every lifecycle exit and never reach DOM snapshots, storage, URLs, logs, analytics, or crash reports.
- Rate limits, replay, concurrency, policy change, provider outage, cross-tenant access, and last-factor removal fail safely.
- Accessibility and responsive tests cover long localized questions and error states.

## 14. Acceptance criteria

- Every screen required for enrollment, challenge, evidence, lifecycle, recovery, policy, diagnostics, and native parity is specified.
- KBA is disabled unless an approved capability and policy enable it.
- The UI communicates lower assurance and recommends stronger methods.
- No answer material or question-source secrets leave their approved boundaries.
- All destructive/recovery actions have proportional safeguards.

## 15. Dependencies

- Product decision to support KBA despite its risk posture.
- Question catalog/source, answer verifier, compromise response, and regional policy.
- Assurance mapping and recovery restrictions.
- Provider health and abuse-detection contracts.

## References

- [AMR screen support matrix](../../amr-screen-support-matrix.md)
- [Universal authenticator ceremony brief](../uix-pairing-briefs/40-authenticator-ceremony-api-universal-authenticator-pages-uix.md)
- [Canonical AMR vocabulary](../../../pkgs/10-concrete/tigrbl-jose-concrete/src/tigrbl_jose_concrete/amr.py)
