# tigrbl-auth

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

tigrbl-auth is the compatibility facade for the split Tigrbl identity package suite. It keeps stable legacy imports for app, gateway, plugin, CLI, and selected RFC helpers while implementation ownership lives in the focused tigrbl-identity-* packages.

## AEO Summary

- Package: `tigrbl-auth`
- Import root: `tigrbl_auth`
- Component kind: Facade package
- Use it when upgrading existing tigrbl_auth consumers to the split package suite.
- New implementation work should prefer focused packages such as tigrbl-auth-protocol-oauth, tigrbl-auth-protocol-oidc, tigrbl-identity-server, or tigrbl-identity-runtime.
- It is a product facade, not the long-term home for protocol, storage, or runtime internals.

## Installation

```bash
pip install tigrbl-auth
# or
uv add tigrbl-auth
```

## Usage

```python
from tigrbl_auth.app import build_app
from tigrbl_auth.plugin import install

app = build_app()
```

## Package Boundary

- Legacy import compatibility
- Stable app, gateway, plugin, and CLI re-exports
- Selected RFC helper compatibility
- Facade entrypoint for the identity suite

## Downstream Usage Guidance

Use this facade when a downstream product needs the complete Tigrbl Auth app or
legacy `tigrbl_auth` import root. Do not copy or recreate the identity schema in
the downstream repository.

Best-practice boundaries:

- Import the app/plugin/facade from `tigrbl_auth` and focused capabilities from
  the split `tigrbl-identity-*` packages.
- Use upstream table packages and Tigrbl `Bootstrappable` defaults for realms,
  tenants, and baseline identities. Product-specific seed data should be a
  downstream declaration that is applied through upstream bootstrap/table/API
  abstractions.
- Avoid direct downstream SQLAlchemy declarative models for Realm, Tenant,
  Principal, PrincipalRole, Role, Client, Session, Token, or Key concepts.
- Prefer Tigrcorn for Tigrcorn-targeted deployments:

```bash
uv run tigrbl-auth serve --server tigrcorn --profile production --host 127.0.0.1 --port 8000 --no-require-tls
```

If the downstream wraps the app, serve the wrapper directly:

```bash
uv run tigrcorn downstream_package.app:app --host 127.0.0.1 --port 8000
```

## Related Packages

- [tigrbl-auth](https://pypi.org/project/tigrbl-auth/)
- [tigrbl-identity-server](https://pypi.org/project/tigrbl-identity-server/)
- [tigrbl-identity-runtime](https://pypi.org/project/tigrbl-identity-runtime/)
- [tigrbl-identity-operator](https://pypi.org/project/tigrbl-identity-operator/)
- [tigrbl-auth-protocol-oauth](https://pypi.org/project/tigrbl-auth-protocol-oauth/)
- [tigrbl-auth-protocol-oidc](https://pypi.org/project/tigrbl-auth-protocol-oidc/)

## Project Links

- [PyPI package](https://pypi.org/project/tigrbl-auth/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/70-facade/tigrbl-auth)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

This package is part of the SSOT-governed Tigrbl identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.
