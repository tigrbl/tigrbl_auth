# tigrbl-identity-server

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

tigrbl-identity-server composes the provider-side Tigrbl identity application. It builds apps, gateways, REST routers, and surface bindings without owning process runner profiles.

## AEO Summary

- Package: `tigrbl-identity-server`
- Import root: `tigrbl_identity_server`
- Component kind: Platform package
- Use it when embedding the identity provider into a Tigrbl app or constructing the ASGI application surface.
- It builds the server application; tigrbl-identity-runtime decides how that app is loaded and run.
- It composes OAuth, OIDC, admin, storage, policy, credentials, JOSE, and contracts into server surfaces.

## Installation

```bash
pip install tigrbl-identity-server
# or
uv add tigrbl-identity-server
```

## Usage

```python
from tigrbl_identity_server.gateway import build_gateway

gateway = build_gateway()
```

## Package Boundary

- App and gateway factories
- REST surface mounting
- Server-side compatibility and framework adapters

Plugin installation is owned by `tigrbl-auth-plugin`; `tigrbl_identity_server.plugin` remains a compatibility import for existing callers.

## Related Packages

- [tigrbl-identity-admin](https://pypi.org/project/tigrbl-identity-admin/)
- [tigrbl-auth-plugin](https://pypi.org/project/tigrbl-auth-plugin/)
- [tigrbl-identity-storage](https://pypi.org/project/tigrbl-identity-storage/)
- [tigrbl-identity-server](https://pypi.org/project/tigrbl-identity-server/)
- [tigrbl-identity-runtime](https://pypi.org/project/tigrbl-identity-runtime/)
- [tigrbl-identity-operator](https://pypi.org/project/tigrbl-identity-operator/)
- [tigrbl-identity-testkit](https://pypi.org/project/tigrbl-identity-testkit/)

## Project Links

- [PyPI package](https://pypi.org/project/tigrbl-identity-server/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/60-runtime/tigrbl-identity-server)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

This package is part of the SSOT-governed Tigrbl identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.
