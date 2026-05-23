# Priority 1 Enterprise Readiness T2 Gate

Boundary: `bnd:priority-1-enterprise-readiness`

The T2 gate verifies readiness and redaction fail-closed behavior:

- degraded posture emits readiness and cookie warnings
- admin authorization, contract, and migration failures block the dashboard
- blocked sections are projected explicitly
- JWT secrets, API tokens, private keys, passwords, and client secrets are
  redacted
- explicit non-secret keys remain visible

Verification:

```powershell
$env:UV_CACHE_DIR='E:\swarmauri_github\tigrbl_auth\.tmp\uv-cache'; uv run --no-sync pytest tests/uix/test_priority1_enterprise_readiness_boundary.py tests/uix/test_readiness_dashboard.py tests/uix/test_admin_shell_security.py
```

Result: 8 passed.
