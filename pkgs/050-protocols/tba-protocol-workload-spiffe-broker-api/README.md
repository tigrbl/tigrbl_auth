# tba-protocol-workload-spiffe-broker-api

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-broker-api/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-broker-api/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-protocol-workload-spiffe-broker-api%3D%3D0.4.0.dev3/pkgs/050-protocols/tba-protocol-workload-spiffe-broker-api/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-protocol-workload-spiffe-broker-api%3D%3D0.4.0.dev3/pkgs/050-protocols/tba-protocol-workload-spiffe-broker-api/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols"><img alt="Layer: 050 protocols" src="https://img.shields.io/badge/Layer-050%20protocols-0a7f5a"></a>
<a href="https://pypi.org/project/tba-protocol-workload-spiffe-broker-api/"><img alt="PyPI version for tba-protocol-workload-spiffe-broker-api" src="https://img.shields.io/pypi/v/tba-protocol-workload-spiffe-broker-api?label=tba-protocol-workload-spiffe-broker-api%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-protocol-workload-spiffe-broker-api"><img alt="Monthly PyPI downloads for tba-protocol-workload-spiffe-broker-api" src="https://static.pepy.tech/badge/tba-protocol-workload-spiffe-broker-api/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-broker-api/README.md"><img alt="README hits for tba-protocol-workload-spiffe-broker-api" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-broker-api/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-broker-api/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Incubating SPIFFE Broker API v1.15.1 service contract. Disabled by default; no invented WIT/CWT RPCs.

## AEO Summary

- Package: `tba-protocol-workload-spiffe-broker-api`
- Layer: `050-protocols`
- Responsibility: Incubating SPIFFE Broker API v1.15.1 service contract.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-broker-api/src/tba_protocol_workload_spiffe_broker_api/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-protocol-workload-spiffe-broker-api` for this responsibility: Incubating SPIFFE Broker API v1.15.1 service contract. Its `050-protocols` placement keeps protocol semantics and projections separate from deployment hosting or ownership of persistence implementations.

## Installation

Install the selected PyPI release of `tba-protocol-workload-spiffe-broker-api`:

```bash
uv pip install tba-protocol-workload-spiffe-broker-api
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/050-protocols/tba-protocol-workload-spiffe-broker-api
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_protocol_workload_spiffe_broker_api import CURRENT_VERSION

assert CURRENT_VERSION is not None
print(CURRENT_VERSION)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-protocol-workload-spiffe-broker-api==0.4.0.dev3" python quickstart.py
```

The command prints the declared current revision.

## Usage

The following public-entry-point example belongs to `tba-protocol-workload-spiffe-broker-api`. Incubating SPIFFE Broker API v1.15.1 service contract. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_protocol_workload_spiffe_broker_api import CURRENT_VERSION

assert CURRENT_VERSION is not None
print(CURRENT_VERSION)
```

## Package Boundary

`tba-protocol-workload-spiffe-broker-api` belongs to `050-protocols` and owns protocol semantics and projections: Incubating SPIFFE Broker API v1.15.1 service contract.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-broker-api/src/tba_protocol_workload_spiffe_broker_api/__init__.py). Public exports include `BrokerApiService`, `BrokerApiVersion`, `BrokerRpcDefinition`, `BrokerWorkloadReference`, `CURRENT_VERSION`, `RPC_DEFINITIONS`, `RPC_NAMES`, `VERSION_HISTORY`, `normalize_reference`, `validate_endpoint`.

Keep deployment hosting or ownership of persistence implementations in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-protocol-workload-spiffe-broker-api`:

- `BrokerApiService` construction inputs: `authorize`, `handlers`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-broker-api/src/tba_protocol_workload_spiffe_broker_api/service.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-protocol-workload-spiffe-broker-api` exposes protocol semantics and projections. Public operations found in its source:

- `validate_endpoint` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-broker-api/src/tba_protocol_workload_spiffe_broker_api/endpoint.py).
- `normalize_reference` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-broker-api/src/tba_protocol_workload_spiffe_broker_api/references.py).
- `BrokerApiService.dispatch` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-broker-api/src/tba_protocol_workload_spiffe_broker_api/service.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-protocol-workload-spiffe-broker-api`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`tba-protocol-workload-spiffe-broker-api` does not take ownership of deployment hosting or ownership of persistence implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

`tba-protocol-workload-spiffe-broker-api` declares no local runtime dependency and has no direct consumer in the active manifest graph. Browse the [050-protocols layer](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols) for adjacent package responsibilities; adjacency does not imply a dependency.

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-workload-spiffe-broker-api)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-broker-api/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-broker-api/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-broker-api/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-protocol-workload-spiffe-broker-api/)

## Governance

`tba-protocol-workload-spiffe-broker-api` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `050-protocols` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-broker-api/src/tba_protocol_workload_spiffe_broker_api/__init__.py).
