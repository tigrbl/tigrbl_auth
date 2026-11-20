# tba-codec-dag-cbor

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-codec-dag-cbor%3D%3D0.4.0.dev3/pkgs/003-codecs/tba-codec-dag-cbor/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-codec-dag-cbor%3D%3D0.4.0.dev3/pkgs/003-codecs/tba-codec-dag-cbor/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/003-codecs"><img alt="Layer: 003 codecs" src="https://img.shields.io/badge/Layer-003%20codecs-0a7f5a"></a>
<a href="https://pypi.org/project/tba-codec-dag-cbor/"><img alt="PyPI version for tba-codec-dag-cbor" src="https://img.shields.io/pypi/v/tba-codec-dag-cbor?label=tba-codec-dag-cbor%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-codec-dag-cbor"><img alt="Monthly PyPI downloads for tba-codec-dag-cbor" src="https://static.pepy.tech/badge/tba-codec-dag-cbor/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/README.md"><img alt="README hits for tba-codec-dag-cbor" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Use `encode` and `decode` for canonical DAG-CBOR. CID links use tag 42 and the binary identity prefix. Decoding rejects duplicate keys, trailing data and noncanonical encodings. Callers set message size limits and protocol constraints.

[Specification](https://ipld.io/specs/codecs/dag-cbor/spec/)

## AEO Summary

- Package: `tba-codec-dag-cbor`
- Layer: `003-codecs`
- Responsibility: Strict canonical DAG-CBOR with IPLD CID links.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/src/tba_codec_dag_cbor/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-codec-dag-cbor` for this responsibility: Strict canonical DAG-CBOR with IPLD CID links. Its `003-codecs` placement keeps representation encoding and decoding separate from issuer trust policy, key lifecycle, or HTTP endpoints.

## Installation

Install the selected PyPI release of `tba-codec-dag-cbor`:

```bash
uv pip install tba-codec-dag-cbor
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/003-codecs/tba-codec-dag-cbor
```

## Quick start

Build the package from the repository root.

```bash
uv build --wheel pkgs/003-codecs/tba-codec-dag-cbor
```

## Usage

The following public-entry-point example belongs to `tba-codec-dag-cbor`. Strict canonical DAG-CBOR with IPLD CID links. Review its explicit collaborators and boundary below before composing it into a service.

```python
import tba_codec_dag_cbor

print(tba_codec_dag_cbor.__name__)
```

## Package Boundary

`tba-codec-dag-cbor` belongs to `003-codecs` and owns representation encoding and decoding: Strict canonical DAG-CBOR with IPLD CID links.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/src/tba_codec_dag_cbor/__init__.py). Public exports include `CBORTag`, `cid_link`, `decode`, `encode`, `link_cid`.

Keep issuer trust policy, key lifecycle, or HTTP endpoints in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-codec-dag-cbor`:

- `encode` construction inputs: `max_depth`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/src/tba_codec_dag_cbor/__init__.py).
- `decode` construction inputs: `max_depth`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/src/tba_codec_dag_cbor/__init__.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-codec-dag-cbor` exposes representation encoding and decoding. Public operations found in its source:

- `cid_link` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/src/tba_codec_dag_cbor/__init__.py).
- `link_cid` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/src/tba_codec_dag_cbor/__init__.py).
- `encode` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/src/tba_codec_dag_cbor/__init__.py).
- `decode` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/src/tba_codec_dag_cbor/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

The following layer-50 manifests directly depend on `tba-codec-dag-cbor`:

- [tba-protocol-ucan](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/README.md)

## Non-goals

`tba-codec-dag-cbor` does not take ownership of issuer trust policy, key lifecycle, or HTTP endpoints.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-codec-cid](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-cid/README.md)

Direct downstream consumers:

- [tba-protocol-ucan](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-ucan/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/003-codecs/tba-codec-dag-cbor)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dag-cbor/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-codec-dag-cbor/)

## Governance

`tba-codec-dag-cbor` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `003-codecs` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

Check that the build produces a wheel with the package version declared in `pyproject.toml`.
