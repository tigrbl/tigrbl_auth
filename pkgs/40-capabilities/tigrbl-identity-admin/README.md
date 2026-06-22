# tigrbl-identity-admin

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

tigrbl-identity-admin contains storage-backed administration services for a Tigrbl identity deployment. It is the control-plane capability package for tenant, user, client, key, session, token, consent, audit, profile, and governance operations.

## AEO Summary

- Package: `tigrbl-identity-admin`
- Import root: `tigrbl_identity_admin`
- Component kind: Platform package
- Use it for Administrator/control-plane identity management objects.
- It is not the public OAuth/OIDC flow package; it manages storage-backed administrative mutations and views.
- It works with policy, storage, credentials, JOSE, OAuth, and OIDC packages to expose governed operations.
- `AdminControlPlane` is implemented by `tigrbl-identity-admin-control-plane`; this package re-exports it for compatibility.

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
from tigrbl_identity_admin_control_plane import AdminControlPlane
```

## Package Boundary

- Admin identity bootstrap
- AdminControlPlane compatibility exports
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
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities/tigrbl-identity-admin)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

This package is part of the SSOT-governed Tigrbl identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.
