# GitHub Actions Certification Pipeline

## Workflow topology

- `/.github/workflows/pr.yml` calls reusable quality and contract lanes for pull requests.
- `/.github/workflows/main.yml` calls reusable quality, contracts, certification-matrix, and evidence lanes for `main` / `master`.
- `/.github/workflows/release-candidate.yml` builds release candidates, SBOMs, signed bundles, and GitHub artifact attestations.
- `/.github/workflows/release.yml` is the tag-driven final release orchestrator and publishes only after the reusable certification, evidence, and attestation lanes succeed.
- `/.github/workflows/recertify.yml` runs the reusable certification stack on schedule or on demand, then records recertification state.

## Reusable workflows

- `/.github/workflows/_quality.yml`
- `/.github/workflows/_contracts.yml`
- `/.github/workflows/_certification-matrix.yml`
- `/.github/workflows/_evidence.yml`
- `/.github/workflows/_release-bundle.yml`
- `/.github/workflows/_publish.yml`

## Security and provenance posture

- every workflow defaults to `permissions: contents: read`
- `id-token: write` is limited to Trusted Publishing and attestation jobs
- `attestations: write` is limited to attestation-producing jobs
- Ed25519 repository release-bundle signing remains in place
- GitHub build provenance attestations are emitted for generated contracts, wheels, sdists, SBOMs, and release bundles
- the release-bundle workflow verifies those attestations before promotion
- PyPI publication uses Trusted Publishing via the `pypi` environment and no longer uses a long-lived `PYPI_API_TOKEN`

## Repository settings that must be enabled in GitHub

These controls cannot be enforced from the repository contents alone and must be enabled in repository or organization settings:

- branch protection for `main` and `master`
- required status checks for `pr`, `main`, `release-candidate`, `release`, and `recertify`
- secret scanning and secret scanning push protection
- the `pypi` environment with Trusted Publishing configured for this repository

## Current checkpoint truth

This pipeline refactor improves automation and provenance, but it does not by itself make the package certifiably fully featured or certifiably fully RFC/spec compliant. The current authoritative truth remains in:

- `CURRENT_STATE.md`
- `CERTIFICATION_STATUS.md`
- `docs/compliance/current_state_report.md`
- `docs/compliance/certification_state_report.md`
- `docs/compliance/truth_chain.md`
