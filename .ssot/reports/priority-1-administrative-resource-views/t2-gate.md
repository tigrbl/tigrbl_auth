# Priority 1 Administrative Resource Views T2 Gate

Boundary: `bnd:priority-1-administrative-resource-views`

The T2 gate verifies fail-closed method backing for administrative resource
views:

- complete views remain backed when their methods are available
- missing `client.show` blocks the client view
- missing `keys.list` blocks the keys/JWKS view
- missing `evidence.status` blocks the profile-certification view
- blocked views expose exact missing methods instead of silently rendering as
  backed

Verification:

```powershell
$env:UV_CACHE_DIR='E:\swarmauri_github\tigrbl_auth\.tmp\uv-cache'; uv run --no-sync pytest tests/uix/test_priority1_administrative_resource_views_boundary.py tests/uix/test_resource_views_contract.py tests/uix/test_resource_views_states.py
```

Result: 7 passed.
