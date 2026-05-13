## Tenant Trust-Domain Authority Phase 3

This checkpoint captures the tenant trust-domain runtime authority slice for `feat:tenant-trust-domain-authority-object`.

Implemented paths:

- `tigrbl_auth/services/tenant_discovery.py`
- `tigrbl_auth/cli/artifacts.py`

Coverage strengthened:

- `tests/features/test_tenant_jwks_discovery.py`

Validated commands:

```text
uv run pytest tests/features/test_tenant_jwks_discovery.py tests/integration/test_profile_surface_and_contract_alignment.py -k "tenant or jwks or issuer"
```

Observed result:

- tenant issuer, JWKS URI, subject namespace, protected-resource scope, and signing scope now derive from one release-path authority object.
- tenant discovery and tenant artifact generation project that same authority object.
- tenant issuer verification now uses the authority contract instead of an ad hoc expected-string check.
- feature may still remain below full repo closure because broader trust-domain adoption outside tenant discovery and verifier/delegation closure are still open.
