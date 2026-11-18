# tba-concrete-cwt

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-cwt/pyproject.toml"><img alt="Checkout: 0.4.0.dev5" src="https://img.shields.io/badge/Checkout-0.4.0.dev5-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-cwt/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-cwt%3D%3D0.4.0.dev5/pkgs/10-concrete/tba-concrete-cwt/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-cwt%3D%3D0.4.0.dev5/pkgs/10-concrete/tba-concrete-cwt/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/10-concrete"><img alt="Layer: 10 concrete" src="https://img.shields.io/badge/Layer-10%20concrete-0a7f5a"></a>
<a href="https://pypi.org/project/tba-concrete-cwt/"><img alt="PyPI version for tba-concrete-cwt" src="https://img.shields.io/pypi/v/tba-concrete-cwt?label=tba-concrete-cwt%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-concrete-cwt"><img alt="Monthly PyPI downloads for tba-concrete-cwt" src="https://static.pepy.tech/badge/tba-concrete-cwt/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-cwt/README.md"><img alt="README hits for tba-concrete-cwt" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-cwt/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-cwt/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Deterministic RFC 8392 CWT claims-set encoding and decoding. COSE protection, trust, profile validation, and proof verification remain separate concerns.

## AEO Summary

- Package: `tba-concrete-cwt`
- Layer: `10-concrete`
- Responsibility: Deterministic provider-free CWT claims-set objects.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-cwt/src/tba_concrete_cwt/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-concrete-cwt` for this responsibility: Deterministic provider-free CWT claims-set objects. Its `10-concrete` placement keeps focused concrete types and algorithms separate from application hosting or ownership of environment-specific providers.

## Installation

Install the selected PyPI release of `tba-concrete-cwt`:

```bash
uv pip install tba-concrete-cwt
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/10-concrete/tba-concrete-cwt
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_concrete_cwt import CwtClaimsSet

assert callable(CwtClaimsSet)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-concrete-cwt==0.4.0.dev5" python quickstart.py
```

The import and assertion succeed when the CwtClaimsSet entry point is available.

## Usage

The following public-entry-point example belongs to `tba-concrete-cwt`. Deterministic provider-free CWT claims-set objects. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_concrete_cwt import CwtClaimsSet

assert callable(CwtClaimsSet)
```

## Package Boundary

`tba-concrete-cwt` belongs to `10-concrete` and owns focused concrete types and algorithms: Deterministic provider-free CWT claims-set objects.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-cwt/src/tba_concrete_cwt/__init__.py). Public exports include `CWT_CLAIM_LABELS`, `CWT_TAG`, `CwtClaimsSet`, `decode_cwt_claims`, `decode_tagged_cwt`, `encode_tagged_cwt`.

Keep application hosting or ownership of environment-specific providers in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-concrete-cwt`:

- `decode_tagged_cwt` construction inputs: `require_tag`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-cwt/src/tba_concrete_cwt/tagged.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-concrete-cwt` exposes focused concrete types and algorithms. Public operations found in its source:

- `CwtClaimsSet.get_registered` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-cwt/src/tba_concrete_cwt/claims.py).
- `CwtClaimsSet.encode` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-cwt/src/tba_concrete_cwt/claims.py).
- `decode_cwt_claims` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-cwt/src/tba_concrete_cwt/claims.py).
- `encode_tagged_cwt` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-cwt/src/tba_concrete_cwt/tagged.py).
- `decode_tagged_cwt` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-cwt/src/tba_concrete_cwt/tagged.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

The following layer-50 manifests directly depend on `tba-concrete-cwt`:

- [tba-protocol-cwt](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-cwt/README.md)

Other direct consumers include [tba-concrete-cwt-svid-extension-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-cwt-svid-extension-credential/README.md).

## Non-goals

`tba-concrete-cwt` does not take ownership of application hosting or ownership of environment-specific providers.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Direct downstream consumers:

- [tba-concrete-cwt-svid-extension-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-cwt-svid-extension-credential/README.md)
- [tba-protocol-cwt](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-cwt/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/10-concrete/tba-concrete-cwt)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-cwt/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-cwt/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-cwt/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-concrete-cwt/)

## Governance

`tba-concrete-cwt` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `10-concrete` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-cwt/src/tba_concrete_cwt/__init__.py).
