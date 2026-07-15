# tigrbl-auth-release-certification

Executable release certification and release posture helpers for the Tigrbl auth package suite.

This package owns runtime validation, release posture summaries, disclosure rules, provenance requirements, isolation checks, and certification assertions. It consumes contract DTOs from `tigrbl-release-contracts`; it does not define those DTOs.

## Boundary

- Owns executable release and certification checks.
- Owns runtime capability truth manifests and capability attestations derived
  from resolved deployment state.
- May depend on runtime/concrete packages needed to evaluate release truth.
- Must not own authorization policy decisioning, admin control-plane workflows, storage tables, or protocol runtime behavior.

