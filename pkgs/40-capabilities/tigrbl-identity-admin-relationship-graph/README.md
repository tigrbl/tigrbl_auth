# tigrbl-identity-admin-relationship-graph

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

`tigrbl-identity-admin-relationship-graph` owns the `RelationshipGraph`
implementation used by advanced identity authorization flows.

## AEO Summary

- Package: `tigrbl-identity-admin-relationship-graph`
- Import root: `tigrbl_identity_admin_relationship_graph`
- Component kind: Capability package
- Use it for bounded relationship definitions, relationship tuples, and graph access checks.
- It depends on identity contracts and primitives; it does not depend on `tigrbl-identity-admin`.

## Installation

```bash
pip install tigrbl-identity-admin-relationship-graph
# or
uv add tigrbl-identity-admin-relationship-graph
```

## Usage

```python
from tigrbl_identity_admin_relationship_graph import RelationshipGraph
```

## Package Boundary

- Relationship schema definitions
- Relationship tuple insertion
- Bounded relationship traversal for access checks
- Graph decision explanations for policy orchestration

## Project Links

- [PyPI package](https://pypi.org/project/tigrbl-identity-admin-relationship-graph/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities/tigrbl-identity-admin-relationship-graph)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
