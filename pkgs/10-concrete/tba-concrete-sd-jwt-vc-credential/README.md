# tba-concrete-sd-jwt-vc-credential

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-sd-jwt-vc-credential/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-sd-jwt-vc-credential/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-sd-jwt-vc-credential%3D%3D0.4.0.dev4/pkgs/10-concrete/tba-concrete-sd-jwt-vc-credential/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-sd-jwt-vc-credential%3D%3D0.4.0.dev4/pkgs/10-concrete/tba-concrete-sd-jwt-vc-credential/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/10-concrete"><img alt="Layer: 10 concrete" src="https://img.shields.io/badge/Layer-10%20concrete-0a7f5a"></a>
<a href="https://pypi.org/project/tba-concrete-sd-jwt-vc-credential/"><img alt="PyPI version for tba-concrete-sd-jwt-vc-credential" src="https://img.shields.io/pypi/v/tba-concrete-sd-jwt-vc-credential?label=tba-concrete-sd-jwt-vc-credential%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-concrete-sd-jwt-vc-credential"><img alt="Monthly PyPI downloads for tba-concrete-sd-jwt-vc-credential" src="https://static.pepy.tech/badge/tba-concrete-sd-jwt-vc-credential/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-sd-jwt-vc-credential/README.md"><img alt="README hits for tba-concrete-sd-jwt-vc-credential" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-sd-jwt-vc-credential/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-sd-jwt-vc-credential/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Owns the standalone SD-JWT VC digital credential object. Draft revision rules,
registered claim sets, media types, and migrations belong to layer 50.

## AEO Summary

- Package: `tba-concrete-sd-jwt-vc-credential`
- Layer: `10-concrete`
- Responsibility: Owns the standalone SD-JWT VC digital credential object.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-sd-jwt-vc-credential/src/tba_concrete_sd_jwt_vc_credential/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-concrete-sd-jwt-vc-credential` for this responsibility: Owns the standalone SD-JWT VC digital credential object. Its `10-concrete` placement keeps focused concrete types and algorithms separate from application hosting or ownership of environment-specific providers.

## Installation

Install the selected PyPI release of `tba-concrete-sd-jwt-vc-credential`:

```bash
uv pip install tba-concrete-sd-jwt-vc-credential
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/10-concrete/tba-concrete-sd-jwt-vc-credential
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_concrete_sd_jwt_vc_credential import SdJwtVcCredential

assert callable(SdJwtVcCredential)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-concrete-sd-jwt-vc-credential==0.4.0.dev4" python quickstart.py
```

The import and assertion succeed when the SdJwtVcCredential entry point is available.

## Usage

The following public-entry-point example belongs to `tba-concrete-sd-jwt-vc-credential`. Owns the standalone SD-JWT VC digital credential object. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_concrete_sd_jwt_vc_credential import SdJwtVcCredential

assert callable(SdJwtVcCredential)
```

## Package Boundary

`tba-concrete-sd-jwt-vc-credential` belongs to `10-concrete` and owns focused concrete types and algorithms: Owns the standalone SD-JWT VC digital credential object.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-sd-jwt-vc-credential/src/tba_concrete_sd_jwt_vc_credential/__init__.py). Public exports include `SdJwtVcCredential`.

Keep application hosting or ownership of environment-specific providers in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-sd-jwt-vc-credential/src/tba_concrete_sd_jwt_vc_credential/__init__.py) for `tba-concrete-sd-jwt-vc-credential` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-concrete-sd-jwt-vc-credential` exposes focused concrete types and algorithms. Public operations found in its source:

- `SdJwtVcCredential.issuer_jwt` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-sd-jwt-vc-credential/src/tba_concrete_sd_jwt_vc_credential/__init__.py).
- `SdJwtVcCredential.disclosures` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-sd-jwt-vc-credential/src/tba_concrete_sd_jwt_vc_credential/__init__.py).
- `SdJwtVcCredential.key_binding_jwt` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-sd-jwt-vc-credential/src/tba_concrete_sd_jwt_vc_credential/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-concrete-sd-jwt-vc-credential`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-profile-credential-sd-jwt-vc](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-sd-jwt-vc/README.md).

## Non-goals

`tba-concrete-sd-jwt-vc-credential` does not take ownership of application hosting or ownership of environment-specific providers.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-bases-digital-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-digital-credential/README.md)
- [tba-concrete-sd-jwt](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-sd-jwt/README.md)

Direct downstream consumers:

- [tba-profile-credential-sd-jwt-vc](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-sd-jwt-vc/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/10-concrete/tba-concrete-sd-jwt-vc-credential)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-sd-jwt-vc-credential/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-sd-jwt-vc-credential/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-sd-jwt-vc-credential/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-concrete-sd-jwt-vc-credential/)

## Governance

`tba-concrete-sd-jwt-vc-credential` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `10-concrete` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-sd-jwt-vc-credential/src/tba_concrete_sd_jwt_vc_credential/__init__.py).
