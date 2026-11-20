# tba-bases-security-trust-domain

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/pyproject.toml"><img alt="Checkout: 0.1.1.dev1" src="https://img.shields.io/badge/Checkout-0.1.1.dev1-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-bases-security-trust-domain%3D%3D0.1.1.dev1/pkgs/005-bases/tba-bases-security-trust-domain/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-bases-security-trust-domain%3D%3D0.1.1.dev1/pkgs/005-bases/tba-bases-security-trust-domain/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/005-bases"><img alt="Layer: 005 bases" src="https://img.shields.io/badge/Layer-005%20bases-0a7f5a"></a>
<a href="https://pypi.org/project/tba-bases-security-trust-domain/"><img alt="PyPI version for tba-bases-security-trust-domain" src="https://img.shields.io/pypi/v/tba-bases-security-trust-domain?label=tba-bases-security-trust-domain%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-bases-security-trust-domain"><img alt="Monthly PyPI downloads for tba-bases-security-trust-domain" src="https://static.pepy.tech/badge/tba-bases-security-trust-domain/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/README.md"><img alt="README hits for tba-bases-security-trust-domain" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Draft standalone package with abstract domain base classes composed from the horizontal security/trust contracts.

These bases are intentionally thin. They encode domain composition only; concrete providers still own runtime behavior.

## AEO Summary

- Package: `tba-bases-security-trust-domain`
- Layer: `005-bases`
- Responsibility: Draft domain base classes composed from tigrbl security/trust contracts.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/src/tba_bases_security_trust_domain/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-bases-security-trust-domain` for this responsibility: Draft domain base classes composed from tigrbl security/trust contracts. Its `005-bases` placement keeps reusable component bases separate from deployment composition or implicit provider selection.

## Installation

Install the selected PyPI release of `tba-bases-security-trust-domain`:

```bash
uv pip install tba-bases-security-trust-domain
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/005-bases/tba-bases-security-trust-domain
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_bases_security_trust_domain import ArtifactCodecBase

assert callable(ArtifactCodecBase)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-bases-security-trust-domain==0.1.1.dev1" python quickstart.py
```

The import and assertion succeed when the ArtifactCodecBase entry point is available.

## Usage

The following public-entry-point example belongs to `tba-bases-security-trust-domain`. Draft domain base classes composed from tigrbl security/trust contracts. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_bases_security_trust_domain import ArtifactCodecBase

assert callable(ArtifactCodecBase)
```

## Package Boundary

`tba-bases-security-trust-domain` belongs to `005-bases` and owns reusable component bases: Draft domain base classes composed from tigrbl security/trust contracts.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/src/tba_bases_security_trust_domain/__init__.py). Public exports include `ArtifactCodecBase`, `ArtifactIssuerBase`, `ArtifactOpenerBase`, `ArtifactVerifierBase`, `AcrEvaluatorBase`, `AmrEvaluatorBase`, `AttestationProviderBase`, `CapabilityProviderBase`, `CertificateDomainBase`, `CertificatePathValidatorBase`, `CertificateServiceDomainBase`, `CipherPolicyDomainBase`.

Keep deployment composition or implicit provider selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/src/tba_bases_security_trust_domain/__init__.py) for `tba-bases-security-trust-domain` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-bases-security-trust-domain` exposes reusable component bases. Public operations found in its source:

- `SigningProviderBase.sign` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/src/tba_bases_security_trust_domain/bases.py).
- `SigningProviderBase.verify_signature` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/src/tba_bases_security_trust_domain/bases.py).
- `PkceVerifierBase.verify_challenge` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/src/tba_bases_security_trust_domain/bases.py).
- `TokenServiceDomainBase.issue_token` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/src/tba_bases_security_trust_domain/bases.py).
- `TokenServiceDomainBase.verify_token` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/src/tba_bases_security_trust_domain/bases.py).
- `TokenServiceDomainBase.export_verification_keys` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/src/tba_bases_security_trust_domain/bases.py).
- `CertificateServiceDomainBase.create_csr` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/src/tba_bases_security_trust_domain/bases.py).
- `CertificateServiceDomainBase.issue_certificate` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/src/tba_bases_security_trust_domain/bases.py).
- `CertificateServiceDomainBase.verify_certificate` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/src/tba_bases_security_trust_domain/bases.py).
- `CertificateServiceDomainBase.parse_certificate` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/src/tba_bases_security_trust_domain/bases.py).
- `KeyProviderDomainBase.resolve_key` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/src/tba_bases_security_trust_domain/bases.py).
- `KeyProviderDomainBase.create_key` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/src/tba_bases_security_trust_domain/bases.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-bases-security-trust-domain`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-provider-security-oidc-federation](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-oidc-federation/README.md), [tba-provider-security-webfinger](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-webfinger/README.md).

## Non-goals

`tba-bases-security-trust-domain` does not take ownership of deployment composition or implicit provider selection.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-bases-authentication-context](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authentication-context/README.md)
- [tba-bases-capability](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-capability/README.md)
- [tba-bases-certificate](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-certificate/README.md)
- [tba-bases-claim](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-claim/README.md)
- [tba-bases-did](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-did/README.md)
- [tba-bases-encryption](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-encryption/README.md)
- [tba-bases-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-identity/README.md)
- [tba-bases-key](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-key/README.md)
- [tba-bases-proof-of-possession](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-proof-of-possession/README.md)
- [tba-bases-protected-artifact](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-protected-artifact/README.md)
- [tba-bases-signing](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-signing/README.md)
- [tba-bases-token-introspection](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-token-introspection/README.md)
- [tba-bases-trust](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-trust/README.md)
- [tba-bases-workload-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-workload-identity/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/README.md)
- [tba-contracts-security-trust](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/README.md)

Direct downstream consumers:

- [tba-provider-security-oidc-federation](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-oidc-federation/README.md)
- [tba-provider-security-webfinger](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-webfinger/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/005-bases/tba-bases-security-trust-domain)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-bases-security-trust-domain/)

## Governance

`tba-bases-security-trust-domain` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `005-bases` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/src/tba_bases_security_trust_domain/__init__.py).
