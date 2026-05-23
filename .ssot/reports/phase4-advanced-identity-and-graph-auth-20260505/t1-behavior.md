# Phase 4 Advanced Identity And Graph Authorization T1 Behavior

Boundary: `bnd:phase4-advanced-identity-and-graph-auth-20260505`

The T1 behavior test composes advanced authentication, SSO/social/federated
identity providers, device and workload identities, ReBAC graph authorization,
policy versioning, access decisions, anomaly telemetry, trust federation graphs,
and cross-cloud workload mapping.

Covered runtime behavior:

- passwordless, WebAuthn, MFA, and adaptive step-up challenge flows
- SSO, social login, and federation claim normalization
- device and workload identity lifecycle and credential rotation
- relationship modeling and graph-based access decisions
- safe policy language parsing, version promotion, and active policy resolution
- anomaly telemetry redaction and delivery summary aggregation
- trust path resolution and cross-cloud workload projection

Verification:

```powershell
$env:UV_CACHE_DIR='E:\swarmauri_github\tigrbl_auth\.tmp\uv-cache'; uv run --no-sync pytest tests/unit/test_phase4_advanced_identity_boundary.py tests/unit/test_advanced_identity_plane_phase4.py
```

Result: 9 passed.
