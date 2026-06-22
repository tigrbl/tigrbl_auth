# tigrbl-authz-policy-rbac-administrator

Standalone RBAC Administrator package for the Tigrbl auth package suite.

- Package: `tigrbl-authz-policy-rbac-administrator`
- Import root: `tigrbl_authz_policy_rbac_administrator`
- Owns `RBACAdministrator`.
- Backs role definitions and tenant role assignments through `tigrbl-identity-storage` tables.
- `tigrbl-authz-policy` re-exports this package for compatibility, but new RBAC administrator imports should target this package directly.

```python
from tigrbl_authz_policy_rbac_administrator import RBACAdministrator

rbac = RBACAdministrator(db)
```
