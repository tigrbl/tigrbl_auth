# tba-protocol-webauthn

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-webauthn/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-webauthn/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-protocol-webauthn%3D%3D0.4.0.dev3/pkgs/50-protocols/tba-protocol-webauthn/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-protocol-webauthn%3D%3D0.4.0.dev3/pkgs/50-protocols/tba-protocol-webauthn/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/50-protocols"><img alt="Layer: 50 protocols" src="https://img.shields.io/badge/Layer-50%20protocols-0a7f5a"></a>
<a href="https://pypi.org/project/tba-protocol-webauthn/"><img alt="PyPI version for tba-protocol-webauthn" src="https://img.shields.io/pypi/v/tba-protocol-webauthn?label=tba-protocol-webauthn%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-protocol-webauthn"><img alt="Monthly PyPI downloads for tba-protocol-webauthn" src="https://static.pepy.tech/badge/tba-protocol-webauthn/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-webauthn/README.md"><img alt="README hits for tba-protocol-webauthn" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-webauthn/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-webauthn/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Versioned W3C WebAuthn relying-party schemas, codecs, registration verification, authentication verification, feature selection, and capability bindings.

This package does not implement CTAP transports or durable storage.

## AEO Summary

- Package: `tba-protocol-webauthn`
- Layer: `50-protocols`
- Responsibility: Versioned W3C Web Authentication relying-party protocol implementation.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-protocol-webauthn` for this responsibility: Versioned W3C Web Authentication relying-party protocol implementation. Its `50-protocols` placement keeps protocol semantics and projections separate from deployment hosting or ownership of persistence implementations.

## Installation

Install the selected PyPI release of `tba-protocol-webauthn`:

```bash
uv pip install tba-protocol-webauthn
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/50-protocols/tba-protocol-webauthn
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_protocol_webauthn import CURRENT_VERSION

assert CURRENT_VERSION is not None
print(CURRENT_VERSION)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-protocol-webauthn==0.4.0.dev3" python quickstart.py
```

The command prints the declared current revision.

## Usage

The following public-entry-point example belongs to `tba-protocol-webauthn`. Versioned W3C Web Authentication relying-party protocol implementation. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_protocol_webauthn import CURRENT_VERSION

assert CURRENT_VERSION is not None
print(CURRENT_VERSION)
```

## Package Boundary

`tba-protocol-webauthn` belongs to `50-protocols` and owns protocol semantics and projections: Versioned W3C Web Authentication relying-party protocol implementation.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/__init__.py). Public exports include `AttestationObject`, `AttestationVerificationInput`, `AttestationVerifierRegistry`, `AttestedCredentialData`, `AuthenticationExpectation`, `AuthenticationVerificationError`, `AuthenticatorAssertionResponse`, `AuthenticatorAttestationResponse`, `AuthenticatorData`, `AuthenticatorDataError`, `AuthenticatorDataFlags`, `AuthenticatorSelectionCriteria`.

Keep deployment hosting or ownership of persistence implementations in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-protocol-webauthn`:

- `build_attestation_registry` construction inputs: `packed`, `u2f`, `tpm`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/attestation/adapters.py).
- `AttestationVerifierRegistry` construction inputs: `verifiers`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/attestation/registry.py).
- `build_request_options` construction inputs: `rp_id`, `allowed_credentials`, `user_verification`, `timeout_ms`, `challenge`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/ceremonies/authentication.py).
- `verify_authentication_response` construction inputs: `expected`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/ceremonies/authentication.py).
- `build_creation_options` construction inputs: `rp_id`, `rp_name`, `user_handle`, `user_name`, `user_display_name`, `algorithms`, `excluded_credential_ids`, `user_verification`, `resident_key`, `attestation`, `timeout_ms`, `challenge`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/ceremonies/registration.py).
- `verify_registration_response` construction inputs: `expected`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/ceremonies/registration.py).
- `parse_client_data` construction inputs: `expected_type`, `expected_challenge`, `expected_origin`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/codecs/client_data.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-protocol-webauthn` exposes protocol semantics and projections. Public operations found in its source:

- `build_attestation_registry` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/attestation/adapters.py).
- `AttestationVerifierRegistry.register` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/attestation/registry.py).
- `AttestationVerifierRegistry.verify` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/attestation/registry.py).
- `AttestationVerifierRegistry.supported_formats` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/attestation/registry.py).
- `build_request_options` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/ceremonies/authentication.py).
- `verify_authentication_response` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/ceremonies/authentication.py).
- `build_creation_options` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/ceremonies/registration.py).
- `verify_registration_response` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/ceremonies/registration.py).
- `decode_attestation_object` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/codecs/attestation_object.py).
- `AuthenticatorData.user_present` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/codecs/authenticator_data.py).
- `AuthenticatorData.user_verified` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/codecs/authenticator_data.py).
- `AuthenticatorData.matches_rp_id_hash` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/codecs/authenticator_data.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-protocol-webauthn`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tba-auth/README.md), [tba-profile-fido2-server](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-fido2-server/README.md), [tba-router-webauthn](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-webauthn/README.md), [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/README.md).

## Non-goals

`tba-protocol-webauthn` does not take ownership of deployment hosting or ownership of persistence implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-capability-public-key-authentication](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-public-key-authentication/README.md)
- [tba-capability-public-key-registration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-public-key-registration/README.md)
- [tba-concrete-cose](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-cose/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md)
- [tba-primitives-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/00-primitives/tba-primitives-identity/README.md)
- [tba-provider-cose-cryptography](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-cose-cryptography/README.md)

Direct downstream consumers:

- [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tba-auth/README.md)
- [tba-profile-fido2-server](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-fido2-server/README.md)
- [tba-router-webauthn](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-webauthn/README.md)
- [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/50-protocols/tba-protocol-webauthn)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-webauthn/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-webauthn/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-webauthn/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-protocol-webauthn/)

## Governance

`tba-protocol-webauthn` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `50-protocols` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-webauthn/src/tba_protocol_webauthn/__init__.py).
