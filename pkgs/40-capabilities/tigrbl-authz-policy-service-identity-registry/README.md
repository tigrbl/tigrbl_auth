# tigrbl-authz-policy-service-identity-registry

Standalone service identity registry package for the Tigrbl auth package suite.

- Package: `tigrbl-authz-policy-service-identity-registry`
- Import root: `tigrbl_authz_policy_service_identity_registry`
- Owns `ServiceIdentityRegistry`.
- Re-exports service identity contract/concrete DTOs for registry callers.
- `tigrbl-authz-policy` re-exports this package for compatibility, but new registry imports should target this package directly.

```python
from tigrbl_authz_policy_service_identity_registry import ServiceIdentityRegistry

registry = ServiceIdentityRegistry()
```
