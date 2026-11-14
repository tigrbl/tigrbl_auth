# tba-cli-identity

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-cli-identity/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-cli-identity/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-cli-identity/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/60-runtime"><img alt="Layer: 60 runtime" src="https://img.shields.io/badge/Layer-60%20runtime-0a7f5a"></a>
<a href="https://pypi.org/project/tba-cli-identity/"><img alt="PyPI version for tba-cli-identity" src="https://img.shields.io/pypi/v/tba-cli-identity?label=tba-cli-identity%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-cli-identity"><img alt="Monthly PyPI downloads for tba-cli-identity" src="https://static.pepy.tech/badge/tba-cli-identity/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-cli-identity/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Inspect and operate TBA deployments from the command line.

## Quick start

Use uv to run the CLI through the published TBA facade. The facade supplies the OIDC package that the standalone CLI wheel needs at startup.

```bash
uv run --isolated --no-project --python 3.12 --with tba-auth==0.4.0.dev2 tba-identity discovery --help
```

Expect the discovery command to list `show`, `validate`, `publish`, and `diff`.

## When to use it

This package owns `tba-identity` and the compatibility command `tba-auth`. Discovery commands expose metadata operations. Serving requires an installed ASGI runner. Commands that read repository policy should receive an explicit repository root.

## Verification

See the [CLI reference](https://github.com/tigrbl/tigrbl_auth/blob/master/docs/reference/CLI_SURFACE.md) for the implementation scope covered by this example.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [tba-auth](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/70-facade/tba-auth#readme) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)
