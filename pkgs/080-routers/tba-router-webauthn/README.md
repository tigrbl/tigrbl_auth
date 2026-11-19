# tba-router-webauthn

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-webauthn/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-webauthn/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-router-webauthn%3D%3D0.4.0.dev3/pkgs/080-routers/tba-router-webauthn/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-router-webauthn%3D%3D0.4.0.dev3/pkgs/080-routers/tba-router-webauthn/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/080-routers"><img alt="Layer: 080 routers" src="https://img.shields.io/badge/Layer-080%20routers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-router-webauthn/"><img alt="PyPI version for tba-router-webauthn" src="https://img.shields.io/pypi/v/tba-router-webauthn?label=tba-router-webauthn%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-router-webauthn"><img alt="Monthly PyPI downloads for tba-router-webauthn" src="https://static.pepy.tech/badge/tba-router-webauthn/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-webauthn/README.md"><img alt="README hits for tba-router-webauthn" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-webauthn/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-webauthn/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Application HTTPS carrier mapping for WebAuthn. Cryptographic and ceremony
verification remain owned by the versioned layer-50 protocol package.

## AEO Summary

- Package: `tba-router-webauthn`
- Layer: `080-routers`
- Responsibility: HTTPS carrier binding for WebAuthn ceremonies.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-webauthn/src/tba_router_webauthn/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-router-webauthn` for this responsibility: HTTPS carrier binding for WebAuthn ceremonies. Its `080-routers` placement keeps transport-facing route composition separate from duplicating credential algorithms or storage ownership.

## Installation

Install the selected PyPI release of `tba-router-webauthn`:

```bash
uv pip install tba-router-webauthn
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/080-routers/tba-router-webauthn
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_router_webauthn import build_webauthn_router

assert callable(build_webauthn_router)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-router-webauthn==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the build_webauthn_router entry point is available.

## Usage

The following public-entry-point example belongs to `tba-router-webauthn`. HTTPS carrier binding for WebAuthn ceremonies. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_router_webauthn import build_webauthn_router

assert callable(build_webauthn_router)
```

## Package Boundary

`tba-router-webauthn` belongs to `080-routers` and owns transport-facing route composition: HTTPS carrier binding for WebAuthn ceremonies.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-webauthn/src/tba_router_webauthn/__init__.py).

Keep duplicating credential algorithms or storage ownership in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-webauthn/src/tba_router_webauthn/__init__.py) for `tba-router-webauthn` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-router-webauthn` exposes transport-facing route composition. Inspect the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-webauthn/src/tba_router_webauthn/__init__.py) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-router-webauthn`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-app-backend-public](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-public/README.md).

## Non-goals

`tba-router-webauthn` does not take ownership of duplicating credential algorithms or storage ownership.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-protocol-webauthn](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/README.md)

Direct downstream consumers:

- [tba-app-backend-public](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-public/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/080-routers/tba-router-webauthn)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-webauthn/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-webauthn/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-webauthn/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-router-webauthn/)

## Governance

`tba-router-webauthn` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `080-routers` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-webauthn/src/tba_router_webauthn/__init__.py).
