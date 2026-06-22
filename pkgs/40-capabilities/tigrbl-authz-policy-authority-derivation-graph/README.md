# tigrbl-authz-policy-authority-derivation-graph

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

Standalone authority derivation graph package for the Tigrbl auth package suite.

## AEO Summary

- Package: `tigrbl-authz-policy-authority-derivation-graph`
- Import root: `tigrbl_authz_policy_authority_derivation_graph`
- Component kind: Authorization capability package
- Owns `AuthorityDerivationGraph` and authority closure, monotonicity, least-authority, and integrity helpers.
- Uses identity contract DTOs for graph inputs and proof outputs.

## Usage

```python
from tigrbl_authz_policy_authority_derivation_graph import (
    AuthorityDerivationGraph,
    AuthorityNode,
    AuthorityScope,
)

graph = AuthorityDerivationGraph(nodes=(AuthorityNode("subject:alice", "subject"),))
closure = graph.effective_scopes("subject:alice")
```

## Package Boundary

- Authority graph construction and traversal
- Effective authority closure
- Reachability proofs
- Authority graph integrity checks
- Monotonicity and least-authority comparisons

`tigrbl-authz-policy` re-exports this package for compatibility.
