# tba-provider-security-authorization-provenance-builder

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-authorization-provenance-builder/pyproject.toml"><img alt="Checkout: 0.1.1.dev2" src="https://img.shields.io/badge/Checkout-0.1.1.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-authorization-provenance-builder/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-security-authorization-provenance-builder%3D%3D0.1.1.dev2/pkgs/20-providers/tba-provider-security-authorization-provenance-builder/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-security-authorization-provenance-builder%3D%3D0.1.1.dev2/pkgs/20-providers/tba-provider-security-authorization-provenance-builder/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers"><img alt="Layer: 20 providers" src="https://img.shields.io/badge/Layer-20%20providers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-provider-security-authorization-provenance-builder/"><img alt="PyPI version for tba-provider-security-authorization-provenance-builder" src="https://img.shields.io/pypi/v/tba-provider-security-authorization-provenance-builder?label=tba-provider-security-authorization-provenance-builder%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-provider-security-authorization-provenance-builder"><img alt="Monthly PyPI downloads for tba-provider-security-authorization-provenance-builder" src="https://static.pepy.tech/badge/tba-provider-security-authorization-provenance-builder/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-authorization-provenance-builder/README.md"><img alt="README hits for tba-provider-security-authorization-provenance-builder" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-authorization-provenance-builder/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-authorization-provenance-builder/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Security trust provenance builders for authorization decisions and delegation.

Import root: `tba_provider_security_authorization_provenance_builder`.

## AEO Summary

- Package: `tba-provider-security-authorization-provenance-builder`
- Layer: `20-providers`
- Responsibility: Security trust provenance builders for authorization decisions and delegation.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-authorization-provenance-builder/src/tba_provider_security_authorization_provenance_builder/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-provider-security-authorization-provenance-builder` for this responsibility: Security trust provenance builders for authorization decisions and delegation. Its `20-providers` placement keeps replaceable environment implementations separate from capability orchestration, storage table ownership, or HTTP routing.

## Installation

Install the selected PyPI release of `tba-provider-security-authorization-provenance-builder`:

```bash
uv pip install tba-provider-security-authorization-provenance-builder
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/20-providers/tba-provider-security-authorization-provenance-builder
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_provider_security_authorization_provenance_builder import AuthorizationDecisionTrace

assert callable(AuthorizationDecisionTrace)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-provider-security-authorization-provenance-builder==0.1.1.dev2" python quickstart.py
```

The import and assertion succeed when the AuthorizationDecisionTrace entry point is available.

## Usage

The following public-entry-point example belongs to `tba-provider-security-authorization-provenance-builder`. Security trust provenance builders for authorization decisions and delegation. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_provider_security_authorization_provenance_builder import AuthorizationDecisionTrace

assert callable(AuthorizationDecisionTrace)
```

## Package Boundary

`tba-provider-security-authorization-provenance-builder` belongs to `20-providers` and owns replaceable environment implementations: Security trust provenance builders for authorization decisions and delegation.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-authorization-provenance-builder/src/tba_provider_security_authorization_provenance_builder/__init__.py).

Keep capability orchestration, storage table ownership, or HTTP routing in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-authorization-provenance-builder/src/tba_provider_security_authorization_provenance_builder/__init__.py) for `tba-provider-security-authorization-provenance-builder` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-provider-security-authorization-provenance-builder` exposes replaceable environment implementations. Inspect the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-authorization-provenance-builder/src/tba_provider_security_authorization_provenance_builder/__init__.py) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-provider-security-authorization-provenance-builder`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tba-auth/README.md), [tba-runtime-authorization-policy](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-authorization-policy/README.md), [tba-runtime-identity-storage](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-runtime-identity-storage/README.md).

## Non-goals

`tba-provider-security-authorization-provenance-builder` does not take ownership of capability orchestration, storage table ownership, or HTTP routing.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-concrete-authorization-provenance](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-provenance/README.md)

Direct downstream consumers:

- [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tba-auth/README.md)
- [tba-runtime-authorization-policy](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-authorization-policy/README.md)
- [tba-runtime-identity-storage](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-runtime-identity-storage/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers/tba-provider-security-authorization-provenance-builder)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-authorization-provenance-builder/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-authorization-provenance-builder/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-authorization-provenance-builder/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-provider-security-authorization-provenance-builder/)

## Governance

`tba-provider-security-authorization-provenance-builder` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `20-providers` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-authorization-provenance-builder/src/tba_provider_security_authorization_provenance_builder/__init__.py).
