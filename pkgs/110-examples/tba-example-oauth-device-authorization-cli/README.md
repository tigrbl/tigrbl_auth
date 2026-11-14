# tba-example-oauth-device-authorization-cli

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli/pyproject.toml"><img alt="Checkout: 0.1.0" src="https://img.shields.io/badge/Checkout-0.1.0-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/110-examples"><img alt="Layer: 110 examples" src="https://img.shields.io/badge/Layer-110%20examples-0a7f5a"></a>
<a href="https://pypi.org/project/tba-example-oauth-device-authorization-cli/"><img alt="PyPI version for tba-example-oauth-device-authorization-cli" src="https://img.shields.io/pypi/v/tba-example-oauth-device-authorization-cli?label=tba-example-oauth-device-authorization-cli%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-example-oauth-device-authorization-cli"><img alt="Monthly PyPI downloads for tba-example-oauth-device-authorization-cli" src="https://static.pepy.tech/badge/tba-example-oauth-device-authorization-cli/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Try OAuth device login from a Python CLI against a configured TBA issuer.

## Quick start

Expect help for `--issuer`, `--client-id`, `--scope`, and `--token-cache`. This command uses the published package and needs no running issuer.

```bash
uvx --from tba-example-oauth-device-authorization-cli==0.1.0 oauth-device-login login --help
```

For a configured test deployment, replace the example issuer and client ID:

```bash
uvx --from tba-example-oauth-device-authorization-cli==0.1.0 oauth-device-login login --issuer https://issuer.example --client-id CLIENT_ID
```

The [device login guide](https://github.com/tigrbl/tigrbl_auth/blob/master/docs/examples/python-cli-device-login.md) explains discovery, browser approval, polling, and token storage.

## When to use it

For a live flow, register a client for the device authorization grant, substitute its ID and your issuer URL, and follow the browser instructions. The example caches returned tokens locally. Use a dedicated test account and protect the cache file.

## Verification

See the [related repository tests](https://github.com/tigrbl/tigrbl_auth/blob/master/tests/examples/test_python_cli_device_login.py) for the implementation scope covered by this example.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [tba-app-backend-public](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/90-backend-apps/tba-app-backend-public#readme) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)
