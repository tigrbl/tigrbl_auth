# Demo Hub + All Product API Surfaces Requirements Brief

**Pairing:** `@tigrbl-auth/demo-hub-uix` + all seven product APIs/UIX  
**Status:** Cross-surface orchestration brief; not a new aggregate API  
**Prepared:** July 11, 2026  
**UIX owner:** `pkgs/95-ui/demo-hub-uix`  
**Deployment owner:** `docker/docker-compose.demo-hub-uix.yml`

## 1. Product Decision

Deliver Demo Hub as the guided evaluation and demonstration layer that explains how the seven separated product surfaces work together.

It may coordinate deterministic demo actions through a narrowly scoped server-side demo runner, but it must not become a privileged production API, universal administrator client, credential broker, or alternate owner of product behavior. Each real operation remains owned by its product API and UIX.

## 2. Users and Jobs

### Primary users

- Technical evaluators exploring the product portfolio.
- Developer Relations running workshops and quickstarts.
- Technical marketing creating accurate demonstrations and screenshots.
- Sales engineers and account teams presenting solution journeys.
- Maintainers checking local multi-surface health.

### Primary jobs

1. Understand the purpose, persona, boundary, and maturity of every product surface.
2. Select a use case instead of learning repository package topology.
3. Run a deterministic, resettable journey across the appropriate surfaces.
4. Open the exact UIX route, contract, documentation, and proof for each step.
5. Distinguish executed proof, simulated walkthrough, manual progress, and unavailable services.
6. Share or print a safe evaluation summary.

## 3. Surface Model

Demo Hub covers:

| Surface | API | UIX |
|---|---|---|
| Public identity | `tigrbl-auth-api-public` | `@tigrbl-auth/public-uix` |
| My Account | `tigrbl-auth-api-my-account` | `@tigrbl-auth/my-account-uix` |
| Platform Admin | `tigrbl-auth-api-platform-admin` | `@tigrbl-auth/platform-admin-uix` |
| Tenant Admin | `tigrbl-auth-api-tenant-admin` | `@tigrbl-auth/tenant-admin-uix` |
| Developer | `tigrbl-auth-api-developer` | `@tigrbl-auth/developer-uix` |
| Service Admin | `tigrbl-auth-api-service-admin` | `@tigrbl-auth/service-admin-uix` |
| Resource Validation | `tigrbl-auth-api-resource-validation` | proposed `@tigrbl-auth/resource-validation-uix` |

Demo Hub must preserve each surface’s authentication, authorization, path allowlist, and data ownership. It may deep-link across surfaces; it must not call a product API directly from the browser with shared administrator secrets.

## 4. Required Experience

### Audience and goal chooser

Offer clear starts:

- Add hosted login
- Manage a user account
- Operate a multi-tenant identity platform
- Administer a tenant
- Register an application
- Configure workload identity
- Protect an API

Each start must identify persona, prerequisites, surfaces involved, time, maturity, and whether the scenario is live, fixture-backed, or static.

### World View

- Show seven bounded product surfaces as one system.
- For each surface show audience, job, API, UIX, primary objects, authentication model, profile/release maturity, current health, and exact launch routes.
- Visualize allowed handoffs without implying that data ownership is shared.
- Replace the Resource Validation “API-only” label when its dedicated UIX is delivered.
- Do not equate HTTP reachability with product readiness or certification.

### Scenario library

Provide at least five canonical scenarios:

1. Hosted login to protected profile
2. Register and test an OAuth/OIDC application
3. Provision and administer a tenant
4. Issue and rotate workload credentials
5. Validate a protected API request

Additional scenarios may cover consent revocation, session control, realm/tenant isolation, key rollover, and representative denial paths.

Every scenario must define:

- scenario ID and version;
- persona and business/technical goal;
- required services/profile/release;
- seeded objects and reset behavior;
- ordered steps with owning surface;
- exact route/action and expected result;
- proof source and limitation;
- failure/rollback behavior;
- static fallback.

### Guided execution

- Deep-link to exact resource or workflow routes, not only application roots.
- Preserve scenario context across handoffs without placing credentials, tokens, or personal data in URLs.
- Show actor, surface, action, expected result, actual result, proof, limitation, and next step.
- Allow single-step execution and full journey execution only through the server-side demo runner.
- Support pause/resume for manual walkthrough progress, but label it separately from executed proof.

### Proof-state integrity

Use four distinct states:

- **Not started:** no action or proof.
- **Walkthrough complete:** user manually marked instructional progress; not evidence.
- **Executed:** the demo runner performed the contracted request and returned a result.
- **Verified fixture:** result matches the scenario’s versioned expected assertion.

The current `Mark verified` control and `localStorage` value must not produce a “Verified” badge. Manual progress may remain locally persisted under a clearly non-evidentiary label. Executed proof must be server-issued, timestamped, scenario/version bound, and short-lived.

### Environment health

- Show API/UIX reachability, contract endpoint status, build version, profile, fixture compatibility, and last check.
- Distinguish offline, unauthorized, incompatible version, unhealthy, degraded, and not configured.
- Expose safe diagnostics and recovery commands without credentials.
- Allow static journeys even when services are unavailable.

### Reset and data safety

- Reset must be explicit, scoped to the demo environment, idempotent, and report affected fixture objects.
- Never permit reset against an unrecognized or production environment.
- Require an environment fingerprint and server-side `demo_mode=true` guard.
- Clear browser progress separately from backend fixture reset.
- Do not display real emails, tenant names, credentials, tokens, or customer data.

### Share and export

- Generate safe scenario links containing only scenario/version and non-sensitive presentation context.
- Provide a printable evaluation summary with surfaces, steps, result categories, profile/version, timestamp, limitations, and documentation links.
- Never export credentials, identifiers, request/response bodies, tokens, claims, or administrator details.

## 5. Demo Runner Boundary

The existing `/demo-api/steps/{id}` and `/demo-api/run-all` pattern may remain only as a development/demo orchestration service.

Required constraints:

- server-side scenario allowlist; no arbitrary URL, method, body, or header input;
- dedicated demo credentials loaded from runtime secrets, never Vite/browser variables;
- no production deployment unless explicitly secured and approved;
- scenario-specific least privilege rather than one universal administrator credential;
- bounded timeouts, response-size limits, redaction, rate limiting, and audit correlation;
- no raw upstream response forwarding to the browser;
- reset endpoints gated by demo environment fingerprint;
- clear distinction between authentication failure and negative boundary proof.

Hard-coded development defaults in Compose must be overrideable and prominently labeled. They are not production credentials or documentation examples.

## 6. Team Requirements

### Technical marketing

- Own stable named screenshot states and scenario narratives tied to a reviewed version/profile.
- Provide reusable boundary diagrams and captions sourced from the surface catalog.
- Use verified fixture results only for proof claims; manual progress cannot support marketing claims.
- Keep limitations and release maturity adjacent to every demonstrated capability.

### Developer relations

- Own one-command startup, prerequisites, health checks, seed/reset, expected output, troubleshooting, and static fallback.
- Make each step copyable and link to the corresponding API/UIX brief and contract.
- Provide workshop mode with presenter notes and learner mode with safe exercises.
- Test scenarios in CI against the supported local stack.

### Sales and account management

- Provide role/use-case launchers, predictable demo duration, safe talking points, and recovery from unavailable services.
- Include “what this proves / what it does not prove” per scenario.
- Preserve scenario context in contact/evaluation handoff without customer or credential data.
- Ensure demos never require improvising unsupported or partial workflows.

### GTM strategy

- Use the canonical surface/use-case taxonomy for navigation, campaigns, events, and handoff.
- Track privacy-safe scenario start/completion, step result category, surface opened, documentation/evidence opened, and handoff initiated.
- Never capture fixture values, endpoints, credentials, tokens, IDs, bodies, or raw results.
- Keep positioning content configurable but proof definitions version-controlled and review-gated.

### Copywriter

- Write persona, goal, action, expected result, actual result, proof, limitation, and next-step copy for every step.
- Distinguish “walkthrough complete,” “executed,” and “verified fixture” consistently.
- Explain boundary-denial results as successful boundary proof only when the scenario explicitly expected denial.
- Avoid “live,” “verified,” “production-ready,” or “complete” unless the exact state supports it.

## 7. Frontend Engineering Instructions

1. Replace manual `Verified` state with separate walkthrough-progress and server-proof models.
2. Define typed, versioned scenario and surface manifests; generate navigation/cards/steps from them.
3. Add exact deep links and resource identifiers only through server-issued opaque demo references, not raw IDs in share URLs.
4. Implement health/compatibility checks for all seven APIs and UIX without exposing secrets.
5. Add static scenario fallbacks generated from the same manifest.
6. Implement deterministic reset with environment fingerprint and `demo_mode` server guard.
7. Redact and normalize all runner results; never forward raw upstream bodies.
8. Add scenario/schema validation, allowlist, secret-exposure, production-reset, proof-integrity, accessibility, and responsive tests.
9. Update the resource-validation surface to launch its dedicated UIX when delivered.
10. Keep Demo Hub deployable independently and prevent it from becoming a runtime dependency of product UIX.

## 8. UIX Designer Instructions

- Design World View as a compact boundary map with accessible list/table fallback.
- Make personas and outcomes primary; packages/protocols/evidence appear progressively.
- Visually distinguish manual progress, execution, verified fixture, denial-as-expected, failure, offline, and static fallback without color alone.
- Design presenter and self-guided modes with the same scenario truth.
- Provide layouts for all healthy, partial outage, incompatible version, unauthorized, reset in progress/failed, and static-only states.
- Preserve stable named frames for screenshots and visual regression.
- Validate keyboard sequence, focus restoration, live-region execution updates, reduced motion, high zoom, and WCAG 2.2 AA.

## 9. Copy Deliverables

Produce:

- surface one-liners, personas, object descriptions, and boundary explanations;
- audience/goal chooser labels and summaries;
- five canonical scenario scripts with presenter notes;
- proof-state definitions, expected denial language, and limitations;
- health, compatibility, reset, static fallback, offline, unauthorized, failure, and recovery copy;
- printable evaluation summary and contextual handoff language.

## 10. Acceptance Criteria

- Demo Hub covers all seven product surfaces and links to exact API/UIX routes.
- It does not become a production aggregate API or expose shared credentials to the browser.
- Manual progress can never render or persist as executed/verified proof.
- Executed results are server-issued, scenario/version-bound, redacted, timestamped, and short-lived.
- Reset is demo-environment-only, fingerprint-gated, deterministic, and separate from browser progress clearing.
- Five canonical journeys have live execution, representative failure, expected result, static fallback, and safe export.
- Health distinguishes reachability, authorization, compatibility, and fixture readiness.
- Scenario, boundary, secret, reset, proof-integrity, accessibility, responsive visual, and end-to-end tests pass.

## 11. Source Evidence

- `pkgs/95-ui/demo-hub-uix/README.md`
- `pkgs/95-ui/demo-hub-uix/surfaces.ts`
- `pkgs/95-ui/demo-hub-uix/demoState.ts`
- `pkgs/95-ui/demo-hub-uix/App.tsx`
- `pkgs/95-ui/demo-hub-uix/surfaces.test.ts`
- `docker/docker-compose.demo-hub-uix.yml`
- Seven product API contracts and individual API/UIX pairing briefs
- Demo/API deployment and package-layering tests
