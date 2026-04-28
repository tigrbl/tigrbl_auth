# Independent package review — 2026-03-26

## Verdict

`tigrbl_auth` is **not certifiably fully featured** and **not certifiably fully RFC/spec compliant** in this checkpoint.

The retained implementation boundary is materially present at Tier 3 for **48 targets**, but final certification is still blocked by missing validated execution evidence and missing preserved independent Tier 4 peer bundles.

## What is complete at the implemented Tier 3 boundary

### RFC targets implemented and mapped

- `RFC 6265`
- `RFC 6749`
- `RFC 6750`
- `RFC 7009`
- `RFC 7515`
- `RFC 7516`
- `RFC 7517`
- `RFC 7518`
- `RFC 7519`
- `RFC 7521`
- `RFC 7523`
- `RFC 7591`
- `RFC 7592`
- `RFC 7636`
- `RFC 7662`
- `RFC 8252`
- `RFC 8414`
- `RFC 8615`
- `RFC 8628`
- `RFC 8693`
- `RFC 8705`
- `RFC 8707`
- `RFC 9068`
- `RFC 9101`
- `RFC 9126`
- `RFC 9207`
- `RFC 9396`
- `RFC 9449`
- `RFC 9700`
- `RFC 9728`

### Non-RFC targets implemented and mapped

- `ASGI 3 application package`
- `Bootstrap and migration lifecycle`
- `CLI operator surface`
- `Import/export portability`
- `Key lifecycle and JWKS publication`
- `OIDC Back-Channel Logout`
- `OIDC Core 1.0`
- `OIDC Discovery 1.0`
- `OIDC Front-Channel Logout`
- `OIDC RP-Initiated Logout`
- `OIDC Session Management`
- `OIDC UserInfo`
- `OpenAPI 3.1 / 3.2 compatible public contract`
- `OpenRPC 1.4.x admin/control-plane contract`
- `Release bundle and signature verification`
- `Runner profile: Hypercorn`
- `Runner profile: Tigrcorn`
- `Runner profile: Uvicorn`

## What is still blocking certification

- Tier 4 independent peer validation is not complete for the retained boundary.
- One or more supported peer profiles still have no preserved external Tier 4 bundle.
- The runtime validation stack now executes real app-factory, serve-check, and HTTP surface probes in the clean-room matrix, but successful execution across the supported interpreter/profile matrix is not preserved in this container.
- Tigrcorn is now pinned and included in the clean-room matrix for Python 3.11/3.12, but preserved independent validation artifacts remain absent.
- The runtime HTTP surface probe did not pass in the current environment.
- The application factory did not materialize in the current environment, so runtime validation could not complete here.
- Real runtime execution probes are implemented in tox and CI, but the full kept-runner probe set was not executed successfully in this container.
- Validated clean-room install matrix evidence is incomplete or missing.
- Validated in-scope certification lane execution evidence is incomplete or missing.
- Migration upgrade → downgrade → reapply portability has not been preserved for both SQLite and PostgreSQL.
- Tier 3 evidence has not yet been explicitly rebuilt from validated-run manifests.

## Additional repository drift fixed in this checkpoint update

- Regenerated CLI reference and conformance artifacts so `docs/reference/CLI_SURFACE.md`, `docs/compliance/cli_conformance_snapshot.*`, and the generated contract artifacts are back in sync with `tigrbl_auth.cli.metadata`.
- Restored dependency-provenance artifact enumeration so runbooks are included in `_dependency_artifact_paths()` and release/dependency manifests expose the expected install-profile documentation.
- Added compatibility fields to `docs/compliance/peer_matrix_report.json` and its generator so existing downstream consumers can read both the canonical and compatibility key names.
- Corrected a stale unit assertion in `tests/unit/test_cli_contract.py` so the test checks the current report semantics instead of expecting a non-gap message inside `open_gaps`.

## Files updated in this checkpoint

- `tigrbl_auth/cli/reports.py`
- `scripts/materialize_tier4_peer_evidence.py`
- `tests/unit/test_cli_contract.py`
- `docs/reference/CLI_SURFACE.md`
- `docs/compliance/cli_conformance_snapshot.json`
- `docs/compliance/cli_conformance_snapshot.md`
- `docs/compliance/peer_matrix_report.json`
- `docs/compliance/PEER_MATRIX_REPORT.md`
- `docs/compliance/TIER4_PROMOTION_MATRIX.md`
- `docs/compliance/current_state_report.json`
- `docs/compliance/current_state_report.md`
- `docs/compliance/certification_state_report.json`
- `docs/compliance/certification_state_report.md`
- `docs/compliance/artifact_truthfulness_report.json`
- `docs/compliance/artifact_truthfulness_report.md`
- `docs/compliance/PACKAGE_REVIEW_GAP_ANALYSIS.json`
- `docs/compliance/PACKAGE_REVIEW_GAP_ANALYSIS.md`

## Files or areas that remain incomplete for certification purposes

- `docs/compliance/validated_execution_report.*` — still records zero validated runtime-matrix artifacts and zero validated test-lane artifacts.
- `docs/compliance/runtime_profile_report.*` — still records app-factory probe failure in this container because the published Tigrbl runtime stack is not installed here.
- `docs/compliance/final_release_gate_report.*` — still fail-closed because runtime, validated execution, migration portability, Tier 3 evidence rebuild, and Tier 4 bundle promotion are incomplete.
- `compliance/evidence/tier4/bundles/` — no preserved qualifying external bundles are counted for final-release truth.
- `dist/tier4-external-handoff/` — templates exist, but completed external submissions are still absent.

## Incomplete or partially complete modules relative to final certification claims

These modules are not necessarily functionally broken, but they are the main owners of the remaining blocked certification lanes:

- `tigrbl_auth/api/app.py` and `tigrbl_auth/gateway.py` — final runtime certification is blocked until the real `tigrbl` runtime dependency stack is present and the app-factory probe passes in the clean-room matrix.
- `tigrbl_auth/cli/runtime.py` and `tigrbl_auth/runtime/*` — runner profiles are declared and smoke-tested, but final kept-runner readiness is still not preserved as validated execution evidence across the supported interpreter/profile matrix.
- `tigrbl_auth/cli/reports.py` — now structurally consistent, but final truth remains negative until validated execution artifacts exist.
- `scripts/materialize_tier4_peer_evidence.py` — now emits compatibility-aware peer-matrix reports, but final Tier 4 promotion still depends on real external preserved bundles.
- `tigrbl_auth/migrations/*` and migration validation workflows — portability is not certifiable until upgrade → downgrade → reapply is preserved for both SQLite and PostgreSQL.

## Current measurable state

- Tier 3 ready targets: `48`
- Tier 4 ready targets: `0`
- Supported peer profiles: `16`
- Missing external peer bundles: `16`
- Validated runtime matrix artifacts: `0` / `14`
- Validated in-scope test lanes: `0` / `15`
- Artifact truthfulness passed: `True`
