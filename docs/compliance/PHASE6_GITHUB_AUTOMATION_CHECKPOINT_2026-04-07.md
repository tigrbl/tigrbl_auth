# Phase 6 GitHub Automation Checkpoint

## What changed

- the repository now uses reusable GitHub Actions workflows for quality, contracts, certification matrix, evidence, release-bundle assembly, and publish orchestration
- PR, main, release-candidate, release, and recertification entrypoints are split into dedicated top-level workflows
- PyPI publication is configured for Trusted Publishing through the `pypi` environment instead of a long-lived `PYPI_API_TOKEN`
- GitHub artifact attestations are emitted in the workflow design for generated contracts, wheels, sdists, SBOMs, and release bundles
- concurrency groups and explicit least-privilege `permissions:` are defined across the workflow topology
- Dependabot and CodeQL configuration are now committed in-repo

## What is still not automatic from repository contents alone

- branch protection and required status checks must still be enabled in GitHub repository settings
- secret scanning push protection must still be enabled in GitHub repository settings
- the `pypi` environment must still be configured in GitHub with Trusted Publishing enabled for this repository

## Current truthful repository state

This workflow refactor does **not** make the package certifiably fully featured or certifiably fully RFC/spec compliant by itself.

The authoritative current-state documents remain:

- `CURRENT_STATE.md`
- `CERTIFICATION_STATUS.md`
- `docs/compliance/current_state_report.md`
- `docs/compliance/certification_state_report.md`
- `docs/compliance/truth_chain.md`

As of this checkpoint, the repository still reports:

- `fully_certifiable_now = false`
- `fully_rfc_compliant_now = false`
- `strict_independent_claims_ready = false`
- `migration_portability_passed = false`
