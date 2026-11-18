# tba-concrete-acr-evaluator-basic

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-acr-evaluator-basic/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-acr-evaluator-basic/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-acr-evaluator-basic%3D%3D0.4.0.dev4/pkgs/10-concrete/tba-concrete-acr-evaluator-basic/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-acr-evaluator-basic%3D%3D0.4.0.dev4/pkgs/10-concrete/tba-concrete-acr-evaluator-basic/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/10-concrete"><img alt="Layer: 10 concrete" src="https://img.shields.io/badge/Layer-10%20concrete-0a7f5a"></a>
<a href="https://pypi.org/project/tba-concrete-acr-evaluator-basic/"><img alt="PyPI version for tba-concrete-acr-evaluator-basic" src="https://img.shields.io/pypi/v/tba-concrete-acr-evaluator-basic?label=tba-concrete-acr-evaluator-basic%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-concrete-acr-evaluator-basic"><img alt="Monthly PyPI downloads for tba-concrete-acr-evaluator-basic" src="https://static.pepy.tech/badge/tba-concrete-acr-evaluator-basic/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-acr-evaluator-basic/README.md"><img alt="README hits for tba-concrete-acr-evaluator-basic" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-acr-evaluator-basic/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-acr-evaluator-basic/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Deterministic basic authentication-context-class evaluation.

## AEO Summary

- Package: `tba-concrete-acr-evaluator-basic`
- Layer: `10-concrete`
- Responsibility: Deterministic basic ACR evaluator.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-acr-evaluator-basic/src/tba_concrete_acr_evaluator_basic/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-concrete-acr-evaluator-basic` for this responsibility: Deterministic basic ACR evaluator. Its `10-concrete` placement keeps focused concrete types and algorithms separate from application hosting or ownership of environment-specific providers.

## Installation

Install the selected PyPI release of `tba-concrete-acr-evaluator-basic`:

```bash
uv pip install tba-concrete-acr-evaluator-basic
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/10-concrete/tba-concrete-acr-evaluator-basic
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_concrete_acr_evaluator_basic import BasicAcrEvaluator

assert callable(BasicAcrEvaluator)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-concrete-acr-evaluator-basic==0.4.0.dev4" python quickstart.py
```

The import and assertion succeed when the BasicAcrEvaluator entry point is available.

## Usage

The following public-entry-point example belongs to `tba-concrete-acr-evaluator-basic`. Deterministic basic ACR evaluator. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_concrete_acr_evaluator_basic import BasicAcrEvaluator

assert callable(BasicAcrEvaluator)
```

## Package Boundary

`tba-concrete-acr-evaluator-basic` belongs to `10-concrete` and owns focused concrete types and algorithms: Deterministic basic ACR evaluator.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-acr-evaluator-basic/src/tba_concrete_acr_evaluator_basic/__init__.py). Public exports include `BasicAcrEvaluator`.

Keep application hosting or ownership of environment-specific providers in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-acr-evaluator-basic/src/tba_concrete_acr_evaluator_basic/__init__.py) for `tba-concrete-acr-evaluator-basic` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-concrete-acr-evaluator-basic` exposes focused concrete types and algorithms. Public operations found in its source:

- `BasicAcrEvaluator.supports` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-acr-evaluator-basic/src/tba_concrete_acr_evaluator_basic/__init__.py).
- `BasicAcrEvaluator.evaluate_acr` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-acr-evaluator-basic/src/tba_concrete_acr_evaluator_basic/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-concrete-acr-evaluator-basic`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-provider-authentication-context-acr-basic](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authentication-context-acr-basic/README.md).

## Non-goals

`tba-concrete-acr-evaluator-basic` does not take ownership of application hosting or ownership of environment-specific providers.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-bases-authentication-context](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authentication-context/README.md)
- [tba-contracts-security-trust](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-security-trust/README.md)

Direct downstream consumers:

- [tba-provider-authentication-context-acr-basic](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authentication-context-acr-basic/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/10-concrete/tba-concrete-acr-evaluator-basic)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-acr-evaluator-basic/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-acr-evaluator-basic/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-acr-evaluator-basic/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-concrete-acr-evaluator-basic/)

## Governance

`tba-concrete-acr-evaluator-basic` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `10-concrete` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-acr-evaluator-basic/src/tba_concrete_acr_evaluator_basic/__init__.py).
