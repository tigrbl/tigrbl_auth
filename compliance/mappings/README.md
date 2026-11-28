# Mapping Manifests

Mappings provide traceability from a standards target to:
- flags and profiles,
- modules and runtime planes,
- installable surfaces and protocol slices,
- current and target operator surfaces,
- contracts,
- evidence bundles,
- release gates,
- and ADR decisions.

Mappings are release-critical because they prevent ambiguous or orphaned claims.
A feature that disappears from an effective deployment must also disappear from
its effective claims, contracts, and evidence manifests.
- `decision-to-check.yaml` — boundary decision to machine-checkable enforcement mapping
- `decision-to-gate.yaml` — boundary decision to release-gate mapping

- `test_classification.yaml` — canonical test-plane checkpoint test taxonomy and category manifest
- `target-to-test.yaml` — in-scope target to classified test mapping
