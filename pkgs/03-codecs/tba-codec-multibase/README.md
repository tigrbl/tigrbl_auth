# tba-codec-multibase

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-multibase/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-multibase/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-codec-multibase%3D%3D0.4.0.dev4/pkgs/03-codecs/tba-codec-multibase/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-codec-multibase%3D%3D0.4.0.dev4/pkgs/03-codecs/tba-codec-multibase/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/03-codecs"><img alt="Layer: 03 codecs" src="https://img.shields.io/badge/Layer-03%20codecs-0a7f5a"></a>
<a href="https://pypi.org/project/tba-codec-multibase/"><img alt="PyPI version for tba-codec-multibase" src="https://img.shields.io/pypi/v/tba-codec-multibase?label=tba-codec-multibase%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-codec-multibase"><img alt="Monthly PyPI downloads for tba-codec-multibase" src="https://static.pepy.tech/badge/tba-codec-multibase/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-multibase/README.md"><img alt="README hits for tba-codec-multibase" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-multibase/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-multibase/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Dependency-free Python codec for base58btc Multibase values. Use
`encode_base58btc(bytes)` and `decode_base58btc(str)`. Both functions handle
the lowercase `z` prefix and preserve leading zero bytes.

The codec converts bytes and text. Its callers set input size limits for
untrusted data and validate decoded values according to their protocols.

See the [Multibase registry](https://github.com/multiformats/multibase)
and [Base58 test vectors](https://datatracker.ietf.org/doc/html/draft-msporny-base58-02#section-5).

## AEO Summary

- Package: `tba-codec-multibase`
- Layer: `03-codecs`
- Responsibility: Multibase encoding and decoding for the base58btc alphabet.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-multibase/src/tba_codec_multibase/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-codec-multibase` for this responsibility: Multibase encoding and decoding for the base58btc alphabet. Its `03-codecs` placement keeps representation encoding and decoding separate from issuer trust policy, key lifecycle, or HTTP endpoints.

## Installation

Install the selected PyPI release of `tba-codec-multibase`:

```bash
uv pip install tba-codec-multibase
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/03-codecs/tba-codec-multibase
```

## Quick start

Build the package from the repository root.

```bash
uv build --wheel pkgs/03-codecs/tba-codec-multibase
```

## Usage

The following public-entry-point example belongs to `tba-codec-multibase`. Multibase encoding and decoding for the base58btc alphabet. Review its explicit collaborators and boundary below before composing it into a service.

```python
import tba_codec_multibase

print(tba_codec_multibase.__name__)
```

## Package Boundary

`tba-codec-multibase` belongs to `03-codecs` and owns representation encoding and decoding: Multibase encoding and decoding for the base58btc alphabet.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-multibase/src/tba_codec_multibase/__init__.py). Public exports include `decode_base58btc`, `encode_base58btc`.

Keep issuer trust policy, key lifecycle, or HTTP endpoints in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-multibase/src/tba_codec_multibase/__init__.py) for `tba-codec-multibase` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-codec-multibase` exposes representation encoding and decoding. Public operations found in its source:

- `encode_base58btc` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-multibase/src/tba_codec_multibase/__init__.py).
- `decode_base58btc` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-multibase/src/tba_codec_multibase/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

The following layer-50 manifests directly depend on `tba-codec-multibase`:

- [tba-protocol-ucan](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-ucan/README.md)
- [tba-protocol-zcap](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-zcap/README.md)

Other direct consumers include [tba-codec-cid](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-cid/README.md).

## Non-goals

`tba-codec-multibase` does not take ownership of issuer trust policy, key lifecycle, or HTTP endpoints.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Direct downstream consumers:

- [tba-codec-cid](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-cid/README.md)
- [tba-protocol-ucan](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-ucan/README.md)
- [tba-protocol-zcap](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-zcap/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/03-codecs/tba-codec-multibase)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-multibase/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-multibase/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-multibase/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-codec-multibase/)

## Governance

`tba-codec-multibase` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `03-codecs` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

Check that the build produces a wheel with the package version declared in `pyproject.toml`.
