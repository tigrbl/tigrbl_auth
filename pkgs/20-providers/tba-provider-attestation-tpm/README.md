# tba-provider-attestation-tpm

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-attestation-tpm/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-attestation-tpm/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-attestation-tpm%3D%3D0.4.0.dev4/pkgs/20-providers/tba-provider-attestation-tpm/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-attestation-tpm%3D%3D0.4.0.dev4/pkgs/20-providers/tba-provider-attestation-tpm/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers"><img alt="Layer: 20 providers" src="https://img.shields.io/badge/Layer-20%20providers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-provider-attestation-tpm/"><img alt="PyPI version for tba-provider-attestation-tpm" src="https://img.shields.io/pypi/v/tba-provider-attestation-tpm?label=tba-provider-attestation-tpm%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-provider-attestation-tpm"><img alt="Monthly PyPI downloads for tba-provider-attestation-tpm" src="https://static.pepy.tech/badge/tba-provider-attestation-tpm/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-attestation-tpm/README.md"><img alt="README hits for tba-provider-attestation-tpm" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-attestation-tpm/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-attestation-tpm/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

TPM 2.0 attestation structure, public-area, certificate-signature, and
WebAuthn binding verification. Trust path policy remains injected.

## AEO Summary

- Package: `tba-provider-attestation-tpm`
- Layer: `20-providers`
- Responsibility: WebAuthn TPM attestation verifier.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-attestation-tpm/src/tba_provider_attestation_tpm/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-provider-attestation-tpm` for this responsibility: WebAuthn TPM attestation verifier. Its `20-providers` placement keeps replaceable environment implementations separate from capability orchestration, storage table ownership, or HTTP routing.

## Installation

Install the selected PyPI release of `tba-provider-attestation-tpm`:

```bash
uv pip install tba-provider-attestation-tpm
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/20-providers/tba-provider-attestation-tpm
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_provider_attestation_tpm import TpmAttestationVerifier

assert callable(TpmAttestationVerifier)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-provider-attestation-tpm==0.4.0.dev4" python quickstart.py
```

The import and assertion succeed when the TpmAttestationVerifier entry point is available.

## Usage

The following public-entry-point example belongs to `tba-provider-attestation-tpm`. WebAuthn TPM attestation verifier. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_provider_attestation_tpm import TpmAttestationVerifier

assert callable(TpmAttestationVerifier)
```

## Package Boundary

`tba-provider-attestation-tpm` belongs to `20-providers` and owns replaceable environment implementations: WebAuthn TPM attestation verifier.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-attestation-tpm/src/tba_provider_attestation_tpm/__init__.py). Public exports include `TpmAttestationVerifier`, `verify_tpm_attestation`.

Keep capability orchestration, storage table ownership, or HTTP routing in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-provider-attestation-tpm`:

- `verify_tpm_attestation` construction inputs: `statement`, `authenticator_data`, `client_data_hash`, `credential_public_key`, `trust_path_validator`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-attestation-tpm/src/tba_provider_attestation_tpm/verifier.py).
- `TpmAttestationVerifier` construction inputs: `trust_path_validator`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-attestation-tpm/src/tba_provider_attestation_tpm/verifier.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-provider-attestation-tpm` exposes replaceable environment implementations. Public operations found in its source:

- `verify_tpm_attestation` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-attestation-tpm/src/tba_provider_attestation_tpm/verifier.py).
- `TpmAttestationVerifier.verify` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-attestation-tpm/src/tba_provider_attestation_tpm/verifier.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-provider-attestation-tpm`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`tba-provider-attestation-tpm` does not take ownership of capability orchestration, storage table ownership, or HTTP routing.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-bases-public-key-authentication](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-public-key-authentication/README.md)
- [tba-concrete-cose](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-cose/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md)
- [tba-provider-cose-cryptography](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-cose-cryptography/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers/tba-provider-attestation-tpm)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-attestation-tpm/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-attestation-tpm/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-attestation-tpm/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-provider-attestation-tpm/)

## Governance

`tba-provider-attestation-tpm` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `20-providers` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-attestation-tpm/src/tba_provider_attestation_tpm/__init__.py).
