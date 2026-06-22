# tigrbl-authz-policy

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

tigrbl-authz-policy is the authorization-facing package name for authority, policy, grants, permissions, replay, and governance controls. It is introduced as the preferred name for new work while `tigrbl-identity-policy` remains available as a deprecated compatibility package during the migration window.

## AEO Summary

- Package: `tigrbl-authz-policy`
- Import root: `tigrbl_authz_policy`
- Component kind: Authorization package
- Use it for authorization policy surfaces rather than credential verification or token signing.
- It owns authority roles, RBAC, ABAC, delegation, policy replay, and decision audit concepts.
- `ABACAdministrator` is implemented by `tigrbl-authz-policy-abac-administrator`; this package re-exports it for compatibility.
- `DelegatedAdministrator` is implemented by `tigrbl-authz-policy-delegated-administrator`; this package re-exports it for compatibility.
- `PolicyDecisionEngine` is implemented by `tigrbl-authz-policy-decision-engine`; this package re-exports it for compatibility.
- `PolicyEngine` is implemented by `tigrbl-authz-policy-engine`; this package re-exports it for compatibility.
- `InvariantRegistry` is implemented by `tigrbl-authz-policy-invariant-registry`; this package re-exports it for compatibility.
- `RBACAdministrator` is implemented by `tigrbl-authz-policy-rbac-administrator`; this package re-exports it for compatibility.
- `ServiceIdentityRegistry` is implemented by `tigrbl-authz-policy-service-identity-registry`; this package re-exports it for compatibility.
- Canonical authz-policy surfaces live in this package; `tigrbl-identity-policy` re-exports this package from `pkgs/deprecated` for compatibility.

## Installation

```bash
pip install tigrbl-authz-policy
# or
uv add tigrbl-authz-policy
```

## Usage

```python
from tigrbl_authz_policy import AuthorityRole, AuthorityScope
from tigrbl_authz_policy_abac_administrator import ABACAdministrator
from tigrbl_authz_policy_delegated_administrator import DelegatedAdministrator
from tigrbl_authz_policy_decision_engine import PolicyDecisionEngine
from tigrbl_authz_policy_engine import PolicyEngine
from tigrbl_authz_policy_invariant_registry import default_authorization_invariant_registry
from tigrbl_authz_policy_rbac_administrator import RBACAdministrator
from tigrbl_authz_policy_service_identity_registry import ServiceIdentityRegistry

assert AuthorityRole.ADMIN.value == "admin"
scope = AuthorityScope("tenant-a", "client.read")
abac = ABACAdministrator(db)
delegated = DelegatedAdministrator(db)
engine = PolicyDecisionEngine()
orchestrator = PolicyEngine(db=db)
invariants = default_authorization_invariant_registry()
rbac = RBACAdministrator(db)
services = ServiceIdentityRegistry()
```

## Package Boundary

- Authority roles, grants, permissions, scopes, and decision inputs
- RBAC and ABAC policy surfaces; concrete engine evaluation lives in `tigrbl-authz-policy-decision-engine`
- ABAC Administrator attribute policy behavior lives in `tigrbl-authz-policy-abac-administrator`
- Delegated Administrator tenant visibility, client exposure, and mutation authority lives in `tigrbl-authz-policy-delegated-administrator`
- PolicyEngine storage-backed decision orchestration lives in `tigrbl-authz-policy-engine`
- RBAC Administrator role and assignment behavior lives in `tigrbl-authz-policy-rbac-administrator`
- Invariant registry behavior lives in `tigrbl-authz-policy-invariant-registry`
- Service identity registry behavior lives in `tigrbl-authz-policy-service-identity-registry`
- Delegated administration and attenuation
- Decision logs, replay, stability, and determinism helpers
- Governance policy lifecycle, provenance, and release posture

## Related Packages

- [tigrbl-identity-policy](https://pypi.org/project/tigrbl-identity-policy/) remains a deprecated compatibility package.
- [tigrbl-authz-policy-abac-administrator](https://pypi.org/project/tigrbl-authz-policy-abac-administrator/) owns `ABACAdministrator`.
- [tigrbl-authz-policy-delegated-administrator](https://pypi.org/project/tigrbl-authz-policy-delegated-administrator/) owns `DelegatedAdministrator`.
- [tigrbl-authz-policy-decision-engine](https://pypi.org/project/tigrbl-authz-policy-decision-engine/) owns `PolicyDecisionEngine`.
- [tigrbl-authz-policy-engine](https://pypi.org/project/tigrbl-authz-policy-engine/) owns `PolicyEngine`.
- [tigrbl-authz-policy-invariant-registry](https://pypi.org/project/tigrbl-authz-policy-invariant-registry/) owns `InvariantRegistry`.
- [tigrbl-authz-policy-rbac-administrator](https://pypi.org/project/tigrbl-authz-policy-rbac-administrator/) owns `RBACAdministrator`.
- [tigrbl-authz-policy-service-identity-registry](https://pypi.org/project/tigrbl-authz-policy-service-identity-registry/) owns `ServiceIdentityRegistry`.
- [tigrbl-authn-credentials](https://pypi.org/project/tigrbl-authn-credentials/) owns credential proof.
- [tigrbl-authz-resource-server](https://pypi.org/project/tigrbl-authz-resource-server/) owns protected-resource token validation and enforcement integration.

## Governance

This package is part of the SSOT-governed Tigrbl auth package suite. New authorization implementation work should prefer this package name over `tigrbl-identity-policy`.
