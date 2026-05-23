# Phase 4 Advanced Identity And Graph Authorization T2 Gate

Boundary: `bnd:phase4-advanced-identity-and-graph-auth-20260505`

The T2 gate verifies fail-closed behavior for advanced identity and graph
authorization drift:

- consumed authentication challenges cannot be replayed
- revoked WebAuthn credentials cannot complete challenges
- SSO/federation sessions reject issuer mismatches
- unsupported provider kinds are rejected
- policy language rejects unsafe constructs
- policy context mismatches deny access decisions
- relationship graph lookups deny when no bounded path grants access
- anomaly telemetry redacts token-bearing details
- revoked trust edges break cross-cloud workload mappings

Verification:

```powershell
$env:UV_CACHE_DIR='E:\swarmauri_github\tigrbl_auth\.tmp\uv-cache'; uv run --no-sync pytest tests/unit/test_phase4_advanced_identity_boundary.py tests/unit/test_advanced_identity_plane_phase4.py
```

Result: 9 passed.
