# tba-middleware-policy-enforcement-asgi

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/85-middleware/tba-middleware-policy-enforcement-asgi/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/85-middleware/tba-middleware-policy-enforcement-asgi/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/85-middleware/tba-middleware-policy-enforcement-asgi/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/85-middleware"><img alt="Layer: 85 middleware" src="https://img.shields.io/badge/Layer-85%20middleware-0a7f5a"></a>
<a href="https://pypi.org/project/tba-middleware-policy-enforcement-asgi/"><img alt="PyPI version for tba-middleware-policy-enforcement-asgi" src="https://img.shields.io/pypi/v/tba-middleware-policy-enforcement-asgi?label=tba-middleware-policy-enforcement-asgi%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-middleware-policy-enforcement-asgi"><img alt="Monthly PyPI downloads for tba-middleware-policy-enforcement-asgi" src="https://static.pepy.tech/badge/tba-middleware-policy-enforcement-asgi/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/85-middleware/tba-middleware-policy-enforcement-asgi/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Apply a synchronous policy decision to HTTP requests at an ASGI boundary.

## Quick start

Install the version used by this example.

```bash
python -m pip install "tba-middleware-policy-enforcement-asgi==0.4.0.dev3"
```

Save the following as `quickstart.py` and run `python quickstart.py`. The assertions should pass.

```python
import asyncio

from tba_middleware_policy_enforcement_asgi import PolicyEnforcementMiddleware

async def protected(scope, receive, send):
    raise AssertionError("a denied request reached the app")

messages = []

async def send(message):
    messages.append(message)

async def receive():
    raise AssertionError("a denied request read the body")

middleware = PolicyEnforcementMiddleware(protected, lambda scope: {"allowed": False})
asyncio.run(middleware({"type": "http"}, receive, send))
assert messages[0]["status"] == 403
assert messages[1]["body"] == b"Forbidden"
```

## When to use it

Inject a decision callable that returns an `allowed` field. The middleware sends 403 for a denied HTTP scope and forwards allowed requests and other scope types. The caller owns identity extraction, policy decisions, and handling transport failures.

## Verification

Run the example above to check the public API against the installed package. Its assertions describe the expected behavior.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [tba-client-policy-decision](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/75-clients/tba-client-policy-decision#readme) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)
