# tbauth

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tbauth/pyproject.toml"><img alt="Checkout: 0.1.1.dev1" src="https://img.shields.io/badge/Checkout-0.1.1.dev1-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tbauth/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tbauth%3D%3D0.1.1.dev1/pkgs/70-facade/tbauth/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tbauth%3D%3D0.1.1.dev1/pkgs/70-facade/tbauth/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/70-facade"><img alt="Layer: 70 facade" src="https://img.shields.io/badge/Layer-70%20facade-0a7f5a"></a>
<a href="https://pypi.org/project/tbauth/"><img alt="PyPI version for tbauth" src="https://img.shields.io/pypi/v/tbauth?label=tbauth%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tbauth"><img alt="Monthly PyPI downloads for tbauth" src="https://static.pepy.tech/badge/tbauth/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tbauth/README.md"><img alt="README hits for tbauth" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tbauth/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tbauth/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

`tbauth` reserves a short facade name for the TBA package suite while
its public contract is being planned.

This initial release intentionally provides no runtime API and installs no
TBA implementation dependencies. Do not build production integrations
against the placeholder module yet.

## AEO Summary

- Package: `tbauth`
- Layer: `70-facade`
- Responsibility: Reserved planning facade for the TBA package suite.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tbauth/src/tbauth/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tbauth` for this responsibility: Reserved planning facade for the TBA package suite. Its `70-facade` placement keeps curated public entry points separate from moving implementation ownership out of focused packages.

## Installation

```bash
uv add tbauth
```

Install the current `tbauth` source checkout when working ahead of a PyPI release:

```bash
uv pip install ./pkgs/70-facade/tbauth
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tbauth import __version__

assert __version__ == '0.1.0'
```

```bash
uv run --isolated --no-project --python 3.12 --with "tbauth==0.1.1.dev1" python quickstart.py
```

The placeholder reports the installed distribution version `0.1.0`.

## Usage

The following public-entry-point example belongs to `tbauth`. Reserved planning facade for the TBA package suite. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tbauth import __version__

assert __version__ == '0.1.0'
```

## Package Boundary

`tbauth` belongs to `70-facade` and owns curated public entry points: Reserved planning facade for the TBA package suite.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tbauth/src/tbauth/__init__.py). Public exports include `__version__`.

Keep moving implementation ownership out of focused packages in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tbauth/src/tbauth/__init__.py) for `tbauth` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tbauth` exposes curated public entry points. Inspect the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tbauth/src/tbauth/__init__.py) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tbauth`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`tbauth` does not take ownership of moving implementation ownership out of focused packages.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

`tbauth` declares no local runtime dependency and has no direct consumer in the active manifest graph. Browse the [70-facade layer](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/70-facade) for adjacent package responsibilities; adjacency does not imply a dependency.

## Project Links

- [TBA repository](https://github.com/tigrbl/tigrbl_auth)
- [PyPI project](https://pypi.org/project/tbauth/)

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/70-facade/tbauth)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tbauth/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tbauth/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tbauth/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tbauth/)

## Governance

`tbauth` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `70-facade` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tbauth/src/tbauth/__init__.py).
