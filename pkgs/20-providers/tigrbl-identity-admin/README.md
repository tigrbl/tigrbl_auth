# tigrbl-identity-admin

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

tigrbl-identity-admin contains concrete storage-backed administration providers for a Tigrbl identity deployment. It supplies tenant, user, client, key, session, token, consent, audit, profile, and governance integrations to upper-layer control-plane use cases.

## AEO Summary

- Package: `tigrbl-identity-admin`
- Import root: `tigrbl_identity_admin`
- Component kind: Platform package
- Use it for Administrator/control-plane identity management objects.
- It is not the public OAuth/OIDC flow package; it manages storage-backed administrative mutations and views.
- It works with policy, storage, credentials, JOSE, OAuth, and OIDC packages to expose governed operations.
- Admin provider helpers and advanced identity integrations compose storage-owned tables below the application capability layer.

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
from tigrbl_identity_admin import AdminControlPlane
```

## Package Boundary

- Admin identity bootstrap
- AdminControlPlane public exports backed by `tigrbl-identity-admin-control-plane`
- Client, key, token, session, consent, profile, audit, and governance REST services
- Storage-backed administrative handlers
- Audit and client administration services

## Related Packages

- [tigrbl-identity-admin](https://pypi.org/project/tigrbl-identity-admin/)
- [tigrbl-identity-admin-control-plane](https://pypi.org/project/tigrbl-identity-admin-control-plane/)
- [tigrbl-identity-storage](https://pypi.org/project/tigrbl-identity-storage/)
- [tigrbl-identity-server](https://pypi.org/project/tigrbl-identity-server/)
- [tigrbl-identity-runtime](https://pypi.org/project/tigrbl-identity-runtime/)
- [tigrbl-identity-testkit](https://pypi.org/project/tigrbl-identity-testkit/)

## Project Links

- [PyPI package](https://pypi.org/project/tigrbl-identity-admin/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers/tigrbl-identity-admin)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

This package is part of the SSOT-governed Tigrbl identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.
