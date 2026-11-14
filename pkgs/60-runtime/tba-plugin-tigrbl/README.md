# tba-plugin-tigrbl

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-plugin-tigrbl/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-plugin-tigrbl/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-plugin-tigrbl/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/60-runtime"><img alt="Layer: 60 runtime" src="https://img.shields.io/badge/Layer-60%20runtime-0a7f5a"></a>
<a href="https://pypi.org/project/tba-plugin-tigrbl/"><img alt="PyPI version for tba-plugin-tigrbl" src="https://img.shields.io/pypi/v/tba-plugin-tigrbl?label=tba-plugin-tigrbl%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-plugin-tigrbl"><img alt="Monthly PyPI downloads for tba-plugin-tigrbl" src="https://static.pepy.tech/badge/tba-plugin-tigrbl/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-plugin-tigrbl/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Standalone `TbaPlugin` package for the TBA package suite.

- Package: `tba-plugin-tigrbl`
- Import root: `tba_plugin_tigrbl`
- Owns `TbaPlugin` and the `install()` convenience function.
- Installs TBA runtime surfaces into an existing `TigrblApp`.
- `tba_server_identity.plugin` and `tba_auth.plugin` are compatibility wrappers.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_plugin_tigrbl import TbaPlugin

assert callable(TbaPlugin)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-plugin-tigrbl==0.4.0.dev2" python quickstart.py
```

The import and assertion succeed when the TbaPlugin entry point is available.

## Adoption Option

`TbaPlugin` is one adoption option for downstream applications that already own a `TigrblApp` and want to mount the identity provider surfaces into that app. Other adoption options remain valid: build a complete provider app through `tba-server-identity`, build a gateway through `tba-server-identity`, or run those app factories through `tba-runtime-identity`.

```python
from tba_plugin_tigrbl import TbaPlugin

plugin = TbaPlugin(settings=settings)
plugin.install(app)
```

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-plugin-tigrbl/src/tba_plugin_tigrbl/__init__.py).
