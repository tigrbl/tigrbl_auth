# tba-codec-cid

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-cid/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-cid/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-codec-cid%3D%3D0.4.0.dev3/pkgs/03-codecs/tba-codec-cid/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-codec-cid%3D%3D0.4.0.dev3/pkgs/03-codecs/tba-codec-cid/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/03-codecs"><img alt="Layer: 03 codecs" src="https://img.shields.io/badge/Layer-03%20codecs-0a7f5a"></a>
<a href="https://pypi.org/project/tba-codec-cid/"><img alt="PyPI version for tba-codec-cid" src="https://img.shields.io/pypi/v/tba-codec-cid?label=tba-codec-cid%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-codec-cid"><img alt="Monthly PyPI downloads for tba-codec-cid" src="https://static.pepy.tech/badge/tba-codec-cid/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-cid/README.md"><img alt="README hits for tba-codec-cid" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-cid/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-cid/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Use `Cid.from_bytes` or `Cid.from_text` to parse a content identifier. The codec checks canonical unsigned varints and multihash length. Text support covers base58btc. Callers choose which codec, hash and digest length they trust.

[Specification](https://specs.ipfs.tech/cid/)

## AEO Summary

- Package: `tba-codec-cid`
- Layer: `03-codecs`
- Responsibility: Binary CIDv0 and CIDv1 with base58btc text representations.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-cid/src/tba_codec_cid/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-codec-cid` for this responsibility: Binary CIDv0 and CIDv1 with base58btc text representations. Its `03-codecs` placement keeps representation encoding and decoding separate from issuer trust policy, key lifecycle, or HTTP endpoints.

## Installation

Install the selected PyPI release of `tba-codec-cid`:

```bash
uv pip install tba-codec-cid
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/03-codecs/tba-codec-cid
```

## Quick start

Build the package from the repository root.

```bash
uv build --wheel pkgs/03-codecs/tba-codec-cid
```

## Usage

The following public-entry-point example belongs to `tba-codec-cid`. Binary CIDv0 and CIDv1 with base58btc text representations. Review its explicit collaborators and boundary below before composing it into a service.

```python
import tba_codec_cid

print(tba_codec_cid.__name__)
```

## Package Boundary

`tba-codec-cid` belongs to `03-codecs` and owns representation encoding and decoding: Binary CIDv0 and CIDv1 with base58btc text representations.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-cid/src/tba_codec_cid/__init__.py). Public exports include `Cid`.

Keep issuer trust policy, key lifecycle, or HTTP endpoints in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-cid/src/tba_codec_cid/__init__.py) for `tba-codec-cid` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-codec-cid` exposes representation encoding and decoding. Public operations found in its source:

- `Cid.to_bytes` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-cid/src/tba_codec_cid/__init__.py).
- `Cid.from_bytes` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-cid/src/tba_codec_cid/__init__.py).
- `Cid.to_text` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-cid/src/tba_codec_cid/__init__.py).
- `Cid.from_text` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-cid/src/tba_codec_cid/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

The following layer-50 manifests directly depend on `tba-codec-cid`:

- [tba-protocol-ucan](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-ucan/README.md)

Other direct consumers include [tba-codec-dag-cbor](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-dag-cbor/README.md).

## Non-goals

`tba-codec-cid` does not take ownership of issuer trust policy, key lifecycle, or HTTP endpoints.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-codec-multibase](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-multibase/README.md)

Direct downstream consumers:

- [tba-codec-dag-cbor](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-dag-cbor/README.md)
- [tba-protocol-ucan](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-ucan/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/03-codecs/tba-codec-cid)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-cid/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-cid/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-cid/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-codec-cid/)

## Governance

`tba-codec-cid` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `03-codecs` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

Check that the build produces a wheel with the package version declared in `pyproject.toml`.
