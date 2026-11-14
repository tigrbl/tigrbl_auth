# tba-primitives-identity

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/00-primitives/tba-primitives-identity/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/00-primitives/tba-primitives-identity/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/00-primitives/tba-primitives-identity/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/00-primitives"><img alt="Layer: 00 primitives" src="https://img.shields.io/badge/Layer-00%20primitives-0a7f5a"></a>
<a href="https://pypi.org/project/tba-primitives-identity/"><img alt="PyPI version for tba-primitives-identity" src="https://img.shields.io/pypi/v/tba-primitives-identity?label=tba-primitives-identity%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-primitives-identity"><img alt="Monthly PyPI downloads for tba-primitives-identity" src="https://static.pepy.tech/badge/tba-primitives-identity/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/00-primitives/tba-primitives-identity/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Encode and normalize shared identity values without pulling in a server stack.

## Quick start

Install the version used by this example.

```bash
python -m pip install "tba-primitives-identity==0.4.0.dev2"
```

Save the following as `quickstart.py` and run `python quickstart.py`. The assertions should pass.

```python
from tba_primitives_identity import base64url_decode, base64url_encode

encoded = base64url_encode(b"tba")
assert encoded == "dGJh"
assert base64url_decode(encoded) == b"tba"
```

## When to use it

Use these helpers for shared wire values such as base64url, digests, and nonces. The deterministic JSON helpers continue to produce the bytes used by existing policy hashes and key thumbprints.

For strict RFC 8785 canonicalization, use [tba-codec-jcs](../../03-codecs/tba-codec-jcs/README.md). The legacy `canonicalize` and `canonicalize_json` imports remain available and emit a `DeprecationWarning` when called. The legacy `tba_primitives_identity.rfc8785` module also warns when imported.

## Verification

See the [related repository tests](https://github.com/tigrbl/tigrbl_auth/blob/master/tests/unit/test_identity_package_split_imports.py) for the implementation scope covered by this example.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [tba-contracts-identity-document](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/02-contracts/tba-contracts-identity-document#readme) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)
