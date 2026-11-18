# tba-provider-cose-cryptography

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-cose-cryptography/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-cose-cryptography/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-cose-cryptography%3D%3D0.4.0.dev3/pkgs/20-providers/tba-provider-cose-cryptography/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-cose-cryptography%3D%3D0.4.0.dev3/pkgs/20-providers/tba-provider-cose-cryptography/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers"><img alt="Layer: 20 providers" src="https://img.shields.io/badge/Layer-20%20providers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-provider-cose-cryptography/"><img alt="PyPI version for tba-provider-cose-cryptography" src="https://img.shields.io/pypi/v/tba-provider-cose-cryptography?label=tba-provider-cose-cryptography%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-provider-cose-cryptography"><img alt="Monthly PyPI downloads for tba-provider-cose-cryptography" src="https://static.pepy.tech/badge/tba-provider-cose-cryptography/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-cose-cryptography/README.md"><img alt="README hits for tba-provider-cose-cryptography" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-cose-cryptography/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-cose-cryptography/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

COSE public-key loading and signature verification implemented with cryptography.

## AEO Summary

- Package: `tba-provider-cose-cryptography`
- Layer: `20-providers`
- Responsibility: Cryptography-backed COSE key and signature provider.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-cose-cryptography/src/tba_provider_cose_cryptography/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-provider-cose-cryptography` for this responsibility: Cryptography-backed COSE key and signature provider. Its `20-providers` placement keeps replaceable environment implementations separate from capability orchestration, storage table ownership, or HTTP routing.

## Installation

Install the selected PyPI release of `tba-provider-cose-cryptography`:

```bash
uv pip install tba-provider-cose-cryptography
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/20-providers/tba-provider-cose-cryptography
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_provider_cose_cryptography import CoseSign1CryptographyProvider

assert callable(CoseSign1CryptographyProvider)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-provider-cose-cryptography==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the CoseSign1CryptographyProvider entry point is available.

## Usage

The following public-entry-point example belongs to `tba-provider-cose-cryptography`. Cryptography-backed COSE key and signature provider. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_provider_cose_cryptography import CoseSign1CryptographyProvider

assert callable(CoseSign1CryptographyProvider)
```

## Package Boundary

`tba-provider-cose-cryptography` belongs to `20-providers` and owns replaceable environment implementations: Cryptography-backed COSE key and signature provider.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-cose-cryptography/src/tba_provider_cose_cryptography/__init__.py). Public exports include `CoseSign1CryptographyProvider`, `load_cose_public_key`, `sign_detached_signature`, `verify_detached_signature`.

Keep capability orchestration, storage table ownership, or HTTP routing in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-provider-cose-cryptography`:

- `CoseSign1CryptographyProvider` construction inputs: `private_keys`, `public_keys`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-cose-cryptography/src/tba_provider_cose_cryptography/provider.py).
- `verify_detached_signature` construction inputs: `algorithm`, `public_key`, `signing_input`, `message`, `signature`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-cose-cryptography/src/tba_provider_cose_cryptography/signatures.py).
- `sign_detached_signature` construction inputs: `algorithm`, `private_key`, `signing_input`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-cose-cryptography/src/tba_provider_cose_cryptography/signing.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-provider-cose-cryptography` exposes replaceable environment implementations. Public operations found in its source:

- `load_cose_public_key` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-cose-cryptography/src/tba_provider_cose_cryptography/keys.py).
- `CoseSign1CryptographyProvider.protect` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-cose-cryptography/src/tba_provider_cose_cryptography/provider.py).
- `CoseSign1CryptographyProvider.verify` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-cose-cryptography/src/tba_provider_cose_cryptography/provider.py).
- `verify_detached_signature` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-cose-cryptography/src/tba_provider_cose_cryptography/signatures.py).
- `sign_detached_signature` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-cose-cryptography/src/tba_provider_cose_cryptography/signing.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

The following layer-50 manifests directly depend on `tba-provider-cose-cryptography`:

- [tba-protocol-webauthn](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-webauthn/README.md)

Other direct consumers include [tba-provider-attestation-packed](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-attestation-packed/README.md), [tba-provider-attestation-tpm](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-attestation-tpm/README.md), [tba-provider-attestation-u2f](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-attestation-u2f/README.md).

## Non-goals

`tba-provider-cose-cryptography` does not take ownership of capability orchestration, storage table ownership, or HTTP routing.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-bases-cose](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-cose/README.md)
- [tba-concrete-cose](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-cose/README.md)

Direct downstream consumers:

- [tba-protocol-webauthn](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-webauthn/README.md)
- [tba-provider-attestation-packed](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-attestation-packed/README.md)
- [tba-provider-attestation-tpm](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-attestation-tpm/README.md)
- [tba-provider-attestation-u2f](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-attestation-u2f/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers/tba-provider-cose-cryptography)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-cose-cryptography/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-cose-cryptography/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-cose-cryptography/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-provider-cose-cryptography/)

## Governance

`tba-provider-cose-cryptography` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `20-providers` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-cose-cryptography/src/tba_provider_cose_cryptography/__init__.py).
