# Priority 1 Administrative Safe Mutations T0 Inventory

Boundary: `bnd:priority-1-administrative-safe-mutations`

Runtime inventory is implemented by:

- `tigrbl_auth.uix.administrative_safe_mutations_boundary_manifest`
- `tigrbl_auth.uix.administrative_safe_mutations_boundary_integrity`
- `tigrbl_identity_operator.uix.administrative_safe_mutations_boundary_manifest`
- `tigrbl_identity_operator.uix.administrative_safe_mutations_boundary_integrity`

The manifest enumerates all 9 frozen safe-mutation feature rows and maps each
row to its action, required OpenRPC method, runtime objects, and guarded
capabilities.

Verification:

```powershell
$env:UV_CACHE_DIR='E:\swarmauri_github\tigrbl_auth\.tmp\uv-cache'; uv run --no-sync pytest tests/uix/test_priority1_administrative_safe_mutations_boundary.py tests/uix/test_safe_mutations.py
```

Result: 5 passed.
