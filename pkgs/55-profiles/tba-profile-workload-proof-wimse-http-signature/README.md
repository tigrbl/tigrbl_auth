# tba-profile-workload-proof-wimse-http-signature

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-proof-wimse-http-signature/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-proof-wimse-http-signature/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-proof-wimse-http-signature/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/55-profiles"><img alt="Layer: 55 profiles" src="https://img.shields.io/badge/Layer-55%20profiles-0a7f5a"></a>
<a href="https://pypi.org/project/tba-profile-workload-proof-wimse-http-signature/"><img alt="PyPI version for tba-profile-workload-proof-wimse-http-signature" src="https://img.shields.io/pypi/v/tba-profile-workload-proof-wimse-http-signature?label=tba-profile-workload-proof-wimse-http-signature%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-profile-workload-proof-wimse-http-signature"><img alt="Monthly PyPI downloads for tba-profile-workload-proof-wimse-http-signature" src="https://static.pepy.tech/badge/tba-profile-workload-proof-wimse-http-signature/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-proof-wimse-http-signature/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

The [WIMSE HTTP Signature draft-08](https://www.ietf.org/archive/id/draft-ietf-wimse-http-signature-08.html#section-3)
request profile uses a Workload Identity Token (WIT) and an RFC 9421 signature.
Import `sign_request` and `authenticate_signature` from
`tba_profile_workload_proof_wimse_http_signature`.

`sign_request` signs the method, path, query and applicable headers, including
`Txn-Token` when supplied in `extra_headers`. Use the workload private key
corresponding to the WIT's `cnf.jwk`. `authenticate_signature` validates the
WIT against configured trust-domain anchors, verifies the message signature
and checks nonce reuse using the supplied replay store. It returns the
authenticated workload subject. Transaction authorization and HTTPS are
provided by the caller and receiver.

This implementation supports a single tagged signature on bodyless GET and
POST requests with Ed25519 or P-256 keys. Requests with bodies, CONNECT,
signed responses, and general RFC 9421 parsing are outside its scope.

## Quick start

Build the package from the repository root.

```bash
uv build --wheel pkgs/55-profiles/tba-profile-workload-proof-wimse-http-signature
```

## Verification

Check that the build produces a wheel with the package version declared in `pyproject.toml`.
