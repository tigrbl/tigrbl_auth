# My Account API + UIX Requirements Brief

**Pairing:** `tigrbl-auth-backend-app-my-account` + `@tigrbl-auth/my-account-uix`<br>
**Status:** Delivery brief<br>
**Prepared:** July 11, 2026<br>
**Backend app owner:** `pkgs/90-backend-apps/tigrbl-auth-backend-app-my-account`<br>
**UIX owner:** `pkgs/105-ui/my-account-uix`

## 1. Product Decision

Deliver this pairing as the authenticated end user’s self-service identity center. It must help the current subject understand and control their profile, password, sessions, authorized applications, and consent grants without exposing tenant-wide resources or administrator operations.

The experience should feel like a continuation of the public hosted-login surface: personal, clear, calm, and slightly denser than an authentication form. It is not a tenant directory, help-desk impersonation tool, or platform console.

## 2. Users and Jobs

### Primary user

An authenticated human subject managing only their own account.

### Primary jobs

1. Review account identity and security posture.
2. Update permitted profile attributes.
3. Change a password safely, including a forced-change condition.
4. Recognize and revoke active sessions.
5. Understand and revoke authorized applications or individual consent grants.
6. Recover gracefully when the public issuer session is missing or expired.

## 3. API Boundary

The UIX consumes exactly one My Account API base URL and sends authenticated requests with browser credentials.

### Owned endpoints

| Method and path | UI responsibility |
|---|---|
| `GET /account/profile` | Establish the current-subject session and render account context. |
| `PATCH /account/profile` | Update only API-permitted profile fields. |
| `POST /account/password/change` | Change the current subject’s password with safe validation and feedback. |
| `GET /account/sessions` | List recognizable sessions with privacy-safe device/activity context. |
| `DELETE /account/sessions/{session_id}` | Revoke a selected session after impact confirmation. |
| `GET /account/authorized-apps` | List applications with current account authorization. |
| `DELETE /account/authorized-apps/{client_id}` | Revoke the application’s account authorization. |
| `GET /account/consents` | List consent grants and scopes. |
| `DELETE /account/consents/{consent_id}` | Revoke an individual consent grant. |

Discovery and JWKS may support session/runtime context, but are not account mutations.

### Prohibited access

The client must fail closed on:

- platform, tenant, user-directory, client-directory, and service-identity administration;
- API-key, service-key, cryptographic-key, key-envelope, and attestation resources;
- raw token, authentication-session, and audit-event tables;
- public login, authorize, token, registration, logout, revocation, UserInfo, and introspection endpoints as My Account operations;
- JSON-RPC and generic table CRUD.

Unauthenticated users must be handed to the public hosted-login surface rather than implementing a second login client inside My Account.

## 4. Required Experience

### Overview

- Summarize profile status, required security action, active sessions, authorized applications, and consent grants.
- Prioritize urgent conditions such as `must_change_password`, inactive account state, or an expired session.
- Use counts as navigation aids, not as security scores.

### Profile

- Show immutable subject and tenant context separately from editable username/email fields.
- Explain which changes may require reverification or affect sign-in.
- Detect unsaved changes, validate before submit, and prevent accidental double submission.
- Never imply that editing a profile changes roles, tenant membership, or administrator authority.

### Security

- Require current password and a validated new password for the existing change endpoint.
- Explain forced password change and what happens to other sessions, only according to contracted behavior.
- Support paste and password-manager workflows; do not obstruct password managers.
- Add passkeys, MFA factors, recovery methods, or passwordless controls only after My Account API contracts own those operations.

### Sessions

- Show current versus other sessions clearly.
- Present privacy-safe device/browser, approximate location only if trustworthy and permitted, created time, last activity, and expiry where available.
- Confirm revocation with the affected device/session and expected consequence.
- If revoking the current session is supported, warn that the user will be signed out and return through Public UIX.

### Authorized applications and consent

- Distinguish application authorization from individual consent grants.
- Show application name, client identifier in details, granted scopes in plain language, grant time, and recent use when supported.
- Explain the difference between revoking an app and revoking one consent.
- After revocation, refresh both application and consent state and show what access may remain.

### Missing or expired session

- Show a clear “account session required” state.
- Offer “Continue to hosted login” and “Retry account session.”
- Preserve only a safe return target; do not persist sensitive account state in the URL.

Every page must cover initial, loading, empty, partial-data, validation-error, mutation-error, unauthorized, expired-session, success, and retry states.

## 5. Security and Privacy Requirements

- Every operation must derive the subject from the authenticated session, never from a user-supplied subject ID.
- Encode session, client, and consent path identifiers before requests.
- Use same-origin credentials and the repository’s session/CSRF model; never store bearer or refresh tokens in UIX persistence.
- Do not expose password values, credential material, raw session cookies, or unnecessary claims in logs or telemetry.
- Treat session metadata as personal data; reveal only what helps recognition and control.
- Use typed confirmations for account-wide or current-session revocation if supported.
- Normalize errors into safe user language while retaining a correlation ID for support.
- Prevent cached authenticated content from flashing after logout or session expiry.

## 6. Team Requirements

### Technical marketing

- Provide stable screenshots for overview, profile, security, session management, and authorized apps.
- Demonstrate continuity from Public UIX login into My Account without presenting them as one API surface.
- Frame the product outcome as end-user control and transparency, not tenant administration.
- Qualify claims about MFA, passkeys, recovery factors, activity, and session intelligence by release/API support.

### Developer relations

- Document the public-login → My Account session handoff, cookie/CSRF expectations, API base configuration, and local demo reset.
- Provide examples for reading/updating profile and revoking a session, app, and consent.
- Explain the semantic difference between application authorization and consent records.
- Include expected `401`, expired-session, stale-resource, and already-revoked behavior.

### Sales and account management

- Provide a seeded, resettable user story showing profile edit, password change, multiple sessions, and app/consent revocation.
- Make “current-subject only” visible as a security boundary and sales proof point.
- Include a concise “what this proves / what it does not prove” summary.
- Do not imply help-desk administration, identity governance, or device-risk analytics unless separately delivered.

### GTM strategy

- Position this pairing around user trust, self-service, session visibility, and consent control.
- Track privacy-safe route, flow completion, non-sensitive error category, and help/evidence engagement.
- Do not send subject, tenant, session, client, consent, email, or scope values to analytics.
- Preserve use-case campaign context only outside authenticated account data.

### Copywriter

- Write in the second person and distinguish “your account,” “this session,” “this application,” and “this consent.”
- Explain revoke, sign out, remove access, password change, and profile change consequences precisely.
- Provide empty-state guidance that does not suggest a security problem when no apps or additional sessions exist.
- Avoid “secure account,” “trusted device,” or “suspicious session” unless backed by an explicit evaluation signal.

## 7. Frontend Engineering Instructions

1. Keep `GET /account/profile` as the session bootstrap and current-subject authority.
2. Centralize authenticated routing, session-expiry handling, hosted-login handoff, safe return targets, and request credentials.
3. Replace toast-only page loading with accessible page skeletons or progress states; reserve toasts for transient outcomes.
4. Standardize mutations as review → submit → success/failure → data refresh, with duplicate-action protection.
5. Reconcile app and consent state after either type of revocation.
6. Detect and label the current session using contracted evidence rather than assumptions based on list order.
7. Add boundary tests proving all mutations remain under `/account/*` and forbidden paths cannot be requested.
8. Add deterministic tests for identifier encoding, expired sessions, stale resources, repeated revocation, and partial list failures.
9. Use shared `@tigrbl-auth/uix-core` shells, forms, tables, confirmation dialogs, problem details, copy controls, and responsive record views.

## 8. UIX Designer Instructions

- Extend the Public UIX visual language into a denser self-service shell.
- Keep account identity and current session visible without making the product feel like an admin console.
- Design sessions and apps as recognizable records on mobile and accessible tables on wider screens.
- Make current session, inactive account, forced password change, revoked state, and consent status understandable without color alone.
- Design confirmations around object, consequence, reversibility, and next sign-in behavior.
- Validate focus restoration, error association, live-region mutation feedback, reduced motion, high zoom, and WCAG 2.2 AA contrast.

## 9. Copy Deliverables

Produce a route-level copy deck containing:

- overview summaries and priority notices;
- profile labels, validation, reverification implications, and save feedback;
- password requirements, forced-change language, and safe errors;
- session recognition, current-session labels, expiry, and revocation confirmations;
- app and consent scope explanations, revocation differences, and post-action outcomes;
- unauthenticated/expired-session handoff, retry, offline, empty, partial, and support-correlation copy.

## 10. Acceptance Criteria

- Every API call is current-subject scoped and uses only the My Account API base URL.
- The UI cannot enumerate or mutate another user, tenant, client directory, service identity, key, raw token/session, or audit table.
- Overview, profile, security, sessions, and authorized apps/consents have complete accessible states.
- Profile and password mutations validate, prevent duplicate submission, and refresh authoritative state.
- Session, app, and consent revocations explain impact, encode identifiers, confirm intent, and reconcile the UI afterward.
- Missing/expired sessions hand off safely to Public UIX without exposing account data.
- No credentials, account identifiers, session metadata, or consent details reach analytics.
- Unit, API-boundary, accessibility, responsive visual, and end-to-end self-service tests pass.

## 11. Source Evidence

- `pkgs/90-backend-apps/tigrbl-auth-backend-app-my-account/README.md`
- `pkgs/90-backend-apps/tigrbl-auth-backend-app-my-account/src/tigrbl_auth_backend_app_my_account/contract.py`
- `pkgs/105-ui/my-account-uix/README.md`
- `pkgs/105-ui/my-account-uix/App.tsx`
- `pkgs/105-ui/my-account-uix/services/myAccountClient.ts`
- `pkgs/105-ui/my-account-uix/services/workflowCrud.test.ts`
- `pkgs/105-ui/my-account-uix/pages/myAccountCrudPages.test.tsx`
- My Account API product-boundary tests and SSOT feature/claim/test/evidence records
