# Phase 5 Provisioning Governance And Ecosystem T1 Behavior

Boundary: `bnd:phase5-provisioning-governance-and-ecosystem-20260505`

The T1 behavior test composes SDK ecosystem alignment, plugin hook execution,
SCIM user/group provisioning, entitlement assignment, access review approval,
campaign closure, and phase 5 summary reporting.

Covered runtime behavior:

- SDK package compatibility and generated contract alignment
- plugin registration, isolated hook execution, and lifecycle audit
- SCIM schema registration, user provisioning, group provisioning, and snapshots
- entitlement definition and assignment inventory
- access review campaign creation, reviewer decision, and closure
- delivery summary aggregation across all phase 5 surfaces

Verification:

```powershell
$env:UV_CACHE_DIR='E:\swarmauri_github\tigrbl_auth\.tmp\uv-cache'; uv run --no-sync pytest tests/unit/test_phase5_governance_extension_boundary.py tests/unit/test_governance_extension_plane_phase5.py
```

Result: 8 passed.
