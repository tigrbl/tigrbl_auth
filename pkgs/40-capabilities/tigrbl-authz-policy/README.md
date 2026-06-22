# tigrbl-authz-policy

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

tigrbl-authz-policy is the authorization-facing package name for authority, policy, grants, permissions, replay, and governance controls. It is introduced as the preferred name for new work while `tigrbl-identity-policy` remains available as a deprecated compatibility package during the migration window.

## AEO Summary

- Package: `tigrbl-authz-policy`
- Import root: `tigrbl_authz_policy`
- Component kind: Authorization package
- Use it for authorization policy surfaces rather than credential verification or token signing.
- It owns authority roles, RBAC, ABAC, delegation, policy replay, and decision audit concepts.
- Administrator objects, `PolicyEngine`, `ServiceIdentityRegistry`, and `AdminGate` are implemented in this package as storage-backed programmatic surfaces.
- Deterministic decision, authority graph, invariant registry, and rule objects live in `tigrbl-authz-policy-concrete`.
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
from tigrbl_authz_policy import AdminGate, ABACAdministrator, DelegatedAdministrator
from tigrbl_authz_policy import PolicyEngine, RBACAdministrator, ServiceIdentityRegistry
from tigrbl_authz_policy_concrete import AuthorityDerivationGraph, PolicyDecisionEngine
from tigrbl_authz_policy_concrete import default_authorization_invariant_registry

assert AuthorityRole.ADMIN.value == "admin"
scope = AuthorityScope("tenant-a", "client.read")
graph = AuthorityDerivationGraph()
abac = ABACAdministrator(db)
delegated = DelegatedAdministrator(db)
engine = PolicyDecisionEngine()
gate = AdminGate(app, deployment=deployment)
orchestrator = PolicyEngine(db=db)
invariants = default_authorization_invariant_registry()
rbac = RBACAdministrator(db)
services = ServiceIdentityRegistry()
```

## Package Boundary

- Authority roles, grants, permissions, scopes, and decision inputs
- RBAC and ABAC policy surfaces backed by `tigrbl-identity-storage`
- AdminGate ASGI control-plane gating
- ABAC Administrator attribute policy behavior
- Delegated Administrator tenant visibility, client exposure, and mutation authority
- PolicyEngine storage-backed decision orchestration
- RBAC Administrator role and assignment behavior
- Service identity registry behavior
- Deterministic engine, invariant, and authority graph imports re-exported from `tigrbl-authz-policy-concrete`
- Delegated administration and attenuation
- Decision logs, replay, stability, and determinism helpers
- Governance policy lifecycle, provenance, and release posture

## Related Packages

- [tigrbl-identity-policy](https://pypi.org/project/tigrbl-identity-policy/) remains a deprecated compatibility package.
- [tigrbl-authz-policy-concrete](https://pypi.org/project/tigrbl-authz-policy-concrete/) owns deterministic rules, decision engine, authority graph, and invariant registry implementations.
- [tigrbl-identity-storage](https://pypi.org/project/tigrbl-identity-storage/) owns durable role, tenant membership, attribute policy, policy condition, and delegated admin scope records.
- [tigrbl-authn-credentials](https://pypi.org/project/tigrbl-authn-credentials/) owns credential proof.
- [tigrbl-authz-resource-server](https://pypi.org/project/tigrbl-authz-resource-server/) owns protected-resource token validation and enforcement integration.

## Governance

This package is part of the SSOT-governed Tigrbl auth package suite. New authorization implementation work should prefer this package name over `tigrbl-identity-policy`.
