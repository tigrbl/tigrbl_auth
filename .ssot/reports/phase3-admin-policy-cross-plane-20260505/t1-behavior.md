# Phase 3 Admin Policy Cross-Plane T1 Behavior

Boundary: `bnd:phase3-admin-policy-cross-plane-20260505`

The T1 behavior test composes service identity authentication, RBAC, ABAC,
dynamic conditions, delegated tenant scope, tenant visibility filtering, policy
simulation, policy audit, and compliance reporting in one in-process runtime
stack.

Covered runtime behavior:

- service identity registration, credential issuance, and authentication
- RBAC role assignment and effective permission resolution
- ABAC attribute and dynamic-condition authorization
- policy engine evaluation with audit event recording
- delegated admin tenant visibility and mutable client-field scope
- compliance report assembly across tenants, clients, policy, and services

Verification:

```powershell
$env:UV_CACHE_DIR='E:\swarmauri_github\tigrbl_auth\.tmp\uv-cache'; uv run --no-sync pytest tests/unit/test_phase3_admin_policy_boundary.py tests/uix/test_rbac_admin.py tests/uix/test_abac_admin.py tests/uix/test_policy_simulation.py
```

Result: 8 passed.
