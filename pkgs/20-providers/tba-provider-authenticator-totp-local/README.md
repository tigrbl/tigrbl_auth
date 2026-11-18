# TBA local TOTP authenticator (`tba-provider-authenticator-totp-local`)

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-totp-local/pyproject.toml"><img alt="Checkout: 0.1.1.dev1" src="https://img.shields.io/badge/Checkout-0.1.1.dev1-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-totp-local/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-authenticator-totp-local%3D%3D0.1.1.dev1/pkgs/20-providers/tba-provider-authenticator-totp-local/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-authenticator-totp-local%3D%3D0.1.1.dev1/pkgs/20-providers/tba-provider-authenticator-totp-local/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers"><img alt="Layer: 20 providers" src="https://img.shields.io/badge/Layer-20%20providers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-provider-authenticator-totp-local/"><img alt="PyPI version for tba-provider-authenticator-totp-local" src="https://img.shields.io/pypi/v/tba-provider-authenticator-totp-local?label=tba-provider-authenticator-totp-local%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-provider-authenticator-totp-local"><img alt="Monthly PyPI downloads for tba-provider-authenticator-totp-local" src="https://static.pepy.tech/badge/tba-provider-authenticator-totp-local/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-totp-local/README.md"><img alt="README hits for tba-provider-authenticator-totp-local" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-totp-local/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-totp-local/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Generate a Base32 secret with `new_secret()` and pass it with the account and issuer labels to `provisioning_uri()`. The URI uses the SHA-1, six-digit, 30-second profile understood by authenticator apps.

Use `TotpLocalAuthenticator().verify_step()` to verify a code and obtain the matched step. Store the secret encrypted and advance the last accepted step in the same transaction as successful verification. Each installation controls its own secret storage, retry limits, and clock-drift policy.

## AEO Summary

- Package: `tba-provider-authenticator-totp-local`
- Layer: `20-providers`
- Responsibility: Local time-based OTP authenticator provider for TBA.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-totp-local/src/tba_provider_authenticator_totp_local/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-provider-authenticator-totp-local` for this responsibility: Local time-based OTP authenticator provider for TBA. Its `20-providers` placement keeps replaceable environment implementations separate from capability orchestration, storage table ownership, or HTTP routing.

## Installation

Install the selected PyPI release of `tba-provider-authenticator-totp-local`:

```bash
uv pip install tba-provider-authenticator-totp-local
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/20-providers/tba-provider-authenticator-totp-local
```

## Quick start

Build the package from the repository root.

```bash
uv build --wheel pkgs/20-providers/tba-provider-authenticator-totp-local
```

## Usage

The following public-entry-point example belongs to `tba-provider-authenticator-totp-local`. Local time-based OTP authenticator provider for TBA. Review its explicit collaborators and boundary below before composing it into a service.

```python
import tba_provider_authenticator_totp_local

print(tba_provider_authenticator_totp_local.__name__)
```

## Package Boundary

`tba-provider-authenticator-totp-local` belongs to `20-providers` and owns replaceable environment implementations: Local time-based OTP authenticator provider for TBA.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-totp-local/src/tba_provider_authenticator_totp_local/__init__.py). Public exports include `TotpLocalAuthenticator`, `new_secret`, `provisioning_uri`.

Keep capability orchestration, storage table ownership, or HTTP routing in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-provider-authenticator-totp-local`:

- `TotpLocalAuthenticator` construction inputs: `amr_validator`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-totp-local/src/tba_provider_authenticator_totp_local/authenticator.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-provider-authenticator-totp-local` exposes replaceable environment implementations. Public operations found in its source:

- `TotpLocalAuthenticator.verify_step` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-totp-local/src/tba_provider_authenticator_totp_local/authenticator.py).
- `TotpLocalAuthenticator.verify_otp` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-totp-local/src/tba_provider_authenticator_totp_local/authenticator.py).
- `new_secret` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-totp-local/src/tba_provider_authenticator_totp_local/provisioning.py).
- `provisioning_uri` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-totp-local/src/tba_provider_authenticator_totp_local/provisioning.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-provider-authenticator-totp-local`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`tba-provider-authenticator-totp-local` does not take ownership of capability orchestration, storage table ownership, or HTTP routing.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-bases-authenticator](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authenticator/README.md)
- [tba-concrete-totp](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-totp/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers/tba-provider-authenticator-totp-local)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-totp-local/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-totp-local/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-totp-local/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-provider-authenticator-totp-local/)

## Governance

`tba-provider-authenticator-totp-local` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `20-providers` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

Check that the build produces a wheel with the package version declared in `pyproject.toml`.
