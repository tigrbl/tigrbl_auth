# tba-middleware-policy-enforcement-asgi

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/85-middleware/tba-middleware-policy-enforcement-asgi/pyproject.toml"><img alt="Checkout: 0.4.0.dev5" src="https://img.shields.io/badge/Checkout-0.4.0.dev5-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/85-middleware/tba-middleware-policy-enforcement-asgi/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-middleware-policy-enforcement-asgi%3D%3D0.4.0.dev5/pkgs/85-middleware/tba-middleware-policy-enforcement-asgi/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-middleware-policy-enforcement-asgi%3D%3D0.4.0.dev5/pkgs/85-middleware/tba-middleware-policy-enforcement-asgi/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/85-middleware"><img alt="Layer: 85 middleware" src="https://img.shields.io/badge/Layer-85%20middleware-0a7f5a"></a>
<a href="https://pypi.org/project/tba-middleware-policy-enforcement-asgi/"><img alt="PyPI version for tba-middleware-policy-enforcement-asgi" src="https://img.shields.io/pypi/v/tba-middleware-policy-enforcement-asgi?label=tba-middleware-policy-enforcement-asgi%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-middleware-policy-enforcement-asgi"><img alt="Monthly PyPI downloads for tba-middleware-policy-enforcement-asgi" src="https://static.pepy.tech/badge/tba-middleware-policy-enforcement-asgi/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/85-middleware/tba-middleware-policy-enforcement-asgi/README.md"><img alt="README hits for tba-middleware-policy-enforcement-asgi" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/85-middleware/tba-middleware-policy-enforcement-asgi/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/85-middleware/tba-middleware-policy-enforcement-asgi/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Apply a synchronous policy decision to HTTP requests at an ASGI boundary.

## AEO Summary

- Package: `tba-middleware-policy-enforcement-asgi`
- Layer: `85-middleware`
- Responsibility: ASGI policy enforcement point using an injected decision client.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/85-middleware/tba-middleware-policy-enforcement-asgi/src/tba_middleware_policy_enforcement_asgi/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Inject a decision callable that returns an `allowed` field. The middleware sends 403 for a denied HTTP scope and forwards allowed requests and other scope types. The caller owns identity extraction, policy decisions, and handling transport failures.

## Installation

Install the selected PyPI release of `tba-middleware-policy-enforcement-asgi`:

```bash
uv pip install tba-middleware-policy-enforcement-asgi
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/85-middleware/tba-middleware-policy-enforcement-asgi
```

## Quick start

Install the version used by this example.

```bash
python -m pip install "tba-middleware-policy-enforcement-asgi==0.4.0.dev5"
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

## Usage

The following public-entry-point example belongs to `tba-middleware-policy-enforcement-asgi`. ASGI policy enforcement point using an injected decision client. Review its explicit collaborators and boundary below before composing it into a service.

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

## Package Boundary

`tba-middleware-policy-enforcement-asgi` belongs to `85-middleware` and owns request middleware integration: ASGI policy enforcement point using an injected decision client.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/85-middleware/tba-middleware-policy-enforcement-asgi/src/tba_middleware_policy_enforcement_asgi/__init__.py). Public exports include `PolicyEnforcementMiddleware`.

Keep implicit key storage or a complete identity deployment in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-middleware-policy-enforcement-asgi`:

- `PolicyEnforcementMiddleware` construction inputs: `app`, `decide`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/85-middleware/tba-middleware-policy-enforcement-asgi/src/tba_middleware_policy_enforcement_asgi/__init__.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-middleware-policy-enforcement-asgi` exposes request middleware integration. Inspect the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/85-middleware/tba-middleware-policy-enforcement-asgi/src/tba_middleware_policy_enforcement_asgi/__init__.py) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-middleware-policy-enforcement-asgi`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`tba-middleware-policy-enforcement-asgi` does not take ownership of implicit key storage or a complete identity deployment.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-client-policy-decision](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/75-clients/tba-client-policy-decision/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/85-middleware/tba-middleware-policy-enforcement-asgi)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/85-middleware/tba-middleware-policy-enforcement-asgi/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/85-middleware/tba-middleware-policy-enforcement-asgi/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/85-middleware/tba-middleware-policy-enforcement-asgi/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-middleware-policy-enforcement-asgi/)

## Governance

`tba-middleware-policy-enforcement-asgi` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `85-middleware` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

Run the example above to check the public API against the installed package. Its assertions describe the expected behavior.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [tba-client-policy-decision](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/75-clients/tba-client-policy-decision#readme) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)
