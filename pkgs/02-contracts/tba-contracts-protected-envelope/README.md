# tba-contracts-protected-envelope

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-protected-envelope/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-protected-envelope/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-contracts-protected-envelope%3D%3D0.4.0.dev4/pkgs/02-contracts/tba-contracts-protected-envelope/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-contracts-protected-envelope%3D%3D0.4.0.dev4/pkgs/02-contracts/tba-contracts-protected-envelope/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/02-contracts"><img alt="Layer: 02 contracts" src="https://img.shields.io/badge/Layer-02%20contracts-0a7f5a"></a>
<a href="https://pypi.org/project/tba-contracts-protected-envelope/"><img alt="PyPI version for tba-contracts-protected-envelope" src="https://img.shields.io/pypi/v/tba-contracts-protected-envelope?label=tba-contracts-protected-envelope%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-contracts-protected-envelope"><img alt="Monthly PyPI downloads for tba-contracts-protected-envelope" src="https://static.pepy.tech/badge/tba-contracts-protected-envelope/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-protected-envelope/README.md"><img alt="README hits for tba-contracts-protected-envelope" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-protected-envelope/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-protected-envelope/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Protocol-neutral signed and encrypted envelope contracts.

## AEO Summary

- Package: `tba-contracts-protected-envelope`
- Layer: `02-contracts`
- Responsibility: Protocol-neutral signed and encrypted envelope contracts.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-protected-envelope/src/tba_contracts_protected_envelope/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-contracts-protected-envelope` for this responsibility: Protocol-neutral signed and encrypted envelope contracts. Its `02-contracts` placement keeps shared types and structural ports separate from environment-specific service implementations or HTTP routing.

## Installation

Install the selected PyPI release of `tba-contracts-protected-envelope`:

```bash
uv pip install tba-contracts-protected-envelope
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/02-contracts/tba-contracts-protected-envelope
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_contracts_protected_envelope import EnvelopeProtectionRequest

assert callable(EnvelopeProtectionRequest)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-contracts-protected-envelope==0.4.0.dev4" python quickstart.py
```

The import and assertion succeed when the EnvelopeProtectionRequest entry point is available.

## Usage

The following public-entry-point example belongs to `tba-contracts-protected-envelope`. Protocol-neutral signed and encrypted envelope contracts. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_contracts_protected_envelope import EnvelopeProtectionRequest

assert callable(EnvelopeProtectionRequest)
```

## Package Boundary

`tba-contracts-protected-envelope` belongs to `02-contracts` and owns shared types and structural ports: Protocol-neutral signed and encrypted envelope contracts.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-protected-envelope/src/tba_contracts_protected_envelope/__init__.py). Public exports include `EnvelopeProtectionRequest`, `EnvelopeVerificationRequest`, `EnvelopeVerificationResult`, `ProtectedEnvelope`, `ProtectedEnvelopeIssuerPort`, `ProtectedEnvelopeVerifierPort`, `VerificationKeyRequest`, `VerificationKeyResolverPort`, `VerificationKeyResult`.

Keep environment-specific service implementations or HTTP routing in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-protected-envelope/src/tba_contracts_protected_envelope/__init__.py) for `tba-contracts-protected-envelope` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-contracts-protected-envelope` exposes shared types and structural ports. Public operations found in its source:

- `ProtectedEnvelopeIssuerPort.protect` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-protected-envelope/src/tba_contracts_protected_envelope/ports.py).
- `ProtectedEnvelopeVerifierPort.verify` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-protected-envelope/src/tba_contracts_protected_envelope/ports.py).
- `VerificationKeyResolverPort.resolve_verification_key` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-protected-envelope/src/tba_contracts_protected_envelope/ports.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

The following layer-50 manifests directly depend on `tba-contracts-protected-envelope`:

- [tba-protocol-jwt](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-jwt/README.md)
- [tba-protocol-security-cose](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-security-cose/README.md)
- [tba-protocol-security-jwe](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-security-jwe/README.md)
- [tba-protocol-security-jws](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-security-jws/README.md)

Other direct consumers include [tba-bases-protected-envelope](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-protected-envelope/README.md), [tba-capability-protected-envelope](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-protected-envelope/README.md), [tba-profile-credential-vc-jose-cose](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-vc-jose-cose/README.md), [tba-provider-jose-cryptography](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-jose-cryptography/README.md).

## Non-goals

`tba-contracts-protected-envelope` does not take ownership of environment-specific service implementations or HTTP routing.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-primitives-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/00-primitives/tba-primitives-identity/README.md)

Direct downstream consumers:

- [tba-bases-protected-envelope](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-protected-envelope/README.md)
- [tba-capability-protected-envelope](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-protected-envelope/README.md)
- [tba-profile-credential-vc-jose-cose](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-credential-vc-jose-cose/README.md)
- [tba-protocol-jwt](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-jwt/README.md)
- [tba-protocol-security-cose](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-security-cose/README.md)
- [tba-protocol-security-jwe](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-security-jwe/README.md)
- [tba-protocol-security-jws](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-security-jws/README.md)
- [tba-provider-jose-cryptography](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-jose-cryptography/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/02-contracts/tba-contracts-protected-envelope)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-protected-envelope/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-protected-envelope/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-protected-envelope/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-contracts-protected-envelope/)

## Governance

`tba-contracts-protected-envelope` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `02-contracts` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-protected-envelope/src/tba_contracts_protected_envelope/__init__.py).
