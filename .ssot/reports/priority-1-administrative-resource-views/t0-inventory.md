# Priority 1 Administrative Resource Views T0 Inventory

Boundary: `bnd:priority-1-administrative-resource-views`

Runtime inventory is implemented by:

- `tigrbl_auth.uix.administrative_resource_views_boundary_manifest`
- `tigrbl_auth.uix.administrative_resource_views_boundary_integrity`
- `tigrbl_identity_operator.uix.administrative_resource_views_boundary_manifest`
- `tigrbl_identity_operator.uix.administrative_resource_views_boundary_integrity`

The manifest enumerates all 9 frozen resource-view feature rows and maps each
row to its view name, required OpenRPC methods, runtime objects, and UI states.

Verification:

```powershell
$env:UV_CACHE_DIR='E:\swarmauri_github\tigrbl_auth\.tmp\uv-cache'; uv run --no-sync pytest tests/uix/test_priority1_administrative_resource_views_boundary.py tests/uix/test_resource_views_contract.py tests/uix/test_resource_views_states.py
```

Result: 7 passed.
