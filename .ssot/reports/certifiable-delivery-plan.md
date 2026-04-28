# Certifiable Delivery Plan

Generated: 2026-04-28T03:07:00Z

## Current State

- SSOT validation passes with 438 features, 6 profiles, 223 tests, 437 claims, 68 evidence rows, 3 issues, and 1 risk.
- SSOT profile validation now has 5 passing active profiles and 1 draft profile. `prf:baseline-development` was promoted to active after CLI profile evaluation passed.
- The verified test registry now has 221 passing tests and no planned test rows.
- Active feature implementation no longer has active absent rows. The remaining absent feature rows are retired or out-of-scope ADR CLI verbs.
- The active provenance naming guard passes, and renamed negative/security proof tests pass.
- The retained-boundary Tier 3 materializer now strips chronology-scoped provenance labels from generator-owned metadata and copied release-bundle evidence paths.
- Pytest now defaults to the repo-local `.pytest-tmp` base temp root, preventing Windows user-temp permission failures from blocking focused and full-suite verification.
- Tier 4 checkpoint repo-copy tests now ignore `.pytest-tmp*` and `.pytest_cache*` so verification temp roots do not recursively poison clean-copy checks.
- The Tier 4 checkpoint fixture copy is now bounded away from generated caches, local virtual environments, transient temp roots, distribution output, and local database files. `tests/unit/test_tier4_checkpoint.py` passes locally.
- The full local pytest suite passes with 558 passed and 2 skipped tests.
- Current contract snapshots are regenerated from executable OpenAPI/OpenRPC/discovery builders, and contract sync now passes.
- Feature-completeness capability closure is now 8 of 10. The remaining capability blockers are supported runner matrix evidence and SQLite/PostgreSQL migration portability evidence.
- Shared pytest fixtures now keep SQLite databases and key-provider material under the repo-local pytest temp root and reset OIDC facade/canonical key-provider caches together.
- Runtime OpenAPI and OpenRPC contract payloads are delegated to the upstream Tigrbl application. The admin gate protects enabled control-plane surfaces without rewriting contract bodies.
- Public-only discovery artifacts now match executable deployment metadata. The public profiles no longer claim the admin OpenRPC target.
- The OpenAPI jsonSchemaDialect issue is closed because generated OpenAPI artifacts omit the dialect field.
- Retained-boundary Tier 3 runtime/operator bundles can now be regenerated from the repo-local transcript and current release-bundle artifacts.
- The peer-claim profile remains draft because preserved external bundles are present but invalid.

## Remaining Certification Blockers

- Tier 4 independent peer validation is not complete for the retained boundary.
- Independent peer-profile bundle validation is incomplete; the external handoff template package is now generated.
- Preserved validated-run inventory is missing for the clean-room interpreter/profile matrix.
- Preserved in-scope test lane evidence is missing.
- Migration upgrade, downgrade, and reapply portability evidence is not preserved for both SQLite and PostgreSQL.
- Tier 3 evidence has not been rebuilt from validated-run manifests.
- All registered test rows are now passing, but release certification still requires preserved clean-room evidence and peer-validation artifacts.
- Release evidence cannot be certified from the current dirty workspace.
- The peer-claim profile remains draft until independent peer bundles validate.
- Active SSOT test rows, active test paths, Tier 3 evidence report paths, active Tier 3 evidence metadata, and package runtime status values now use capability-scoped names. Generated compliance report content and preserved bundle metadata still expose chronology-oriented provenance names. SSOT tracks this as `iss:active-provenance-naming-blocks-certification` and `rsk:legacy-provenance-evidence-ambiguity`.
- Retained-boundary generated bundle metadata and copied retained-boundary release-bundle evidence paths now use capability-scoped names. Broader generated compliance reports, target manifests, and legacy bundle metadata still expose chronology-oriented provenance names.

## Delivery Workstreams

### Implemented In This Run

- Promoted `prf:baseline-development` from draft to active through the SSOT CLI after `profile evaluate` passed.
- Added `tests/unit/test_runtime_profile_configuration.py::test_development_profile_is_active_in_ssot_registry` so the packaged development deployment profile cannot silently regress to draft.
- Added the repo-local retained-boundary runtime/operator transcript at `docs/compliance/retained-boundary-runtime-operator-test-output.txt`.
- Updated the retained-boundary Tier 3 materializer to emit capability-scoped generator metadata and resolve current release-bundle artifacts instead of a stale package-version path.
- Regenerated retained-boundary Tier 3 runtime/operator evidence bundles successfully.
- Verified the full local suite with `558 passed, 2 skipped` and revalidated SSOT successfully.
- Repaired the authoritative `.ssot/registry.json` after BOM/truncation made every SSOT CLI read fail.
- Refreshed stale SPEC-1051 and SPEC-1052 hashes and restored SSOT validation.
- Added `tests/unit/test_ssot_registry_integrity.py` to fail fast on BOM-encoded, unparsable, truncated, or duplicate-ID registry content.
- Added SSOT feature, claim, test, and evidence rows for `feat:ssot-registry-json-integrity`, `clm:ssot-registry-json-integrity`, `tst:tests-unit-test-ssot-registry-integrity-py`, and `evd:ssot-registry-integrity-passed-json`.
- Updated the document-authority regression to verify the supported loader contract after the SPEC CLI rewrote non-schema extension fields.
- Renamed active Tier 3 retained-boundary runtime/operator transcript files from chronology-scoped names to `retained-boundary-runtime-operator-test-output.txt`.
- Updated the retained-boundary Tier 3 materialization script so regenerated bundles use capability-scoped report names and metadata.
- Extended `tests/unit/test_provenance_naming_guard.py` to fail when active Tier 3 evidence report paths regress to chronology-scoped names.
- Updated the SSOT feature, issue, and risk descriptions through the SSOT CLI to reflect the reduced but still release-blocking provenance naming gap.
- Replaced active package runtime status values that used chronology-scoped names with capability-scoped names across OAuth/OIDC owner modules.
- Extended `tests/unit/test_provenance_naming_guard.py` to fail when active runtime status values regress to chronology-scoped names.
- Updated Tier 3 runtime contract snapshots for the renamed capability-scoped runtime status values.
- Extended `tests/unit/test_provenance_naming_guard.py` to fail when active Tier 3 evidence contracts, manifests, mappings, hashes, or signatures regress to chronology-scoped names.
- Updated the retained-boundary release-bundle snapshot to reference `retained-boundary-runtime-operator-test-output.txt` instead of deleted chronology-scoped targeted-test transcripts.
- Updated the SSOT provenance issue, risk, and evidence rows through the SSOT CLI to capture the expanded guard scope.
- Extended the provenance guard to cover retained-boundary generator-owned bundle metadata.
- Updated the retained-boundary Tier 3 materializer to sanitize chronology-scoped copied evidence strings while preserving source artifacts.
- Regenerated retained-boundary Tier 3 evidence bundles after the materializer update.
- Fixed the Tier 4 checkpoint repo-copy fixture to ignore repo-local pytest temp roots created by verification runs.
- Verified the provenance, registry integrity, Tier 3 rebuild, release-bundle signing, final aggregation, and Tier 4 checkpoint slices locally. A full-suite attempt reached 89% without reported failures before the 15-minute command timeout; the late-suite timeout was reproduced and narrowed to the Tier 4 repo-copy temp-root issue, which now passes in isolation.
- Extended the provenance guard to cover current document-authority projections and current review/status reports.
- Removed the chronology-scoped current-doc reference from the document-authority projection generator and the report authoring list.
- Regenerated package review, non-RFC status, current-state, certification-state, OpenAPI, OpenRPC, and discovery report artifacts from current executable sources.
- Updated the active provenance feature, issue, and risk rows through the SSOT CLI to reflect the narrowed release blocker.
- Closed the contract-sync feature-completeness gap by regenerating profile OpenAPI/OpenRPC snapshots from executable builders and verifying focused contract tests.
- Added a current certification gap inventory generator at `scripts/generate_certification_gap_inventory.py`.
- Added `.ssot/reports/certification-gap-inventory.json` and `.ssot/reports/certification-gap-inventory.md` as current SSOT-backed gap review artifacts.
- Added `tests/unit/test_certification_gap_inventory.py` to keep the inventory aligned with live registry counts, proof-chain gaps, and capability-scoped delivery track naming.
- Added SSOT feature, claim, test, and evidence rows for `feat:certification-gap-inventory`, `clm:certification-gap-inventory-current`, `tst:tests-unit-test-certification-gap-inventory-py`, and `evd:ssot-reports-certification-gap-inventory-json`.
- Certified the new gap inventory claim after `claim evaluate` and `evidence verify` passed through the SSOT CLI.
- Declared `tigrbl_auth/profiles/*.yaml` as package data in `pyproject.toml` so runtime profiles remain package resources after build/install.
- Added `tests/unit/test_runtime_profile_configuration.py::test_runtime_profile_yaml_files_are_included_in_build_config` to guard the packaged profile-resource contract.
- Added SSOT test and evidence rows for `tst:runtime-profile-build-config-includes-yaml` and `evd:ssot-reports-development-runtime-profile-build-config-passed-json`.
- Verified the runtime-profile and registry-integrity slice locally with `9 passed`, then revalidated SSOT successfully.
- Added generated external Tier 4 handoff templates under `dist/tier4-external-handoff/` for every supported peer profile.
- Updated `scripts/materialize_tier4_peer_evidence.py` so preserved non-qualifying Tier 4 bundles remain counted and rejected honestly when no external root is supplied.
- Added SSOT evidence row `evd:ssot-reports-peer-validation-external-handoff-templates-passed-json` for the handoff-template pytest proof.
- Verified the Tier 4 peer template and matrix slice locally with `10 passed`, then revalidated SSOT successfully.

### Registry Integrity Closure

Goal: make the SSOT registry itself certifiable before downstream feature, claim, and evidence evaluation.

- Keep `.ssot/registry.json` UTF-8 encoded without BOM.
- Keep all registry entity sections parseable and non-empty.
- Keep entity ids unique within each section.
- Validate with the SSOT CLI after every registry mutation.
- Gate this phase with `tests/unit/test_ssot_registry_integrity.py`, `scripts/generate_claim_registries.py`, full pytest, and SSOT validation.

### Runtime And Contract Closure

Goal: keep the package executable surfaces aligned with generated public artifacts.

- Maintain public-only defaults for package runtime startup.
- Keep diagnostics and admin resources absent from public-only OpenAPI.
- Keep admin OpenRPC claims scoped to mixed and admin-only plugin modes.
- Regenerate discovery snapshots whenever deployment target composition changes.
- Gate this phase with full pytest, artifact truthfulness report generation, and SSOT validation.

### Evidence Inventory Closure

Goal: preserve machine-derived evidence for every retained target.

- Materialize validated-run manifests for all required runtime matrix cells.
- Preserve in-scope lane execution manifests for the current test taxonomy.
- Rebuild Tier 3 evidence from validated-run manifests instead of ad hoc local runs.
- Link all generated evidence back to tests and claims through the SSOT CLI.
- Gate this phase with `validated_inventory_complete`, `runtime_matrix_green`, `in_scope_test_lanes_green`, and `tier3_evidence_rebuilt_from_validated_runs`.

### Portability Closure

Goal: prove migration portability across declared storage targets.

- Run upgrade, downgrade, and reapply flows for SQLite.
- Run upgrade, downgrade, and reapply flows for PostgreSQL.
- Preserve logs, manifests, and checksums as evidence rows.
- Link storage portability evidence to the migration and bootstrap claims.
- Gate this phase with `migration_portability_passed`.

### Provenance Naming Closure

Goal: make active proof chains capability-scoped rather than chronology-scoped.

- Rename active test files and evidence manifests to capability and target names.
- Preserve historical chronology references only under archived/historical evidence roots.
- Update generated compliance reports and preserved bundle metadata to point at renamed paths.
- Keep passing regressions that block active SSOT-facing test names, Tier 3 evidence paths, Tier 3 evidence metadata, and runtime status values from using chronology labels.
- Close `iss:active-provenance-naming-blocks-certification` and mitigate `rsk:legacy-provenance-evidence-ambiguity` only after the renamed proof chain validates.

### Peer Validation Closure

Goal: finish independent certification for the retained boundary.

- Produce the external handoff template set for every supported peer profile.
- Validate each preserved peer bundle.
- Promote valid peer bundles into Tier 4 evidence.
- Move the peer-claim profile out of draft only after all bundle checks pass.
- Gate this phase with peer bundle completeness, zero invalid peer bundles, and strict independent claims readiness.

### Release Certification Closure

Goal: certify the package from a clean checkout.

- Start from a clean worktree after implementation changes are reviewed.
- Regenerate current-state, certification-state, truth-chain, install-substrate, runtime-profile, feature-completeness, and release-gate reports.
- Build, sign, verify, and preserve the release bundle.
- Re-run full pytest and SSOT validation.
- Certify only when `fully_certifiable_now`, `fully_rfc_compliant_now`, and release evidence clean-checkout checks all pass.

## Immediate Follow-Up Work

- Execute the preserved clean-room matrix outside this local single-interpreter run.
- Generate qualifying independent external peer bundles from the handoff assets.
- Preserve SQLite and PostgreSQL migration portability evidence.
- Finish renaming old chronology-oriented evidence paths in a governed pass.
- Preserve the current full-suite execution as durable release evidence before attempting release certification.
