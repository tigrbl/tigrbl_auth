# Platform Admin API + UIX Requirements Brief

**Pairing:** `tigrbl-auth-backend-app-platform-admin` + `@tigrbl-auth/platform-admin-uix`<br>
**Status:** Delivery brief<br>
**Prepared:** July 11, 2026<br>
**Backend app owner:** `pkgs/90-backend-apps/tigrbl-auth-backend-app-platform-admin`<br>
**UIX owner:** `pkgs/105-ui/platform-admin-uix`

## 1. Product Decision

Deliver this pairing as the platform owner and operator control plane for realms, tenant lifecycle, platform identities, authority assignment, signing-key posture, and platform audit context.

It must make scope and consequence unmistakable. Operators should always know which environment, realm, tenant, identity, and authority level they are viewing before taking action. It is not a public login surface, tenant self-service console, developer client portal, or service-identity console.

## 2. Users and Jobs

### Primary users

- Platform owners and superusers.
- Identity/platform operators with explicitly delegated platform authority.
- Security and reliability reviewers inspecting platform posture.

### Primary jobs

1. Create and manage issuer realms.
2. Create, inspect, suspend, resume, update, and—where safe—delete tenants.
3. Inspect and manage platform-visible identities within their realm/tenant context.
4. Understand and assign platform versus tenant authority.
5. Review signing-key lifecycle and rotation posture.
6. Investigate platform-level changes and operational state.

## 3. API Boundary

The UIX consumes exactly one configured platform-admin API base URL through `VITE_TIGRBL_AUTH_PLATFORM_ADMIN_API_BASE_URL`.

### Owned resources

- `Realm`
- `Tenant`
- `User`
- `AuditEvent`
- `CryptoKey`
- `CryptoKeyVersion`
- `PrincipalKeyBinding`
- `KeyEnvelope`
- `KeyAttestationEvidence`
- `KeyRotationEvent`

Owned REST groups are `admin_auth`, `admin_realms`, and `admin_identities`.

### Prohibited access

The UIX must fail closed on:

- developer clients and client registrations;
- consent;
- service identities, service keys, and API keys;
- raw token, revoked-token, and authentication-session resources;
- public login, authorize, token, registration, logout, revocation, UserInfo, and introspection;
- public discovery/JWKS as administrative operations;
- tenant self-service routes outside the `/admin/*` control-plane boundary.

### Contract drift to resolve

The package README advertises `/rpc` and `/openrpc.json`, while the current `PLATFORM_ADMIN_BACKEND_APP_CONTRACT` lists both as forbidden. Until source, generated contracts, tests, and documentation agree, the frontend must treat the machine-readable contract as authoritative and must not depend on JSON-RPC. Delivery must either:

1. remove the stale README claims and keep the product REST-only; or
2. deliberately add the RPC surface to the contract, boundary tests, authorization model, generated docs, and UIX client.

No UI implementation may silently choose between these interpretations.

## 4. Required Experience

### Dashboard

- Summarize visible realms, tenants, active/suspended tenants, platform identities, authority gaps, key-rotation posture, and recent governed changes.
- Make partial or unavailable audit/key data explicit rather than converting resource counts into a health score.
- Prioritize required operator actions and link to the exact affected resource.

### Realms

- List, filter, create, inspect, edit, and delete realms where contracted.
- Show slug, issuer path, description, tenant count, administrator count, and lifecycle state.
- Validate issuer namespace uniqueness and explain the effect of issuer-path changes.
- Prevent deletion until dependent tenants, keys, and issuer commitments are understood and API preconditions pass.

### Tenants

- Treat tenant lifecycle as an explicit state model, not a boolean toggle hidden behind generic edit.
- Support create, inspect, update, suspend, resume, and delete only where the API supports each transition.
- Show owning realm, slug, contact, state, identities/administrators, issuer context, dependent resources, and recent lifecycle events.
- Require impact review and typed confirmation for destructive transitions.
- Distinguish suspension from deletion and state what continues to work during suspension.

### Platform identities

- Scope every identity to its tenant and realm.
- Support create, inspect, update, activate/suspend, and delete only through platform-authorized operations.
- Display authority, account state, tenant, realm, and immutable identifier.
- Never imply that platform identity CRUD is general tenant-user administration; detailed tenant-local workflows belong to Tenant Admin.

### Authority

- Visualize realm → tenant → administrator relationships.
- Distinguish platform owner/superuser authority from tenant administrator roles.
- Show effective authority, source, scope, and conflicts; do not rely on role-name strings alone for a permission decision.
- Mutating authority must include before/after scope, risk, and recovery path once the API owns that action.

### Key rotation

- Show current, next, retiring, and retired keys; algorithm, key ID, binding, publication status, creation/activation/retirement times, and rotation policy where available.
- Separate policy, requested rotation, generated material, publication, propagation, and retirement stages.
- Never expose private key or envelope material.
- The current UI page is a front door; enabled rotation controls require corresponding API operations and evidence.

### Audit and settings

- Replace the current posture placeholder with a filtered platform audit view only after the API exposes it.
- Show actor, action, target, scope, outcome, timestamp, and correlation ID without leaking secrets.
- Settings should expose safe runtime/product context, not dump the raw administrator session object.
- Provide environment, API base, build version, profile, and contract status in a sanitized support panel.

### Deep links and member routes

- Preserve direct realm, tenant, and identity member routes.
- Filter related records by authoritative IDs to prevent cross-realm and cross-tenant leakage.
- Provide clear not-found, unauthorized, deleted, and stale-link states.

## 5. Security and Operational Requirements

- Enforce authenticated administrator sessions and server-side authorization for every mutation.
- Never embed development API keys in production assets or telemetry.
- Derive available actions from effective permissions and resource state, not UI role-name checks alone.
- Encode resource identifiers and reject paths outside the platform-admin allowlist.
- Require review screens for realm/tenant deletion, tenant suspension, authority change, identity deletion, and key rotation.
- Display optimistic progress but reconcile from authoritative API state after mutations.
- Prevent cross-realm and cross-tenant data leakage in collections, member pages, search, counts, and error messages.
- Redact credentials, tokens, private keys, envelopes, attestation secrets, and raw session material.
- Preserve audit correlation for all security-sensitive actions.

## 6. Team Requirements

### Technical marketing

- Provide stable screenshots for realm topology, tenant lifecycle, authority, key posture, and platform dashboard.
- Demonstrate separation between platform, tenant, developer, service, and public surfaces.
- Describe key rotation and audit only to the level supported by current API operations and evidence.
- Use a named seeded environment and label all repository-checkpoint capabilities.

### Developer relations

- Document isolated Docker startup, administrator session/API-key setup, OpenAPI access, seed/reset, and safe teardown.
- Provide tested examples for realm and tenant creation, tenant suspension/resume, member deep links, and failure preconditions.
- Explain the contract/README RPC discrepancy until resolved.
- Include troubleshooting for authorization failure, locked tenant, stale member route, identifier encoding, and cross-scope visibility.

### Sales and account management

- Provide a guided scenario: create realm → create tenant → assign/inspect authority → suspend/resume tenant → review posture.
- Include “what this proves / what it does not prove” for lifecycle, audit, key rotation, and delegated administration.
- Produce a printable environment summary with tenancy model, profile, storage/runtime context, release state, and known gaps.
- Avoid implying a hosted control plane, universal IGA, or complete key-management system.

### GTM strategy

- Position the pairing around multi-tenant identity operations and visible authority boundaries.
- Track privacy-safe scenario completion, lifecycle action category/outcome, contract/help engagement, and handoff initiation.
- Never emit tenant, realm, identity, issuer, contact, key, or audit values to analytics.
- Preserve role/use-case context in demo deep links without carrying administrator credentials.

### Copywriter

- Use “realm,” “tenant,” “platform identity,” “tenant administrator,” and “platform owner” consistently.
- Explain create, suspend, resume, delete, rotate, retire, assign, and revoke as distinct actions.
- Write consequence-led confirmations naming affected scope, dependencies, reversibility, and follow-up.
- Avoid “healthy,” “secure,” “compliant,” or “fully isolated” unless the displayed evidence supports that exact scoped statement.

## 7. Frontend Engineering Instructions

1. Resolve REST/RPC contract drift before depending on RPC in the UIX.
2. Generate or validate typed clients against the platform-admin OpenAPI contract and retain explicit path allowlists.
3. Model realm, tenant, identity, and key lifecycles as explicit states and permitted transitions.
4. Centralize authenticated routing, effective-permission gates, environment context, member routes, and safe mutation review.
5. Replace global error toasts and end-of-page loading errors with route-specific skeleton, stale, partial, and retry states.
6. Replace raw session JSON with a sanitized, typed operator-context view.
7. Re-fetch affected collections/member records after every mutation and handle concurrency/precondition failures.
8. Add server-backed pagination, filtering, and search before claiming high-scale platform operations.
9. Add cross-realm/cross-tenant leakage tests for data, counts, member links, search, errors, and cached state.
10. Maintain a legacy `admin-uix` parity map; do not import cross-boundary legacy client behavior into this package.

## 8. UIX Designer Instructions

- Use the shared operational console shell with persistent environment and authority context.
- Visualize realm/tenant hierarchy and lifecycle without turning the interface into an infrastructure graph by default.
- Design dense collections plus accessible mobile record views for realms, tenants, identities, keys, and audit events.
- Use distinct, non-color-only treatments for active, suspended, pending, retiring, retired, failed, and unavailable states.
- Design mutation reviews around before/after state, affected resources, reversibility, and audit outcome.
- Provide layouts for empty platform, single realm, many realms/tenants, partial API data, forbidden scope, and stale deep links.
- Validate keyboard navigation, focus restoration, live-region feedback, reduced motion, high zoom, and WCAG 2.2 AA.

## 9. Copy Deliverables

Produce a route-level copy deck containing:

- dashboard summaries and action priorities;
- realm/tenant creation, issuer-path, lifecycle, suspension, resume, and deletion language;
- identity and authority labels, help, empty states, and safe mutation confirmations;
- key lifecycle and rotation-stage explanations;
- audit placeholder/current capability, filtering, result, and correlation language;
- environment, contract drift, unauthorized, not-found, stale, partial, offline, and support copy.

## 10. Acceptance Criteria

- The UIX calls only the platform-admin API base URL and rejects forbidden public, tenant-self-service, developer, service, token, and session paths.
- REST/RPC documentation and machine-readable contracts agree before release.
- Realm, tenant, and identity member routes preserve scope and do not leak cross-realm or cross-tenant data.
- Tenant lifecycle actions are explicit, permission-gated, consequence-led, and reconciled from the API.
- Authority views distinguish platform and tenant scope and never infer permission solely from presentation labels.
- Key and audit screens enable only contracted operations and clearly label partial/read-only states.
- Sensitive operator, credential, key, session, and audit values never reach analytics or unsafe UI output.
- Unit, contract, boundary, accessibility, responsive visual, and end-to-end operator tests pass.
- Legacy admin parity is tracked without weakening the separated product boundary.

## 11. Source Evidence

- `pkgs/90-backend-apps/tigrbl-auth-backend-app-platform-admin/README.md`
- `pkgs/90-backend-apps/tigrbl-auth-backend-app-platform-admin/src/tigrbl_auth_backend_app_platform_admin/contract.py`
- `pkgs/105-ui/platform-admin-uix/README.md`
- `pkgs/105-ui/platform-admin-uix/App.tsx`
- `pkgs/105-ui/platform-admin-uix/services/platformAdminClient.ts`
- `pkgs/105-ui/platform-admin-uix/services/workflowCrud.test.ts`
- `pkgs/105-ui/platform-admin-uix/pages/platformCrudPages.test.tsx`
- `tests/packages/tigrbl-auth-backend-app-platform-admin/`
- `tests/unit/test_product_api_surfaces.py`
- Platform-admin SSOT feature/claim/test/evidence/boundary records
