# Password AMR Frontend UIX Brief

- **AMR:** `pwd`
- **Current delivery status:** Core support exists; lifecycle and adverse-state coverage is incomplete
- **Delivery target:** Complete first-party password enrollment, authentication, lifecycle, reset, recovery, policy, support, and operations product
- **Category:** Knowledge factor
- **Platforms:** Public web, native apps, account management, tenant/platform administration, support/recovery

## UIX delivery priority

**P0 — Actual authentication UIX (ship first):** identifier-first entry → password screen → secure entry/password-manager interaction → submitting → generic invalid/rate-limited/locked/disabled/expired/compromised states → forced-change continuation where required → MFA/next-step transition → success. Sign-in and recent-authentication/step-up are the release gate.

**P1 — Enrollment and user lifecycle:** create, change, forced change, forgot/reset, compromise response, password detail, disable/remove, recovery, and passwordless transition.

**P2 — Administration and operations:** password policy, breached-secret integration, admin reset, posture, lockout monitoring, audit, and diagnostics.

Policy editors and reset administration are secondary. Password is first class only when the P0 login and adverse-state experience is complete, accessible, enumeration-safe, and password-manager compatible.

**Release gate:** P0 must be interaction-complete and validated before P2 administration/configuration/management UIX is treated as delivery. P2 screens cannot be used to claim first-class authenticator support.

## 1. Mandate

Deliver the complete password lifecycle from creation through sign-in, step-up, change, forced change, reset, compromise response, suspension, recovery, evidence, policy, diagnostics, and retirement. Preserve password-manager compatibility, enumeration resistance, secret minimization, and safe fallback.

## 2. Required screens

| Screen | Purpose |
|---|---|
| Identifier-first login | Collect account hint without enumeration |
| Password sign-in | Submit current password |
| Password step-up/reauthentication | Confirm recent knowledge factor for sensitive actions |
| Create password | Initial registration/invite/credential setup |
| Password requirements | Explain server policy without aiding guessing |
| Change password | Verify current password and set replacement |
| Forced change | Replace expired/bootstrap/administratively reset password |
| Forgot-password request | Start reset without revealing account existence |
| Reset-link/code verification | Validate bound, expiring recovery artifact |
| Reset completion | Set new password and invalidate artifact |
| Invalid/expired/used reset | Provide safe restart/support path |
| Compromised-password response | Require replacement and explain protective actions |
| Password detail/status | Show status, dates, events, and available lifecycle actions |
| Disable/remove password | Permit passwordless transition only with safe alternatives |
| Evidence/session detail | Show `pwd`, time, freshness, purpose, and assurance |
| Password policy editor | Configure length, blocklists, attempts, reset, and app scope |
| User posture/admin reset | Govern support reset and forced change |
| Lockout/security event detail | Investigate redacted failures and notifications |
| Native password screen | Secure native entry and password-manager integration |

## 3. Sign-in and step-up

1. Identifier submission always returns an enumeration-safe next state.
2. Password screen uses persistent label, `autocomplete="current-password"`, paste, password-manager, and show/hide controls.
3. Server validates password, status, attempts, tenant/realm, and policy.
4. Invalid credentials return generic error; retry, rate limit, locked, forced-change, compromise, and MFA-required states are server-directed.
5. Success produces `pwd` evidence and either completes or advances to another factor.

## 4. Creation/change/forced-change

1. Server returns purpose, requirements projection, token/ceremony binding, and allowed actions.
2. New password uses `autocomplete="new-password"`; confirmation prevents local typing mismatch only.
3. Server owns blocklist, breached-secret, similarity/history, and acceptance decisions.
4. Change verifies current password or a policy-approved recent-authentication gate.
5. Forced change cannot navigate into the application until completed or an approved recovery/support path is chosen.
6. Success clears fields, invalidates relevant sessions/artifacts, sends notification, and shows next steps.

## 5. Forgot/reset flow

1. Request screen accepts identifier and always shows the same completion response.
2. Delivery channel and artifact are server owned.
3. Reset callback validates token/code before rendering new-password fields.
4. Used, expired, revoked, malformed, wrong-tenant, and replayed artifacts show safe restart guidance.
5. Successful reset consumes the artifact, applies session/token invalidation policy, and optionally requires MFA or account review.

## 6. Compromise and lifecycle

- Compromise screen explains that a change is required without revealing breach-source details.
- Password detail shows enabled/disabled, created/changed/last-used dates, forced-change status, session impact, and event history—never hashes or policy internals.
- Removing password requires another active authenticator and recent authentication.
- Admin reset creates a temporary recovery state or reset artifact; administrators never set/view user passwords.

## 7. States

Support loading, ready, submitting, invalid, rate limited, locked, disabled, expired, compromised, forced change, reset requested, reset pending, token invalid/expired/used/revoked, password rejected, history/blocklist/breach rejection with safe copy, mismatch, policy changed, provider unavailable, success, MFA required, and recovery required.

## 8. Components

Reuse `CeremonyShell`, `PasswordField`, `PasswordRequirements`, `RecentAuthenticationGate`, `RecoveryImpactNotice`, `AuthenticatorDetailPanel`, `AuthenticatorEventTimeline`, `PolicyImpactPreview`, and shared error/result states.

Add `PasswordCompromiseNotice`, `PasswordLifecycleSummary`, `SessionInvalidationChoice`, `ResetArtifactState`, and `PasswordlessTransitionGate`.

## 9. Data/API expectations

The server owns password verification, hashing, policy, blocklists, attempts, rate limits, lockout, compromise result, history, reset artifact, session invalidation, lifecycle state, safe errors, and audit references. Frontend payloads never contain hashes, breach corpus matches, password history, or reset secrets beyond the currently consumed artifact.

## 10. Responsive, accessibility, and native

- Forms remain one-column and usable at 200% zoom.
- Labels persist; requirements update without overwhelming live announcements.
- Show/hide preserves cursor, value, label, and accessible state.
- Native fields use secure entry, password-manager APIs, autofill, and app-switcher privacy without disabling paste.
- Errors focus the summary and link to relevant fields.

## 11. Security

- Passwords exist only until submission and clear on success, navigation, timeout, and unmount.
- Never place passwords/reset artifacts in analytics, logs, URLs beyond unavoidable callback token transport, support payloads, or hidden markup.
- Enforce CSRF, enumeration resistance, rate limiting, tenant/subject binding, reset replay protection, and safe redirect validation.
- Do not require arbitrary periodic changes unless policy explicitly does.
- Administrators cannot retrieve or directly assign permanent user passwords.

## 12. Analytics and audit

Analytics records screen/funnel, safe error class, reset request/completion, forced-change completion, and passwordless transition. Audit sign-in outcome, lockout, reset, forced change, compromise, change, disable/remove, session invalidation, admin action, and policy version without secret data.

## 13. Tests

- Sign-in, step-up, create, change, forced change, forgot, reset, invalid/expired/used artifact, compromise, disable/remove, and admin reset pass.
- Enumeration timing/content remains equivalent.
- Paste/password managers/autofill/show-hide work.
- Secrets clear and never leak to telemetry/storage/DOM snapshots.
- Rate-limit, replay, CSRF, open redirect, policy change, concurrency, cross-tenant, and last-factor tests pass.
- Keyboard, screen reader, zoom, contrast, reduced-motion, and native tests pass.

## 14. Acceptance criteria

- Every password screen and adverse state is implemented end to end.
- `pwd` evidence is server-produced and visible with freshness/purpose.
- Reset and support flows never reveal account existence or passwords.
- Password managers, paste, accessibility, and native secure entry work.
- Users can transition away from passwords without lockout.

## 15. Dependencies

- Password verifier/hash and policy services.
- Reset artifact/delivery and session invalidation services.
- Compromised-password and notification integrations.
- Account lifecycle and authenticator inventory APIs.

## References

- [AMR screen support matrix](../../amr-screen-support-matrix.md)
- [Universal authenticator ceremony brief](../uix-pairing-briefs/40-authenticator-ceremony-api-universal-authenticator-pages-uix.md)
- [Canonical AMR vocabulary](../../../pkgs/10-concrete/tigrbl-jose-concrete/src/tigrbl_jose_concrete/amr.py)
