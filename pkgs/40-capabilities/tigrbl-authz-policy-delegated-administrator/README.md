# tigrbl-authz-policy-delegated-administrator

Standalone Delegated Administrator package for the Tigrbl auth package suite.

- Package: `tigrbl-authz-policy-delegated-administrator`
- Import root: `tigrbl_authz_policy_delegated_administrator`
- Owns `DelegatedAdministrator`.
- Backs delegated tenant visibility, client exposure, mutation authority, and service-identity permission scopes through `tigrbl-identity-storage` tables.
- `tigrbl-authz-policy` re-exports this package for compatibility, but new delegated administrator imports should target this package directly.

```python
from tigrbl_authz_policy_delegated_administrator import DelegatedAdministrator

delegated = DelegatedAdministrator(db)
```
