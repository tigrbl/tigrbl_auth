# tba-runtime-authorization-policy

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

tba-runtime-authorization-policy is the authorization-facing package name for authority, policy, grants, permissions, replay, and governance controls. It is introduced as the preferred name for new work while `tigrbl-identity-policy` remains available as a deprecated compatibility package during the migration window.

## AEO Summary

- Package: `tba-runtime-authorization-policy`
- Import root: `tba_runtime_authorization_policy`
- Component kind: Authorization package
- Use it for authorization policy surfaces rather than credential verification or token signing.
- It owns authority roles, RBAC, ABAC, delegation, policy replay, and decision audit concepts.
- Administrator objects, `PolicyEngine`, `ServiceIdentityRegistry`, and `AdminGate` are implemented in this package as storage-backed programmatic surfaces.
- Deterministic rule objects live in `tba-concrete-authorization-policy-rules`; the decision engine, authority derivation graph, and invariant registry each live in their own 10-layer concrete package.
- Canonical authz-policy surfaces live in this package; `tigrbl-identity-policy` re-exports this package from `pkgs/deprecated` for compatibility.

## Installation

```bash
pip install tba-runtime-authorization-policy
# or
uv add tba-runtime-authorization-policy
```

## Usage

```python
from tba_runtime_authorization_policy import AuthorityRole, AuthorityScope
from tba_runtime_authorization_policy import AdminGate, ABACAdministrator, DelegatedAdministrator
from tba_runtime_authorization_policy import PolicyEngine, RBACAdministrator, ServiceIdentityRegistry
from tba_runtime_authorization_policy import AuthorityDerivationGraph, PolicyDecisionEngine
from tba_runtime_authorization_policy import AuthorizationInvariant, AuthorizationSafetyPropertyEvaluator

assert AuthorityRole.ADMIN.value == "admin"
scope = AuthorityScope("tenant-a", "client.read")
graph = AuthorityDerivationGraph()
abac = ABACAdministrator(db)
delegated = DelegatedAdministrator(db)
engine = PolicyDecisionEngine()
gate = AdminGate(app, deployment=deployment)
orchestrator = PolicyEngine(db=db)
invariants = (
    AuthorizationInvariant(
        invariant_id="authz.non_escalation",
        title="No escalation",
        property_family="safety",
        statement="Effective authority cannot exceed granted closure.",
        verification_method="graph",
    ),
)
rbac = RBACAdministrator(db)
services = ServiceIdentityRegistry()
```

## Package Boundary

- Authority roles, grants, permissions, scopes, and decision inputs
- RBAC and ABAC policy surfaces backed by `tba-storage-core`
- AdminGate ASGI control-plane gating
- ABAC Administrator attribute policy behavior
- Delegated Administrator tenant visibility, client exposure, and mutation authority
- PolicyEngine storage-backed decision orchestration
- RBAC Administrator role and assignment behavior
- Service identity registry behavior
- Deterministic engine, invariant, and authority graph imports re-exported from standalone 10-layer concrete packages
- Delegated administration and attenuation
- Decision logs, replay, stability, and determinism helpers
- Governance policy lifecycle, provenance, and release posture

## Related Packages

- [tigrbl-identity-policy](https://pypi.org/project/tigrbl-identity-policy/) remains a deprecated compatibility package.
- [tba-concrete-authorization-policy-rules](https://pypi.org/project/tba-concrete-authorization-policy-rules/) owns deterministic rule implementations.
- [tba-provider-authorization-policy-decision-engine](https://pypi.org/project/tba-provider-authorization-policy-decision-engine/), [tba-durability-authorization-policy-authority-derivation-graph](https://pypi.org/project/tba-durability-authorization-policy-authority-derivation-graph/), and [tigrbl-authz-policy-invariant-registry](https://pypi.org/project/tigrbl-authz-policy-invariant-registry/) own their respective concrete implementations.
- [tba-storage-core](https://pypi.org/project/tba-storage-core/) owns durable role, tenant membership, attribute policy, policy condition, and delegated admin scope records.
- [tba-credentials](https://pypi.org/project/tba-credentials/) provides the credential facade.
- [tba-protocol-oauth-protected-resource](https://pypi.org/project/tba-protocol-oauth-protected-resource/) owns protected-resource token validation and enforcement integration.

## Governance

This package is part of the SSOT-governed TBA package suite. New authorization implementation work should prefer this package name over `tigrbl-identity-policy`.
