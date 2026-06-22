# tigrbl-authz-policy-abac-administrator

Standalone ABAC Administrator package for the Tigrbl auth package suite.

- Package: `tigrbl-authz-policy-abac-administrator`
- Import root: `tigrbl_authz_policy_abac_administrator`
- Owns `ABACAdministrator`.
- Backs attribute policy definitions and dynamic conditions through `tigrbl-identity-storage` tables.
- `tigrbl-authz-policy` re-exports this package for compatibility, but new ABAC administrator imports should target this package directly.

```python
from tigrbl_authz_policy_abac_administrator import ABACAdministrator

abac = ABACAdministrator(db)
```
