# Tenant Admin API + UIX Requirements Brief

**Pairing:** `tigrbl-auth-api-tenant-admin` + `@tigrbl-auth/tenant-admin-uix`  
**Status:** Delivery brief  
**Prepared:** July 11, 2026  
**API owner:** `pkgs/80-apis/tigrbl-auth-api-tenant-admin`  
**UIX owner:** `pkgs/95-ui/tenant-admin-uix`

## 1. Product Decision

Deliver this pairing as the delegated tenant control plane for tenant-local identities, administrators, OAuth/OIDC clients, consent grants, sessions, roles, signing-key activity, and audit posture.

The active tenant and effective administrator authority must remain visible throughout the experience. The UIX must never create, delete, or reassign tenants; cross-tenant and platform authority belong to Platform Admin. Service/workload identities belong to Service Admin.

## 2. Users and Jobs

### Primary users

- Tenant administrators managing one tenant.
- Delegated identity/help-desk operators with limited tenant permissions.
- Tenant security reviewers inspecting consent, sessions, keys, and audit state.

### Primary jobs

1. Create, update, lock, unlock, and remove tenant identities.
2. Delegate and review tenant-local administrative roles.
3. Register and maintain tenant OAuth/OIDC clients.
4. Review and revoke consent grants.
5. Review and revoke tenant sessions when supported.
6. Inspect tenant JWKS/key lifecycle and request rotation.
7. Review tenant-scoped audit events and operational posture.

## 3. API Boundary

The UIX consumes exactly one configured tenant-admin API base URL through `VITE_TIGRBL_AUTH_TENANT_ADMIN_API_BASE_URL`.

### Owned resources

- `User`
- `Client`
- `ClientRegistration`
- `Consent`
- `AuditEvent`
- `CryptoKey`
- `CryptoKeyVersion`
- `PrincipalKeyBinding`
- `KeyEnvelope`
- `KeyAttestationEvidence`
- `KeyRotationEvent`

Owned REST groups are `admin_auth` and `admin_identities`; the package also documents a tenant-filtered `/rpc` and `/openrpc.json` surface.

### Prohibited access

The UIX must fail closed on:

- `/tenant*` platform lifecycle operations and cross-tenant authority;
- service identities, service keys, and API keys;
- raw token, revoked-token, and authentication-session tables;
- public login, authorize, token, registration, logout, revocation, UserInfo, and introspection as tenant-admin operations;
- global discovery/JWKS as an administrative mutation surface.

Tenant-specific published discovery and JWKS may be linked for inspection, but private key material must never be exposed.

## 4. Required Experience

### Dashboard

- Show the current tenant, operator, effective authority, identity/client/consent counts, key activity, and required actions.
- Distinguish authoritative API-backed values from derived or unavailable information.
- Never present record counts as a security or compliance score.

### Identities

- Support create, inspect, update, lock, unlock, and delete within the current tenant.
- Show username, email, immutable ID, status, roles, administrator state, password-change requirement, and relevant activity when contracted.
- Prefer invite/onboarding flows over displaying or transmitting temporary passwords once the API supports invitations.
- Until then, temporary-password handling must be one-time, masked, excluded from logs/telemetry, and force change where configured.
- Separate account lock from deletion and explain session/access consequences.

### Groups and roles

- The current page derives role assignments from visible identity records; label it “Role assignments” unless first-class group resources exist.
- Do not offer group CRUD, nested groups, effective-policy calculation, or role assignment mutations without dedicated API operations.
- When delivered, show direct versus inherited roles, scope, grantor, timestamp, and effective authority.

### Clients

- Support create, inspect, update, and delete for tenant-local OAuth/OIDC clients.
- Validate redirect URIs, grant types, scopes, client type, and authentication method against the active profile and contract.
- Distinguish client metadata from registration metadata and credential material.
- Never reveal an existing client secret; newly issued secrets require one-time display and acknowledgment.
- Explain the login and integration impact of client deletion or redirect changes.

### Consents

- Show user, application, exact scopes, plain-language access, grant time, status, and recent use when supported.
- Confirm revocation with user/application/scope context rather than only an opaque consent ID.
- Explain whether revocation ends sessions or only future authorized access according to API behavior.

### Sessions

- The current page shows only the tenant administrator’s session and explicitly lacks tenant-wide listing/revocation paths.
- Label the current state as “Administrator session” rather than “Tenant sessions.”
- Add tenant-user session inventory and revocation only after dedicated tenant-filtered endpoints and authorization tests exist.
- Future session views must distinguish current/other sessions and prevent cross-tenant discovery.

### Key events and JWKS

- Preserve tenant key-rotation event review and tenant-scoped rotation requests.
- Show reason, state, actor, requested/completed time, affected key ID, publication status, and failure/recovery information where available.
- Link to the tenant’s published `jwks_uri` and show active/next/retired public keys without private material.
- Explain that requesting rotation is not equivalent to completed publication and propagation.

### Audit

- The current page is a tenant-scoped posture placeholder.
- Enable audit listing only after a filtered `AuditEvent` API view exists and proves tenant isolation.
- Show actor, action, target, outcome, timestamp, and correlation ID; redact credentials, tokens, personal data, and private claims.

### Routing and context

- Add stable member deep links for identity, client, consent, key event, and—when available—session/audit records.
- Keep tenant ID/name, environment, profile, and operator authority visible.
- Provide not-found, unauthorized, deleted, stale, and cross-scope denial states.

## 5. Security and Isolation Requirements

- Server-side authorization and tenant filtering are required for every collection, member lookup, count, search, and mutation.
- Never accept a client-selected tenant ID as sufficient authorization.
- Encode resource identifiers and reject paths outside the tenant-admin allowlist.
- Prevent privilege escalation: an administrator cannot grant authority beyond their own effective delegation.
- Require consequence review for identity lock/delete, admin-role change, client deletion, consent revocation, session revocation, and key rotation.
- Reconcile every mutation from authoritative API state and handle stale/precondition failures.
- Exclude passwords, client secrets, tokens, keys, session identifiers, emails, user IDs, consent values, and audit contents from analytics.
- Preserve safe correlation IDs and operator auditability.

## 6. Team Requirements

### Technical marketing

- Provide stable screenshots for tenant dashboard, identity lifecycle, client registration, consent, role assignments, and key rotation.
- Demonstrate tenant isolation and the separation between Platform Admin and Tenant Admin.
- Label groups/roles, sessions, and audit according to current implementation maturity.
- Avoid universal SCIM, IGA, session intelligence, or automated key-management claims unless separately evidenced.

### Developer relations

- Document isolated Docker startup, tenant administrator authentication/API key, OpenAPI/OpenRPC, seed/reset, and local tenant context.
- Provide tested examples for identity CRUD, client CRUD, consent revocation, and rotation request.
- Explain profile-driven client constraints and tenant discovery/JWKS inspection.
- Include troubleshooting for forbidden tenant lifecycle, cross-tenant denial, locked identity, invalid redirect, stale resource, and encoded IDs.

### Sales and account management

- Provide a resettable journey: inspect tenant → create identity → register client → review/revoke consent → request key rotation.
- Include “what this proves / what it does not prove” for roles, sessions, audit, provisioning, and key completion.
- Make delegated authority, tenant isolation, profile, version, and demo data visible.
- Avoid implying full workforce lifecycle, identity governance, or cross-tenant platform control.

### GTM strategy

- Position the pairing around delegated tenant operations, local identity/client control, and visible isolation.
- Track privacy-safe journey/action categories, outcomes, docs/evidence engagement, and handoff initiation.
- Never emit tenant, identity, client, consent, session, key, or audit values.
- Use one taxonomy for tenant identity, client, consent, delegated role, key rotation, and audit across campaigns and analytics.

### Copywriter

- Use “tenant,” “tenant administrator,” “identity,” “client application,” “consent grant,” “administrator session,” and “key rotation request” consistently.
- Explain lock, unlock, suspend, delete, revoke, rotate, publish, and retire as different actions.
- Write consequence-led confirmations with object, scope, impact, reversibility, and next step.
- Avoid “group management,” “all sessions,” or “audit log” where the current UI is derived or placeholder-only.

## 7. Frontend Engineering Instructions

1. Generate or validate typed REST/RPC clients against the tenant-admin contracts and preserve explicit path/method allowlists.
2. Centralize tenant context, effective-permission gates, auth/session handling, member routes, and safe mutation review.
3. Rename or maturity-label derived/placeholder navigation until dedicated APIs exist: Role assignments, Administrator session, and Audit posture.
4. Model identity, client, consent, and rotation lifecycles with explicit states and permitted actions.
5. Validate client fields from live contract/profile metadata rather than comma-separated free text alone.
6. Add member detail routes and server-backed search/filter/pagination before claiming operational scale.
7. Re-fetch affected collections/member records after mutations and handle concurrency/precondition errors.
8. Add cross-tenant leakage tests covering collections, member IDs, counts, search, errors, caches, and deep links.
9. Add privilege-escalation tests for administrator-role edits and self-impact warnings for operator lock/delete.
10. Maintain a legacy `admin-uix` parity map without importing platform or service administration into this client.

## 8. UIX Designer Instructions

- Use the shared operational console shell with persistent tenant, environment, profile, and authority context.
- Design dense collections and accessible mobile record views for identities, clients, consents, role assignments, key events, sessions, and audit.
- Distinguish active, locked, must-change-password, admin, revoked, pending rotation, published, failed, and unavailable without color alone.
- Make cross-scope limitations understandable without exposing forbidden resource existence.
- Design mutation reviews around before/after state, affected access, reversibility, and audit result.
- Include empty tenant, large tenant, partial data, unavailable feature, unauthorized action, stale link, and offline states.
- Validate keyboard interaction, focus restoration, live-region feedback, reduced motion, high zoom, and WCAG 2.2 AA.

## 9. Copy Deliverables

Produce a route-level copy deck containing:

- dashboard context and priority summaries;
- identity onboarding, temporary password, role, lock/unlock, and deletion language;
- client metadata, redirect, grant, scope, credential, and deletion explanations;
- consent scope translations and revocation consequences;
- administrator-session versus future tenant-session labels;
- key request/publication/propagation states;
- audit placeholder/current capability, unauthorized, stale, partial, empty, offline, and support copy.

## 10. Acceptance Criteria

- The UIX calls only the tenant-admin API base URL and rejects platform lifecycle, service, raw token/session, and public protocol paths.
- Every collection, count, detail, search, and mutation is tenant-filtered and tested against cross-tenant leakage.
- Identity and client CRUD, consent revocation, and key-rotation requests are explicit, permission-gated, consequence-led, and reconciled.
- Derived roles, administrator-only session, and audit placeholder are accurately labeled until dedicated APIs exist.
- Client configuration is validated against the active contract/profile, and secrets receive one-time safe handling.
- No operator or tenant-sensitive values reach analytics or unsafe UI output.
- Unit, API-boundary, isolation, privilege, accessibility, responsive visual, and end-to-end tests pass.
- Legacy admin parity work does not weaken product-surface separation.

## 11. Source Evidence

- `pkgs/80-apis/tigrbl-auth-api-tenant-admin/README.md`
- `pkgs/80-apis/tigrbl-auth-api-tenant-admin/src/tigrbl_auth_api_tenant_admin/contract.py`
- `pkgs/95-ui/tenant-admin-uix/README.md`
- `pkgs/95-ui/tenant-admin-uix/App.tsx`
- `pkgs/95-ui/tenant-admin-uix/services/tenantAdminClient.ts`
- `pkgs/95-ui/tenant-admin-uix/services/backendSurface.ts`
- `pkgs/95-ui/tenant-admin-uix/services/workflowCrud.test.ts`
- `pkgs/95-ui/tenant-admin-uix/pages/tenantCrudPages.test.tsx`
- `tests/packages/tigrbl-auth-api-tenant-admin/`
- `tests/unit/test_product_api_surfaces.py`
- Tenant-admin SSOT feature/claim/test/evidence/boundary records
