# Tenant Public Discovery And JWKS Runtime T1 Behavior

Boundary: `bnd:tenant-public-discovery-and-jwks-runtime`

The T1 behavior test composes tenant-scoped issuer resolution, tenant OpenID
configuration, tenant JWKS publication, OpenAPI route contracts, profile
artifact snapshots, operator JWKS publication, and runtime JWKS parity.

Covered runtime behavior:

- tenant issuer and trust-domain authority construction
- tenant OpenID configuration route payloads
- tenant JWKS route payloads
- tenant `jwks_uri` construction
- active and next key publication visibility
- operator-generated JWKS parity with runtime route output
- OpenAPI registration for tenant discovery routes
- generated tenant profile discovery artifacts

Verification:

```powershell
$env:UV_CACHE_DIR='E:\swarmauri_github\tigrbl_auth\.tmp\uv-cache'; uv run --no-sync pytest tests/unit/test_tenant_public_discovery_boundary.py tests/features/test_tenant_jwks_discovery.py
```

Result: 18 passed.
