# Legacy Admin UIX Extraction and Retirement Brief

**Surface:** `@tigrbl-auth/admin-uix`  
**Pairing:** Legacy aggregate admin contract; no approved one-to-one product API  
**Status:** Migration source, security maintenance, and retirement  
**Prepared:** July 11, 2026  
**Current owner:** `pkgs/95-ui/admin-uix`

## 1. Product Decision

Do not enhance Legacy Admin into a new universal administration product. Freeze net-new product capability and use it only as a behavioral/design source while required workflows move to their proper owners:

- Platform Admin: realms, tenant lifecycle, platform identities, authority, platform keys/audit.
- Tenant Admin: tenant identities, roles, clients, consent, tenant sessions/JWKS/audit.
- Developer: application/client registration and integration metadata.
- Service Admin: workload identities, service/API keys, token/validation views.

Retire the package after required parity, boundary, migration, and evidence gates pass. Security and correctness fixes remain permitted during the transition.

## 2. Current Risks

### Boundary ambiguity

The legacy UIX was adapted around an aggregate OpenRPC `/rpc` surface while the repository now has separated product APIs. Copying its backend assumptions into new packages would defeat product-surface isolation.

### Mixed truth sources

The UIX combines live backend services with IndexedDB/localStorage-backed control-plane state for identities, clients, policies, abuse rules, traffic profiles, infrastructure, and lockdown behavior. Locally persisted state must never be presented as authoritative runtime configuration or audit evidence.

### Credential and recovery handling

- A temporary administrator API key may be read from `sessionStorage` or `localStorage`.
- Password recovery can return and render `debug_reset_token`.
- Development-only behavior risks becoming visible in production builds.

These are transition liabilities and must not become requirements for replacement UIX.

### UX and implementation debt

- Tab state lacks stable resource deep links.
- Native `confirm()` remains in sensitive mutations.
- Loading intentionally waits through `setTimeout` rather than representing actual request state.
- A 500 ms polling loop reads locally stored lockdown state.
- Raw/simulated infrastructure, abuse, and policy controls can look operational.
- Styling and components are largely separate from `@tigrbl-auth/uix-core`.

## 3. Allowed Work

Until retirement, changes are limited to:

- fixing exploitable security issues;
- preventing data loss, cross-tenant exposure, or incorrect mutations;
- correcting accessibility blockers on still-required migration paths;
- removing or clearly labeling simulated/local-only functionality;
- adding migration links and deprecation guidance;
- creating parity tests and evidence for replacement surfaces;
- eliminating development credentials/debug artifacts from non-development builds.

Do not add new business workflows, new aggregate API calls, new local simulations, or visual redesign that competes with replacement UIX.

## 4. Workflow Ownership Matrix

| Legacy capability | Target owner | Migration requirement |
|---|---|---|
| Administrator login/session/password change | Product-specific admin authentication | Prove equivalent session and forced-password behavior per target surface. |
| Realm and tenant selection/lifecycle | Platform Admin | Replace global selector with explicit realm/tenant member routes and authority. |
| Tenant identities and administrator flags | Tenant Admin; platform authority subset in Platform Admin | Split local identity lifecycle from cross-tenant/platform authority. |
| Client/app management | Developer or Tenant Admin | Assign developer-owned registration versus tenant policy ownership explicitly. |
| Tenant JWKS publication and rotation | Tenant Admin; platform key governance in Platform Admin | Preserve public/private key separation and lifecycle proof. |
| Policies/RBAC/ABAC/simulation | Owning policy/admin surface determined by API contract | Do not migrate local-only policy state as runtime truth. |
| Service mesh/infrastructure | No UIX owner unless an operator API is approved | Remove simulated broker/infrastructure controls. |
| Abuse mitigation/traffic profiles | No UIX owner until runtime contract exists | Preserve only as planned concept; delete local toggles from product claims. |
| Lockdown | Platform/operator control only if server-owned | Replace browser-local polling with authenticated server state or retire. |
| Audit/telemetry/alerts | Product-filtered audit APIs | Replace sample/local data with scoped, redacted events. |
| Password recovery debug token | No production owner | Remove; use out-of-band delivery/test fixtures only. |

Every legacy component must receive one disposition: migrate, split, replace, archive as reference, or delete.

## 5. Migration Requirements

### Parity ledger

Create a machine-reviewable ledger with:

- legacy route/component/service;
- user/persona and job;
- data source and whether live/local/simulated;
- operation and API contract;
- target UIX/API owner;
- security/authority requirements;
- target route and test;
- disposition and status;
- migration note and removal gate.

Visual resemblance is not parity. Parity requires the correct owner, authorization, lifecycle semantics, failure behavior, accessibility, and evidence.

### Data migration

- Do not migrate IndexedDB/localStorage demo state into production APIs.
- Preserve only explicitly exportable user preferences after schema review.
- Clear legacy administrator keys, cached state, and reset artifacts during migration.
- Provide an operator-safe way to verify that no authoritative data depended on browser-local stores.

### Navigation and deep links

- Map every still-supported legacy entry to the exact replacement UIX route.
- Redirect only after target auth/authority and route compatibility are proven.
- Unsupported/simulated surfaces should route to explanatory retirement documentation, not empty replacement pages.

### Authentication handoff

- Do not pass administrator API keys through URLs, browser storage, or cross-app messages.
- Product UIX must establish their own scoped sessions.
- Preserve safe return context only; never transfer credentials or aggregate authority.

## 6. Immediate Security Requirements

- Prevent `debug_reset_token` from rendering outside an explicit compile-time development/test mode.
- Remove localStorage persistence for administrator API keys; use same-origin sessions or runtime-only secure mechanisms.
- Clear any legacy key on logout, session expiry, migration, and deprecation acknowledgement.
- Label all local/simulated data and disable its mutation in non-demo builds.
- Replace native `confirm()` with shared consequence-led dialogs for required remaining actions.
- Remove artificial loading delays and browser-local lockdown polling from production builds.
- Redact tokens, credentials, reset artifacts, keys, personal data, and raw errors from logs/telemetry.
- Add a production-build test that fails on debug token, development key, sample credential, or simulated-control exposure.

## 7. Deprecation Experience

Do not show a deprecation banner until replacement routes exist for the current user’s required workflows.

Once ready, the UI must:

- state that the aggregate console is being replaced by scoped product consoles;
- explain which console owns the current task;
- link to exact replacement routes;
- preserve no secrets in the handoff;
- give a published retirement date and support path;
- allow temporary dismissal only within the announced migration window.

After the cutoff, serve a static migration page rather than the operational bundle.

## 8. Team Requirements

### Technical marketing

- Stop using Legacy Admin screenshots as current product proof once replacement screenshots exist.
- Never market local policy, abuse, infrastructure, or lockdown simulations as implemented runtime features.
- Maintain a visual archive only for migration provenance.
- Update diagrams and collateral to the separated API/UIX model.

### Developer relations

- Publish a migration guide mapping old tasks/routes/configuration to new product surfaces.
- Explain authentication/session changes and removal of browser-stored administrator keys.
- Update examples, workshops, Docker commands, and screenshots.
- Provide troubleshooting for lost bookmarks, changed authority, and unsupported legacy concepts.

### Sales and account management

- Use Demo Hub and replacement consoles for demonstrations.
- Provide a clear account-facing explanation of why separated boundaries improve scope and authority clarity.
- Identify unsupported legacy simulations before customer demonstrations.
- Track customer dependencies on legacy workflows before setting the final cutoff.

### GTM strategy

- Remove Legacy Admin from new campaigns and conversion paths.
- Track privacy-safe migration-link use and replacement-surface adoption, not activity contents.
- Keep product naming and taxonomy aligned to the separated surfaces.
- Do not present retirement as removal of capabilities that were only simulated.

### Copywriter

- Write deprecation, migration, unsupported-feature, and replacement-route copy.
- Distinguish “moved,” “replaced,” “not supported,” “previously simulated,” and “retired.”
- Avoid suggesting that browser-local state was authoritative or migrated.
- Provide concise operator instructions for clearing legacy local state safely.

## 9. Frontend Engineering Instructions

1. Build the parity ledger before moving additional components.
2. Add environment-gated tests for debug reset tokens, stored admin keys, sample credentials, and simulated controls.
3. Replace required shared behaviors with `@tigrbl-auth/uix-core`; do not refactor retired-only components for aesthetics.
4. Add exact replacement links only after route/authority/end-to-end proof.
5. Instrument privacy-safe migration events without tenant/user/resource identifiers.
6. Remove legacy routes, services, persistence stores, and dependencies incrementally after target gates pass.
7. Keep an archived source tag or documentation snapshot rather than shipping dead code indefinitely.
8. Update SSOT test/evidence paths and lifecycle status as each capability moves or retires.

## 10. UIX Designer Instructions

- Design a restrained migration banner, task-to-surface chooser, and final static retirement page.
- Reuse replacement product naming and visual system; do not visually modernize the legacy console as a competing destination.
- Clearly label local/demo/simulated state and disabled controls during transition.
- Design unauthorized, replacement unavailable, migration link failed, and cutoff states.
- Validate keyboard access, focus, zoom, screen-reader announcements, and WCAG 2.2 AA for remaining required paths.

## 11. Copy Deliverables

Produce:

- migration banner and retirement announcement;
- task-to-replacement mapping;
- local-state/credential clearing instructions;
- moved/replaced/unsupported/previously-simulated definitions;
- route unavailable, authority changed, support, and cutoff copy;
- internal sales/DevRel talking points that accurately distinguish implemented from simulated legacy behavior.

## 12. Retirement Gates

The operational package may be retired when:

- every component has an approved disposition;
- every required workflow has a tested replacement route and correct API owner;
- cross-surface authority and isolation tests pass;
- no supported documentation, demo, bookmark handoff, or deployment depends on Legacy Admin;
- browser-local administrator credentials and authoritative-looking simulated state are removed;
- SSOT features/claims/tests/evidence identify replacements or deprecation lifecycle;
- migration communications and support window are complete;
- a final security scan finds no remaining credential/session exposure;
- package publishing/deployment is disabled and the static migration page is available.

## 13. Acceptance Criteria

- No net-new product workflow is added to Legacy Admin.
- The parity ledger covers all components and services with a target/disposition.
- Debug reset tokens, browser-persisted administrator keys, and simulated controls cannot appear in production builds.
- Replacement UIX preserve required semantics without recreating an aggregate API boundary.
- Existing users receive exact safe handoffs and clear migration language.
- Required legacy paths remain accessible during the migration window.
- Retirement removes operational code while retaining sufficient provenance and documentation.

## 14. Source Evidence

- `pkgs/95-ui/admin-uix/README.md`
- `pkgs/95-ui/admin-uix/App.tsx`
- `pkgs/95-ui/admin-uix/components/`
- `pkgs/95-ui/admin-uix/services/backendService.ts`
- `pkgs/95-ui/admin-uix/services/adminAuthService.ts`
- `pkgs/95-ui/admin-uix/services/controlPlaneStateService.ts`
- `pkgs/95-ui/admin-uix/services/persistence.ts`
- Admin UIX boundary, auth, resource, mutation, policy, and governance tests
- Platform/Tenant/Developer/Service API/UIX pairing briefs
- Admin UIX SSOT feature/claim/test/evidence/boundary records
