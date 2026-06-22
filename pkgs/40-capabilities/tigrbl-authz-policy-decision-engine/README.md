# tigrbl-authz-policy-decision-engine

Standalone policy decision engine package for the Tigrbl auth package suite.

- Package: `tigrbl-authz-policy-decision-engine`
- Import root: `tigrbl_authz_policy_decision_engine`
- Owns `PolicyDecisionEngine`, which evaluates concrete RBAC, ABAC, PBAC, delegation, and administrator policy objects against policy request contracts.
- Depends on identity policy contracts, identity core primitives, and concrete policy rule dataclasses.
- `tigrbl-authz-policy` re-exports this package for compatibility, but new engine imports should target this package directly.

```python
from tigrbl_authz_policy_decision_engine import PolicyDecisionEngine

engine = PolicyDecisionEngine()
```
