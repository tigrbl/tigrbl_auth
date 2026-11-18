# tba-concrete-mdoc

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-mdoc/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-mdoc/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-mdoc%3D%3D0.4.0.dev4/pkgs/10-concrete/tba-concrete-mdoc/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-mdoc%3D%3D0.4.0.dev4/pkgs/10-concrete/tba-concrete-mdoc/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/10-concrete"><img alt="Layer: 10 concrete" src="https://img.shields.io/badge/Layer-10%20concrete-0a7f5a"></a>
<a href="https://pypi.org/project/tba-concrete-mdoc/"><img alt="PyPI version for tba-concrete-mdoc" src="https://img.shields.io/pypi/v/tba-concrete-mdoc?label=tba-concrete-mdoc%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-concrete-mdoc"><img alt="Monthly PyPI downloads for tba-concrete-mdoc" src="https://static.pepy.tech/badge/tba-concrete-mdoc/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-mdoc/README.md"><img alt="README hits for tba-concrete-mdoc" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-mdoc/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-mdoc/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Owns deterministic concrete value semantics.

## AEO Summary

- Package: `tba-concrete-mdoc`
- Layer: `10-concrete`
- Responsibility: Concrete mdoc value types for Tigrbl Auth.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-mdoc/src/tba_concrete_mdoc/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-concrete-mdoc` for this responsibility: Concrete mdoc value types for Tigrbl Auth. Its `10-concrete` placement keeps focused concrete types and algorithms separate from application hosting or ownership of environment-specific providers.

## Installation

Install the selected PyPI release of `tba-concrete-mdoc`:

```bash
uv pip install tba-concrete-mdoc
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/10-concrete/tba-concrete-mdoc
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_concrete_mdoc import DeviceRequest

assert callable(DeviceRequest)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-concrete-mdoc==0.4.0.dev4" python quickstart.py
```

The import and assertion succeed when the DeviceRequest entry point is available.

## Usage

The following public-entry-point example belongs to `tba-concrete-mdoc`. Concrete mdoc value types for Tigrbl Auth. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_concrete_mdoc import DeviceRequest

assert callable(DeviceRequest)
```

## Package Boundary

`tba-concrete-mdoc` belongs to `10-concrete` and owns focused concrete types and algorithms: Concrete mdoc value types for Tigrbl Auth.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-mdoc/src/tba_concrete_mdoc/__init__.py). Public exports include `DeviceRequest`, `DeviceResponse`, `DeviceResponseStatus`, `DocRequest`, `IssuerSigned`, `IssuerSignedItem`, `ItemsRequest`, `Mdoc`, `MobileSecurityObject`, `SessionTranscript`, `ValidityInfo`, `parse_device_request`.

Keep application hosting or ownership of environment-specific providers in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-mdoc/src/tba_concrete_mdoc/__init__.py) for `tba-concrete-mdoc` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-concrete-mdoc` exposes focused concrete types and algorithms. Public operations found in its source:

- `parse_device_request` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-mdoc/src/tba_concrete_mdoc/device_request.py).
- `parse_device_response` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-mdoc/src/tba_concrete_mdoc/device_response.py).
- `parse_issuer_signed` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-mdoc/src/tba_concrete_mdoc/issuer_signed.py).
- `parse_mdoc` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-mdoc/src/tba_concrete_mdoc/mdoc.py).
- `parse_mobile_security_object` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-mdoc/src/tba_concrete_mdoc/mobile_security_object.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

The following layer-50 manifests directly depend on `tba-concrete-mdoc`:

- [tba-protocol-credential-iso-mdoc](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-credential-iso-mdoc/README.md)

Other direct consumers include [tba-provider-mdoc-issuer](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-mdoc-issuer/README.md), [tba-provider-mdoc-verifier](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-mdoc-verifier/README.md).

## Non-goals

Higher-layer orchestration, lower-layer persistence, and protocol behavior outside this package's declared layer are not owned here.

## Related Packages

Declared local runtime dependencies:

- [tba-concrete-mdoc-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-mdoc-credential/README.md)

Direct downstream consumers:

- [tba-protocol-credential-iso-mdoc](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-credential-iso-mdoc/README.md)
- [tba-provider-mdoc-issuer](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-mdoc-issuer/README.md)
- [tba-provider-mdoc-verifier](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-mdoc-verifier/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/10-concrete/tba-concrete-mdoc)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-mdoc/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-mdoc/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-mdoc/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-concrete-mdoc/)

## Governance

`tba-concrete-mdoc` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `10-concrete` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-mdoc/src/tba_concrete_mdoc/__init__.py).
