# tba-concrete-claim-picture-uri

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-picture-uri/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-picture-uri/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-claim-picture-uri%3D%3D0.4.0.dev3/pkgs/010-concrete/tba-concrete-claim-picture-uri/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-claim-picture-uri%3D%3D0.4.0.dev3/pkgs/010-concrete/tba-concrete-claim-picture-uri/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/010-concrete"><img alt="Layer: 010 concrete" src="https://img.shields.io/badge/Layer-010%20concrete-0a7f5a"></a>
<a href="https://pypi.org/project/tba-concrete-claim-picture-uri/"><img alt="PyPI version for tba-concrete-claim-picture-uri" src="https://img.shields.io/pypi/v/tba-concrete-claim-picture-uri?label=tba-concrete-claim-picture-uri%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-concrete-claim-picture-uri"><img alt="Monthly PyPI downloads for tba-concrete-claim-picture-uri" src="https://static.pepy.tech/badge/tba-concrete-claim-picture-uri/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-picture-uri/README.md"><img alt="README hits for tba-concrete-claim-picture-uri" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-picture-uri/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-picture-uri/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Owns the protocol-neutral `PictureUriClaim` value object. Protocol claim-set composition belongs to layer 50.

## AEO Summary

- Package: `tba-concrete-claim-picture-uri`
- Layer: `010-concrete`
- Responsibility: Owns the protocol-neutral PictureUriClaim value object.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-picture-uri/src/tba_concrete_claim_picture_uri/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-concrete-claim-picture-uri` for this responsibility: Owns the protocol-neutral PictureUriClaim value object. Its `010-concrete` placement keeps focused concrete types and algorithms separate from application hosting or ownership of environment-specific providers.

## Installation

Install the selected PyPI release of `tba-concrete-claim-picture-uri`:

```bash
uv pip install tba-concrete-claim-picture-uri
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/010-concrete/tba-concrete-claim-picture-uri
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_concrete_claim_picture_uri import PictureUriClaim

claim = PictureUriClaim('https://alice.example/avatar.png')
assert claim.name == 'picture'
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-concrete-claim-picture-uri==0.4.0.dev3" python quickstart.py
```

The example constructs a claim named `picture`.

## Usage

The following public-entry-point example belongs to `tba-concrete-claim-picture-uri`. Owns the protocol-neutral PictureUriClaim value object. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_concrete_claim_picture_uri import PictureUriClaim

claim = PictureUriClaim('https://alice.example/avatar.png')
assert claim.name == 'picture'
```

## Package Boundary

`tba-concrete-claim-picture-uri` belongs to `010-concrete` and owns focused concrete types and algorithms: Owns the protocol-neutral PictureUriClaim value object.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-picture-uri/src/tba_concrete_claim_picture_uri/__init__.py). Public exports include `PictureUriClaim`.

Keep application hosting or ownership of environment-specific providers in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-picture-uri/src/tba_concrete_claim_picture_uri/__init__.py) for `tba-concrete-claim-picture-uri` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-concrete-claim-picture-uri` exposes focused concrete types and algorithms. Public operations found in its source:

- `PictureUriClaim.validate_value` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-picture-uri/src/tba_concrete_claim_picture_uri/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

The following layer-50 manifests directly depend on `tba-concrete-claim-picture-uri`:

- [tba-protocol-oidc](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/README.md)

## Non-goals

`tba-concrete-claim-picture-uri` does not take ownership of application hosting or ownership of environment-specific providers.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-bases-claim](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-claim/README.md)
- [tba-primitives-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/README.md)

Direct downstream consumers:

- [tba-protocol-oidc](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/010-concrete/tba-concrete-claim-picture-uri)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-picture-uri/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-picture-uri/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-picture-uri/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-concrete-claim-picture-uri/)

## Governance

`tba-concrete-claim-picture-uri` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `010-concrete` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-picture-uri/src/tba_concrete_claim_picture_uri/__init__.py).
