# tba-runtime-identity-administration

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity-administration/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity-administration/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity-administration/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/60-runtime"><img alt="Layer: 60 runtime" src="https://img.shields.io/badge/Layer-60%20runtime-0a7f5a"></a>
<a href="https://pypi.org/project/tba-runtime-identity-administration/"><img alt="PyPI version for tba-runtime-identity-administration" src="https://img.shields.io/pypi/v/tba-runtime-identity-administration?label=tba-runtime-identity-administration%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-runtime-identity-administration"><img alt="Monthly PyPI downloads for tba-runtime-identity-administration" src="https://static.pepy.tech/badge/tba-runtime-identity-administration/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity-administration/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

tba-runtime-identity-administration contains runtime composition for storage-backed administration capabilities for a TBA identity deployment. It supplies tenant, user, client, key, session, token, consent, audit, profile, and governance integrations to upper-layer control-plane use cases.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_runtime_identity_administration import AdminControlPlane

assert callable(AdminControlPlane)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-runtime-identity-administration==0.4.0.dev2" python quickstart.py
```

The import and assertion succeed when the AdminControlPlane entry point is available.

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

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity-administration/src/tba_runtime_identity_administration/__init__.py).
