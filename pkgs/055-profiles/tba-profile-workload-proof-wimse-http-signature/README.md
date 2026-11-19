# tba-profile-workload-proof-wimse-http-signature

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-proof-wimse-http-signature/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-proof-wimse-http-signature/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-profile-workload-proof-wimse-http-signature%3D%3D0.4.0.dev3/pkgs/055-profiles/tba-profile-workload-proof-wimse-http-signature/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-profile-workload-proof-wimse-http-signature%3D%3D0.4.0.dev3/pkgs/055-profiles/tba-profile-workload-proof-wimse-http-signature/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/055-profiles"><img alt="Layer: 055 profiles" src="https://img.shields.io/badge/Layer-055%20profiles-0a7f5a"></a>
<a href="https://pypi.org/project/tba-profile-workload-proof-wimse-http-signature/"><img alt="PyPI version for tba-profile-workload-proof-wimse-http-signature" src="https://img.shields.io/pypi/v/tba-profile-workload-proof-wimse-http-signature?label=tba-profile-workload-proof-wimse-http-signature%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-profile-workload-proof-wimse-http-signature"><img alt="Monthly PyPI downloads for tba-profile-workload-proof-wimse-http-signature" src="https://static.pepy.tech/badge/tba-profile-workload-proof-wimse-http-signature/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-proof-wimse-http-signature/README.md"><img alt="README hits for tba-profile-workload-proof-wimse-http-signature" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-proof-wimse-http-signature/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-proof-wimse-http-signature/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
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

## AEO Summary

- Package: `tba-profile-workload-proof-wimse-http-signature`
- Layer: `055-profiles`
- Responsibility: WIMSE draft-08 HTTP request proof profile.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-proof-wimse-http-signature/src/tba_profile_workload_proof_wimse_http_signature/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-profile-workload-proof-wimse-http-signature` for this responsibility: WIMSE draft-08 HTTP request proof profile. Its `055-profiles` placement keeps focused protocol and credential profiles separate from a universal deployment or implicit trust-policy selection.

## Installation

Install the selected PyPI release of `tba-profile-workload-proof-wimse-http-signature`:

```bash
uv pip install tba-profile-workload-proof-wimse-http-signature
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/055-profiles/tba-profile-workload-proof-wimse-http-signature
```

## Quick start

Build the package from the repository root.

```bash
uv build --wheel pkgs/055-profiles/tba-profile-workload-proof-wimse-http-signature
```

## Usage

The following public-entry-point example belongs to `tba-profile-workload-proof-wimse-http-signature`. WIMSE draft-08 HTTP request proof profile. Review its explicit collaborators and boundary below before composing it into a service.

```python
import tba_profile_workload_proof_wimse_http_signature

print(tba_profile_workload_proof_wimse_http_signature.__name__)
```

## Package Boundary

`tba-profile-workload-proof-wimse-http-signature` belongs to `055-profiles` and owns focused protocol and credential profiles: WIMSE draft-08 HTTP request proof profile.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-proof-wimse-http-signature/src/tba_profile_workload_proof_wimse_http_signature/__init__.py). Public exports include `authenticate_signature`, `sign_request`.

Keep a universal deployment or implicit trust-policy selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-profile-workload-proof-wimse-http-signature`:

- `sign_request` construction inputs: `extra_headers`, `authority`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-proof-wimse-http-signature/src/tba_profile_workload_proof_wimse_http_signature/request.py).
- `authenticate_signature` construction inputs: `method`, `path`, `audience`, `trust_by_domain`, `now`, `replay_store`, `verify_credential`, `authority`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-proof-wimse-http-signature/src/tba_profile_workload_proof_wimse_http_signature/request.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-profile-workload-proof-wimse-http-signature` exposes focused protocol and credential profiles. Public operations found in its source:

- `sign_request` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-proof-wimse-http-signature/src/tba_profile_workload_proof_wimse_http_signature/request.py).
- `authenticate_signature` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-proof-wimse-http-signature/src/tba_profile_workload_proof_wimse_http_signature/request.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-profile-workload-proof-wimse-http-signature`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`tba-profile-workload-proof-wimse-http-signature` does not take ownership of a universal deployment or implicit trust-policy selection.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-profile-workload-credential-wimse-wit](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/README.md)
- [tba-provider-jose-cryptography](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-jose-cryptography/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/055-profiles/tba-profile-workload-proof-wimse-http-signature)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-proof-wimse-http-signature/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-proof-wimse-http-signature/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-proof-wimse-http-signature/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-profile-workload-proof-wimse-http-signature/)

## Governance

`tba-profile-workload-proof-wimse-http-signature` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `055-profiles` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

Check that the build produces a wheel with the package version declared in `pyproject.toml`.
