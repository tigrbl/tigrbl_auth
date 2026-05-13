# Certification Gap Inventory

- package: `tigrbl_auth`
- SSOT validation passed: `True`
- registry counts: `{'features': 575, 'profiles': 6, 'tests': 273, 'claims': 494, 'evidence': 105, 'issues': 26, 'risks': 1}`
- current partial or absent features: `16`
- draft profiles: `0`
- open issues: `19`
- active risks: `1`
- dirty worktree: `True`

## Current Feature Gaps

- `feat:authorization-decision-trace-artifact`: absent - Authorization decision trace artifact
- `feat:authorization-provenance-hash`: absent - Authorization provenance hash
- `feat:delegation-graph-persistence`: absent - Delegation graph persistence
- `feat:delegation-lineage-export`: absent - Delegation lineage export
- `feat:discovery-runtime-snapshot-drift-gate`: absent - Discovery runtime-snapshot drift gate
- `feat:evidence-secret-hygiene-gates`: absent - Evidence secret hygiene gates
- `feat:request-scoped-deployment-authority`: absent - Request-scoped deployment authority
- `feat:resource-verifier-contract-metadata-projection`: absent - Resource verifier contract metadata projection
- `feat:resource-verifier-contract-model`: absent - Resource verifier contract model
- `feat:runtime-plane-hard-isolation-tier`: absent - Runtime-plane hard isolation tier
- `feat:runtime-plane-mixed-mode-downgrade-classification`: absent - Runtime-plane mixed-mode downgrade classification
- `feat:tier4-independent-resource-server-peer`: absent - Tier 4 independent resource-server peer
- `feat:tracked-openid-federation-target`: absent - Tracked OpenID Federation target
- `feat:tracked-spiffe-spire-target`: absent - Tracked SPIFFE/SPIRE target
- `feat:trust-domain-authority-object`: absent - Trust-domain authority object
- `feat:trust-domain-scoped-jwks-authority`: absent - Trust-domain-scoped JWKS authority

## Draft Profiles

- None

## Certification Blockers

- Tier 4 independent peer validation is not complete for the retained boundary.
- The peer-bundle completeness gate is not satisfied for the declared peer-profile set.
- One or more supported peer profiles have incomplete or invalid preserved external evidence bundles.
- Validated in-scope certification lane execution evidence is incomplete or missing.
- At least one claim row is still missing a machine-derived certification proof binding.
- Release evidence can now be built only from a clean checkout, and the current workspace is dirty.

## Delivery Tracks

- Registry and proof-chain closure: Keep every current feature linked to passing tests, evidence, claims, and validation output. Current status: 16 current feature(s) remain partial or absent.
- Runtime and contract closure: Keep executable OpenAPI, OpenRPC, discovery, runner, and deployment profiles aligned with generated artifacts. Current status: Current contract snapshots are generated, but release certification still depends on preserved clean-room evidence.
- Evidence inventory closure: Preserve validated-run manifests for the supported interpreter, profile, runner, and lane matrix. Current status: Validated clean-room and lane inventories remain certification blockers.
- Portability closure: Preserve upgrade, downgrade, and reapply migration evidence for SQLite and PostgreSQL. Current status: Migration portability evidence remains incomplete.
- Peer validation closure: Validate independent peer bundles for the retained supported peer-profile set. Current status: The peer-claim profile remains draft while external bundle validation is incomplete.
- Release certification closure: Produce final release evidence from a clean checkout and certify only after all gates pass. Current status: The current worktree is dirty, so final release evidence cannot be certified from this checkout state.

## Source Marker Scan

- files with marker terms: `121`
- `tigrbl_auth/cli/boundary.py:22` "compliance/targets/partial-feature-consumption.yaml",
- `tigrbl_auth/cli/claims.py:185` if "placeholder" in artifact:
- `tigrbl_auth/cli/feature_surface.py:87` repo_root / "compliance" / "targets" / "partial-feature-consumption.yaml",
- `tigrbl_auth/cli/governance.py:23` "docs/adr/ADR-0016-installable-surfaces-and-partial-feature-consumption.md",
- `tigrbl_auth/cli/install_substrate.py:471` failures.append("dependency lock install profiles are incomplete")
- `tigrbl_auth/cli/runtime.py:270` reasons.append("install substrate evidence is missing or incomplete")
- `tigrbl_auth/cli/reports.py:1292` certification_state["open_gaps"].append("One or more supported peer profiles have incomplete or invalid preserved external evidence bundles.")
- `tigrbl_auth/cli/claim_registry.py:612` failures.append("Public route atomic claim coverage is incomplete.")
- `tigrbl_auth/config/feature_flags.py:71` "description": "Installable surface selection and partial feature consumption.",
- `tigrbl_auth/ops/token.py:131` _jwt = JWTCoder.default if False else None  # placeholder to keep name bound

