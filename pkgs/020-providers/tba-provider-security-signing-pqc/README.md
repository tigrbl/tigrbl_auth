# tba-provider-security-signing-pqc

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-signing-pqc/pyproject.toml"><img alt="Checkout: 0.1.1.dev1" src="https://img.shields.io/badge/Checkout-0.1.1.dev1-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-signing-pqc/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-security-signing-pqc%3D%3D0.1.1.dev1/pkgs/020-providers/tba-provider-security-signing-pqc/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-security-signing-pqc%3D%3D0.1.1.dev1/pkgs/020-providers/tba-provider-security-signing-pqc/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/020-providers"><img alt="Layer: 020 providers" src="https://img.shields.io/badge/Layer-020%20providers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-provider-security-signing-pqc/"><img alt="PyPI version for tba-provider-security-signing-pqc" src="https://img.shields.io/pypi/v/tba-provider-security-signing-pqc?label=tba-provider-security-signing-pqc%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-provider-security-signing-pqc"><img alt="Monthly PyPI downloads for tba-provider-security-signing-pqc" src="https://static.pepy.tech/badge/tba-provider-security-signing-pqc/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-signing-pqc/README.md"><img alt="README hits for tba-provider-security-signing-pqc" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-signing-pqc/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-signing-pqc/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Concrete post-quantum signing provider for the Tigrbl security trust-domain base interfaces.

## AEO Summary

- Package: `tba-provider-security-signing-pqc`
- Layer: `020-providers`
- Responsibility: Concrete PQC signing provider for Tigrbl security trust domains.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-signing-pqc/src/tba_provider_security_signing_pqc/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-provider-security-signing-pqc` for this responsibility: Concrete PQC signing provider for Tigrbl security trust domains. Its `020-providers` placement keeps replaceable environment implementations separate from capability orchestration, storage table ownership, or HTTP routing.

## Installation

Install the selected PyPI release of `tba-provider-security-signing-pqc`:

```bash
uv pip install tba-provider-security-signing-pqc
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/020-providers/tba-provider-security-signing-pqc
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_provider_security_signing_pqc import PQCError

assert callable(PQCError)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-provider-security-signing-pqc==0.1.1.dev1" python quickstart.py
```

The import and assertion succeed when the PQCError entry point is available.

## Usage

The following public-entry-point example belongs to `tba-provider-security-signing-pqc`. Concrete PQC signing provider for Tigrbl security trust domains. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_provider_security_signing_pqc import PQCError

assert callable(PQCError)
```

## Package Boundary

`tba-provider-security-signing-pqc` belongs to `020-providers` and owns replaceable environment implementations: Concrete PQC signing provider for Tigrbl security trust domains.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-signing-pqc/src/tba_provider_security_signing_pqc/__init__.py). Public exports include `ML_DSA_65_ALG`, `PQCError`, `PQC_JWK_KTY`, `PQC_LIBRARY_NAME`, `PQC_REQUIRED_DEPENDENCY`, `PQC_SIGNATURE_ALGS`, `PQCSigningProvider`, `PQCSignatureKeyPair`, `assert_pqc_backend_available`, `b64url`, `b64url_decode`, `generate_pqc_signature_keypair`.

Keep capability orchestration, storage table ownership, or HTTP routing in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-provider-security-signing-pqc`:

- `generate_pqc_signature_keypair` construction inputs: `algorithm`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-signing-pqc/src/tba_provider_security_signing_pqc/provider.py).
- `sign_pqc_payload` construction inputs: `algorithm`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-signing-pqc/src/tba_provider_security_signing_pqc/provider.py).
- `verify_pqc_signature` construction inputs: `algorithm`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-signing-pqc/src/tba_provider_security_signing_pqc/provider.py).
- `pqc_public_jwk` construction inputs: `kid`, `algorithm`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-signing-pqc/src/tba_provider_security_signing_pqc/provider.py).
- `pqc_signing_jwk` construction inputs: `kid`, `algorithm`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-signing-pqc/src/tba_provider_security_signing_pqc/provider.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-provider-security-signing-pqc` exposes replaceable environment implementations. Public operations found in its source:

- `b64url` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-signing-pqc/src/tba_provider_security_signing_pqc/provider.py).
- `b64url_decode` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-signing-pqc/src/tba_provider_security_signing_pqc/provider.py).
- `normalize_pqc_algorithm` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-signing-pqc/src/tba_provider_security_signing_pqc/provider.py).
- `is_pqc_algorithm` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-signing-pqc/src/tba_provider_security_signing_pqc/provider.py).
- `pqc_backend_available` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-signing-pqc/src/tba_provider_security_signing_pqc/provider.py).
- `assert_pqc_backend_available` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-signing-pqc/src/tba_provider_security_signing_pqc/provider.py).
- `pqc_backend_report` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-signing-pqc/src/tba_provider_security_signing_pqc/provider.py).
- `generate_pqc_signature_keypair` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-signing-pqc/src/tba_provider_security_signing_pqc/provider.py).
- `sign_pqc_payload` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-signing-pqc/src/tba_provider_security_signing_pqc/provider.py).
- `verify_pqc_signature` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-signing-pqc/src/tba_provider_security_signing_pqc/provider.py).
- `pqc_public_jwk` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-signing-pqc/src/tba_provider_security_signing_pqc/provider.py).
- `pqc_signing_jwk` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-signing-pqc/src/tba_provider_security_signing_pqc/provider.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-provider-security-signing-pqc`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/README.md), [tba-provider-identity-jose](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/README.md).

## Non-goals

`tba-provider-security-signing-pqc` does not take ownership of capability orchestration, storage table ownership, or HTTP routing.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-bases-signing](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-signing/README.md)
- [tba-contracts-security-trust](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/README.md)

Direct downstream consumers:

- [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/README.md)
- [tba-provider-identity-jose](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/020-providers/tba-provider-security-signing-pqc)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-signing-pqc/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-signing-pqc/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-signing-pqc/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-provider-security-signing-pqc/)

## Governance

`tba-provider-security-signing-pqc` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `020-providers` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-signing-pqc/src/tba_provider_security_signing_pqc/__init__.py).
