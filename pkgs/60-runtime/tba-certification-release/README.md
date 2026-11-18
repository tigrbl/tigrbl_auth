# tba-certification-release

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-certification-release/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-certification-release/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-certification-release%3D%3D0.4.0.dev4/pkgs/60-runtime/tba-certification-release/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-certification-release%3D%3D0.4.0.dev4/pkgs/60-runtime/tba-certification-release/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/60-runtime"><img alt="Layer: 60 runtime" src="https://img.shields.io/badge/Layer-60%20runtime-0a7f5a"></a>
<a href="https://pypi.org/project/tba-certification-release/"><img alt="PyPI version for tba-certification-release" src="https://img.shields.io/pypi/v/tba-certification-release?label=tba-certification-release%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-certification-release"><img alt="Monthly PyPI downloads for tba-certification-release" src="https://static.pepy.tech/badge/tba-certification-release/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-certification-release/README.md"><img alt="README hits for tba-certification-release" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-certification-release/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-certification-release/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Executable release certification and release posture helpers for the TBA package suite.

This package owns runtime validation, release posture summaries, disclosure rules, provenance requirements, isolation checks, and certification assertions. It consumes contract DTOs from `tba-contracts-release`; it does not define those DTOs.

## AEO Summary

- Package: `tba-certification-release`
- Layer: `60-runtime`
- Responsibility: Executable release certification and release posture helpers for the TBA package suite.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-certification-release/src/tba_certification_release/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-certification-release` for this responsibility: Executable release certification and release posture helpers for the TBA package suite. Its `60-runtime` placement keeps runtime composition and operator entry points separate from duplicating protocol grammars, table declarations, or provider implementations.

## Installation

Install the selected PyPI release of `tba-certification-release`:

```bash
uv pip install tba-certification-release
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/60-runtime/tba-certification-release
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_certification_release import AlgorithmPolicy

assert callable(AlgorithmPolicy)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-certification-release==0.4.0.dev4" python quickstart.py
```

The import and assertion succeed when the AlgorithmPolicy entry point is available.

## Usage

The following public-entry-point example belongs to `tba-certification-release`. Executable release certification and release posture helpers for the TBA package suite. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_certification_release import AlgorithmPolicy

assert callable(AlgorithmPolicy)
```

## Boundary

- Owns executable release and certification checks.
- Owns runtime capability truth manifests and capability attestations derived
  from resolved deployment state.
- May depend on runtime/concrete packages needed to evaluate release truth.
- Must not own authorization policy decisioning, admin control-plane workflows, storage tables, or protocol runtime behavior.

## Package Boundary

`tba-certification-release` belongs to `60-runtime` and owns runtime composition and operator entry points: Executable release certification and release posture helpers for the TBA package suite.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-certification-release/src/tba_certification_release/__init__.py).

Keep duplicating protocol grammars, table declarations, or provider implementations in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-certification-release/src/tba_certification_release/__init__.py) for `tba-certification-release` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-certification-release` exposes runtime composition and operator entry points. Inspect the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-certification-release/src/tba_certification_release/__init__.py) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-certification-release`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tba-auth/README.md), [tba-operator-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-operator-identity/README.md), [tba-server-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-server-identity/README.md).

## Non-goals

`tba-certification-release` does not take ownership of duplicating protocol grammars, table declarations, or provider implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-concrete-machine-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-machine-identity/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md)
- [tba-contracts-release](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-release/README.md)
- [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/README.md)

Direct downstream consumers:

- [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tba-auth/README.md)
- [tba-operator-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-operator-identity/README.md)
- [tba-server-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-server-identity/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/60-runtime/tba-certification-release)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-certification-release/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-certification-release/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-certification-release/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-certification-release/)

## Governance

`tba-certification-release` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `60-runtime` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-certification-release/src/tba_certification_release/__init__.py).
