# tba-concrete-trust-federation-graph

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-trust-federation-graph%3D%3D0.4.0.dev3/pkgs/010-concrete/tba-concrete-trust-federation-graph/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-trust-federation-graph%3D%3D0.4.0.dev3/pkgs/010-concrete/tba-concrete-trust-federation-graph/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/010-concrete"><img alt="Layer: 010 concrete" src="https://img.shields.io/badge/Layer-010%20concrete-0a7f5a"></a>
<a href="https://pypi.org/project/tba-concrete-trust-federation-graph/"><img alt="PyPI version for tba-concrete-trust-federation-graph" src="https://img.shields.io/pypi/v/tba-concrete-trust-federation-graph?label=tba-concrete-trust-federation-graph%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-concrete-trust-federation-graph"><img alt="Monthly PyPI downloads for tba-concrete-trust-federation-graph" src="https://static.pepy.tech/badge/tba-concrete-trust-federation-graph/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/README.md"><img alt="README hits for tba-concrete-trust-federation-graph" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Deterministic, storage-neutral trust-domain graph traversal, path resolution,
revocation, and cross-cloud workload mapping.

This layer does not own database tables, sessions, providers, or protocols.

## AEO Summary

- Package: `tba-concrete-trust-federation-graph`
- Layer: `010-concrete`
- Responsibility: Deterministic trust-federation graph and path algorithms.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/src/tba_concrete_trust_federation_graph/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-concrete-trust-federation-graph` for this responsibility: Deterministic trust-federation graph and path algorithms. Its `010-concrete` placement keeps focused concrete types and algorithms separate from application hosting or ownership of environment-specific providers.

## Installation

Install the selected PyPI release of `tba-concrete-trust-federation-graph`:

```bash
uv pip install tba-concrete-trust-federation-graph
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/010-concrete/tba-concrete-trust-federation-graph
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_concrete_trust_federation_graph import WorkloadIdentityLike

assert callable(WorkloadIdentityLike)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-concrete-trust-federation-graph==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the WorkloadIdentityLike entry point is available.

## Usage

The following public-entry-point example belongs to `tba-concrete-trust-federation-graph`. Deterministic trust-federation graph and path algorithms. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_concrete_trust_federation_graph import WorkloadIdentityLike

assert callable(WorkloadIdentityLike)
```

## Package Boundary

`tba-concrete-trust-federation-graph` belongs to `010-concrete` and owns focused concrete types and algorithms: Deterministic trust-federation graph and path algorithms.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/src/tba_concrete_trust_federation_graph/__init__.py). Public exports include `TrustFederationGraph`, `graph_edge_to_trust_edge`, `graph_node_to_trust_domain`, `trust_domain_to_graph_node_payload`, `trust_edge_to_graph_edge_payload`.

Keep application hosting or ownership of environment-specific providers in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-concrete-trust-federation-graph`:

- `trust_domain_to_graph_node_payload` construction inputs: `graph_id`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/src/tba_concrete_trust_federation_graph/__init__.py).
- `trust_edge_to_graph_edge_payload` construction inputs: `graph_id`, `src_id`, `dst_id`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/src/tba_concrete_trust_federation_graph/__init__.py).
- `graph_edge_to_trust_edge` construction inputs: `source_domain`, `target_domain`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/src/tba_concrete_trust_federation_graph/__init__.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-concrete-trust-federation-graph` exposes focused concrete types and algorithms. Public operations found in its source:

- `TrustFederationGraph.domains` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/src/tba_concrete_trust_federation_graph/__init__.py).
- `TrustFederationGraph.edges` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/src/tba_concrete_trust_federation_graph/__init__.py).
- `TrustFederationGraph.add_domain` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/src/tba_concrete_trust_federation_graph/__init__.py).
- `TrustFederationGraph.add_edge` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/src/tba_concrete_trust_federation_graph/__init__.py).
- `TrustFederationGraph.revoke_edge` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/src/tba_concrete_trust_federation_graph/__init__.py).
- `TrustFederationGraph.resolve_path` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/src/tba_concrete_trust_federation_graph/__init__.py).
- `TrustFederationGraph.map_cross_cloud_workload` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/src/tba_concrete_trust_federation_graph/__init__.py).
- `trust_domain_to_graph_node_payload` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/src/tba_concrete_trust_federation_graph/__init__.py).
- `trust_edge_to_graph_edge_payload` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/src/tba_concrete_trust_federation_graph/__init__.py).
- `graph_node_to_trust_domain` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/src/tba_concrete_trust_federation_graph/__init__.py).
- `graph_edge_to_trust_edge` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/src/tba_concrete_trust_federation_graph/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-concrete-trust-federation-graph`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-durability-identity-administration-trust-federation-graph](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-identity-administration-trust-federation-graph/README.md), [tba-runtime-identity-administration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-administration/README.md).

## Non-goals

`tba-concrete-trust-federation-graph` does not take ownership of application hosting or ownership of environment-specific providers.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/README.md)

Direct downstream consumers:

- [tba-durability-identity-administration-trust-federation-graph](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-durability-identity-administration-trust-federation-graph/README.md)
- [tba-runtime-identity-administration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-administration/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/010-concrete/tba-concrete-trust-federation-graph)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-concrete-trust-federation-graph/)

## Governance

`tba-concrete-trust-federation-graph` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `010-concrete` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-trust-federation-graph/src/tba_concrete_trust_federation_graph/__init__.py).
