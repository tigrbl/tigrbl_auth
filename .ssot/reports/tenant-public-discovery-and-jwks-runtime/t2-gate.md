# Tenant Public Discovery And JWKS Runtime T2 Gate

Boundary: `bnd:tenant-public-discovery-and-jwks-runtime`

The T2 gate verifies fail-closed behavior for tenant discovery and JWKS drift:

- missing tenants return 404 for tenant discovery
- disabled tenants return 404 for tenant JWKS
- tenant JWKS excludes other tenants' keys
- retired tenant keys are hidden from public tenant JWKS
- tenant discovery payloads do not leak sibling tenant paths
- tenant token issuer validation rejects root or wrong issuers

Verification:

```powershell
$env:UV_CACHE_DIR='E:\swarmauri_github\tigrbl_auth\.tmp\uv-cache'; uv run --no-sync pytest tests/unit/test_tenant_public_discovery_boundary.py tests/features/test_tenant_jwks_discovery.py
```

Result: 18 passed.
