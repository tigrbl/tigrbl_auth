# Tenant Public Discovery And JWKS Runtime T0 Inventory

Boundary: `bnd:tenant-public-discovery-and-jwks-runtime`

Runtime inventory is implemented by:

- `tigrbl_auth.services.tenant_discovery.tenant_public_discovery_boundary_manifest`
- `tigrbl_auth.services.tenant_discovery.tenant_public_discovery_boundary_integrity`
- `tigrbl_identity_principals.tenant_public_discovery_boundary_manifest`
- `tigrbl_identity_principals.tenant_public_discovery_boundary_integrity`

The manifest enumerates all 12 frozen boundary feature rows and maps each row
to runtime objects, category, and guarded capability.

Verification:

```powershell
$env:UV_CACHE_DIR='E:\swarmauri_github\tigrbl_auth\.tmp\uv-cache'; uv run --no-sync pytest tests/unit/test_tenant_public_discovery_boundary.py tests/features/test_tenant_jwks_discovery.py
```

Result: 18 passed.
