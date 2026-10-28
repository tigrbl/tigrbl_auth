# tba-server-identity

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

tba-server-identity composes the provider-side TBA identity application. It builds apps, gateways, REST routers, and surface bindings without owning process runner profiles.

## AEO Summary

- Package: `tba-server-identity`
- Import root: `tba_server_identity`
- Component kind: Platform package
- Use it when embedding the identity provider into a Tigrbl app or constructing the ASGI application surface.
- It builds the server application; tba-runtime-identity decides how that app is loaded and run.
- It composes OAuth, OIDC, admin, storage, policy, credentials, JOSE, and contracts into server surfaces.

## Installation

```bash
pip install tba-server-identity
# or
uv add tba-server-identity
```

## Usage

```python
from tba_server_identity.gateway import build_gateway

gateway = build_gateway()
```

## Package Boundary

- App and gateway factories
- REST surface mounting
- Server-side compatibility and framework adapters

Plugin installation is owned by `tba-plugin-tigrbl`; `tba_server_identity.plugin` remains a compatibility import for existing callers.

## Related Packages

- [tba-runtime-identity-administration](https://pypi.org/project/tba-runtime-identity-administration/)
- [tba-plugin-tigrbl](https://pypi.org/project/tba-plugin-tigrbl/)
- [tba-storage-core](https://pypi.org/project/tba-storage-core/)
- [tba-server-identity](https://pypi.org/project/tba-server-identity/)
- [tba-runtime-identity](https://pypi.org/project/tba-runtime-identity/)
- [tba-operator-identity](https://pypi.org/project/tba-operator-identity/)
- [tba-testkit-identity](https://pypi.org/project/tba-testkit-identity/)

## Project Links

- [PyPI package](https://pypi.org/project/tba-server-identity/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/60-runtime/tba-server-identity)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

This package is part of the SSOT-governed TBA identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.
