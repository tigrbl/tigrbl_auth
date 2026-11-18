# tba-bases-authenticator

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authenticator/pyproject.toml"><img alt="Checkout: 0.1.1.dev2" src="https://img.shields.io/badge/Checkout-0.1.1.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authenticator/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-bases-authenticator%3D%3D0.1.1.dev2/pkgs/05-bases/tba-bases-authenticator/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-bases-authenticator%3D%3D0.1.1.dev2/pkgs/05-bases/tba-bases-authenticator/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/05-bases"><img alt="Layer: 05 bases" src="https://img.shields.io/badge/Layer-05%20bases-0a7f5a"></a>
<a href="https://pypi.org/project/tba-bases-authenticator/"><img alt="PyPI version for tba-bases-authenticator" src="https://img.shields.io/pypi/v/tba-bases-authenticator?label=tba-bases-authenticator%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-bases-authenticator"><img alt="Monthly PyPI downloads for tba-bases-authenticator" src="https://static.pepy.tech/badge/tba-bases-authenticator/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authenticator/README.md"><img alt="README hits for tba-bases-authenticator" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authenticator/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authenticator/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Build authenticator providers with shared metadata, evidence, and challenge interfaces.

## AEO Summary

- Package: `tba-bases-authenticator`
- Layer: `05-bases`
- Responsibility: Authenticator base classes and mixins for the TBA package suite.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authenticator/src/tba_bases_authenticator/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Extend `AuthenticatorBase` for a single ceremony or `ChallengeAuthenticatorBase` for start/finish flows. Supply the actual authentication behavior in your provider implementation. Use a layer 20 provider if you need a ready-made authenticator.

## Installation

Install the selected PyPI release of `tba-bases-authenticator`:

```bash
uv pip install tba-bases-authenticator
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/05-bases/tba-bases-authenticator
```

## Quick start

Install the version used by this example.

```bash
python -m pip install "tba-bases-authenticator==0.1.1.dev2"
```

Save the following as `quickstart.py` and run `python quickstart.py`. The assertions should pass.

```python
from tba_bases_authenticator import AuthenticatorBase

base = AuthenticatorBase(
    kind="password_local", factor_class="knowledge", amr=("pwd",)
)
assert base.supported_amr() == ("pwd",)
assert base.metadata().challenge_based is False
```

## Usage

The following public-entry-point example belongs to `tba-bases-authenticator`. Authenticator base classes and mixins for the TBA package suite. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_bases_authenticator import AuthenticatorBase

base = AuthenticatorBase(
    kind="password_local", factor_class="knowledge", amr=("pwd",)
)
assert base.supported_amr() == ("pwd",)
assert base.metadata().challenge_based is False
```

## Package Boundary

`tba-bases-authenticator` belongs to `05-bases` and owns reusable component bases: Authenticator base classes and mixins for the TBA package suite.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authenticator/src/tba_bases_authenticator/__init__.py). Public exports include `AalEvidenceMixin`, `AmrEmitterMixin`, `AuthenticatorBase`, `AuthenticatorEvidenceEvaluatorBase`, `ChallengeAuthenticatorBase`, `ChallengeLifecycleMixin`, `CredentialKindMixin`, `CredentialLookupMixin`, `HardwareKeyProtectionEvaluatorBase`, `OtpVerifierMixin`, `PhishingResistanceMixin`, `PhishingResistanceEvaluatorBase`.

Keep deployment composition or implicit provider selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-bases-authenticator`:

- `AuthenticatorBase` construction inputs: `kind`, `factor_class`, `credential_kind`, `amr`, `properties`, `challenge_based`, `description`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authenticator/src/tba_bases_authenticator/bases.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-bases-authenticator` exposes reusable component bases. Public operations found in its source:

- `AuthenticatorBase.metadata` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authenticator/src/tba_bases_authenticator/bases.py).
- `AuthenticatorBase.supported_amr` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authenticator/src/tba_bases_authenticator/bases.py).
- `AuthenticatorBase.authenticate` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authenticator/src/tba_bases_authenticator/bases.py).
- `ChallengeAuthenticatorBase.start_challenge` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authenticator/src/tba_bases_authenticator/bases.py).
- `ChallengeAuthenticatorBase.finish_challenge` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authenticator/src/tba_bases_authenticator/bases.py).
- `AuthenticatorEvidenceEvaluatorBase.evaluate_evidence` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authenticator/src/tba_bases_authenticator/evidence.py).
- `PhishingResistanceEvaluatorBase.is_phishing_resistant` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authenticator/src/tba_bases_authenticator/evidence.py).
- `HardwareKeyProtectionEvaluatorBase.is_hardware_protected` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authenticator/src/tba_bases_authenticator/evidence.py).
- `AmrEmitterMixin.normalize_amr` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authenticator/src/tba_bases_authenticator/mixins.py).
- `AmrEmitterMixin.evidence` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authenticator/src/tba_bases_authenticator/mixins.py).
- `CredentialKindMixin.expects_credential_kind` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authenticator/src/tba_bases_authenticator/mixins.py).
- `CredentialLookupMixin.lookup_credential` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authenticator/src/tba_bases_authenticator/mixins.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-bases-authenticator`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-provider-authenticator-api-key-local](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-api-key-local/README.md), [tba-provider-authenticator-client-secret-local](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-client-secret-local/README.md), [tba-provider-authenticator-dpop-proof](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-dpop-proof/README.md), [tba-provider-authenticator-federated-oidc](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-federated-oidc/README.md), [tba-provider-authenticator-mtls-client-cert](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-mtls-client-cert/README.md), [tba-provider-authenticator-otp-local](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-otp-local/README.md), [tba-provider-authenticator-password-local](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-password-local/README.md), [tba-provider-authenticator-recovery-code-local](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-recovery-code-local/README.md).

## Non-goals

`tba-bases-authenticator` does not take ownership of deployment composition or implicit provider selection.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md)
- [tba-contracts-security-trust](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-security-trust/README.md)

Direct downstream consumers:

- [tba-provider-authenticator-api-key-local](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-api-key-local/README.md)
- [tba-provider-authenticator-client-secret-local](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-client-secret-local/README.md)
- [tba-provider-authenticator-dpop-proof](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-dpop-proof/README.md)
- [tba-provider-authenticator-federated-oidc](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-federated-oidc/README.md)
- [tba-provider-authenticator-mtls-client-cert](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-mtls-client-cert/README.md)
- [tba-provider-authenticator-otp-local](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-otp-local/README.md)
- [tba-provider-authenticator-password-local](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-password-local/README.md)
- [tba-provider-authenticator-recovery-code-local](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-recovery-code-local/README.md)
- [tba-provider-authenticator-remote-introspection](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-remote-introspection/README.md)
- [tba-provider-authenticator-service-key-local](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-service-key-local/README.md)
- [tba-provider-authenticator-session-local](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-session-local/README.md)
- [tba-provider-authenticator-totp-local](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-totp-local/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/05-bases/tba-bases-authenticator)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authenticator/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authenticator/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authenticator/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-bases-authenticator/)

## Governance

`tba-bases-authenticator` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `05-bases` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

See the [related repository tests](https://github.com/tigrbl/tigrbl_auth/blob/master/tests/unit/test_authenticator_contracts_and_providers.py) for the implementation scope covered by this example.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [tba-provider-authenticator-password-local](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers/tba-provider-authenticator-password-local#readme) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)
