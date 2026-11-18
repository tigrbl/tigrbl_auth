# tba-profile-workload-proof-wimse-wpt

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-proof-wimse-wpt/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-proof-wimse-wpt/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/55-profiles"><img alt="Layer: 55 profiles" src="https://img.shields.io/badge/Layer-55%20profiles-0a7f5a"></a>
<a href="https://pypi.org/project/tba-profile-workload-proof-wimse-wpt/"><img alt="PyPI version for tba-profile-workload-proof-wimse-wpt" src="https://img.shields.io/pypi/v/tba-profile-workload-proof-wimse-wpt?label=tba-profile-workload-proof-wimse-wpt%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-profile-workload-proof-wimse-wpt"><img alt="Monthly PyPI downloads for tba-profile-workload-proof-wimse-wpt" src="https://static.pepy.tech/badge/tba-profile-workload-proof-wimse-wpt/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-proof-wimse-wpt/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

WIMSE Workload Proof Token. This is a revision-pinned IETF draft profile and is disabled by default at runtime.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_profile_workload_proof_wimse_wpt import CURRENT_VERSION

assert CURRENT_VERSION is not None
print(CURRENT_VERSION)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-profile-workload-proof-wimse-wpt==0.4.0.dev2" python quickstart.py
```

The command prints the declared current revision.

When presenting a transaction token, pass its exact value as
`transaction_token` to `present_wit()`. Send the returned headers together.
They include `Txn-Token` and a signed WPT whose `tth` claim binds that token
according to [WPT draft-02 §2](https://datatracker.ietf.org/doc/html/draft-ietf-wimse-wpt-02#section-2).

## Verification

`issue_wpt(signer, wit, workload_key_reference=..., audience=..., now=...)`
returns a compact signed WPT without HTTP headers. It generates a fresh `jti`,
binds the exact WIT, checks that the signing key matches the WIT's confirmation
key, and caps expiry at the earlier of the requested lifetime and WIT expiry.
WPT lifetime is limited to 1–300 seconds. The recipient authenticates the WIT issuer.

`WptProofIssuer(signer, wit, workload_key_reference=...).issue(context)`
implements `PossessionProofIssuerPort` and returns a `PossessionProof` with
its populated credential digest, proof ID, expiry, and bound context.
`context` is a `PossessionProofContext` with `audience` or `target_uri`.
Conflicting audiences, a different WIT digest, and requested HTTP method binding
are rejected. This WPT profile binds audience, not HTTP method. Audiences follow
the pinned HTTP profile: absolute HTTP(S) URIs normalized without query or fragment.

For additional bindings, supply lowercase header names and SHA-256 base64url
digests through `accompanying_token_digests`. `txn-token` becomes `tth`; other
tokens become `oth`. `present_wit()` retains its HTTP headers interface and
delegates signing to `issue_wpt()`. `normalize_wpt_audience()` exposes the shared
audience normalization used by issuers and remote-verifier configuration.

The receiver's configured `bound_token_headers` are required even when the
sender omits both the header and its proof claim. `WptProofVerifier` reserves
replay state only after validating trust, signature, audience and token bindings.

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-proof-wimse-wpt/src/tba_profile_workload_proof_wimse_wpt/__init__.py).
