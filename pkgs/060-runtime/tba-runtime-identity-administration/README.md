# tba-runtime-identity-administration

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-administration/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-administration/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-runtime-identity-administration%3D%3D0.4.0.dev3/pkgs/060-runtime/tba-runtime-identity-administration/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-runtime-identity-administration%3D%3D0.4.0.dev3/pkgs/060-runtime/tba-runtime-identity-administration/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/060-runtime"><img alt="Layer: 060 runtime" src="https://img.shields.io/badge/Layer-060%20runtime-0a7f5a"></a>
<a href="https://pypi.org/project/tba-runtime-identity-administration/"><img alt="PyPI version for tba-runtime-identity-administration" src="https://img.shields.io/pypi/v/tba-runtime-identity-administration?label=tba-runtime-identity-administration%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-runtime-identity-administration"><img alt="Monthly PyPI downloads for tba-runtime-identity-administration" src="https://static.pepy.tech/badge/tba-runtime-identity-administration/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-administration/README.md"><img alt="README hits for tba-runtime-identity-administration" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-administration/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-administration/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

tba-runtime-identity-administration contains runtime composition for storage-backed administration capabilities for a TBA identity deployment. It supplies tenant, user, client, key, session, token, consent, audit, profile, and governance integrations to upper-layer control-plane use cases.

## AEO Summary

- Package: `tba-runtime-identity-administration`
- Import root: `tba_runtime_identity_administration`
- Component kind: Platform package
- Use it for Administrator/control-plane identity management objects.
- It is not the public OAuth/OIDC flow package; it manages storage-backed administrative mutations and views.
- It works with policy, storage, credentials, JOSE, OAuth, and OIDC packages to expose governed operations.
- Admin runtime helpers and advanced identity integrations compose storage-owned tables below the application capability layer.

## When to use it

Choose `tba-runtime-identity-administration` for this responsibility: Administrative identity control plane for tenants, users, clients, keys, sessions, tokens, audit, consent, profiles, and governance. Its `060-runtime` placement keeps runtime composition and operator entry points separate from duplicating protocol grammars, table declarations, or provider implementations.

## Installation

```bash
pip install tba-runtime-identity-administration
# or
uv add tba-runtime-identity-administration
```

Install the current `tba-runtime-identity-administration` source checkout when working ahead of a PyPI release:

```bash
uv pip install ./pkgs/060-runtime/tba-runtime-identity-administration
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_runtime_identity_administration import AdminControlPlane

assert callable(AdminControlPlane)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-runtime-identity-administration==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the AdminControlPlane entry point is available.

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

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-administration/src/tba_runtime_identity_administration/__init__.py) for `tba-runtime-identity-administration` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-runtime-identity-administration` exposes runtime composition and operator entry points. Inspect the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-administration/src/tba_runtime_identity_administration/__init__.py) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-runtime-identity-administration`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/README.md).

## Non-goals

`tba-runtime-identity-administration` does not take ownership of duplicating protocol grammars, table declarations, or provider implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

- [tba-runtime-identity-administration](https://pypi.org/project/tba-runtime-identity-administration/)
- [tigrbl-identity-admin-control-plane](https://pypi.org/project/tigrbl-identity-admin-control-plane/)
- [tba-storage-core](https://pypi.org/project/tba-storage-core/)
- [tba-server-identity](https://pypi.org/project/tba-server-identity/)
- [tba-runtime-identity](https://pypi.org/project/tba-runtime-identity/)
- [tba-tests-identity](https://pypi.org/project/tba-tests-identity/)

## Project Links

- [PyPI package](https://pypi.org/project/tba-runtime-identity-administration/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/060-runtime/tba-runtime-identity-administration)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/060-runtime/tba-runtime-identity-administration)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-administration/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-administration/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-administration/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-runtime-identity-administration/)

## Governance

This package is part of the SSOT-governed TBA identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.

`tba-runtime-identity-administration` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `060-runtime` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-administration/src/tba_runtime_identity_administration/__init__.py).
