# Certification Gap Inventory

- package: `tigrbl_auth`
- SSOT validation passed: `True`
- registry counts: `{'features': 438, 'profiles': 6, 'tests': 223, 'claims': 437, 'evidence': 68, 'issues': 3, 'risks': 1, 'boundaries': 8, 'releases': 1, 'adrs': 60, 'specs': 81}`
- current partial or absent features: `0`
- draft profiles: `1`
- open issues: `1`
- active risks: `1`
- dirty worktree: `True`

## Current Feature Gaps

- None

## Draft Profiles

- `prf:peer-claim`: draft - peer-claim

## Certification Blockers

- Tier 4 independent peer validation is not complete for the retained boundary.
- The fill-in external handoff template package is not present for the full supported peer-profile set.
- The peer-bundle completeness gate is not satisfied for the declared peer-profile set.
- One or more supported peer profiles have incomplete or invalid preserved external evidence bundles.
- The runtime validation stack now executes real app-factory, serve-check, and HTTP surface probes in the clean-room matrix, but successful execution across the supported interpreter/profile matrix is not preserved in this container.
- Tigrcorn is now pinned and included in the clean-room matrix for Python 3.11/3.12, but preserved independent validation artifacts remain absent.
- Validated clean-room install matrix evidence is incomplete or missing.
- Validated in-scope certification lane execution evidence is incomplete or missing.
- Migration upgrade → downgrade → reapply portability has not been preserved for both SQLite and PostgreSQL.
- Tier 3 evidence has not yet been explicitly rebuilt from validated-run manifests.
- One or more operator-visible package capabilities still lacks end-to-end verification in the current environment.
- At least one claim row is still missing a machine-derived certification proof binding.
- Release evidence can now be built only from a clean checkout, and the current workspace is dirty.

## Delivery Tracks

- Registry and proof-chain closure: Keep every current feature linked to passing tests, evidence, claims, and validation output. Current status: No current feature is missing claims, tests, evidence, or implementation status.
- Runtime and contract closure: Keep executable OpenAPI, OpenRPC, discovery, runner, and deployment profiles aligned with generated artifacts. Current status: Current contract snapshots are generated, but release certification still depends on preserved clean-room evidence.
- Evidence inventory closure: Preserve validated-run manifests for the supported interpreter, profile, runner, and lane matrix. Current status: Validated clean-room and lane inventories remain certification blockers.
- Portability closure: Preserve upgrade, downgrade, and reapply migration evidence for SQLite and PostgreSQL. Current status: Migration portability evidence remains incomplete.
- Peer validation closure: Validate independent peer bundles for the retained supported peer-profile set. Current status: The peer-claim profile remains draft while external bundle validation is incomplete.
- Release certification closure: Produce final release evidence from a clean checkout and certify only after all gates pass. Current status: The current worktree is dirty, so final release evidence cannot be certified from this checkout state.

## Source Marker Scan

- files with marker terms: `115`
- `tigrbl_auth/cli/boundary.py:22` "compliance/targets/partial-feature-consumption.yaml",
- `tigrbl_auth/cli/claims.py:180` if "placeholder" in artifact:
- `tigrbl_auth/cli/feature_surface.py:87` repo_root / "compliance" / "targets" / "partial-feature-consumption.yaml",
- `tigrbl_auth/cli/governance.py:23` "docs/adr/ADR-0016-installable-surfaces-and-partial-feature-consumption.md",
- `tigrbl_auth/cli/install_substrate.py:470` failures.append("dependency lock install profiles are incomplete")
- `tigrbl_auth/cli/runtime.py:269` reasons.append("install substrate evidence is missing or incomplete")
- `tigrbl_auth/cli/reports.py:1277` certification_state["open_gaps"].append("One or more supported peer profiles have incomplete or invalid preserved external evidence bundles.")
- `tigrbl_auth/cli/claim_registry.py:612` failures.append("Public route atomic claim coverage is incomplete.")
- `tigrbl_auth/config/feature_flags.py:71` "description": "Installable surface selection and partial feature consumption.",
- `tigrbl_auth/ops/token.py:131` _jwt = JWTCoder.default if False else None  # placeholder to keep name bound
