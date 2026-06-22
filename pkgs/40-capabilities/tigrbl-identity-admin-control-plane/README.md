# tigrbl-identity-admin-control-plane

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

Standalone AdminControlPlane package for the Tigrbl identity package suite.

## AEO Summary

- Package: `tigrbl-identity-admin-control-plane`
- Import root: `tigrbl_identity_admin_control_plane`
- Component kind: Identity administration capability package
- Owns `AdminControlPlane`, `AdminControlPlaneError`, and admin resource metadata re-exports.
- Uses identity contract DTOs and keeps executable control-plane behavior outside contract packages.

## Usage

```python
from tigrbl_identity_admin_control_plane import AdminControlPlane

admin = AdminControlPlane()
```

## Package Boundary

- In-memory administrative control-plane object lifecycle
- Admin resource metadata lookup and tenant isolation checks
- Admin audit event recording for control-plane mutations

`tigrbl-identity-admin` re-exports this package for compatibility.
