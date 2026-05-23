# Priority 1 Enterprise Readiness T1 Behavior

Boundary: `bnd:priority-1-enterprise-readiness`

The T1 behavior test composes the enterprise readiness dashboard and redacted
configuration viewer for a healthy runtime posture.

Covered runtime behavior:

- healthy readiness status
- runtime/database/issuer/key/admin/cookie section projection
- warning-free healthy dashboard
- top-level and nested secret redaction
- preservation of non-secret diagnostic values

Verification:

```powershell
$env:UV_CACHE_DIR='E:\swarmauri_github\tigrbl_auth\.tmp\uv-cache'; uv run --no-sync pytest tests/uix/test_priority1_enterprise_readiness_boundary.py tests/uix/test_readiness_dashboard.py tests/uix/test_admin_shell_security.py
```

Result: 8 passed.
