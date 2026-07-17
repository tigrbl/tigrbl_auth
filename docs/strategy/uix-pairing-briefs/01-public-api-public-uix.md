# Public Identity API + UIX Requirements Brief

**Pairing:** `tigrbl-auth-backend-app-public` + `@tigrbl-auth/public-uix`<br>
**Status:** Delivery brief<br>
**Prepared:** July 11, 2026<br>
**Backend app owner:** `pkgs/90-backend-apps/tigrbl-auth-backend-app-public`<br>
**UIX owner:** `pkgs/105-ui/public-uix`

## 1. Product Decision

Deliver this pairing as the hosted public identity front door for Tigrbl Auth. It must let an end user authenticate, register, recover access, satisfy additional verification, review consent, complete an OAuth/OIDC redirect, and sign out without exposing administrative authority or requiring protocol knowledge.

The experience should feel trustworthy, calm, brandable, and precise. It is not an account-administration console, developer portal, or generic API explorer.

## 2. Users and Jobs

### Primary users

- End users signing into a relying-party application.
- New users creating an identity where registration is enabled.
- Returning users recovering access or completing MFA/email verification.
- Users reviewing requested OAuth/OIDC consent.

### Primary jobs

1. Understand which issuer and application are requesting authentication.
2. Sign in or register safely.
3. Complete MFA, verification, recovery, or consent when required.
4. Return to the requesting application with a clear success or failure outcome.
5. End the identity session deliberately.

## 3. API Boundary

The UIX consumes exactly one configured public API base URL through `VITE_TIGRBL_AUTH_PUBLIC_BASE_URL`.

### Baseline-profile capabilities

- Login
- Authorization
- Token exchange
- OpenID Provider configuration
- Tenant OpenID Provider configuration
- OAuth authorization-server metadata
- Global and tenant JWKS

### Production-profile additions

- UserInfo
- Introspection
- Client registration and registration management
- Revocation
- Logout
- OAuth protected-resource metadata

Capability visibility must be derived from the active runtime profile and discovery/OpenAPI contracts. A route or button must not appear merely because a React page exists.

### Prohibited access

The client must fail closed on:

- `/admin*`
- cryptographic key administration resources
- `/tenant` and `/tenant/*` lifecycle administration
- `/diagnostics*`
- `/rpc`

Public tenant discovery and tenant JWKS are allowed; tenant administration is not.

## 4. Required Experience

### Routes and states

| Route/flow | Requirement |
|---|---|
| Login | Password and enabled provider choices, requesting-app context, recovery and registration links, safe errors. |
| Registration | Validated fields, password guidance, terms acknowledgment, verification handoff, disabled state when unsupported. |
| Callback | Normalize callback location, validate transaction context, show progress, recover safely from invalid/expired state. |
| MFA | Identify the required factor without disclosing sensitive policy; support retry, alternative factor, and cancellation when contracted. |
| Email verification | Verify, resend with rate-limit feedback, change-address guidance, and expiry recovery. |
| Forgot/reset password | Enumeration-safe request response, token expiry handling, password validation, and return-to-login path. |
| Consent | Show application identity, requested scopes in plain language, existing versus new access, approve and deny outcomes. |
| Profile/session continuation | Show minimal authenticated identity and route richer self-service to My Account. |
| Logout | Explain local versus provider/session logout, perform contracted logout, and honor only allowlisted redirect targets. |
| Terms | Deployment-owned legal content with version/date; no hard-coded claims that exceed the configured service. |

Every route must cover initial, loading, validation-error, API-error, offline, expired-session, unsupported-capability, success, and cancellation states.

### Trust and context

The UI must show, where applicable:

- issuer or tenant brand;
- requesting application name and verified redirect context;
- current action and reason for any step-up;
- requested scopes translated into user outcomes;
- a safe way to inspect technical details without showing secrets or tokens.

Never ask users to trust a raw `client_id`, redirect URL, or protocol error as the primary explanation.

## 5. Security and Privacy Requirements

- Preserve the implemented cookie-session, CSRF, browser-token, origin, redirect, and safe-error boundaries.
- Use authorization code with PKCE for browser journeys; do not accept or store browser client secrets.
- Validate `state`, `nonce`, issuer, redirect target, and callback transaction context where owned by the browser client.
- Never place access tokens, refresh tokens, passwords, reset tokens, authorization codes, or private claims in analytics, logs, URLs beyond protocol-required transient parameters, or persistent browser storage.
- Password recovery responses must not reveal whether an identity exists.
- Consent must not use preselected approval or misleading button hierarchy.
- Errors shown to end users must be actionable and sanitized; correlation IDs may be exposed for support.
- Legal and privacy content must be deployment-configurable and versioned.

## 6. Team Requirements

### Technical marketing

- Provide stable screenshot states for login, registration, consent, MFA, recovery, and successful return.
- Supply a demonstrable “hosted login to protected profile” journey with sanitized protocol detail.
- Associate every standards/capability statement with its profile and release maturity.
- Avoid universal federation, passwordless, MFA, or compliance claims when the selected profile does not expose them.

### Developer relations

- Provide a five-minute local journey: start public API/UIX, inspect discovery, register/select a client, complete authorization code + PKCE, and observe callback success.
- Include copyable discovery, authorization, callback, logout, and troubleshooting examples.
- Document expected redirect URI, cookies, local TLS exception, seeded credentials, reset steps, and common `state`/issuer/redirect failures.
- Link directly to public OpenAPI and OIDC discovery from an expert/help panel.

### Sales and account management

- Provide a resettable demo showing brand/tenant context, login, consent, MFA or verification, callback, and logout.
- Include “what this proves” and “not demonstrated” notes for each scenario.
- Make release, profile, deployment mode, and demo-data status visible.
- Provide a shareable scenario URL that contains no credentials or transaction secrets.

### GTM strategy

- Position the pairing around hosted identity and safe OAuth/OIDC journeys, not broad IAM administration.
- Instrument privacy-safe events for flow started/completed/cancelled, route family, non-sensitive error category, docs opened, and demo reset.
- Preserve campaign/use-case context through the demo without mixing it into OAuth transaction state.
- Use the same taxonomy for public identity, hosted login, registration, recovery, consent, and federation across campaigns and analytics.

### Copywriter

- Write concise, reassuring transaction copy that names the application and requested action.
- Translate scopes into user-understandable access statements while preserving exact scope names in optional details.
- Produce safe copy for unknown identity, invalid password, expired transaction, blocked redirect, consent denial, rate limiting, and unavailable provider.
- Avoid “secure,” “compliant,” “passwordless,” or “single sign-on” as unqualified claims; state the exact behavior and profile.

## 7. Frontend Engineering Instructions

1. Keep the generated public OpenAPI and OIDC discovery documents authoritative for endpoint and capability availability.
2. Centralize routes, auth guards, callback normalization, redirect allowlisting, and capability gates.
3. Move reusable cards, fields, buttons, validation, problem details, brand configuration, and auth shell behavior into `@tigrbl-auth/uix-core` without lowering current visual quality.
4. Replace route-level `null` rendering during redirects with accessible progress states that prevent flashes of protected or incorrect content.
5. Model authentication as an explicit state machine covering anonymous, authenticating, MFA pending, verification pending, consent pending, authenticated, callback processing, recovery, error, and logout.
6. Keep My Account as the owner of extended profile, session, consent, and security-method administration.
7. Add redaction and boundary tests proving that forbidden paths cannot be requested by the client.
8. Add deterministic end-to-end fixtures for success and representative OAuth/OIDC failures.

## 8. UIX Designer Instructions

- Preserve the current hosted-identity direction: calm neutral background, focused white card, deployment brand accent, clear hierarchy, and restrained motion.
- Design responsive states for every route at desktop, tablet, and narrow mobile widths.
- Keep issuer, tenant, application, and transaction purpose visible without crowding the primary action.
- Give approve and deny actions honest visual weight; do not dark-pattern consent.
- Design progressive disclosure for exact scopes, issuer, redirect, and sanitized protocol details.
- Validate focus order, focus restoration, screen-reader announcements, error association, reduced motion, high zoom, and WCAG 2.2 AA contrast.

## 9. Copy Deliverables

Produce a route-level copy deck containing:

- headings, introductions, labels, help, validation, primary/secondary actions;
- loading, empty, unsupported, error, retry, expiry, cancellation, and success messages;
- consent scope explanations and technical-detail labels;
- recovery enumeration-safe language;
- profile/release caveats and demo labeling;
- tenant-brand placeholders and legal-content requirements.

## 10. Acceptance Criteria

- The public UIX calls only the public API base URL and rejects prohibited surface paths.
- Capability visibility matches the active profile and live contracts.
- Authorization code + PKCE works end to end with safe callback and redirect handling.
- Login, registration, MFA, verification, recovery, consent, profile continuation, and logout have complete accessible states or are omitted when unsupported.
- No secrets or sensitive transaction values reach telemetry or persistent browser storage.
- Primary journeys pass unit, contract, accessibility, responsive visual, and end-to-end tests.
- Demo fixtures reset deterministically and have a static fallback.
- Claims shown in UI or collateral identify their applicable profile and release maturity.

## 11. Source Evidence

- `pkgs/90-backend-apps/tigrbl-auth-backend-app-public/README.md`
- `pkgs/90-backend-apps/tigrbl-auth-backend-app-public/src/tigrbl_auth_backend_app_public/contract.py`
- `pkgs/90-backend-apps/tigrbl-auth-backend-app-public/src/tigrbl_auth_backend_app_public/openapi.py`
- `pkgs/105-ui/public-uix/README.md`
- `pkgs/105-ui/public-uix/App.tsx`
- `pkgs/105-ui/public-uix/services/publicRouting.ts`
- `pkgs/105-ui/public-uix/services/publicUxPolicy.ts`
- `tests/unit/test_public_route_contracts.py`
- `tests/unit/test_public_operator_surface_boundary.py`
- `tests/uix/` public UIX boundary and browser-security coverage
- SSOT public API/UIX features, claims, tests, evidence, boundaries, and release records
