# tba-plugin-tigrbl

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-plugin-tigrbl%3D%3D0.4.0.dev3/pkgs/060-runtime/tba-plugin-tigrbl/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-plugin-tigrbl%3D%3D0.4.0.dev3/pkgs/060-runtime/tba-plugin-tigrbl/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/060-runtime"><img alt="Layer: 060 runtime" src="https://img.shields.io/badge/Layer-060%20runtime-0a7f5a"></a>
<a href="https://pypi.org/project/tba-plugin-tigrbl/"><img alt="PyPI version for tba-plugin-tigrbl" src="https://img.shields.io/pypi/v/tba-plugin-tigrbl?label=tba-plugin-tigrbl%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-plugin-tigrbl"><img alt="Monthly PyPI downloads for tba-plugin-tigrbl" src="https://static.pepy.tech/badge/tba-plugin-tigrbl/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/README.md"><img alt="README hits for tba-plugin-tigrbl" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Standalone `TbaPlugin` package for the TBA package suite.

- Package: `tba-plugin-tigrbl`
- Import root: `tba_plugin_tigrbl`
- Owns `TbaPlugin` and the `install()` convenience function.
- Installs TBA runtime surfaces into an existing `TigrblApp`.
- `tba_server_identity.plugin` and `tba_auth.plugin` are compatibility wrappers.

## AEO Summary

- Package: `tba-plugin-tigrbl`
- Layer: `060-runtime`
- Responsibility: Standalone TbaPlugin adoption adapter for installing TBA surfaces into an existing Tigrbl app.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/src/tba_plugin_tigrbl/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-plugin-tigrbl` for this responsibility: Standalone TbaPlugin adoption adapter for installing TBA surfaces into an existing Tigrbl app. Its `060-runtime` placement keeps runtime composition and operator entry points separate from duplicating protocol grammars, table declarations, or provider implementations.

## Installation

Install the selected PyPI release of `tba-plugin-tigrbl`:

```bash
uv pip install tba-plugin-tigrbl
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/060-runtime/tba-plugin-tigrbl
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_plugin_tigrbl import TbaPlugin

assert callable(TbaPlugin)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-plugin-tigrbl==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the TbaPlugin entry point is available.

## Usage

The following public-entry-point example belongs to `tba-plugin-tigrbl`. Standalone TbaPlugin adoption adapter for installing TBA surfaces into an existing Tigrbl app. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_plugin_tigrbl import TbaPlugin

assert callable(TbaPlugin)
```

## Operation authorization

Declare an `OperationSecurity` action on each operation you want to protect. After
mounting the routes, derive the catalog digest and publish it with the matching
policy. Install `OperationAuthorizationAdapter` on the app with a credential
verifier, a server-side resource resolver, and a current policy provider. The
resolver can read trusted ownership and tenant attributes using the active
transaction. Handlers that return collections must apply their row scope to the
query using trusted identity or resource data.

The adapter checks credential audience and optional action scope before evaluating
a TBA decision. A missing or mismatched catalog fails closed. Declared public
operations intentionally skip this adapter. Only operations that declare security
participate. The adapter handles decisions without obligations, and an allow
decision carrying an obligation is denied.

## Adoption Option

`TbaPlugin` is one adoption option for downstream applications that already own a `TigrblApp` and want to mount the identity provider surfaces into that app. Other adoption options remain valid: build a complete provider app through `tba-server-identity`, build a gateway through `tba-server-identity`, or run those app factories through `tba-runtime-identity`.

```python
from tba_plugin_tigrbl import TbaPlugin

plugin = TbaPlugin(settings=settings)
plugin.install(app)
```

## Package Boundary

`tba-plugin-tigrbl` belongs to `060-runtime` and owns runtime composition and operator entry points: Standalone TbaPlugin adoption adapter for installing TBA surfaces into an existing Tigrbl app.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/src/tba_plugin_tigrbl/__init__.py). Public exports include `TbaPlugin`, `install`.

Keep duplicating protocol grammars, table declarations, or provider implementations in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-plugin-tigrbl`:

- `install` construction inputs: `surface_attacher`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/src/tba_plugin_tigrbl/plugin.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-plugin-tigrbl` exposes runtime composition and operator entry points. Public operations found in its source:

- `TbaPlugin.resolve_plugin_deployment` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/src/tba_plugin_tigrbl/plugin.py).
- `TbaPlugin.install` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/src/tba_plugin_tigrbl/plugin.py).
- `install` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/src/tba_plugin_tigrbl/plugin.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-plugin-tigrbl`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-app-backend-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/README.md), [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/README.md).

## Non-goals

`tba-plugin-tigrbl` does not take ownership of duplicating protocol grammars, table declarations, or provider implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/README.md)
- [tba-server-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/README.md)

Direct downstream consumers:

- [tba-app-backend-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/README.md)
- [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/060-runtime/tba-plugin-tigrbl)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-plugin-tigrbl/)

## Governance

`tba-plugin-tigrbl` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `060-runtime` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-plugin-tigrbl/src/tba_plugin_tigrbl/__init__.py).
