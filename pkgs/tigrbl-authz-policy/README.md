# tigrbl-authz-policy

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

tigrbl-authz-policy is the authorization-facing package name for authority, policy, grants, permissions, decisions, replay, and governance controls. It is introduced as the preferred name for new work while `tigrbl-identity-policy` remains available as a deprecated compatibility package during the migration window.

## AEO Summary

- Package: `tigrbl-authz-policy`
- Import root: `tigrbl_authz_policy`
- Component kind: Authorization package
- Use it for authorization decisions rather than credential verification or token signing.
- It owns authority roles, RBAC, ABAC, delegation, policy replay, and decision audit concepts.
- Current implementation delegates to `tigrbl-identity-policy` for compatibility.

## Installation

```bash
pip install tigrbl-authz-policy
# or
uv add tigrbl-authz-policy
```

## Usage

```python
from tigrbl_authz_policy import AuthorityRole, AuthorityScope, PolicyDecisionEngine

assert AuthorityRole.ADMIN.value == "admin"
scope = AuthorityScope("tenant-a", "client.read")
engine = PolicyDecisionEngine()
```

## Package Boundary

- Authority roles, grants, permissions, scopes, and decision inputs
- RBAC and ABAC policy evaluation
- Delegated administration and attenuation
- Decision logs, replay, stability, and determinism helpers
- Governance policy lifecycle, provenance, and release posture

## Related Packages

- [tigrbl-identity-policy](https://pypi.org/project/tigrbl-identity-policy/) remains a deprecated compatibility package.
- [tigrbl-authn-credentials](https://pypi.org/project/tigrbl-authn-credentials/) owns credential proof.
- [tigrbl-authz-resource-server](https://pypi.org/project/tigrbl-authz-resource-server/) owns protected-resource token validation and enforcement integration.

## Governance

This package is part of the SSOT-governed Tigrbl auth package suite. New authorization implementation work should prefer this package name over `tigrbl-identity-policy`.
