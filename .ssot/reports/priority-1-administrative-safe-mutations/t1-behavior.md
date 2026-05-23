# Priority 1 Administrative Safe Mutations T1 Behavior

Boundary: `bnd:priority-1-administrative-safe-mutations`

The T1 behavior test executes every safe mutation with exact confirmation text
and verifies required method mapping plus audit outcome projection.

Covered runtime behavior:

- revoke session, revoke token, revoke consent, lock identity, toggle tenant,
  toggle client, rotate key, publish JWKS, and update client registration
- action-to-required-method mapping
- confirmed mutation execution
- executed audit events

Verification:

```powershell
$env:UV_CACHE_DIR='E:\swarmauri_github\tigrbl_auth\.tmp\uv-cache'; uv run --no-sync pytest tests/uix/test_priority1_administrative_safe_mutations_boundary.py tests/uix/test_safe_mutations.py
```

Result: 5 passed.
