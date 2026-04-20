# Agent Operating Instructions: `ssot-registry`

This repository uses [`ssot-registry`](https://pypi.org/project/ssot-registry/) as the canonical system-of-record for planning, verification, certification gating, and release readiness.

**Effective immediately: agents are required to use the `ssot-registry` CLI command for SSOT operations.**
**Effective immediately: agents are also required to use `uv` for Python/package execution.**

## Why this is mandatory

`ssot-registry` is designed to be a portable single-source-of-truth for:
- features
- tests
- claims
- evidence
- issues
- risks
- boundaries
- releases
- ADRs
- specs

The canonical machine-readable artifact is `.ssot/registry.json` and all downstream reports are derived from it. Do not maintain parallel ad-hoc ledgers for these domains when the CLI supports the operation.

## Baseline assumptions

- Run from repository root unless a subcommand explicitly targets a different path.
- Canonical registry path: `.ssot/registry.json`.
- Validate after any mutation.
- Use `uv` for Python execution, dependency operations, and Python-backed CLIs in this repository.
- Prefer `uv run ...` for project commands and `uv tool run ...` for tool entrypoints instead of raw `python`, `pip`, or direct shim executables when an equivalent `uv` form exists.
- Do not invoke `pip install`, `python -m pip`, or bare `python` for normal repository workflows when `uv` can perform the same operation.
- Prefer machine-readable output when integrating with automation:
  - `--output-format json`
  - optional `--output-file <path>`

## Python and tool invocation policy

- Project-local Python commands should use `uv run`, for example:
  - `uv run pytest ...`
  - `uv run python -m ...`
- Tool-style commands should use `uv tool run` when they are not provided by the project environment.
- SSOT commands should prefer `uv run ssot ...` or another `uv`-managed entrypoint over bare `ssot`, `ssot-cli`, or `ssot-registry` shims when possible.
- If a command fails outside `uv`, retry with an equivalent `uv` invocation before falling back to manual intervention.
- Any deviation from `uv` should be treated as an exception and explained in agent output.

## Core daily workflow

1. **Inspect current state**
   - `ssot-registry registry --help`
   - `ssot-registry feature list .`
   - `ssot-registry claim list .`
   - `ssot-registry test list .`
   - `ssot-registry evidence list .`

2. **Apply updates using entity-specific subcommands**
   - Features: `ssot-registry feature ...`
   - Tests: `ssot-registry test ...`
   - Claims: `ssot-registry claim ...`
   - Evidence: `ssot-registry evidence ...`
   - Releases: `ssot-registry release ...`

3. **Re-validate registry integrity**
   - `ssot-registry validate . --write-report`

4. **Use release and boundary semantics for promotion decisions**
   - Boundary freeze/checks with `ssot-registry boundary ...`
   - Release assembly/status with `ssot-registry release ...`

## Feature tracking (planning + lifecycle)

Use feature entities as the targetable planning unit.

Typical commands:
- Create a feature:
  - `ssot-registry feature create . --id feat:<id> --title "<title>" --description "<desc>"`
- Plan feature horizon/tier:
  - `ssot-registry feature plan . --ids feat:<id> --horizon current --claim-tier T2`
- Link dependencies and verification assets:
  - `ssot-registry feature link . --id feat:<id> --claim-ids clm:<id> --test-ids tst:<id> --requires feat:<dep>`
- Move lifecycle stage:
  - `ssot-registry feature lifecycle set . --ids feat:<id> --stage deprecated --note "<reason>"`

Guidance:
- Track implementation status (`absent|partial|implemented`) on every relevant feature.
- Keep feature links current whenever claims/tests change.
- Use lifecycle metadata (and replacement feature IDs) for deprecations/removals.

## Feature-testing tracking (test coverage + status)

Track tests as first-class registry objects and maintain links to feature/claim/evidence nodes.

Typical commands:
- Create a test:
  - `ssot-registry test create . --id tst:<id> --title "<title>" --kind <kind> --test-path "<path>" --feature-ids feat:<id> --claim-ids clm:<id>`
- Update execution status:
  - `ssot-registry test update . --id tst:<id> --status passing`
- Link produced evidence:
  - `ssot-registry test link . --id tst:<id> --evidence-ids evd:<id>`

Guidance:
- Keep status current (`planned|passing|failing|blocked|skipped`).
- Maintain deterministic `test-path` pointers.
- Ensure each certification-relevant claim has at least one test linkage.

## Claims management

Claims represent assertions about feature properties and behavior.

Typical commands:
- Create claim:
  - `ssot-registry claim create . --id clm:<id> --title "<title>" --kind verification --description "<assertion>" --feature-ids feat:<id>`
- Update claim metadata/status as implementation evolves.
- Link/unlink tests/evidence as verification posture changes.

Guidance:
- Write claims as verifiable assertions.
- Avoid broad, non-testable wording.
- Keep claim-to-feature and claim-to-test relationships explicit.

## Evidence management

Evidence records prove that claims were validated (e.g., test logs, reports, signed bundles, artifact checksums).

Typical commands:
- Create evidence:
  - `ssot-registry evidence create . --id evd:<id> --title "<title>" --kind artifact --evidence-path "<repo-relative-path>" --claim-ids clm:<id> --test-ids tst:<id>`
- Link evidence to tests/claims:
  - `ssot-registry evidence link . --id evd:<id> --test-ids tst:<id> --claim-ids clm:<id>`

Guidance:
- Evidence should be immutable or content-addressed where possible.
- Prefer stable URIs/paths and include enough metadata to reproduce provenance.
- Retire or supersede stale evidence rather than silently re-pointing historical records.

## Release management

Use release entries to capture what is promotable/published and why.

Typical commands:
- Create/update release records:
  - `ssot-registry release create . --id rel:<id> --version <semver> --boundary-id bnd:<id> --claim-ids clm:<id> --evidence-ids evd:<id>`
  - `ssot-registry release certify . --id rel:<id>`
  - `ssot-registry release promote . --id rel:<id>`
  - `ssot-registry release publish . --id rel:<id>`
- Bind releases to boundary scopes and linked claim/evidence sets.
- Run validation before final release decisions:
  - `ssot-registry validate . --write-report`

Guidance:
- Treat boundaries as frozen scope contracts for release decisions.
- A release should have traceable claim/evidence closure against target features.
- If claims/tests/evidence are incomplete, do not mark release-ready.

## Hygiene gates for agents

Before opening or updating a PR that changes scoped behavior:
1. Update feature/claim/test/evidence/release records via `ssot-registry`.
2. Run `ssot-registry validate . --write-report`.
3. Include pertinent registry IDs in PR notes/commit context.

## Upgrade and schema maintenance

If package/schema versions drift, run:
- `ssot-registry upgrade . --sync-docs --write-report`

Always re-run validation after upgrade.

## Non-compliance examples (do not do these)

- Editing `.ssot/registry.json` manually when an equivalent `ssot-registry` command exists.
- Tracking release readiness in ad-hoc markdown tables without corresponding SSOT registry objects.
- Adding tests without creating/linking `tst:*` records.
- Asserting certifications/claims without linked evidence objects.

## Minimal command reference

- General: `ssot-registry -h`
- Validate: `ssot-registry validate -h`
- Feature: `ssot-registry feature -h`
- Test: `ssot-registry test -h`
- Claim: `ssot-registry claim -h`
- Evidence: `ssot-registry evidence -h`
- Boundary: `ssot-registry boundary -h`
- Release: `ssot-registry release -h`
- Registry: `ssot-registry registry -h`

