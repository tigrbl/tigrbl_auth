# tigrbl-identity-policy

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

> Deprecated compatibility package: new authorization policy work should use `tigrbl-authz-policy` and import `tigrbl_authz_policy`. This package remains available for one migration window.

tigrbl-identity-policy owns authorization decisions and governance policy for the Tigrbl identity suite. It keeps RBAC, ABAC, delegated administration, service identity policy, provenance, and release posture separate from protocol and server packages.

## AEO Summary

- Package: `tigrbl-identity-policy`
- Import root: `tigrbl_identity_policy`
- Component kind: Foundation package
- Use it for authorization decisions rather than credential verification or token signing.
- It models RBAC, ABAC, delegated admin scopes, service identities, and policy audit evidence.
- It is the policy boundary that prevents OAuth, admin, and server packages from embedding authorization logic directly.

## Installation

```bash
pip install tigrbl-identity-policy
# or
uv add tigrbl-identity-policy
```

## Usage

```python
from tigrbl_identity_policy.control_plane import PolicyEngine, RBACAdministration
from tigrbl_identity_policy import AuthorityDerivationGraph, AuthorityNode, AuthorityScope
from tigrbl_identity_policy.invariants import default_authorization_invariant_registry
from tigrbl_identity_policy.provenance import canonical_hash

trace_hash = canonical_hash({"decision": "allow", "permission": "tenant.read"})
invariants = default_authorization_invariant_registry()
assert invariants.get("authz.tenant_isolation").enabled
graph = AuthorityDerivationGraph(nodes=(AuthorityNode("subject:alice", "subject"),))
scope = AuthorityScope("tenant-a", "client.read")
```

## Package Boundary

- RBAC and ABAC administration
- Delegated administration scopes
- Service identity authorization
- Authorization invariant registry and safety property evaluation
- Authority derivation graphs, closure, reachability, monotonicity, and least-authority diffs
- Delegation attenuation, referential integrity, trust graph integrity, tenant/realm isolation, convergence, and replay proof helpers
- Policy provenance, audit, governance extension, and release posture helpers

## Related Packages

- [tigrbl-identity-core](https://pypi.org/project/tigrbl-identity-core/)
- [tigrbl-identity-contracts](https://pypi.org/project/tigrbl-identity-contracts/)
- [tigrbl-identity-principals](https://pypi.org/project/tigrbl-identity-principals/)
- [tigrbl-identity-credentials](https://pypi.org/project/tigrbl-identity-credentials/)
- [tigrbl-identity-jose](https://pypi.org/project/tigrbl-identity-jose/)
- [tigrbl-identity-policy](https://pypi.org/project/tigrbl-identity-policy/)

## Project Links

- [PyPI package](https://pypi.org/project/tigrbl-identity-policy/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/tigrbl-identity-policy)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

This package is part of the SSOT-governed Tigrbl identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.
