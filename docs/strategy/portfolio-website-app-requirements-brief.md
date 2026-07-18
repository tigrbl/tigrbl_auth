# Tigrbl Auth Portfolio Website — App Requirements Brief

**Status:** Draft for product, GTM, design, engineering, and copy review  
**Prepared:** July 11, 2026  
**Product baseline:** repository checkpoint `0.4.0.dev2`; latest stable PyPI release reviewed: `0.3.4` (April 1, 2026)

## Executive Summary

- **Build an evidence-led product portfolio, not a conventional package landing page.** Tigrbl Auth is a suite of provider, relying-party, resource-server, administration, policy, runtime, SDK, and certification surfaces. The website must help each visitor choose a use case and reach runnable proof without making them understand the package graph first.
- **Make product truth visible at the point of every claim.** The repository contains 1,160 governed features, 1,766 claims, six active profiles, and 11 registry releases, but the current SSOT validation is failing and final certification remains blocked. Every capability shown publicly must be labeled `Published`, `Checkpoint`, `Planned`, or `Certification pending`; “independently certified,” “fully RFC compliant,” and “production certified” are prohibited until the governing gates permit them.
- **Anchor the experience around five demonstrable journeys.** The initial portfolio should prove hosted login, developer app registration, tenant administration, machine-to-machine access, and protected-API validation. A demo hub and evidence explorer should connect these journeys to installable packages, docs, contracts, tests, and release status.
- **Ship a focused first release.** The minimum credible site is a homepage, use-case portfolio, product-surface pages, interactive demo hub, developer quickstart, standards/evidence center, release page, and sales-ready deployment/security page. Broader feature catalogs and competitor comparisons should follow once the truth pipeline is automated.

## 1. Decision and Product Goal

The website must let a technical evaluator, developer, buyer, or account stakeholder answer four questions quickly:

1. What problem does Tigrbl Auth solve for me?
2. Which product surface and deployment profile fit my use case?
3. Can I see and run a realistic flow?
4. What is published, verified, planned, or still blocked?

The primary conversion is **qualified technical evaluation**: select a use case, inspect proof, and start a runnable quickstart. Secondary conversions are opening the repository, reviewing deployment/security material, and contacting the team for architecture or account support.

The website is not the admin console, a generated API reference, or a raw SSOT browser. It is the portfolio and evaluation layer that routes visitors into those deeper surfaces.

## 2. Evidence Baseline and Implications

### 2.1 What exists now

| Area | Repository evidence | Website implication |
|---|---|---|
| Distribution | Python workspace `0.4.0.dev2`; stable `tigrbl-auth` `0.3.4` on PyPI; Python 3.10–3.12 | Show stable install separately from repository checkpoint. Never present dev-only package versions as the default install. |
| Product APIs | Public, platform-admin, tenant-admin, developer, service-admin, resource-validation packages | Organize portfolio pages by user job and boundary, not internal directory layer. |
| UIX | Admin, platform-admin, tenant-admin, developer, service-admin, my-account, public, demo-hub, and browser RP workspaces | Use real UI screenshots/flows as proof; clearly mark partial product-boundary extraction where applicable. |
| Runtime | ASGI app/plugin model; Uvicorn, Hypercorn, and Tigrcorn runner profiles; SQLite/PostgreSQL options | Provide a deployment selector and architecture explainer. Avoid implying Tigrbl Auth is a bundled hosting service. |
| Interactive tooling | `tigrbl-auth` operator CLI, OpenAPI, OpenRPC, JSON Schema, demo hub, Docker examples | Give developers runnable commands, contract links, and copyable flows; use progressive disclosure for operator tooling. |
| Examples | Docker compose paths and `acme_notes_cli` device-authorization consumer | Turn examples into guided journeys with expected results, prerequisites, and reset instructions. |
| Profiles | Baseline, baseline-development, FAPI2 security, hardening, peer-claim, production | Present profiles as selectable policy/deployment postures, not badges of universal compliance. |
| Governed scope | 1,160 features: 824 implemented, 48 partial, 288 absent | Do not publish a flat “all features” checklist without state and scope filters. |
| Claims | 1,766 claims: 956 T2, 479 T1, 331 T0; 453 certified, 931 evidenced, 262 proposed, with smaller published/retired sets | Translate tiers and statuses into plain language; preserve links to evidence for technical review. |
| Certification | Current docs say final certification is blocked and prohibit strict independent wording | Put a persistent truth note in the evidence center and claim tooltips. |

### 2.2 Conflicts the website must resolve

- The top-level README contains older blocker wording that conflicts with newer generated status fields. The site must use a defined source precedence, not manually copied prose.
- `CURRENT_STATE.md` reports green runtime/test/migration checks while `CERTIFICATION_STATUS.md` still reports final certification blocked.
- The SSOT registry validation currently fails, including UIX test/evidence paths that reference the former `apps/` and `packages/` layout instead of current `pkgs/105-ui/` and `pkgs/100-uix-core/` paths.
- The public stable distribution trails the repository checkpoint. Feature availability cannot be inferred from `main` alone.

Required precedence for public status:

1. Published package/release metadata for what users can install.
2. `.ssot/registry.json` and generated authoritative compliance reports for governed checkpoint truth.
3. Runtime contracts and tests for demonstrable behavior.
4. Handwritten strategy or focus documents for roadmap context only.

If sources disagree, the site must show the more conservative state and link to the governing evidence.

## 3. Audience and Team Requirements

### 3.1 Technical marketing

Needs:

- A crisp category: **composable identity and authorization infrastructure for Tigrbl applications**.
- Narrative proof that spans human login, service identity, authorization policy, tenant control, and API protection.
- Reusable diagrams, screenshots, capability cards, release callouts, and evidence-backed comparison points.
- SEO landing routes for OAuth/OIDC provider, OAuth 2.1 alignment, resource-server validation, machine identity, multi-tenant IAM, RBAC/ABAC, and Tigrbl authentication.

Requirements:

- Every campaign-capable claim must have a source, status, applicable profile, and last-reviewed date.
- Social cards and screenshots must be generated from stable, named demo states.
- Provide campaign-specific deep links that preserve the selected use case/profile.
- Do not lead with registry counts; use them as trust evidence after the product value is clear.

### 3.2 Developer relations

Needs:

- A five-minute path from install to a visible authentication result.
- Copyable Python, CLI, curl, TypeScript/RP, and Docker examples with prerequisites and expected output.
- A concept map connecting provider, RP, resource server, API front doors, UIX, profiles, and runners.
- Troubleshooting, version compatibility, local reset, security warnings, and “where to go next.”

Requirements:

- Quickstarts must default to the latest stable release and offer checkpoint instructions in a clearly separate tab.
- Code samples must be tested in CI or derived from tested examples.
- Interactive examples must expose OpenAPI/OpenRPC/discovery artifacts and a resettable seeded environment.
- Each journey ends with a productionization checklist, not only a successful localhost response.

### 3.3 Sales and account management

Needs:

- Fast qualification by deployment model, identity type, assurance needs, tenant model, datastore, and integration surface.
- A non-technical account story: what is ready, what requires solution work, and what is roadmap.
- Security, architecture, interoperability, support, license, and release materials suitable for follow-up.
- Shareable, stable URLs for a specific solution narrative.

Requirements:

- Add a guided “Fit for your environment” selector that produces a summary without implying a binding certification result.
- Provide a deployment/security overview with downloadable or printable content.
- Show explicit “available now,” “checkpoint preview,” and “planned” states.
- Contact CTA should capture the selected use case/profile in context; do not require a generic form restart.

### 3.4 GTM strategy

Needs:

- Segmentation by buyer/problem rather than by repository package.
- A measurable funnel from discovery to proof to evaluation.
- Message testing across developer platform, multi-tenant IAM, workload identity, and authorization-control-plane positions.
- Release-aware campaigns that cannot accidentally advertise unreleased code.

Requirements:

- Support campaign parameters and event tracking for use-case selected, quickstart copied, demo completed, evidence opened, release viewed, GitHub clicked, and contact initiated.
- Maintain one canonical capability taxonomy used by navigation, campaigns, analytics, and sales materials.
- Make positioning modules configurable without changing product-truth modules.
- Do not publish competitor “better than” claims from internal research without separate legal and evidence review.

### 3.5 Copywriter

Needs:

- A controlled vocabulary and a clear distinction between product value, technical capability, governed claim, and certification statement.
- Persona-specific benefits supported by concrete proof.
- Short explanations for Tigrbl-specific terms, profiles, evidence tiers, and package boundaries.

Requirements:

- Use “supports,” “implements,” or “provides” only when the selected published/checkpoint state supports it.
- Use “aligned with” for OAuth 2.1; do not call it a formal RFC certification.
- Reserve “certified” for claims whose governing status is certified and whose release/profile context is visible.
- Never use “fully compliant,” “independently verified,” “production certified,” or “complete” without a current green gate explicitly authorizing that exact wording.
- Prefer outcomes: “register an OAuth client,” “validate a protected API,” and “administer tenant identities” over package names.

## 4. Positioning and Message Architecture

### Proposed promise

**Compose identity, authorization, and API protection as governed Tigrbl product surfaces.**

### Supporting pillars

1. **One identity system, separated product boundaries.** Public login, developer registration, tenant administration, service identity, and resource validation expose intentionally scoped surfaces.
2. **Protocol depth with profile honesty.** OAuth, OIDC, JOSE, discovery, sender constraints, and related standards are activated and described by explicit profiles.
3. **Proof travels with the product.** Features connect to claims, tests, evidence, boundaries, and releases rather than relying on marketing assertions alone.
4. **Choose how you compose and run it.** Use an ASGI app, application factory, Tigrbl plugin, operator CLI, runner profile, and SQLite or PostgreSQL storage.

### Category and audience variations

| Audience | Lead message | Primary proof |
|---|---|---|
| App developer | Add login and token validation without rebuilding identity tables or protocol flows. | Five-minute quickstart, RP flow, discovery/JWKS, protected API. |
| Platform team | Run separated public and administrative identity surfaces for a multi-tenant Tigrbl platform. | Architecture, surface allowlists, tenant controls, deployment profiles. |
| Security/identity engineer | Inspect the exact profile, claim tier, test, and evidence behind a capability. | Evidence center, standards matrix, negative tests, release boundary. |
| Engineering leader/buyer | Adopt a composable identity foundation with visible maturity and integration scope. | Solution journeys, status labeling, deployment/security overview, roadmap boundaries. |

## 5. Required Information Architecture

Top navigation:

- **Product** — overview and product surfaces
- **Solutions** — human identity, developer platform, workload identity, multi-tenant administration, API protection
- **Developers** — quickstart, examples, CLI, contracts, package/distribution map
- **Demos** — guided demo hub and runnable flows
- **Trust** — standards, profiles, evidence, security posture, releases
- **Docs** — authoritative documentation entry point
- **GitHub** and **Start evaluating** CTAs

Required pages:

1. Homepage
2. Product overview
3. Public identity and hosted login
4. Developer app/client management
5. Tenant and platform administration
6. Service/workload identity
7. Resource-server/API protection
8. Policy and authorization
9. Interactive demo hub
10. Developer quickstart
11. Examples gallery
12. Packages and distributions
13. Runtime and deployment profiles
14. Standards and evidence center
15. Releases and compatibility
16. Architecture/security overview
17. Contact/evaluation handoff

## 6. Core Journeys and Interactive Requirements

### Journey A — Hosted login to protected profile

Show discovery, authorization code + PKCE, login, callback, session/profile display, logout, and safe error states. Offer a “show protocol” drawer with sanitized requests and responses.

### Journey B — Register an application

Show developer surface selection, client registration, redirect URI policy, grant selection, generated client metadata, and a copyable integration snippet. Secrets must be demo-only, masked by default, and never stored in analytics.

### Journey C — Administer a tenant

Show tenant selection, principals, credentials, clients, policies, keys/JWKS, sessions, and safe mutations. Emphasize boundary separation between platform and tenant administration.

### Journey D — Machine-to-machine access

Show service/workload identity, client credentials or stronger client authentication option, scope/audience grant, token request, protected call, and audit/provenance result. Label unfinished first-party SDK coverage honestly.

### Journey E — Validate a protected API

Show issuer discovery, JWKS/introspection choice, audience and scope requirements, sender-constraint options, successful enforcement, and representative rejection cases.

### Interactive tooling requirements

- Resettable seeded demo state with visible “demo data” labeling.
- Stable scenarios for screenshots and event instrumentation.
- Step-by-step mode and expert/raw-contract mode.
- Copy controls with versioned snippets.
- Inline expected result and common failure explanation.
- Keyboard-complete operation and mobile-readable output.
- No real credentials, tokens, emails, tenant names, or external callbacks.
- Demo availability must not block access to static walkthroughs.

## 7. Page-Level Requirements

### Homepage

- State the category and primary value in one screen.
- Offer three starts: `Add login`, `Protect an API`, `Run an identity platform`.
- Show one animated or stepped end-to-end proof, not a decorative code background.
- Introduce product boundaries, proof model, and deployment options.
- Display current stable version and a restrained checkpoint status link.

### Product and solution pages

- Lead with user job and outcome.
- Show applicable surfaces, flow diagram, supported-now capabilities, profile constraints, demo, quickstart, and evidence links.
- Include “not included / planned” where absence changes a buying decision.

### Developer center

- Stable/checkpoint version toggle.
- Environment selector: local Python, Docker, plugin composition.
- Runner and storage selector.
- Tested snippets with expected outputs.
- Clear links to OpenAPI, OpenRPC, JSON Schema, CLI surface, examples, and source.

### Trust and evidence center

- Plain-language explanation of T0–T4 and claim statuses.
- Filters for capability family, product surface, profile, implementation state, claim tier/status, and release.
- A capability detail view linking feature → claim → test → evidence → release/boundary.
- Prominent certification caveat and last-generated timestamp.
- Raw artifact links for expert reviewers; summarized interpretation for buyers.

### Releases and compatibility

- Separate PyPI stable releases from repository/registry checkpoints.
- Show Python, Tigrbl dependency, storage, runner, and UI/package compatibility.
- Provide migration notes and known limitations.
- Never translate an internal registry publication status into a public package release unless the artifact is actually published.

## 8. Design Direction for UX/UI

The experience should feel like a trustworthy technical instrument: precise, calm, inspectable, and modern. Avoid security clichés such as padlocks, shields, neon “cyber” grids, or anonymous server racks.

Design principles:

- **Outcome first, system depth on demand.** Begin with journeys; reveal packages, protocols, and evidence progressively.
- **State is visual grammar.** Use consistent badges for Published, Checkpoint, Planned, Partial, Deprecated, and Certification pending. Do not encode state by color alone.
- **Boundaries are visible.** Distinguish public, developer, tenant-admin, platform-admin, service-admin, and resource-validation surfaces in diagrams and demos.
- **Evidence stays adjacent.** A claim’s state/profile/release tooltip or evidence link belongs near the claim, not only in a legal footer.
- **Code remains readable.** Snippets need line wrapping/scroll behavior, copy feedback, filenames, language labels, and accessible contrast.

Required responsive breakpoints and QA states:

- Desktop, tablet, and narrow mobile layouts.
- Loading, empty, error, offline-demo, and stale-status states.
- Keyboard focus, reduced motion, high zoom, and screen-reader semantics.
- WCAG 2.2 AA target.

## 9. Frontend Engineering Instructions

### Data and truth model

Create a build-time normalized content model with these minimum entities:

- `Capability`: id, title, outcome, surface, implementation status, lifecycle, profiles, package/release availability.
- `Claim`: id, tier, status, exact assertion, feature links, test/evidence links.
- `Distribution`: ecosystem, package name, stable version, prerelease version, compatibility, install command, published timestamp.
- `Profile`: id, audience meaning, enabled/disabled behavior, dependencies, status.
- `Demo`: journey, prerequisites, steps, expected results, reset mechanism, supported versions.
- `Release`: public/internal type, version, date, boundary, claim/evidence scope, limitations.

Generate this model from authoritative artifacts where practical. Fail the website build on unknown status values, broken internal evidence links, or claims that lack a required state label. Warn on stale source timestamps and stable/checkpoint version drift.

### Application requirements

- Use static generation or server rendering for public content and SEO-critical routes.
- Keep demos isolated from the content renderer and deployable behind feature flags.
- Preserve deep links for selected use case, profile, release, and evidence filters.
- Provide client-side search across products, docs entry points, capabilities, standards, and releases.
- Instrument privacy-conscious first-party events; exclude code, tokens, identifiers, and form contents.
- Add structured metadata for SoftwareApplication/SoftwareSourceCode and release/version information where accurate.
- Provide a print stylesheet for security/architecture and evaluation summaries.
- Create automated link, accessibility, responsive, snippet, content-schema, and claim-language checks.

### Definition of done

- Every public capability statement resolves to a state, profile context, and source.
- Stable quickstarts execute against published dependencies in CI.
- Demo journeys have deterministic reset and static fallback.
- No route exposes a dev/checkpoint capability as stable by default.
- Core Web Vitals meet agreed budgets on representative mobile and desktop profiles.
- Accessibility audit meets WCAG 2.2 AA for critical paths.

## 10. Copywriter Instructions

Produce:

- Homepage value proposition and three journey entry points.
- Product/solution page headlines, concise benefits, proof captions, and limitations.
- Status badge definitions and tooltips.
- Quickstart instructional copy and expected-result explanations.
- Evidence tier/status glossary.
- Security, release, and certification caveat language.
- Demo step copy, empty/error states, and conversion CTAs.

Style:

- Direct, technically literate, and specific.
- Explain acronyms on first use.
- Prefer active verbs and observable outcomes.
- Avoid “enterprise-grade,” “seamless,” “complete,” “turnkey,” and “best-in-class” unless replaced by specific proof.
- Treat Tigrbl Auth as a singular product suite and named packages as components/surfaces.

Example approved pattern:

> Run separate public, developer, tenant-administration, service-administration, and resource-validation surfaces from one governed identity system. Availability varies by release and profile.

Example prohibited pattern:

> A fully compliant, independently certified enterprise identity platform for every authentication use case.

## 11. Measurement Plan

Primary metrics:

- Qualified evaluation starts: visitor selects a solution and opens a quickstart or demo.
- Quickstart completion proxy: copies all required steps and opens expected-result/troubleshooting content.
- Demo completion by journey.
- Evidence engagement among solution/deployment visitors.
- GitHub/PyPI outbound conversion.
- Context-preserving contact/evaluation submissions.

Guardrails:

- Zero published claim-language violations.
- Zero stable/checkpoint availability mismatches.
- Demo error and reset-failure rates.
- Search exits with no useful result.
- Accessibility and performance regressions.

## 12. Delivery Phases

### Phase 0 — Truth foundation

- Repair/normalize SSOT UIX paths and make validation green.
- Define stable versus checkpoint release ingestion.
- Approve capability taxonomy, status vocabulary, and prohibited claims.
- Select five deterministic demo scenarios.

### Phase 1 — Credible evaluation site

- Homepage and solution/product portfolio.
- Developer quickstart and package/distribution map.
- Guided demo hub with static fallback.
- Trust/evidence summary and releases/compatibility page.
- Architecture/security overview and contextual contact handoff.

### Phase 2 — Evidence-led differentiation

- Searchable feature/claim/evidence explorer.
- Profile/deployment selector.
- More examples, SDK paths, and productionization guides.
- Campaign landing modules and sales-shareable evaluation summaries.

### Phase 3 — Continuous release truth

- Automated release/status refresh with review gates.
- Version-aware docs and snippets.
- Expanded solution journeys and approved competitor evaluation content.

## 13. Open Decisions

1. Is the first launch intended to market the stable `0.3.4` distribution, preview `0.4.0.dev2`, or deliberately do both?
2. Will demos run as hosted disposable environments, client-side simulations, or guided local Docker flows?
3. What is the approved commercial CTA: community/GitHub, architecture review, hosted offering waitlist, or account contact?
4. Which deployment/support commitments may sales state today?
5. Who owns approval for public certification and standards wording?
6. Should the website live in this repository or a separate portfolio/site repository consuming exported truth artifacts?

## 14. Caveats and Source Notes

This brief evaluates repository product and delivery evidence, not customer research, pipeline data, support history, or stakeholder interviews. Team needs are therefore evidence-backed working requirements, not confirmed organizational commitments.

Primary repository sources reviewed include `README.md`, `CURRENT_STATE.md`, `CERTIFICATION_STATUS.md`, `pyproject.toml`, `package.json`, `.ssot/registry.json`, SSOT graph/registry exports, generated compliance material, architecture/strategy documents, product API and UIX packages, examples, tests, CLI/runtime surfaces, and Git tags. Public release evidence was checked against the `tigrbl-auth` PyPI project on July 11, 2026.

Reproducible SSOT inspection commands:

```powershell
$env:UV_CACHE_DIR='.uv-cache'
uv run ssot --output-format json --output-file .tmp/feature.json feature list .
uv run ssot --output-format json --output-file .tmp/claim.json claim list .
uv run ssot --output-format json --output-file .tmp/release.json release list .
uv run ssot --output-format json --output-file .tmp/profile.json profile list .
uv run ssot graph export . --format json --output .tmp/graph.json
uv run ssot registry export . --format json --output .tmp/registry.json
uv run ssot validate .
```

