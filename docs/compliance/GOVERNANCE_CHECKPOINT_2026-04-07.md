# RFC-family runtime checkpoint Governance Checkpoint

## Implemented in-repo

- `/.github/CODEOWNERS` now assigns ownership for compliance, standards, security, workflows, and release-sensitive files
- `/compliance/governance/github-release-controls.yaml` now records the required GitHub branch, environment, and scanning controls as machine-readable release policy
- `/docs/runbooks/GITHUB_RELEASE_CONTROLS.md` now records the exact platform settings required to make the certification pipeline enforceable

## Not yet enforced from GitHub

The following controls still require direct GitHub repository configuration:

- branch protection or rulesets for `main` and `release/*`
- required status checks for the reusable certification pipeline
- environment protection for `pypi` and `production-release`
- secret scanning and push protection
- code scanning enablement
- dependency review enablement
- Dependabot alerts enablement

## Truthful current state

this track improves governance readiness, but it does not complete external GitHub enforcement by itself.

As of this checkpoint:

- `repository_settings_enforced_from_github_now = false`
- `repository_settings_materialized_in_repo_now = true`
- `can_merge_around_pipeline_now = true`
- `can_publish_around_attestations_now = true`

The repository therefore remains a certification checkpoint, not a final certifiable release.
