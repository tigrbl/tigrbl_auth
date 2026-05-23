# Priority 1 Administrative Resource Views T1 Behavior

Boundary: `bnd:priority-1-administrative-resource-views`

The T1 behavior test composes all administrative resource views from the
baseline-development OpenRPC contract and proves every required method is
present.

Covered runtime behavior:

- tenant, client, identity, session, token, consent, audit, keys/JWKS, and
  profile-certification view construction
- required OpenRPC method mapping per view
- backed view status for complete contracts
- stable empty/loading/error/filtered/detail view states

Verification:

```powershell
$env:UV_CACHE_DIR='E:\swarmauri_github\tigrbl_auth\.tmp\uv-cache'; uv run --no-sync pytest tests/uix/test_priority1_administrative_resource_views_boundary.py tests/uix/test_resource_views_contract.py tests/uix/test_resource_views_states.py
```

Result: 7 passed.
