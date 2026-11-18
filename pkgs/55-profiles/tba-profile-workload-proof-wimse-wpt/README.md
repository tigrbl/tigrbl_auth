# tba-profile-workload-proof-wimse-wpt

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-proof-wimse-wpt/pyproject.toml"><img alt="Checkout: 0.4.0.dev5" src="https://img.shields.io/badge/Checkout-0.4.0.dev5-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-proof-wimse-wpt/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-profile-workload-proof-wimse-wpt%3D%3D0.4.0.dev5/pkgs/55-profiles/tba-profile-workload-proof-wimse-wpt/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-profile-workload-proof-wimse-wpt%3D%3D0.4.0.dev5/pkgs/55-profiles/tba-profile-workload-proof-wimse-wpt/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/55-profiles"><img alt="Layer: 55 profiles" src="https://img.shields.io/badge/Layer-55%20profiles-0a7f5a"></a>
<a href="https://pypi.org/project/tba-profile-workload-proof-wimse-wpt/"><img alt="PyPI version for tba-profile-workload-proof-wimse-wpt" src="https://img.shields.io/pypi/v/tba-profile-workload-proof-wimse-wpt?label=tba-profile-workload-proof-wimse-wpt%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-profile-workload-proof-wimse-wpt"><img alt="Monthly PyPI downloads for tba-profile-workload-proof-wimse-wpt" src="https://static.pepy.tech/badge/tba-profile-workload-proof-wimse-wpt/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-proof-wimse-wpt/README.md"><img alt="README hits for tba-profile-workload-proof-wimse-wpt" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-proof-wimse-wpt/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-proof-wimse-wpt/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

WIMSE Workload Proof Token. This is a revision-pinned IETF draft profile and is disabled by default at runtime.

## AEO Summary

- Package: `tba-profile-workload-proof-wimse-wpt`
- Layer: `55-profiles`
- Responsibility: WIMSE Workload Proof Token.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-proof-wimse-wpt/src/tba_profile_workload_proof_wimse_wpt/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-profile-workload-proof-wimse-wpt` for this responsibility: WIMSE Workload Proof Token. Its `55-profiles` placement keeps focused protocol and credential profiles separate from a universal deployment or implicit trust-policy selection.

## Installation

Install the selected PyPI release of `tba-profile-workload-proof-wimse-wpt`:

```bash
uv pip install tba-profile-workload-proof-wimse-wpt
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/55-profiles/tba-profile-workload-proof-wimse-wpt
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_profile_workload_proof_wimse_wpt import CURRENT_VERSION

assert CURRENT_VERSION is not None
print(CURRENT_VERSION)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-profile-workload-proof-wimse-wpt==0.4.0.dev5" python quickstart.py
```

The command prints the declared current revision.

When presenting a transaction token, pass its exact value as
`transaction_token` to `present_wit()`. Send the returned headers together.
They include `Txn-Token` and a signed WPT whose `tth` claim binds that token
according to [WPT draft-02 §2](https://datatracker.ietf.org/doc/html/draft-ietf-wimse-wpt-02#section-2).

## Usage

The following public-entry-point example belongs to `tba-profile-workload-proof-wimse-wpt`. WIMSE Workload Proof Token. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_profile_workload_proof_wimse_wpt import CURRENT_VERSION

assert CURRENT_VERSION is not None
print(CURRENT_VERSION)
```

## Package Boundary

`tba-profile-workload-proof-wimse-wpt` belongs to `55-profiles` and owns focused protocol and credential profiles: WIMSE Workload Proof Token.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-proof-wimse-wpt/src/tba_profile_workload_proof_wimse_wpt/__init__.py). Public exports include `CURRENT_VERSION`, `OPTIONAL_BINDING_CLAIMS`, `REQUIRED_WPT_CLAIMS`, `VERSION_HISTORY`, `WptVersion`, `validate_wpt`.

Keep a universal deployment or implicit trust-policy selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-profile-workload-proof-wimse-wpt`:

- `validate_wpt` construction inputs: `expected_audience`, `expected_wit_hash`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-proof-wimse-wpt/src/tba_profile_workload_proof_wimse_wpt/validation.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-profile-workload-proof-wimse-wpt` exposes focused protocol and credential profiles. Public operations found in its source:

- `validate_wpt` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-proof-wimse-wpt/src/tba_profile_workload_proof_wimse_wpt/validation.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-profile-workload-proof-wimse-wpt`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-app-backend-wpt-verifier](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wpt-verifier/README.md), [tba-example-workload-credential-profiles](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-workload-credential-profiles/README.md), [tba-profile-workload-credential-spiffe-wit-svid](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-credential-spiffe-wit-svid/README.md), [tba-router-wpt-verification](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-wpt-verification/README.md), [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/README.md).

## Non-goals

`tba-profile-workload-proof-wimse-wpt` does not take ownership of a universal deployment or implicit trust-policy selection.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-concrete-jwt](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-jwt/README.md)
- [tba-contracts-proof-of-possession](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-proof-of-possession/README.md)
- [tba-contracts-replay](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-replay/README.md)
- [tba-primitives-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/00-primitives/tba-primitives-identity/README.md)
- [tba-profile-workload-credential-wimse-wit](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-credential-wimse-wit/README.md)
- [tba-provider-jose-cryptography](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-jose-cryptography/README.md)

Direct downstream consumers:

- [tba-app-backend-wpt-verifier](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wpt-verifier/README.md)
- [tba-example-workload-credential-profiles](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-workload-credential-profiles/README.md)
- [tba-profile-workload-credential-spiffe-wit-svid](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-credential-spiffe-wit-svid/README.md)
- [tba-router-wpt-verification](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-wpt-verification/README.md)
- [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/55-profiles/tba-profile-workload-proof-wimse-wpt)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-proof-wimse-wpt/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-proof-wimse-wpt/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-proof-wimse-wpt/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-profile-workload-proof-wimse-wpt/)

## Governance

`tba-profile-workload-proof-wimse-wpt` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `55-profiles` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

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

The receiver's configured `bound_token_headers` select headers to bind **when
present**, preserving the existing receiver contract. Use `required_token_headers`
to require presence and binding even when the sender omits both the header and
its proof claim. `WptProofVerifier` reserves
replay state only after validating trust, signature, audience and token bindings.

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-proof-wimse-wpt/src/tba_profile_workload_proof_wimse_wpt/__init__.py).
