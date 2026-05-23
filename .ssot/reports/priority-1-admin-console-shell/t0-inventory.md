# Priority 1 Admin Console Shell T0 Inventory

Boundary: `bnd:priority-1-admin-console-shell`

Runtime inventory is implemented by:

- `tigrbl_auth.uix.priority1_admin_console_shell_boundary_manifest`
- `tigrbl_auth.uix.priority1_admin_console_shell_boundary_integrity`
- `tigrbl_identity_operator.uix.priority1_admin_console_shell_boundary_manifest`
- `tigrbl_identity_operator.uix.priority1_admin_console_shell_boundary_integrity`

The manifest enumerates all 3 frozen boundary feature rows and maps each row to
runtime objects, category, and guarded capability.

Verification:

```powershell
$env:UV_CACHE_DIR='E:\swarmauri_github\tigrbl_auth\.tmp\uv-cache'; uv run --no-sync pytest tests/uix/test_priority1_admin_console_shell_boundary.py tests/uix/test_admin_shell.py tests/uix/test_admin_shell_security.py
```

Result: 8 passed.
