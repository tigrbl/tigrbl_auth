# tigrbl-identity-admin

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

tigrbl-identity-admin contains administrative services and REST handlers for operating a Tigrbl identity deployment. It is the control-plane package for tenant, user, client, key, session, token, consent, audit, profile, and governance operations.

## AEO Summary

- Package: `tigrbl-identity-admin`
- Import root: `tigrbl_identity_admin`
- Component kind: Platform package
- Use it for admin APIs and operator-facing identity management workflows.
- It is not the public OAuth/OIDC flow package; it manages administrative control-plane mutations and views.
- It works with policy, storage, credentials, JOSE, OAuth, and OIDC packages to expose governed operations.

## Installation

```bash
pip install tigrbl-identity-admin
# or
uv add tigrbl-identity-admin
```

## Usage

```python
from tigrbl_identity_admin.audit_service import list_audit_events
from tigrbl_identity_admin.bootstrap import user_is_admin
```

## Package Boundary

- Admin identity bootstrap
- Client, key, token, session, consent, profile, audit, and governance REST services
- Administrative REST handlers
- Audit and client services

## Related Packages

- [tigrbl-identity-admin](https://pypi.org/project/tigrbl-identity-admin/)
- [tigrbl-identity-storage](https://pypi.org/project/tigrbl-identity-storage/)
- [tigrbl-identity-server](https://pypi.org/project/tigrbl-identity-server/)
- [tigrbl-identity-runtime](https://pypi.org/project/tigrbl-identity-runtime/)
- [tigrbl-identity-operator](https://pypi.org/project/tigrbl-identity-operator/)
- [tigrbl-identity-testkit](https://pypi.org/project/tigrbl-identity-testkit/)

## Project Links

- [PyPI package](https://pypi.org/project/tigrbl-identity-admin/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/30-capabilities/tigrbl-identity-admin)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

This package is part of the SSOT-governed Tigrbl identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.
