# Priority 1 Admin Console Shell T2 Gate

Boundary: `bnd:priority-1-admin-console-shell`

The T2 gate verifies fail-closed behavior for the priority 1 admin shell:

- unauthenticated sessions cannot render the admin shell
- authenticated non-admin users cannot render the admin shell
- admin scope authorization is accepted independently from role authorization
- unsafe readiness emits warnings without disclosing secrets
- nested database passwords and JWT secrets are redacted

Verification:

```powershell
$env:UV_CACHE_DIR='E:\swarmauri_github\tigrbl_auth\.tmp\uv-cache'; uv run --no-sync pytest tests/uix/test_priority1_admin_console_shell_boundary.py tests/uix/test_admin_shell.py tests/uix/test_admin_shell_security.py
```

Result: 8 passed.
