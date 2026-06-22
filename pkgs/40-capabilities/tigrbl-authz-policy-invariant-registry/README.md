# tigrbl-authz-policy-invariant-registry

Standalone authorization invariant registry package for the Tigrbl auth package suite.

- Package: `tigrbl-authz-policy-invariant-registry`
- Import root: `tigrbl_authz_policy_invariant_registry`
- Owns `InvariantRegistry` and `default_authorization_invariant_registry`.
- Re-exports invariant contract DTOs from `tigrbl_identity_contracts.invariants` for registry callers.
- `tigrbl-authz-policy` re-exports this package for compatibility, but new registry imports should target this package directly.

```python
from tigrbl_authz_policy_invariant_registry import default_authorization_invariant_registry

registry = default_authorization_invariant_registry()
```
