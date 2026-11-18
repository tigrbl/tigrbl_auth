# tba-codec-jcs

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-jcs/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-jcs/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-codec-jcs%3D%3D0.4.0.dev3/pkgs/03-codecs/tba-codec-jcs/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-codec-jcs%3D%3D0.4.0.dev3/pkgs/03-codecs/tba-codec-jcs/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/03-codecs"><img alt="Layer: 03 codecs" src="https://img.shields.io/badge/Layer-03%20codecs-0a7f5a"></a>
<a href="https://pypi.org/project/tba-codec-jcs/"><img alt="PyPI version for tba-codec-jcs" src="https://img.shields.io/pypi/v/tba-codec-jcs?label=tba-codec-jcs%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-codec-jcs"><img alt="Monthly PyPI downloads for tba-codec-jcs" src="https://static.pepy.tech/badge/tba-codec-jcs/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-jcs/README.md"><img alt="README hits for tba-codec-jcs" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-jcs/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-jcs/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Use `canonicalize` for JSON values or `canonicalize_json` for raw JSON. Both produce canonical UTF-8 bytes using the rfc8785 library. The raw JSON entry point rejects duplicate keys.

This package owns TBA’s strict JCS API. New callers should import from `tba_codec_jcs`.
The [RFC 8785 conformance suite](../../../tests/conformance/backlog/test_rfc8785_jcs.py) verifies this package.

[Specification](https://www.rfc-editor.org/rfc/rfc8785.html)

## AEO Summary

- Package: `tba-codec-jcs`
- Layer: `03-codecs`
- Responsibility: RFC 8785 JSON Canonicalization Scheme codec.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-jcs/src/tba_codec_jcs/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-codec-jcs` for this responsibility: RFC 8785 JSON Canonicalization Scheme codec. Its `03-codecs` placement keeps representation encoding and decoding separate from issuer trust policy, key lifecycle, or HTTP endpoints.

## Installation

Install the selected PyPI release of `tba-codec-jcs`:

```bash
uv pip install tba-codec-jcs
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/03-codecs/tba-codec-jcs
```

## Quick start

Build the package from the repository root.

```bash
uv build --wheel pkgs/03-codecs/tba-codec-jcs
```

## Usage

The following public-entry-point example belongs to `tba-codec-jcs`. RFC 8785 JSON Canonicalization Scheme codec. Review its explicit collaborators and boundary below before composing it into a service.

```python
import tba_codec_jcs

print(tba_codec_jcs.__name__)
```

## Package Boundary

`tba-codec-jcs` belongs to `03-codecs` and owns representation encoding and decoding: RFC 8785 JSON Canonicalization Scheme codec.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-jcs/src/tba_codec_jcs/__init__.py). Public exports include `canonicalize`, `canonicalize_json`.

Keep issuer trust policy, key lifecycle, or HTTP endpoints in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-jcs/src/tba_codec_jcs/__init__.py) for `tba-codec-jcs` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-codec-jcs` exposes representation encoding and decoding. Public operations found in its source:

- `canonicalize` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-jcs/src/tba_codec_jcs/__init__.py).
- `canonicalize_json` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-jcs/src/tba_codec_jcs/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

The following layer-50 manifests directly depend on `tba-codec-jcs`:

- [tba-protocol-zcap](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-zcap/README.md)

## Non-goals

`tba-codec-jcs` does not take ownership of issuer trust policy, key lifecycle, or HTTP endpoints.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Direct downstream consumers:

- [tba-protocol-zcap](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-zcap/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/03-codecs/tba-codec-jcs)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-jcs/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-jcs/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-jcs/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-codec-jcs/)

## Governance

`tba-codec-jcs` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `03-codecs` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

Check that the build produces a wheel with the package version declared in `pyproject.toml`.
