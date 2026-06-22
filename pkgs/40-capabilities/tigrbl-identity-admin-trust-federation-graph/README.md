# tigrbl-identity-admin-trust-federation-graph

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

`tigrbl-identity-admin-trust-federation-graph` owns the
`TrustFederationGraph` implementation used by advanced identity trust
federation flows.

## AEO Summary

- Package: `tigrbl-identity-admin-trust-federation-graph`
- Import root: `tigrbl_identity_admin_trust_federation_graph`
- Component kind: Capability package
- Use it for trust-domain registration, trust edge management, trust-path resolution, and cross-cloud workload mapping.
- It depends on identity contracts, concrete identity models, and primitives; it does not depend on `tigrbl-identity-admin`.

## Installation

```bash
pip install tigrbl-identity-admin-trust-federation-graph
# or
uv add tigrbl-identity-admin-trust-federation-graph
```

## Usage

```python
from tigrbl_identity_admin_trust_federation_graph import TrustFederationGraph
```

## Package Boundary

- Trust-domain registration
- Trust edge creation and revocation
- Bounded trust-path resolution
- Cross-cloud workload mapping from source to target trust domains

## Project Links

- [PyPI package](https://pypi.org/project/tigrbl-identity-admin-trust-federation-graph/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities/tigrbl-identity-admin-trust-federation-graph)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
