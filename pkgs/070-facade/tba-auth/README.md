# tba-auth

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-auth%3D%3D0.4.0.dev3/pkgs/070-facade/tba-auth/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-auth%3D%3D0.4.0.dev3/pkgs/070-facade/tba-auth/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/070-facade"><img alt="Layer: 070 facade" src="https://img.shields.io/badge/Layer-070%20facade-0a7f5a"></a>
<a href="https://pypi.org/project/tba-auth/"><img alt="PyPI version for tba-auth" src="https://img.shields.io/pypi/v/tba-auth?label=tba-auth%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-auth"><img alt="Monthly PyPI downloads for tba-auth" src="https://static.pepy.tech/badge/tba-auth/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/README.md"><img alt="README hits for tba-auth" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Keep existing applications working with the compatibility facade for the split TBA identity suite.

## AEO Summary

- Package: `tba-auth`
- Import root: `tba_auth`
- Component kind: Facade package
- Use it when upgrading existing tba_auth consumers to the split package suite.
- New implementation work should prefer focused packages such as tba-protocol-oauth, tba-protocol-oidc, tba-plugin-tigrbl, tba-server-identity, or tba-runtime-identity.
- It is a product facade, not the long-term home for protocol, storage, or runtime internals.

## When to use it

Use this distribution when maintaining code with `tba_auth` imports. New integrations can use the focused public backend, server, or Tigrbl plugin packages directly. The example plans a local runner without starting it.

## Installation

Install the selected PyPI release of `tba-auth`:

```bash
uv pip install tba-auth
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/070-facade/tba-auth
```

## Quick start

Install the version used by this example.

```bash
python -m pip install "tba-auth==0.4.0.dev3"
```

Save the following as `quickstart.py` and run `python quickstart.py`. The assertions should pass.

```python
from tba_auth.app import build_application_runtime_plan

plan = build_application_runtime_plan(runner="uvicorn", host="127.0.0.1", port=8000)
assert plan.runner == "uvicorn"
assert plan.port == 8000
```

## Usage

The following public-entry-point example belongs to `tba-auth`. Compatibility facade for the split TBA identity package suite, preserving legacy app, gateway, plugin, CLI, and RFC imports. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_auth.app import build_application_runtime_plan

plan = build_application_runtime_plan(runner="uvicorn", host="127.0.0.1", port=8000)
assert plan.runner == "uvicorn"
assert plan.port == 8000
```

## Package Boundary

- Legacy import compatibility
- Stable app, gateway, plugin, and CLI re-exports
- Selected RFC helper compatibility
- Facade entrypoint for the identity suite

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/src/tba_auth/__init__.py) for `tba-auth` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-auth` exposes curated public entry points. Inspect the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/src/tba_auth/__init__.py) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-auth`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-app-backend-developer](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-developer/README.md), [tba-app-backend-my-account](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-my-account/README.md), [tba-app-backend-platform-administration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-platform-administration/README.md), [tba-app-backend-public](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-public/README.md), [tba-app-backend-resource-validation](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-resource-validation/README.md), [tba-app-backend-service-administration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-service-administration/README.md), [tba-app-backend-tenant-administration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-tenant-administration/README.md).

## Non-goals

`tba-auth` does not take ownership of moving implementation ownership out of focused packages.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

- [tba-auth](https://pypi.org/project/tba-auth/)
- [tba-plugin-tigrbl](https://pypi.org/project/tba-plugin-tigrbl/)
- [tba-server-identity](https://pypi.org/project/tba-server-identity/)
- [tba-runtime-identity](https://pypi.org/project/tba-runtime-identity/)
- [tba-operator-identity](https://pypi.org/project/tba-operator-identity/)
- [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/)
- [tba-protocol-oidc](https://pypi.org/project/tba-protocol-oidc/)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/070-facade/tba-auth)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-auth/)

## Governance

This package is part of the SSOT-governed TBA identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.

`tba-auth` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `070-facade` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

See the [related repository tests](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-architecture/tests/unit/test_facade_compatibility_boundary.py) for the implementation scope covered by this example.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [tba-app-backend-public](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/090-backend-apps/tba-app-backend-public#readme) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)
