> [!WARNING]
> Archived historical reference. This document is retained for audit history only and is **not** an authoritative current-state artifact.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` for the current source of truth.

# tigrbl_auth — Implementation Plan

## Basis

This plan is grounded in two inputs:

1. the unified package planning markdown and current-to-target architectural markdown, which define the certification tiers, implementation s, Tigrbl-native target tree, ADR requirement, release-gate requirement, and CLI/governance surfaces; and
2. the attached `tigrbl_auth.zip` archive, which shows the package is already functionally substantial but architecturally flat.

## Current package findings

The attached archive shows that the package is **not greenfield**. It already contains:

- a Tigrbl composition root in `tigrbl_auth/app.py`
- a `TigrblRouter` assembly root in `tigrbl_auth/routers/surface.py`
- tenant-aware persistence models under `tigrbl_auth/orm/`
- a flat standards implementation layer under `tigrbl_auth/rfc/`
- a flat auth surface under `tigrbl_auth/routers/`
- a package-local vendor indirection layer under `tigrbl_auth/vendor/`
- environment-backed settings in `tigrbl_auth/runtime_cfg.py`
- no live CLI entrypoint, only a commented-out script line in `pyproject.toml`
- no ADR tree
- no compliance target manifests
- no release gate manifests
- no contract artifacts under `specs/`
- no migration framework

The archive also shows strong salvage value:

- 67 unit tests
- 15 integration-style tests under `tests/integration/`
- 1 usage example test
- 37 RFC implementation modules under `tigrbl_auth/rfc/`
- 37 matching RFC-oriented test files

That means the package is best handled as a **controlled restructure with certification layering**, not a rewrite.

## Program objective

Build a **Tigrbl-native, certifiable, evidence-first** `tigrbl_auth` package that:

- adheres strictly to the Tigrbl framework shape
- uses ADRs for architectural decisions
- enforces release gates as code
- exposes explicit OpenAPI and OpenRPC contracts
- carries a machine-readable standards target matrix
- supports certification tiers through independent peer claims
- is fully compliant to the **declared auth-server target boundary**
- avoids backward-compatibility shims

## Interpretation of “fully RFC compliant”

For this package, “fully RFC compliant” must mean:

- every **declared** target RFC/spec is explicitly listed in manifests
- every declared target maps to runtime modules, endpoints, tests, ADRs, and evidence
- every declared target has negative tests where security-sensitive
- every declared target is covered by release gates
- no undeclared target is implied by package layout or marketing claims

It does **not** mean “claim every adjacent auth/security RFC currently represented by helper code.”

## Non-negotiable design decisions

1. **No compatibility shims.**
   Every structural slice is moved atomically. Imports, tests, and docs are updated in the same change set.

2. **Keep the import root `tigrbl_auth/`.**
   Do not introduce a `src/` split.

3. **Move to the Tigrbl-native runtime shape.**
   Runtime code is organized around:
   - `plugin.py`
   - `gateway.py`
   - `api/`
   - `tables/`
   - `ops/`
   - `services/`
   - `standards/`
   - `security/`
   - `config/`
   - `adapters/`
   - `migrations/`

4. **Delete `vendor/`.**
   Import directly from `tigrbl`, `fastapi`, `pydantic`, `sqlalchemy`, and first-party Swarmauri packages.

5. **Replace flat `rfc/` with domain-grouped `standards/`.**
   RFC numbers are claim metadata and test organization, not primary runtime architecture.

6. **Add a first-class governance plane.**
   `docs/adr/`, `compliance/`, `specs/`, and release gates must exist before certification work begins.

7. **OpenRPC is control-plane only.**
   OAuth/OIDC interoperability remains HTTP-based.

8. **Do not formally claim OAuth 2.1 as an RFC target.**
   Use an `oauth2_1_alignment` profile instead.

## Program structure

The implementation is organized into nine workstreams executed in four certification s.

---

# foundation-boundary — Boundary definition and governance installation

## Workstream 0 — Freeze certification boundary

### Objective
Define exactly what enters the certifiable auth-server boundary and what moves to optional extensions.

### Tasks
- Adopt the canonical standards matrix as the package claim boundary.
- Split targets into:
  - **core certifiable boundary**
  - **optional extensions**
  - **out-of-boundary helpers**
- Lock target profiles:
  - `baseline`
  - `production`
  - `hardening`
  - `peer-claim`
- Reword package claims so they align to the matrix.
- Remove implicit or overstated claims from README and public API.

### Core baseline target set
The initial core claim set should include:

- RFC 6749
- RFC 6750
- RFC 7636
- RFC 8414
- RFC 5785
- RFC 7515
- RFC 7517
- RFC 7518
- RFC 7519
- OIDC Core
- OIDC Discovery

### Production target set
Add:

- RFC 7009
- RFC 7662
- RFC 7591
- RFC 8252
- RFC 9068
- RFC 6265
- OIDC UserInfo
- OIDC Session Management
- OIDC RP-Initiated Logout

### Hardening target set
Add:

- RFC 7592
- RFC 8628
- RFC 8693
- RFC 8707
- RFC 9101
- RFC 9126
- RFC 9396
- RFC 9449 and/or RFC 8705
- OIDC Front-Channel Logout
- OIDC Back-Channel Logout
- OAuth Security BCP alignment

### Move to `extensions/` unless explicitly promoted later
At minimum, quarantine these until they are deliberately included with evidence:

- Web Push encryption helpers
- WebAuthn/passkey-specific helpers
- SET/security-event-token helpers
- any non-core metadata enhancement helpers not part of the formal target matrix
- any helper whose current RFC mapping is ambiguous or outside the auth-server certification boundary

### Deliverables
- `compliance/targets/rfc-targets.yaml`
- `compliance/targets/oidc-targets.yaml`
- `compliance/targets/openapi-targets.yaml`
- `compliance/targets/openrpc-targets.yaml`
- `compliance/targets/profiles.yaml`
- ADR-0002 certification boundary
- ADR-0005 standards vs extensions separation

### Exit criteria
- Every claimed standard is declared.
- Every undeclared standard is either removed or placed under `extensions/`.
- Public docs no longer overclaim the target surface.

---

## Workstream 1 — Install ADRs, manifests, and release-gate skeleton

### Objective
Create the governance plane before further runtime refactoring.

### Tasks
- Create `docs/adr/` and adopt numbering plus template.
- Create `compliance/targets/`, `compliance/mappings/`, `compliance/claims/`, `compliance/evidence/`, `compliance/gates/`, and `compliance/waivers/`.
- Write the first ADRs:
  - ADR-0001 use ADRs
  - ADR-0002 certification boundary
  - ADR-0003 Tigrbl-native package shape
  - ADR-0004 remove vendor shims
  - ADR-0005 standards vs extensions
  - ADR-0006 release gates as code
  - ADR-0007 OpenAPI/OpenRPC generation
  - ADR-0008 evidence retention and peer-claim policy
- Create target mappings:
  - feature → target
  - target → endpoint
  - target → test
  - target → evidence
  - target → ADR

### Deliverables
- `docs/adr/*`
- `compliance/mappings/*.yaml`
- initial gate manifests

### Exit criteria
- Every core target links to at least one ADR placeholder.
- Gate files exist, even if some checks are initially advisory.

---

# baseline-interoperability — Tigrbl-native structural reshape and interoperable baseline

## Workstream 2 — Reshape the runtime package to the target tree

### Objective
Move the package from the current flat runtime layout to the Tigrbl-native tree.

### Source modules to migrate
Current runtime sources:

- `app.py`
- `backends.py`
- `crypto.py`
- `db.py`
- `errors.py`
- `security.deps.py`
- `jwtoken.py`
- `oidc_discovery.py`
- `oidc_id_token.py`
- `oidc_userinfo.py`
- `runtime_cfg.py`
- `principal_ctx.py`
- `orm/*`
- `routers/*`
- `rfc/*`
- `vendor/*`

### Target structure
Create the following runtime tree under `tigrbl_auth/`:

- `plugin.py`
- `gateway.py`
- `api/`
  - `app.py`
  - `lifecycle.py`
  - `surfaces.py`
  - `rest/`
  - `rpc/`
- `tables/`
- `ops/`
- `services/`
- `standards/`
- `extensions/`
- `security/`
- `config/`
- `adapters/`
- `schemas/`
- `migrations/`

### Atomic move map
- `app.py` → `api/app.py` plus `gateway.py`
- `routers/surface.py` → `api/surfaces.py`
- `routers/auth_flows.py` → `api/rest/routers/*` + `ops/login.py` / `ops/logout.py` / `ops/authorize.py`
- `routers/authz/oidc.py` → `api/rest/routers/authorize.py` + `ops/authorize.py` + `standards/oidc/*`
- `orm/*` → `tables/*`
- `db.py` → `tables/engine.py` and shared DB/session helpers
- `runtime_cfg.py` → `config/settings.py`
- `security.deps.py` → `api/rest/deps/*` and `security/deps.py`
- `crypto.py` → `services/key_management.py` and `standards/jose/*`
- `jwtoken.py` → `standards/jose/jwt.py` + `services/token_service.py`
- `oidc_discovery.py` → `standards/oidc/discovery.py` + discovery router
- `oidc_id_token.py` → `standards/oidc/id_token.py`
- `oidc_userinfo.py` → `standards/oidc/userinfo.py` + `ops/userinfo.py`
- `rfc/*` → `standards/{oauth2,oidc,jose,http}/*`
- `vendor/*` → deleted

### Rules
- No compatibility alias modules.
- No partial dual-tree state.
- Update tests and imports in the same PR as each move.

### Deliverables
- complete target runtime tree
- deleted `vendor/`
- deleted flat `rfc/`
- deleted flat `routers/`
- deleted `orm/`

### Exit criteria
- All imports resolve through the target tree only.
- Tests no longer reference removed paths.
- Application still boots under the new tree.

---

## Workstream 3 — Create `plugin.py` and `gateway.py`

### Objective
Make the package conform to the Tigrbl integration model.

### Tasks
- Implement `plugin.install(app, settings=...)` to mount REST and RPC surfaces into an existing `TigrblApp`.
- Implement `gateway.py` as the standalone service assembly root.
- Keep `api/app.py` focused on app construction and lifecycle wiring only.
- Move startup initialization out of the current top-level app module into `api/lifecycle.py`.

### Deliverables
- `tigrbl_auth/plugin.py`
- `tigrbl_auth/gateway.py`
- `tigrbl_auth/api/app.py`
- `tigrbl_auth/api/lifecycle.py`

### Exit criteria
- The package supports both embedded plugin installation and standalone service execution.

---

## Workstream 4 — Establish the interoperable baseline standards surface

### Objective
Ship the baseline-interoperability baseline using the new structure.

### Tasks
#### HTTP / well-known
- `standards/http/well_known.py`
- `standards/http/tls.py`
- publish `/.well-known/openid-configuration`
- publish `/.well-known/oauth-authorization-server`
- publish JWKS

#### JOSE / JWT
- `standards/jose/jws.py`
- `standards/jose/jwk.py`
- `standards/jose/jwa.py`
- `standards/jose/jwt.py`
- `standards/jose/thumbprint.py`

#### OAuth 2.0 baseline
- `standards/oauth2/core.py`
- `standards/oauth2/bearer.py`
- `standards/oauth2/pkce.py`
- `standards/oauth2/metadata.py`

#### OIDC baseline
- `standards/oidc/core.py`
- `standards/oidc/discovery.py`
- `standards/oidc/id_token.py`

#### REST routers
- authorization endpoint
- token endpoint
- metadata endpoint
- discovery endpoint
- JWKS endpoint

### Deliverables
- working baseline-interoperability runtime surface
- initial OpenAPI 3.1 generation
- initial claim manifests at Tier 2

### Exit criteria
- Authorization code + PKCE works.
- Discovery and JWKS validate.
- OpenAPI 3.1 builds and validates.
- Gate levels up through baseline-interoperability/Tier 2 pass.

---

# production-readiness — Production completion

## Workstream 5 — Persistence, migrations, and data-model hardening

### Objective
Replace implicit DB bootstrapping with an explicit migration framework and durable data model.

### Tasks
- Create `tables/base.py`, `tables/engine.py`, `tables/mixins.py`.
- Move current ORM models into `tables/`.
- Add missing core tables where required:
  - `consent.py`
  - `audit_event.py`
- Add migration environment and versions.
- Create ordered migration set:
  - 0001 initial identity tables
  - 0002 client and service tables
  - 0003 authorization runtime tables
  - 0004 device/PAR/revocation tables
  - 0005 session/logout tables
  - 0006 key rotation and audit tables
- Add schema drift detection.

### Deliverables
- `migrations/env.py`
- `migrations/versions/*`
- migration CLI wiring

### Exit criteria
- Fresh bootstrap works.
- Upgrade/downgrade works.
- Drift check passes.

---

## Workstream 6 — Production standards tranche

### Objective
Bring the package to evidence-backed production certification.

### Targets to complete
- RFC 7009 token revocation
- RFC 7662 token introspection
- RFC 7591 dynamic client registration
- RFC 8252 native app handling
- RFC 9068 JWT access token profile
- RFC 6265 cookie/session policy
- OIDC UserInfo
- OIDC Session Management
- OIDC RP-Initiated Logout

### Tasks
- Split current RFC and OIDC helpers into standards modules and ops modules.
- Introduce explicit session services and cookie policy services.
- Add access-token validation profile for JWT resource-server interop.
- Add registration router and client metadata validation.
- Introduce audit logging for revocation, session, registration, and token issuance.

### Deliverables
- production-ready standards modules
- production OpenAPI coverage
- Tier 3 evidence-backed internal claims for production-readiness targets

### Exit criteria
- Revocation and introspection produce preserved evidence.
- Browser session and logout behavior are documented and tested.
- Client registration passes conformance and negative tests.

---

## Workstream 7 — Contract plane and CLI surface

### Objective
Materialize the published API contracts and operational CLI.

### Tasks
#### Contracts
- Generate OpenAPI 3.1 public/admin specs under `specs/openapi/`.
- Generate OpenRPC control-plane specs under `specs/openrpc/`.
- Add `rpc.discover` and contract/runtime parity checks.
- Add spec build, validate, diff, and publish commands.

#### CLI
Create `tigrbl_auth/cli/` with subcommands:
- `serve`
- `migrate`
- `spec`
- `verify`
- `gate`
- `evidence`
- `claims`
- `adr`
- `doctor`
- `keys`

Enable the package entry point:

```toml
[project.scripts]
tigrbl-auth = "tigrbl_auth.cli:app"
```

### Deliverables
- generated specs
- CLI entry point
- CLI subcommands wired to compliance and runtime services

### Exit criteria
- Spec build/validate/diff/publish is automated.
- CLI can run gates, collect evidence, and inspect claims.

---

# hardening-interop — Hardening, advanced interop, and peer claims

## Workstream 8 — Hardening standards tranche

### Objective
Complete the hardened target set needed for enterprise and peer-claim readiness.

### Targets to complete
- RFC 7592 client management
- RFC 8628 device flow
- RFC 8693 token exchange
- RFC 8707 resource indicators
- RFC 9101 JAR
- RFC 9126 PAR
- RFC 9396 RAR
- RFC 9449 DPoP and/or RFC 8705 mTLS
- OIDC Front-Channel Logout
- OIDC Back-Channel Logout
- refresh-token rotation
- key-rotation and replay defenses
- OAuth Security BCP alignment

### Recommended order
1. Device flow
2. Token exchange
3. Resource indicators
4. JAR
5. PAR
6. RAR
7. DPoP
8. mTLS
9. front-channel logout
10. back-channel logout
11. replay/rotation hardening

### Why this order
- It aligns to the current codebase, which already has working seeds for device flow, token exchange, DPoP, mTLS, and PAR-like structures.
- It allows hardening features to build on a stable production baseline.
- It keeps sender-constrained tokens late enough that key-management and replay infrastructure already exist.

### Deliverables
- hardened runtime features
- security-specific evidence bundles
- Tier 3/4 candidate claims

### Exit criteria
- Replay protection tests pass.
- Key rotation and JWKS rollover are exercised in automated suites.
- Security gate passes without waivers for claimed hardening targets.

---

## Workstream 9 — Test reclassification, evidence, release gates, and peer-claim promotion

### Objective
Convert the existing broad test base into a certifiable evidence system.

### Use the current test base as seed material
Current archive provides:
- `tests/unit/` with broad RFC coverage
- `tests/integration/` with integration flows
- `tests/examples/` with usage verification

### New test structure
- `tests/unit/`
- `tests/integration/`
- `tests/conformance/`
  - `oauth2/`
  - `jose/`
  - `oidc/`
  - `http/`
- `tests/interop/`
- `tests/negative/`
- `tests/security/`
- `tests/e2e/`
- `tests/perf/`
- `tests/fixtures/`

### Mapping strategy
- Current `tests/integration/*` → `tests/integration/*`
- Current `tests/unit/test_rfc*.py` → `tests/conformance/<domain>/<rfc>/*`
- Current non-RFC behavior tests remain in `tests/unit/`
- Add missing `tests/negative/` for invalid tokens, replay, bad redirect URIs, bad request objects, weak algorithms, etc.
- Add `tests/interop/` against generic RP/RS and selected peer implementations.

### Release gates to implement
Use gate manifests as code:

- gate-00 structure
- gate-10 format/lint/types
- gate-20 unit
- gate-30 integration
- gate-40 conformance
- gate-50 interop
- gate-60 security
- gate-70 contracts
- gate-80 evidence
- gate-90 release

### Evidence system
Implement:
- evidence collection
- evidence bundling
- checksums and manifest verification
- attestation generation
- SBOM capture
- claims locking per release
- waiver review flow

### Tier advancement rules
- **Tier 2**: implemented and internally asserted
- **Tier 3**: preserved evidence + release-gate certification
- **Tier 4**: independent peer report and reproducible interop evidence

### Initial peer targets
Promote to Tier 4 only after external evidence for:
- discovery + JWKS correctness
- bearer validation / RFC 7662 interop
- JWT access-token profile / RFC 9068 interop
- DPoP or mTLS sender-constrained flows
- token exchange where claimed
- front/back-channel logout where claimed

### Deliverables
- full gate system
- evidence bundles
- peer-claim promotion workflow

### Exit criteria
- No Tier 3 claim is releasable without evidence.
- No Tier 4 claim is promotable without independent peer material.

---

# Recommended delivery sequence (PR / change-set order)

## PR-01 — Governance skeleton
Create ADRs, compliance manifests, gate files, and the initial standards matrix. No runtime moves yet.

## PR-02 — Target tree creation
Create empty target tree and move package to the Tigrbl-native shape. Update imports. Remove `vendor/`.

## PR-03 — App composition split
Introduce `plugin.py`, `gateway.py`, `api/app.py`, `api/lifecycle.py`, `api/surfaces.py`.

## PR-04 — Persistence split
Rename `orm/` to `tables/`, split engine/session/bootstrap concerns, and add migrations.

## PR-05 — Standards regrouping
Move flat `rfc/` modules into `standards/` and `extensions/`. Delete the flat `rfc/` tree.

## PR-06 — REST/RPC surface split
Move transport code into `api/rest/` and `api/rpc/`. Split operations into `ops/`.

## PR-07 — baseline-interoperability baseline certification
Complete discovery, metadata, JOSE/JWT, OAuth core, PKCE, OIDC baseline, and OpenAPI 3.1 baseline.

## PR-08 — production-readiness production tranche
Complete revocation, introspection, client registration, native apps, sessions, logout, JWT access-token profile.

## PR-09 — CLI and contract toolchain
Add CLI, OpenAPI/OpenRPC generation, contract validation, and claim inspection tooling.

## PR-10 — hardening-interop hardening tranche
Complete device flow, token exchange, resource indicators, JAR, PAR, RAR, sender-constrained tokens, replay and rotation controls.

## PR-11 — Evidence and gate enforcement
Turn advisory gates into blocking gates and wire evidence/attestation into release flow.

## PR-12 — Interop and peer claims
Add external interop suites and promote selected targets to Tier 4.

---

# Acceptance criteria by ## foundation-boundary accepted when
- certification boundary is frozen
- ADR system exists
- compliance manifests exist
- target mappings exist

## baseline-interoperability accepted when
- target tree is complete
- app/plugin/gateway shape is live
- baseline-interoperability standards baseline works
- OpenAPI 3.1 baseline is generated and validated

## production-readiness accepted when
- migrations are live
- production standards tranche passes conformance
- session/logout and registration are evidence-backed
- contracts and CLI are live

## hardening-interop accepted when
- hardening tranche passes security gate
- interop suites pass
- evidence bundle and attestation are generated automatically
- Tier 4 claims can be promoted via peer material

---

# Risks and mitigation

## Risk 1 — Structural churn breaks import graph
### Mitigation
Move by responsibility slice, not by file type alone. Keep each PR fully green before the next.

## Risk 2 — Flat RFC modules carry mixed responsibilities
### Mitigation
Split runtime behavior into `ops/`, `services/`, and `standards/`; quarantine ambiguous helpers into `extensions/`.

## Risk 3 — Overclaiming standards support
### Mitigation
Only claim targets present in manifests and passing gates.

## Risk 4 — Existing tests do not produce certification evidence
### Mitigation
Reclassify tests and add explicit evidence capture per target.

## Risk 5 — OpenRPC is mistaken for external auth interop
### Mitigation
Limit OpenRPC to internal/admin control-plane surfaces and document that boundary in ADRs and specs.

## Risk 6 — Sender-constrained token work expands scope too early
### Mitigation
Sequence DPoP and mTLS after baseline, token service stabilization, and key rotation infrastructure.

---

# Definition of done

`tigrbl_auth` is done when all of the following are true:

- the package uses the Tigrbl-native tree
- `vendor/`, flat `rfc/`, flat `routers/`, and `orm/` are gone
- ADRs govern major decisions
- standards targets are machine-readable
- OpenAPI and OpenRPC are generated and validated
- migrations are explicit and versioned
- tests are partitioned into unit/integration/conformance/interop/negative/security/e2e/perf
- evidence bundles and attestations are produced automatically
- release gates are blocking
- Tier 3 claims are evidence-backed
- Tier 4 claims require independent peer material
- the package is fully compliant to the declared target boundary, and nothing outside that boundary is implied

## Immediate next actions

1. Freeze the certification boundary and write ADR-0001 through ADR-0005.
2. Create `compliance/targets/`, `compliance/mappings/`, and `compliance/gates/`.
3. Create the target runtime tree and delete `vendor/` in the same change set.
4. Move `orm/` to `tables/` and `routers/` to `api/` without shims.
5. Split `runtime_cfg.py`, `db.py`, `backends.py`, `crypto.py`, and `jwtoken.py` by responsibility.
6. Regroup `rfc/*` into `standards/*` and `extensions/*`.
7. Bring up `plugin.py`, `gateway.py`, and the CLI root.
8. Start baseline-interoperability certification with discovery, metadata, JOSE/JWT, OAuth core, PKCE, and OIDC baseline.
