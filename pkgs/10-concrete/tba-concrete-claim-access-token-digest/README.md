# tba-concrete-claim-access-token-digest

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-claim-access-token-digest/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-claim-access-token-digest/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/10-concrete"><img alt="Layer: 10 concrete" src="https://img.shields.io/badge/Layer-10%20concrete-0a7f5a"></a>
<a href="https://pypi.org/project/tba-concrete-claim-access-token-digest/"><img alt="PyPI version for tba-concrete-claim-access-token-digest" src="https://img.shields.io/pypi/v/tba-concrete-claim-access-token-digest?label=tba-concrete-claim-access-token-digest%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-concrete-claim-access-token-digest"><img alt="Monthly PyPI downloads for tba-concrete-claim-access-token-digest" src="https://static.pepy.tech/badge/tba-concrete-claim-access-token-digest/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-claim-access-token-digest/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Owns the standalone RFC 9449 `ath` claim object. Protocol packages compose it
into versioned claim sets; this package does not own DPoP request processing.

`to_cwt_value()` validates canonical base64url SHA-256 and returns 32 raw
bytes. `from_cwt_value()` converts the CBOR byte string back to the textual
claim. Existing textual claim construction remains compatible. CWT usage is
based on draft-nandakumar-moq-generic-dpop-proof-00; use text key `ath`
until a numeric label is assigned.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_concrete_claim_access_token_digest import AccessTokenDigestClaim

claim = AccessTokenDigestClaim('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
assert claim.name == 'ath'
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-concrete-claim-access-token-digest==0.4.0.dev3" python quickstart.py
```

The example constructs a claim named `ath`.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-claim-access-token-digest/src/tba_concrete_claim_access_token_digest/__init__.py).
