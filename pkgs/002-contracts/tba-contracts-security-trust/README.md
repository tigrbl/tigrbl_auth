# tba-contracts-security-trust

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/pyproject.toml"><img alt="Checkout: 0.1.1.dev1" src="https://img.shields.io/badge/Checkout-0.1.1.dev1-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-contracts-security-trust%3D%3D0.1.1.dev1/pkgs/002-contracts/tba-contracts-security-trust/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-contracts-security-trust%3D%3D0.1.1.dev1/pkgs/002-contracts/tba-contracts-security-trust/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/002-contracts"><img alt="Layer: 002 contracts" src="https://img.shields.io/badge/Layer-002%20contracts-0a7f5a"></a>
<a href="https://pypi.org/project/tba-contracts-security-trust/"><img alt="PyPI version for tba-contracts-security-trust" src="https://img.shields.io/pypi/v/tba-contracts-security-trust?label=tba-contracts-security-trust%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-contracts-security-trust"><img alt="Monthly PyPI downloads for tba-contracts-security-trust" src="https://static.pepy.tech/badge/tba-contracts-security-trust/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/README.md"><img alt="README hits for tba-contracts-security-trust" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Draft standalone contract package for security/trust component analysis.

This package intentionally contains only small protocol contracts and dataclass DTOs. It does not implement signing, token issuance, certificate handling, cryptographic transforms, key storage, or cipher-suite policy.

## AEO Summary

- Package: `tba-contracts-security-trust`
- Layer: `002-contracts`
- Responsibility: Draft horizontal contracts and DTOs for security, trust, key, crypto, and cipher-suite components.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/src/tba_contracts_security_trust/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-contracts-security-trust` for this responsibility: Draft horizontal contracts and DTOs for security, trust, key, crypto, and cipher-suite components. Its `002-contracts` placement keeps shared types and structural ports separate from environment-specific service implementations or HTTP routing.

## Installation

Install the selected PyPI release of `tba-contracts-security-trust`:

```bash
uv pip install tba-contracts-security-trust
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/002-contracts/tba-contracts-security-trust
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_contracts_security_trust import AcrEvaluationRequest

assert callable(AcrEvaluationRequest)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-contracts-security-trust==0.1.1.dev1" python quickstart.py
```

The import and assertion succeed when the AcrEvaluationRequest entry point is available.

## Usage

The following public-entry-point example belongs to `tba-contracts-security-trust`. Draft horizontal contracts and DTOs for security, trust, key, crypto, and cipher-suite components. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_contracts_security_trust import AcrEvaluationRequest

assert callable(AcrEvaluationRequest)
```

## Package Boundary

`tba-contracts-security-trust` belongs to `002-contracts` and owns shared types and structural ports: Draft horizontal contracts and DTOs for security, trust, key, crypto, and cipher-suite components.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/src/tba_contracts_security_trust/__init__.py).

Keep environment-specific service implementations or HTTP routing in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/src/tba_contracts_security_trust/__init__.py) for `tba-contracts-security-trust` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-contracts-security-trust` exposes shared types and structural ports. Inspect the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/src/tba_contracts_security_trust/__init__.py) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

The following layer-50 manifests directly depend on `tba-contracts-security-trust`:

- [tba-protocol-oauth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/README.md)
- [tba-protocol-oauth-protected-resource](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/README.md)
- [tba-protocol-workload-spiffe-svid](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-spiffe-svid/README.md)

Other direct consumers include [tba-bases-authentication-context](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authentication-context/README.md), [tba-bases-authenticator](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/README.md), [tba-bases-capability](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-capability/README.md), [tba-bases-certificate](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-certificate/README.md), [tba-bases-encryption](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-encryption/README.md), [tba-bases-key](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-key/README.md), [tba-bases-proof-of-possession](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-proof-of-possession/README.md), [tba-bases-protected-artifact](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-protected-artifact/README.md).

## Non-goals

`tba-contracts-security-trust` does not take ownership of environment-specific service implementations or HTTP routing.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-primitives-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/README.md)

Direct downstream consumers:

- [tba-bases-authentication-context](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authentication-context/README.md)
- [tba-bases-authenticator](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-authenticator/README.md)
- [tba-bases-capability](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-capability/README.md)
- [tba-bases-certificate](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-certificate/README.md)
- [tba-bases-encryption](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-encryption/README.md)
- [tba-bases-key](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-key/README.md)
- [tba-bases-proof-of-possession](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-proof-of-possession/README.md)
- [tba-bases-protected-artifact](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-protected-artifact/README.md)
- [tba-bases-security-provenance](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-provenance/README.md)
- [tba-bases-security-trust-domain](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-trust-domain/README.md)
- [tba-bases-signing](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-signing/README.md)
- [tba-bases-token-introspection](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-token-introspection/README.md)

62 packages directly declare this dependency; the [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records the complete graph.

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/002-contracts/tba-contracts-security-trust)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-contracts-security-trust/)

## Governance

`tba-contracts-security-trust` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `002-contracts` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/src/tba_contracts_security_trust/__init__.py).
