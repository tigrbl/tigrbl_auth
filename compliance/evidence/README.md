# Evidence Plane

Evidence is required for claim promotion beyond Tier 1.

## Required evidence structure

- `manifest.yaml` — bundle inventory and policy anchors
- `retention-policy.yaml` — retention and reproducibility rules
- `tier3/` — release-gated internal evidence bundles
- `tier4/` — independent peer evidence bundles
- `schemas/` — expected evidence-bundle document shapes

## Rule

A missing evidence bundle is a certification failure, not a documentation gap.

## runtime-foundation checkpoint3 additions

- `peer_profiles/` — peer profile manifests bound to retained targets, runtime profiles, scenarios, and contract snapshots
- `peer_counterparts/` — external counterpart catalog used for Tier 4 bundle normalization and strict independence requirements
- `tier4/candidates/` — candidate bundle layouts that do **not** count as preserved Tier 4 evidence
- `tier4/bundles/` — normalized preserved external bundles eligible for Tier 4 promotion when populated
- fail-closed promotion logic that refuses independent claims without counterpart identity, runtime/container provenance, scenario coverage, and reproduction material
