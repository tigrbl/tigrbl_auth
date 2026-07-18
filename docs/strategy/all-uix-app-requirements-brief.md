# Tigrbl Auth All-UIX Application Requirements Brief

**Status:** Delivery brief for product, frontend, UIX design, and copy  
**Prepared:** July 11, 2026  
**Scope:** Every UIX and browser-facing integration surface in `tigrbl_auth`  
**Repository checkpoint:** `0.4.0.dev2`  
**Public distribution baseline:** PyPI `tigrbl-auth` `0.3.4`; no reviewed `@tigrbl-auth/*` npm package is publicly available

## 1. Decision

Enhance all Tigrbl Auth UIX as one coherent identity product portfolio while preserving the strict boundary between each UIX and its paired API. Do not turn the separated applications into one privileged universal console. Share design language, components, terminology, telemetry, and evidence conventions through `@tigrbl-auth/uix-core`; keep data access, permissions, routes, and workflows product-specific.

The delivery has ten distinct workstreams:

1. Shared UIX core and system behavior
2. Public identity UIX
3. My Account UIX
4. Platform Admin UIX
5. Tenant Admin UIX
6. Developer UIX
7. Service Admin UIX
8. Resource Validation experience
9. Demo Hub UIX
10. Legacy Admin extraction and retirement, including browser RP integration guidance

The primary product outcome is that an evaluator can move from a credible demonstration to the correct working surface without encountering placeholder screens, ambiguous authority, unsupported actions, or claims that exceed the installed release.

## 2. Evidence and Release Baseline

### Repository truth reviewed

- Product APIs: public, my-account, platform-admin, tenant-admin, developer, service-admin, and resource-validation.
- UI workspaces: shared core, public, my-account, platform-admin, tenant-admin, developer, service-admin, legacy admin, demo hub, and browser RP SDK.
- Interactive tooling: REST/OpenAPI, JSON-RPC/OpenRPC, discovery metadata, operator CLI, Docker Compose, demo hub, and the `acme_notes_cli` device-flow example.
- Runtime profiles: `baseline`, `baseline-development`, `production`, `hardening`, `fapi2-security`, and `peer-claim`.
- SSOT inventory: 1,160 features (824 implemented, 48 partial, 288 absent), 1,766 claims, and 11 release records. Ten registry releases are internally marked `published`; these are governed checkpoints, not automatically public package publications.
- UIX-related feature slice: 72 implemented, 13 partial, and 9 absent records matched by UIX/demo/browser-RP identifiers.

### Public release truth reviewed

- PyPI reports `tigrbl-auth` `0.3.4` as the latest stable release and `0.4.0.dev2` as an available prerelease.
- GitHub Releases publishes the split `tigrbl-identity-*==0.4.0.dev2` packages as prereleases dated May 22, 2026.
- npm returned `404 Not Found` for the reviewed `@tigrbl-auth/rp`, `@tigrbl-auth/uix-core`, `@tigrbl-auth/public-uix`, and `@tigrbl-auth/admin-uix` packages. Treat all UIX npm install instructions as future work until publication is verified.
- Current repository documentation still prohibits “fully compliant,” “independently certified,” and equivalent global claims.

### Required maturity language

Every UI capability, demo step, help link, screenshot, and sales narrative must use one of these states:

| State | Meaning |
|---|---|
| Public stable | Available in a verified public stable artifact. |
| Public prerelease | Available in a verified public prerelease. |
| Repository checkpoint | Implemented and evidenced in the reviewed repository, but not verified in a stable public artifact. |
| Partial | Boundary or workflow exists but lacks parity, complete behavior, or production proof. |
| Planned | Governed but absent; never render as an enabled action. |
| Deprecated | Retained only for migration or extraction. |

Internal SSOT `published` must never be presented as public package availability without registry evidence.

## 3. Portfolio Requirements

### Product architecture

Each UIX must consume exactly one product API base URL. Cross-surface navigation may link to another UIX, but must not call that UIX's API from the current client. The resource-validation API must receive a dedicated experience rather than remaining only an unlabeled link in the demo hub.

Use shared concepts consistently:

- **Realm:** issuer namespace above tenants.
- **Tenant:** isolated administrative and identity scope.
- **Human identity:** user or administrator subject.
- **Service identity:** non-human workload principal.
- **Application/client:** OAuth or OIDC relying party registration.
- **Profile:** selectable runtime/security posture, not a universal certification badge.
- **Evidence:** trace from capability to claim, test, artifact, boundary, and release.

### Shared functional requirements

All applications must provide:

- authenticated, unauthenticated, unauthorized, expired-session, loading, empty, partial-data, network-error, and retry states;
- route-level deep links and predictable browser back/forward behavior;
- explicit current realm, tenant, subject, profile, environment, API base, and release/checkpoint context where applicable;
- confirmation plus impact summary for destructive or security-sensitive mutations;
- masked secrets with one-time reveal semantics and copy feedback;
- copy controls for IDs, issuers, URLs, key IDs, scopes, audiences, and snippets;
- accessible tables that collapse into labeled records on narrow screens;
- audit correlation IDs and safe error details without tokens, credentials, or sensitive claims;
- keyboard-complete interaction, visible focus, reduced-motion support, 200% zoom support, and WCAG 2.2 AA targeting;
- a stable demo/seed state and static fallback for every primary journey;
- no analytics collection of secrets, tokens, identifiers, request bodies, or user-entered values.

### Shared visual requirements

Use the public UIX visual direction as the source language: calm neutral backgrounds, white surfaces, a deployment brand accent, clear typography, restrained shadows, consistent radii, visible validation, and purposeful motion. Operational consoles should be denser than hosted identity pages without becoming raw database browsers.

`@tigrbl-auth/uix-core` must own tokens and canonical implementations for auth/app shells, navigation, page headers, cards, forms, tables, detail panels, status/maturity badges, confirmation dialogs, secret/copy controls, JSON and protocol viewers, toasts, skeletons, error/empty states, filters, pagination, and responsive behavior.

## 4. Stakeholder Requirements

### Technical marketing

- Needs stable, named screenshot states for each UIX and five end-to-end narratives: hosted login, app registration, tenant administration, workload identity, and API validation.
- Each screenshot and capability caption must carry surface, profile, version, maturity, and last-reviewed metadata.
- Provide a safe “show the protocol” layer for technically credible campaigns without exposing secrets.
- Supply reusable visual diagrams showing the seven API/UIX boundaries as one system.

### Developer relations

- Needs copyable, tested quickstarts that land in a visible UI result and explain expected behavior.
- Each UIX must expose its OpenAPI/OpenRPC/discovery source, configured endpoint, version, and a troubleshooting path.
- Demo actions require reset instructions, example inputs, expected output, representative failure cases, and productionization notes.
- Browser RP examples must show PKCE, state/nonce handling, callback, session, logout, and the prohibition on browser client secrets.

### Sales and account management

- Needs a role-based demo launcher and shareable scenario URLs that do not require explaining package topology.
- Each surface needs a concise “what this proves / what it does not prove” panel.
- Deployment, storage, profile, tenancy, integration, security, and release context must be visible in printable evaluation summaries.
- Partial and planned workflows must be obvious before a customer demonstration.

### GTM strategy

- Needs one canonical taxonomy across navigation, events, campaigns, demo steps, and sales summaries.
- Instrument privacy-safe events for journey start/completion, non-sensitive action outcome, docs/contract opened, copy control used, evidence opened, and handoff initiated.
- Preserve use case, UIX surface, profile, and version in deep links and contact handoff context.
- Messaging modules may change independently; product truth and maturity state may not.

### Copywriter

- Write observable outcomes and role-appropriate instructions, not generic “enterprise-grade” claims.
- Explain acronyms on first use and distinguish human identities, service identities, clients, realms, and tenants.
- Supply page introductions, field help, confirmation impact, empty/loading/error/recovery copy, demo narration, glossary, and maturity tooltips.
- Use “supports,” “implements,” or “provides” only with the applicable release/profile state. Use “aligned with” for OAuth 2.1. Reserve “certified” for a visible, scoped certified claim.

## 5. Unique Application Briefs

### A. Shared UIX Core (`@tigrbl-auth/uix-core`)

**Users:** all UIX teams and downstream integrators.  
**Job:** make every surface consistent without weakening API boundaries.

Required delivery:

- Move duplicated public and console primitives into core and publish a documented token/component contract.
- Add `MaturityBadge`, `EnvironmentBanner`, `ContextSwitcher`, `ProtocolDrawer`, `SecretField`, `CopyButton`, `ProblemDetails`, `AuditReference`, `MutationReview`, and responsive resource patterns.
- Centralize routing helpers, auth guards, safe error normalization, redaction, telemetry event schemas, and brand/theme configuration.
- Provide Storybook-equivalent component states or a local component gallery; include light/dark/high-contrast validation if themes are supported.
- Version core independently and define compatibility with each UIX. Do not claim npm installation until the package exists publicly.

Acceptance: every non-legacy UIX consumes core for shared primitives; no local component fork changes common behavior; accessibility and visual regression tests cover every primitive state.

### B. Public Identity UIX (`@tigrbl-auth/public-uix` → public API)

**Users:** end users authenticating or granting consent.  
**Job:** complete identity flows with clear trust, tenant branding, and safe recovery.

Required routes/workflows:

- Login, registration, authorization callback, consent, MFA, email verification, forgot/reset password, profile/session continuation, and logout.
- Preserve the implemented browser protections: cookie session model, CSRF protection, safe token handling, origin/redirect constraints, problem-details rendering, and safe error disclosure.
- Show issuer/tenant identity and requesting application on login and consent; warn clearly on unrecognized redirect or application context.
- Add passkey/federation/social/provider choices only when the active profile and runtime contract expose them; otherwise omit or label planned.
- Separate end-user self-service links from the authentication transaction and route full account management to My Account.

Copy direction: reassuring and concise; identify the requesting app and action; never expose raw protocol errors by default.

Acceptance: deterministic authorization-code + PKCE journey, recovery and cancellation paths, branded/neutral variants, mobile and keyboard proof, and safe rendered failures.

### C. My Account UIX (`@tigrbl-auth/my-account-uix` → my-account API)

**Users:** currently authenticated subjects.  
**Job:** understand and control personal identity, security, sessions, applications, and consent.

Required routes/workflows:

- Overview, profile edit, security/password change, sessions/revocation, authorized apps, and consent revocation.
- Add recent security activity, authentication methods, recovery factors, and passkeys only when backed by my-account contracts.
- Explain effects before revoking the current session, another session, an app, or consent; distinguish sign-out from authorization revocation.
- Make device/session recognition understandable using privacy-safe metadata and accessible relative/absolute timestamps.
- Use the hosted identity style with a denser self-service shell so login and account management feel continuous.

Acceptance: all current CRUD tests remain authoritative; current-subject boundary is enforced; empty and single-session states are credible; no tenant-wide administration leaks into the client.

### D. Platform Admin UIX (`@tigrbl-auth/platform-admin-uix` → platform-admin API)

**Users:** platform owners and operators.  
**Job:** govern realms, tenants, authority, platform identities, keys, and operational posture.

Required routes/workflows:

- Dashboard, realms, tenants, tenant detail, platform identities, authority, key rotation, audit/posture, and settings/context.
- Turn tenant lifecycle into an explicit state machine with prerequisites, impact, dependent resources, suspension/resume behavior, and typed destructive confirmation.
- Show realm → tenant → identity authority hierarchy and prevent ambiguous cross-tenant actions.
- Key rotation must show current/next/retired state, policy, propagation/readiness, rollback implications, and evidence reference.
- Replace read-only placeholders only when API support exists. SSOT currently marks platform tenant CRUD implemented while tenant lifecycle and lifecycle views are absent; render unavailable controls accordingly.

Copy direction: operational, precise, and consequence-led. Never call a tenant delete “remove” without explaining data and access impact.

Acceptance: member deep links, high-volume filtering/pagination, authority boundary proof, safe lifecycle mutations, and parity decision against legacy admin.

### E. Tenant Admin UIX (`@tigrbl-auth/tenant-admin-uix` → tenant-admin API)

**Users:** delegated tenant administrators.  
**Job:** administer tenant-local identities, clients, consent, roles/groups, sessions, keys, and audit.

Required routes/workflows:

- Dashboard, identities, groups/roles, clients, consents, sessions, key events/JWKS, and audit.
- Keep tenant and active profile context persistent and impossible to overlook.
- Identity CRUD must include invite/onboarding state, lock/unlock meaning, credential reset boundaries, and last activity where supported.
- Client management must validate redirect URIs, auth method, grants, scopes, and secret-handling rules before submission.
- Replace derived/read-only groups, sessions, or audit placeholders only through dedicated tenant API paths. Existing page copy already admits that some dedicated paths are pending.
- Preserve implemented tenant JWKS publication and administration behavior; expose active/next/retired keys and tenant `jwks_uri` without private material.

Acceptance: no platform lifecycle calls, cross-tenant leakage tests, clear delegated authority, safe consent/client/key actions, and an honest partial-state treatment for missing workflows.

### F. Developer UIX (`@tigrbl-auth/developer-uix` → developer API)

**Users:** application developers and integration engineers.  
**Job:** register, configure, test, and troubleshoot OAuth/OIDC applications.

Required routes/workflows:

- Dashboard, applications, application detail, client metadata, redirect URIs, credentials, scopes, OAuth tester, and discovery.
- Convert the app pages into one guided lifecycle: create → configure redirects/grants/auth method → obtain credentials → integrate → test → rotate/revoke.
- Generate tested snippets for browser RP, server-side Python, curl, and discovery based on the selected app and profile; mask secrets and never put them in URLs or telemetry.
- OAuth tester must visualize authorize/callback/token steps, state/nonce/PKCE, sanitized requests/responses, expected errors, and reset.
- Credentials currently describe planned rotation controls; do not render active rotation until the API contract supports it.
- Show compatibility and maturity for the selected stable/prerelease release and profile.

Acceptance: successful app registration and edit/delete proof, invalid redirect and unsafe browser-secret rejection, accessible protocol trace, and a five-minute first-app journey.

### G. Service Admin UIX (`@tigrbl-auth/service-admin-uix` → service-admin API)

**Users:** platform engineers, SRE, security engineers, and service owners.  
**Job:** govern workload identities, service keys, API keys, token inspection, and validation.

Required routes/workflows:

- Dashboard, service identities, service keys, API keys, token inspection, validation, and audit.
- Model service identity lifecycle: create, owner/purpose, scope/audience policy, activate/suspend, credential issue/rotation/revocation, last use, expiry, and deletion impact.
- Secret material is one-time reveal, non-recoverable, masked, excluded from logs, and paired with an immediate download/copy acknowledgment.
- Token inspection and validation must clearly distinguish decode, cryptographic validation, introspection, and authorization decision; show why a request failed without leaking sensitive claims.
- SSOT marks the service-admin boundary partial and service-identity workflows absent despite CRUD tests for services/keys. Present CRUD as checkpoint capability and the complete lifecycle as incomplete.

Acceptance: safe service/API-key flows, expired/revoked/wrong-audience failure demos, owner and audit context, and no human login or tenant lifecycle paths.

### H. Resource Validation Experience (new UIX → resource-validation API)

**Users:** protected-API developers and security reviewers.  
**Job:** configure and prove token enforcement for a resource server.

Required delivery:

- Create a dedicated UIX workspace or a clearly isolated application inside the demo deployment; do not hide this API behind Demo Hub links.
- Provide verifier configuration for issuer/discovery, JWKS or introspection, audience, scopes/permissions, clock tolerance, profile, and sender constraints where exposed.
- Offer a safe token/sample input, sanitized decoded header/claims, validation-stage timeline, final allow/deny result, reason codes, and copyable server integration configuration.
- Include positive and negative fixtures: expired, not-yet-valid, wrong issuer, wrong audience, missing scope, bad signature, revoked, and sender-constraint mismatch.
- Never transmit pasted production tokens to analytics or persistence; make local/demo handling explicit.

Acceptance: successful and failed validation journeys, deterministic fixtures, resource-server quickstart, raw contract link, and evidence/maturity context.

### I. Demo Hub UIX (`@tigrbl-auth/demo-hub-uix`)

**Users:** evaluators, technical marketers, DevRel, sales, and account teams.  
**Job:** present all product surfaces as one system and guide repeatable demonstrations.

Required routes/workflows:

- Retain World View, Demo Journey, and Links; add audience/goal chooser, environment health, reset, scenario library, static fallback, and printable/shareable summary.
- Expand the seven current surface cards into explicit boundary diagrams with role, purpose, API, UIX, maturity, profile, and live health.
- Provide five canonical guided scenarios: hosted login, app registration, tenant administration, workload identity, and protected-API validation.
- Each step must state actor, surface, action, expected result, proof, limitation, and next step. Deep-link to the exact route rather than only app roots.
- Keep seeded credentials and demo-only data visibly labeled; never present simulated state as a live backend result.

Acceptance: one-command Docker startup, deterministic reset, health degradation behavior, static walkthrough when services are offline, stable screenshot states, and privacy-safe event instrumentation.

### J. Legacy Admin UIX (`@tigrbl-auth/admin-uix`)

**Users:** maintainers during extraction only.  
**Job:** provide behavioral source material until separated product UIX reach approved parity.

Required delivery:

- Freeze net-new product design except security, correctness, and migration-critical fixes.
- Build a route/workflow parity ledger mapping each legacy function to platform-admin, tenant-admin, developer, or service-admin ownership.
- Remove unsupported aggregate views instead of copying cross-boundary API access into new clients.
- Add an in-product deprecation banner only after replacement routes and migration guidance exist.
- Define retirement gates: workflow parity accepted, product APIs proven, deep links migrated, documentation updated, and tests/evidence repointed.

Acceptance: no unique required workflow remains unowned; no production navigation depends on legacy admin; package is archived or explicitly marked deprecated.

### K. Browser RP SDK (`@tigrbl-auth/rp`)

This is not a standalone UIX, but it is a required browser-experience dependency and must have its own integration brief.

- Provide framework-neutral quickstarts plus React adapters/examples without making React part of the protocol core.
- Cover discovery, authorization URL, PKCE, state/nonce, callback validation, session handoff, refresh posture, logout, cancellation, and error recovery.
- Reject browser client secrets and unsafe storage policies with actionable copy.
- Supply a local interactive example connected to public UIX and resource validation.
- Treat npm installation as unavailable until the scoped package is actually published; use workspace/checkpoint instructions separately.

## 6. Frontend Engineer Instructions

1. Establish a versioned UIX contract manifest for each app: paired API, allowed route families, auth model, roles, profile, build version, and supported workflows.
2. Implement core tokens and primitives first, then migrate public and my-account, then product consoles, then demo/resource-validation.
3. Centralize route definitions and generate navigation, breadcrumbs, route tests, and demo deep links from them.
4. Generate typed clients from the authoritative product OpenAPI/OpenRPC contracts where practical; retain explicit allowlists and fail closed on out-of-bound paths.
5. Add a capability gate that combines contract availability, runtime profile, role/permission, and maturity. Disabled actions must say why; absent actions should generally be omitted.
6. Standardize async mutation behavior: review → submit → progress → success/failure → refresh → audit reference.
7. Add route-level error boundaries, redaction tests, auth/session tests, contract drift checks, accessibility checks, responsive screenshot tests, and end-to-end golden journeys.
8. Emit privacy-safe telemetry from a shared schema. Never emit field values, identifiers, secrets, tokens, protocol bodies, or raw errors.
9. Make local Docker/demo configuration observable. Display environment and build metadata without leaking infrastructure secrets.
10. Add release automation for UIX artifacts, provenance, changelogs, compatibility, and npm publication verification before exposing install commands.

## 7. UIX Designer Instructions

1. Produce a shared foundation covering type, spacing, color, elevation, radius, iconography, density, motion, focus, state, and data visualization.
2. Design three related modes: hosted identity, self-service account, and operational console. Demo Hub may combine them but must preserve surface identity.
3. Design every critical route at desktop, tablet, and narrow mobile widths, including loading, empty, error, unauthorized, stale, partial, success, and destructive-confirmation states.
4. Make current authority and boundary visible: actor, realm, tenant, profile, environment, and app/API surface.
5. Use progressive disclosure for protocol/evidence detail; keep expert data available without overwhelming primary tasks.
6. Do not use color alone for lifecycle, risk, maturity, or validation results.
7. Provide high-density table and lower-density record/card variants with the same information priority.
8. Validate keyboard order, focus restoration, dialog semantics, error association, screen-reader names, reduced motion, zoom, and contrast to WCAG 2.2 AA.
9. Deliver stable named frames/states for marketing screenshots and automated visual comparison.

## 8. Copywriter Instructions

Deliver a copy deck per application containing:

- product one-liner, audience, job, route titles, page introductions, primary/secondary actions;
- field labels/help/examples, validation, loading, empty, partial, offline, unauthorized, error, retry, success, and audit-reference language;
- confirmation copy that names the object, consequence, reversibility, dependent impact, and required follow-up;
- maturity labels/tooltips, profile explanations, release caveats, glossary, demo narration, and “what this proves / does not prove” text;
- security-sensitive language for secrets, keys, tokens, redirect URIs, sessions, consent, rotation, suspension, and deletion.

Voice: calm, exact, direct, and technically literate. Prefer “Register an application” to “Provision client artifact.” Avoid “seamless,” “turnkey,” “military-grade,” “enterprise-grade,” “fully compliant,” and “independently certified” unless separately authorized by current evidence.

## 9. Delivery Order

### Phase 0 — Truth and contracts

- Approve vocabulary, maturity model, route ownership, API allowlists, and legacy parity map.
- Repair stale SSOT UIX test/evidence paths and validate the registry before adding new certification claims.
- Decide public stable versus prerelease demo baseline and npm publication plan.

### Phase 1 — Foundation and critical journeys

- Shared core, Public UIX, My Account, Developer first-app journey, Demo Hub health/reset/static fallback.
- Visual/accessibility baselines and contract-driven capability gates.

### Phase 2 — Administrative control planes

- Platform Admin, Tenant Admin, Service Admin, safe lifecycle/mutation patterns, audit correlation.
- Close or clearly expose partial/absent workflow gaps.

### Phase 3 — API protection and proof

- Dedicated Resource Validation UIX, protocol drawers, negative fixtures, evidence links, evaluation summaries.
- Browser RP interactive integration example.

### Phase 4 — Release and retirement

- Publish UIX/RP npm artifacts with provenance if intended for external consumption.
- Complete legacy admin parity review and retirement.
- Release-versioned screenshots, copy, quickstarts, and compatibility data.

## 10. Portfolio Definition of Done

- Every product API has an intentional UIX or documented no-UI decision; resource validation is no longer an orphaned API experience.
- Every UIX calls only its paired API and fails closed on cross-surface paths.
- Every visible action is supported by contract, runtime profile, permission, and declared maturity.
- All primary journeys have deterministic demo data, reset, expected results, static fallback, and end-to-end proof.
- Shared components, terminology, maturity states, redaction, telemetry, and accessibility behavior come from UIX core.
- Public release, prerelease, repository checkpoint, and internal SSOT release states are never conflated.
- Every UIX passes build, unit, contract, accessibility, responsive visual, and primary journey tests.
- Frontend, UIX design, and copy deliverables are reviewed together per route; placeholder copy and visually polished unsupported actions do not pass acceptance.

## 11. Open Product Decisions

1. Which release is the demonstration default: stable `0.3.4`, prerelease `0.4.0.dev2`, or an explicit selector?
2. Are UIX packages intended for public npm distribution, deployment-only artifacts, or both?
3. Should Resource Validation be standalone, embedded in Developer UIX, or shipped in both modes from one package?
4. Which legacy admin workflows are still required, and who approves parity/retirement?
5. Which profiles may customers select directly versus operator-configured only?
6. What hosted-demo security model, reset SLA, retention policy, and account/contact handoff are approved?

## 12. Source Notes

This brief is based on repository source, UIX/API package manifests and clients, page inventories, Docker deployments, examples, tests, strategy and compliance documents, SSOT CLI inventories, git tags/history, PyPI metadata, GitHub Releases, and npm registry checks reviewed July 11, 2026. It does not substitute for stakeholder interviews, customer research, accessibility testing with users, or approval of commercial/support commitments.
