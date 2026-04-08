# GitHub Release Controls

## Scope

This runbook records the GitHub repository settings that must be enabled for `Tigrbl/tigrbl_auth` so the certification pipeline becomes an actual release control instead of a documentation-only intention.

## Required branch protection or rulesets

Apply branch protection or repository rulesets to:

- `main`
- `release/*`

Required controls:

- pull requests required before merge
- stale review dismissal enabled
- code owner review required
- last-push approval required
- conversation resolution required
- force pushes blocked
- branch deletion blocked

## Required status checks

Require these checks before merge on protected branches:

- `quality / governance-and-devtest`
- `quality / dependency-review`
- `quality / codeql`
- `contracts / build-contracts`
- `contracts / verify-contract-attestations`
- `certification-matrix / final-certification`
- `evidence / evidence`
- `release-bundle / verify`

For release tags or release branches, require the same certification and attestation model before promotion.

## Environment protection

Create and protect these environments:

- `pypi`
- `production-release`

Recommended environment rules:

- required reviewers
- deployment branch restrictions
- manual approval before publish or promote

## Security features

Enable these repository features in GitHub:

- secret scanning
- secret scanning push protection
- code scanning
- dependency review
- Dependabot alerts
- Dependabot updates

## Repository-owned governance files

- `/.github/CODEOWNERS`
- `/.github/dependabot.yml`
- `/.github/codeql/codeql-config.yml`
- `/.github/workflows/*.yml`
- `/compliance/governance/github-release-controls.yaml`

## Truthful current state

The repository now declares the required governance controls in versioned files, but GitHub platform enforcement is still pending. Until those settings are applied in GitHub itself, the repository can still merge or publish around the intended certification controls.
