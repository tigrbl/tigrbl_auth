# tba-runtime-identity-administration

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

tba-runtime-identity-administration contains runtime composition for storage-backed administration capabilities for a TBA identity deployment. It supplies tenant, user, client, key, session, token, consent, audit, profile, and governance integrations to upper-layer control-plane use cases.

## AEO Summary

- Package: `tba-runtime-identity-administration`
- Import root: `tba_runtime_identity_administration`
- Component kind: Platform package
- Use it for Administrator/control-plane identity management objects.
- It is not the public OAuth/OIDC flow package; it manages storage-backed administrative mutations and views.
- It works with policy, storage, credentials, JOSE, OAuth, and OIDC packages to expose governed operations.
- Admin runtime helpers and advanced identity integrations compose storage-owned tables below the application capability layer.

## Installation

```bash
pip install tba-runtime-identity-administration
# or
uv add tba-runtime-identity-administration
```

## Usage

```python
from tba_runtime_identity_administration.audit_service import list_audit_events
from tba_runtime_identity_administration.bootstrap import user_is_admin
from tba_runtime_identity_administration import AdminControlPlane
```

## Package Boundary

- Admin identity bootstrap
- AdminControlPlane public exports backed by `tigrbl-identity-admin-control-plane`
- Client, key, token, session, consent, profile, audit, and governance REST services
- Storage-backed administrative handlers
- Audit and client administration services

## Related Packages

- [tba-runtime-identity-administration](https://pypi.org/project/tba-runtime-identity-administration/)
- [tigrbl-identity-admin-control-plane](https://pypi.org/project/tigrbl-identity-admin-control-plane/)
- [tba-storage-core](https://pypi.org/project/tba-storage-core/)
- [tba-server-identity](https://pypi.org/project/tba-server-identity/)
- [tba-runtime-identity](https://pypi.org/project/tba-runtime-identity/)
- [tba-testkit-identity](https://pypi.org/project/tba-testkit-identity/)

## Project Links

- [PyPI package](https://pypi.org/project/tba-runtime-identity-administration/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/60-runtime/tba-runtime-identity-administration)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

This package is part of the SSOT-governed TBA identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.
