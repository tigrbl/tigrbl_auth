# Target Manifests

This directory declares the certification boundary.

## Required files

- `boundaries.yaml`
- `profiles.yaml`
- `target-buckets.yaml`
- `public-operator-surface.yaml`
- `modularity-planes.yaml`
- `partial-feature-consumption.yaml`
- `boundary-decisions.yaml`
- `boundary-enforcement.yaml`
- `rfc-targets.yaml`
- `oidc-targets.yaml`
- `openapi-targets.yaml`
- `openrpc-targets.yaml`
- `extension-targets.yaml`
- `alignment-targets.yaml`
- `legacy-label-corrections.yaml`

## Boundary classes

- `core` — release-claimable within the declared certification boundary
- `extension` — implemented or tracked work that is quarantined by default
- `alignment-only` — tracked for future alignment, not claimable as an RFC

## Rule

A target bucket, public surface, modularity plane, or partial-consumption
profile is not certifiable unless it is declared here and mapped under
`compliance/mappings/`.
- `boundary-certification-plan.yaml` — track-specific certification objective, deliverables, and blockers
- `certification_scope.yaml` — authoritative boundary-lock checkpoint certification scope and reconciliation manifest
- `out-of-scope-baseline.yaml` — explicit out-of-scope capability list for baseline claims hygiene
