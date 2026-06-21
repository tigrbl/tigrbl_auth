# tigrbl-authz-policy-concrete

Concrete authorization policy rule dataclass variants for the Tigrbl auth package suite.

- `tigrbl_identity_contracts.policy.rules.PolicyRule` owns the dependency-light contract shape.
- This package owns concrete rule variants such as `RolePolicy`, `AttributePolicy`, `PermissionPolicy`, `DelegationPolicy`, and `AdminPolicy`.
- Capability packages evaluate and re-export these variants; contract packages must not import capability packages.
