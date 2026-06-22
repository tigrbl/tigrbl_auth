# tigrbl-authz-policy-engine

Standalone storage-backed policy orchestration engine package for the Tigrbl auth package suite.

- Package: `tigrbl-authz-policy-engine`
- Import root: `tigrbl_authz_policy_engine`
- Owns `PolicyEngine`.
- Orchestrates RBAC, ABAC, delegated administrator, and service identity decisions through their storage-backed package surfaces.
- `tigrbl-authz-policy` re-exports this package for compatibility, but new policy orchestration imports should target this package directly.

```python
from tigrbl_authz_policy_engine import PolicyEngine

engine = PolicyEngine(db=db)
```
