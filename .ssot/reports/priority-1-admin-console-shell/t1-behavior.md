# Priority 1 Admin Console Shell T1 Behavior

Boundary: `bnd:priority-1-admin-console-shell`

The T1 behavior test composes the administrator shell, authenticated admin
session, tenant/profile selection, active surface sets, diagnostic redaction, and
admin context golden-path events.

Covered runtime behavior:

- authenticated admin shell rendering
- admin navigation and environment banner exposure
- tenant and deployment profile selection
- active surface set projection
- diagnostic redaction for sensitive values
- golden-path session/context/audit event ordering

Verification:

```powershell
$env:UV_CACHE_DIR='E:\swarmauri_github\tigrbl_auth\.tmp\uv-cache'; uv run --no-sync pytest tests/uix/test_priority1_admin_console_shell_boundary.py tests/uix/test_admin_shell.py tests/uix/test_admin_shell_security.py
```

Result: 8 passed.
