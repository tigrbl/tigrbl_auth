# Phase 5 Provisioning Governance And Ecosystem T2 Gate

Boundary: `bnd:phase5-provisioning-governance-and-ecosystem-20260505`

The T2 gate verifies fail-closed behavior for provisioning governance and
ecosystem extension drift:

- SDK registration requires contract alignment metadata
- SDK alignment reports contract version mismatches
- faulty plugin hooks fail in isolated execution and disable the plugin
- disabled plugins cannot execute hooks
- SCIM users require schema-declared required fields
- SCIM patching rejects tenant mismatch and unsupported operations
- access review campaigns cannot close with pending items
- reviewer mismatch is denied
- entitlement revocation and expiry deactivate assignments

Verification:

```powershell
$env:UV_CACHE_DIR='E:\swarmauri_github\tigrbl_auth\.tmp\uv-cache'; uv run --no-sync pytest tests/unit/test_phase5_governance_extension_boundary.py tests/unit/test_governance_extension_plane_phase5.py
```

Result: 8 passed.
