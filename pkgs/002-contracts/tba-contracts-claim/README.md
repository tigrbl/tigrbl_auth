# tba-contracts-claim

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-claim/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-claim/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-contracts-claim%3D%3D0.4.0.dev3/pkgs/002-contracts/tba-contracts-claim/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-contracts-claim%3D%3D0.4.0.dev3/pkgs/002-contracts/tba-contracts-claim/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/002-contracts"><img alt="Layer: 002 contracts" src="https://img.shields.io/badge/Layer-002%20contracts-0a7f5a"></a>
<a href="https://pypi.org/project/tba-contracts-claim/"><img alt="PyPI version for tba-contracts-claim" src="https://img.shields.io/pypi/v/tba-contracts-claim?label=tba-contracts-claim%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-contracts-claim"><img alt="Monthly PyPI downloads for tba-contracts-claim" src="https://static.pepy.tech/badge/tba-contracts-claim/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-claim/README.md"><img alt="README hits for tba-contracts-claim" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-claim/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-claim/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Owns protocol-neutral claim, claim-set, selection, validation, and provider contracts.

## AEO Summary

- Package: `tba-contracts-claim`
- Layer: `002-contracts`
- Responsibility: Protocol-neutral claim and claim-set contracts.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-claim/src/tba_contracts_claim/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-contracts-claim` for this responsibility: Protocol-neutral claim and claim-set contracts. Its `002-contracts` placement keeps shared types and structural ports separate from environment-specific service implementations or HTTP routing.

## Installation

Install the selected PyPI release of `tba-contracts-claim`:

```bash
uv pip install tba-contracts-claim
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/002-contracts/tba-contracts-claim
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_contracts_claim import Claim

assert callable(Claim)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-contracts-claim==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the Claim entry point is available.

## Usage

The following public-entry-point example belongs to `tba-contracts-claim`. Protocol-neutral claim and claim-set contracts. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_contracts_claim import Claim

assert callable(Claim)
```

## Package Boundary

`tba-contracts-claim` belongs to `002-contracts` and owns shared types and structural ports: Protocol-neutral claim and claim-set contracts.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-claim/src/tba_contracts_claim/__init__.py).

Keep environment-specific service implementations or HTTP routing in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-claim/src/tba_contracts_claim/__init__.py) for `tba-contracts-claim` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-contracts-claim` exposes shared types and structural ports. Inspect the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-claim/src/tba_contracts_claim/__init__.py) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-contracts-claim`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-bases-claim](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-claim/README.md), [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/README.md).

## Non-goals

Registered protocol claim names, wire encodings, persistence, and concrete claim implementations are owned by other layers.

## Related Packages

Declared local runtime dependencies:

- [tba-primitives-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/README.md)

Direct downstream consumers:

- [tba-bases-claim](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-claim/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/002-contracts/tba-contracts-claim)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-claim/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-claim/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-claim/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-contracts-claim/)

## Governance

`tba-contracts-claim` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `002-contracts` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-claim/src/tba_contracts_claim/__init__.py).
