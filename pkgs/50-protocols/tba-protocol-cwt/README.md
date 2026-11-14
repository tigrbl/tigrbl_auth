# tba-protocol-cwt

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-cwt/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-cwt/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/50-protocols"><img alt="Layer: 50 protocols" src="https://img.shields.io/badge/Layer-50%20protocols-0a7f5a"></a>
<a href="https://pypi.org/project/tba-protocol-cwt/"><img alt="PyPI version for tba-protocol-cwt" src="https://img.shields.io/pypi/v/tba-protocol-cwt?label=tba-protocol-cwt%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-protocol-cwt"><img alt="Monthly PyPI downloads for tba-protocol-cwt" src="https://static.pepy.tech/badge/tba-protocol-cwt/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-cwt/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Compose typed claims into a CBOR Web Token claims set using the RFC 8392 registry.

## Quick start

Install the version used by this example.

```bash
python -m pip install "tba-protocol-cwt==0.4.0.dev3"
```

Save the following as `quickstart.py` and run `python quickstart.py`. The assertions should pass.

```python
from tba_concrete_claim_issuer import IssuerClaim
from tba_protocol_cwt import build_cwt_claims, cwt_label_for

issuer = IssuerClaim("https://issuer.example")
assert cwt_label_for(issuer) == 1
encoded = build_cwt_claims(issuer).encode()
assert encoded.startswith(b"\xa1\x01")
```

See the [protocol source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/50-protocols/tba-protocol-cwt/src/tba_protocol_cwt) for version history, carriers, and claim bindings.

## When to use it

This package maps registered claims to integer labels. Draft `actx` and `ath` remain text keys. `build_cwt_claims` accepts explicit `actx_field_labels` and represents `ath` as a SHA-256 digest. Use a COSE provider for signing and verification and a DPoP verifier for proof validation.

## Verification

See the [related repository tests](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-jose/tests/unit/test_cwt_standalone_claim_packages.py) for the implementation scope covered by this example.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)
