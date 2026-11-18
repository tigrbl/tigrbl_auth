# tba-concrete-authority-graph

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authority-graph/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authority-graph/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-authority-graph%3D%3D0.4.0.dev4/pkgs/10-concrete/tba-concrete-authority-graph/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-authority-graph%3D%3D0.4.0.dev4/pkgs/10-concrete/tba-concrete-authority-graph/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/10-concrete"><img alt="Layer: 10 concrete" src="https://img.shields.io/badge/Layer-10%20concrete-0a7f5a"></a>
<a href="https://pypi.org/project/tba-concrete-authority-graph/"><img alt="PyPI version for tba-concrete-authority-graph" src="https://img.shields.io/pypi/v/tba-concrete-authority-graph?label=tba-concrete-authority-graph%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-concrete-authority-graph"><img alt="Monthly PyPI downloads for tba-concrete-authority-graph" src="https://static.pepy.tech/badge/tba-concrete-authority-graph/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authority-graph/README.md"><img alt="README hits for tba-concrete-authority-graph" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authority-graph/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authority-graph/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Deterministic, storage-neutral authority graph traversal, closure, integrity,
monotonicity, and least-authority algorithms.

This layer does not own database tables, sessions, providers, or protocols.

## AEO Summary

- Package: `tba-concrete-authority-graph`
- Layer: `10-concrete`
- Responsibility: Deterministic authority graph and closure algorithms.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authority-graph/src/tba_concrete_authority_graph/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-concrete-authority-graph` for this responsibility: Deterministic authority graph and closure algorithms. Its `10-concrete` placement keeps focused concrete types and algorithms separate from application hosting or ownership of environment-specific providers.

## Installation

Install the selected PyPI release of `tba-concrete-authority-graph`:

```bash
uv pip install tba-concrete-authority-graph
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/10-concrete/tba-concrete-authority-graph
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_concrete_authority_graph import normalize_authority_roles

assert callable(normalize_authority_roles)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-concrete-authority-graph==0.4.0.dev4" python quickstart.py
```

The import and assertion succeed when the normalize_authority_roles entry point is available.

## Usage

The following public-entry-point example belongs to `tba-concrete-authority-graph`. Deterministic authority graph and closure algorithms. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_concrete_authority_graph import normalize_authority_roles

assert callable(normalize_authority_roles)
```

## Package Boundary

`tba-concrete-authority-graph` belongs to `10-concrete` and owns focused concrete types and algorithms: Deterministic authority graph and closure algorithms.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authority-graph/src/tba_concrete_authority_graph/__init__.py). Public exports include `AuthorityClosure`, `AuthorityDerivationGraph`, `AuthorityEdge`, `AuthorityGraphIntegrityReport`, `AuthorityMonotonicityReport`, `AuthorityMutationKind`, `AuthorityNode`, `AuthorityPath`, `AuthorityReachabilityProof`, `AuthorityRole`, `AuthorityScope`, `LeastAuthorityDiff`.

Keep application hosting or ownership of environment-specific providers in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-concrete-authority-graph`:

- `has_admin_authority` construction inputs: `principal_kind`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authority-graph/src/tba_concrete_authority_graph/__init__.py).
- `AuthorityDerivationGraph` construction inputs: `nodes`, `edges`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authority-graph/src/tba_concrete_authority_graph/__init__.py).
- `authority_node_to_graph_node_payload` construction inputs: `graph_id`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authority-graph/src/tba_concrete_authority_graph/__init__.py).
- `authority_edge_to_graph_edge_payload` construction inputs: `graph_id`, `src_id`, `dst_id`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authority-graph/src/tba_concrete_authority_graph/__init__.py).
- `graph_edge_to_authority_edge` construction inputs: `source`, `target`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authority-graph/src/tba_concrete_authority_graph/__init__.py).
- `compare_authority_monotonicity` construction inputs: `mutation_kind`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authority-graph/src/tba_concrete_authority_graph/__init__.py).
- `diff_least_authority` construction inputs: `required`, `effective`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authority-graph/src/tba_concrete_authority_graph/__init__.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-concrete-authority-graph` exposes focused concrete types and algorithms. Public operations found in its source:

- `normalize_authority_roles` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authority-graph/src/tba_concrete_authority_graph/__init__.py).
- `has_admin_authority` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authority-graph/src/tba_concrete_authority_graph/__init__.py).
- `has_owner_authority` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authority-graph/src/tba_concrete_authority_graph/__init__.py).
- `has_superuser_authority` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authority-graph/src/tba_concrete_authority_graph/__init__.py).
- `AuthorityDerivationGraph.nodes` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authority-graph/src/tba_concrete_authority_graph/__init__.py).
- `AuthorityDerivationGraph.edges` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authority-graph/src/tba_concrete_authority_graph/__init__.py).
- `AuthorityDerivationGraph.add_node` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authority-graph/src/tba_concrete_authority_graph/__init__.py).
- `AuthorityDerivationGraph.add_edge` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authority-graph/src/tba_concrete_authority_graph/__init__.py).
- `AuthorityDerivationGraph.outgoing` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authority-graph/src/tba_concrete_authority_graph/__init__.py).
- `AuthorityDerivationGraph.derive_paths` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authority-graph/src/tba_concrete_authority_graph/__init__.py).
- `AuthorityDerivationGraph.effective_scopes` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authority-graph/src/tba_concrete_authority_graph/__init__.py).
- `AuthorityDerivationGraph.prove_reachability` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authority-graph/src/tba_concrete_authority_graph/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-concrete-authority-graph`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tba-auth/README.md), [tba-capability-policy-assurance](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-policy-assurance/README.md), [tba-durability-authorization-policy-authority-derivation-graph](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-durability-authorization-policy-authority-derivation-graph/README.md), [tba-runtime-authorization-policy](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-authorization-policy/README.md).

## Non-goals

`tba-concrete-authority-graph` does not take ownership of application hosting or ownership of environment-specific providers.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md)

Direct downstream consumers:

- [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tba-auth/README.md)
- [tba-capability-policy-assurance](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-policy-assurance/README.md)
- [tba-durability-authorization-policy-authority-derivation-graph](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-durability-authorization-policy-authority-derivation-graph/README.md)
- [tba-runtime-authorization-policy](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-authorization-policy/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/10-concrete/tba-concrete-authority-graph)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authority-graph/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authority-graph/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authority-graph/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-concrete-authority-graph/)

## Governance

`tba-concrete-authority-graph` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `10-concrete` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authority-graph/src/tba_concrete_authority_graph/__init__.py).
