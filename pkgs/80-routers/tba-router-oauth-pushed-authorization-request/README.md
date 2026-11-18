# tba-router-oauth-pushed-authorization-request

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-pushed-authorization-request/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-pushed-authorization-request/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-router-oauth-pushed-authorization-request%3D%3D0.4.0.dev3/pkgs/80-routers/tba-router-oauth-pushed-authorization-request/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-router-oauth-pushed-authorization-request%3D%3D0.4.0.dev3/pkgs/80-routers/tba-router-oauth-pushed-authorization-request/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/80-routers"><img alt="Layer: 80 routers" src="https://img.shields.io/badge/Layer-80%20routers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-router-oauth-pushed-authorization-request/"><img alt="PyPI version for tba-router-oauth-pushed-authorization-request" src="https://img.shields.io/pypi/v/tba-router-oauth-pushed-authorization-request?label=tba-router-oauth-pushed-authorization-request%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-router-oauth-pushed-authorization-request"><img alt="Monthly PyPI downloads for tba-router-oauth-pushed-authorization-request" src="https://static.pepy.tech/badge/tba-router-oauth-pushed-authorization-request/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-pushed-authorization-request/README.md"><img alt="README hits for tba-router-oauth-pushed-authorization-request" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-pushed-authorization-request/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-pushed-authorization-request/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

HTTP carrier binding for OAuth 2.0 Pushed Authorization Requests (RFC 9126).

This package owns request decoding, `/par` routing, HTTP error mapping, and
response serialization. It receives normalization, client authentication,
durability, and observation collaborators from runtime composition.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_router_oauth_pushed_authorization_request import PushedAuthorizationAuthorizer

assert callable(PushedAuthorizationAuthorizer)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-router-oauth-pushed-authorization-request==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the PushedAuthorizationAuthorizer entry point is available.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-oauth-pushed-authorization-request/src/tba_router_oauth_pushed_authorization_request/__init__.py).
