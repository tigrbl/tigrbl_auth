# tba-bases-public-key-authentication

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-public-key-authentication/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-public-key-authentication/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-bases-public-key-authentication%3D%3D0.4.0.dev3/pkgs/05-bases/tba-bases-public-key-authentication/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-bases-public-key-authentication%3D%3D0.4.0.dev3/pkgs/05-bases/tba-bases-public-key-authentication/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/05-bases"><img alt="Layer: 05 bases" src="https://img.shields.io/badge/Layer-05%20bases-0a7f5a"></a>
<a href="https://pypi.org/project/tba-bases-public-key-authentication/"><img alt="PyPI version for tba-bases-public-key-authentication" src="https://img.shields.io/pypi/v/tba-bases-public-key-authentication?label=tba-bases-public-key-authentication%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-bases-public-key-authentication"><img alt="Monthly PyPI downloads for tba-bases-public-key-authentication" src="https://static.pepy.tech/badge/tba-bases-public-key-authentication/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-public-key-authentication/README.md"><img alt="README hits for tba-bases-public-key-authentication" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-public-key-authentication/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-public-key-authentication/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Protocol-neutral extension bases for public-key registration, assertion verification, credential lookup, attestation appraisal, and normalized evidence.

This package does not own WebAuthn wire structures, HTTP bindings, persistence, trust policy, or key loading.

## AEO Summary

- Package: `tba-bases-public-key-authentication`
- Layer: `05-bases`
- Responsibility: Protocol-neutral public-key authenticator extension bases.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-public-key-authentication/src/tba_bases_public_key_authentication/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-bases-public-key-authentication` for this responsibility: Protocol-neutral public-key authenticator extension bases. Its `05-bases` placement keeps reusable component bases separate from deployment composition or implicit provider selection.

## Installation

Install the selected PyPI release of `tba-bases-public-key-authentication`:

```bash
uv pip install tba-bases-public-key-authentication
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/05-bases/tba-bases-public-key-authentication
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_bases_public_key_authentication import AttestationStatementVerifierBase

assert callable(AttestationStatementVerifierBase)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-bases-public-key-authentication==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the AttestationStatementVerifierBase entry point is available.

## Usage

The following public-entry-point example belongs to `tba-bases-public-key-authentication`. Protocol-neutral public-key authenticator extension bases. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_bases_public_key_authentication import AttestationStatementVerifierBase

assert callable(AttestationStatementVerifierBase)
```

## Package Boundary

`tba-bases-public-key-authentication` belongs to `05-bases` and owns reusable component bases: Protocol-neutral public-key authenticator extension bases.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-public-key-authentication/src/tba_bases_public_key_authentication/__init__.py).

Keep deployment composition or implicit provider selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-public-key-authentication/src/tba_bases_public_key_authentication/__init__.py) for `tba-bases-public-key-authentication` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-bases-public-key-authentication` exposes reusable component bases. Inspect the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-public-key-authentication/src/tba_bases_public_key_authentication/__init__.py) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-bases-public-key-authentication`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-provider-attestation-packed](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-attestation-packed/README.md), [tba-provider-attestation-tpm](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-attestation-tpm/README.md), [tba-provider-attestation-u2f](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-attestation-u2f/README.md), [tba-provider-fido-metadata-service](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-fido-metadata-service/README.md).

## Non-goals

`tba-bases-public-key-authentication` does not take ownership of deployment composition or implicit provider selection.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-contracts-public-key-authentication](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-public-key-authentication/README.md)

Direct downstream consumers:

- [tba-provider-attestation-packed](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-attestation-packed/README.md)
- [tba-provider-attestation-tpm](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-attestation-tpm/README.md)
- [tba-provider-attestation-u2f](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-attestation-u2f/README.md)
- [tba-provider-fido-metadata-service](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-fido-metadata-service/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/05-bases/tba-bases-public-key-authentication)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-public-key-authentication/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-public-key-authentication/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-public-key-authentication/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-bases-public-key-authentication/)

## Governance

`tba-bases-public-key-authentication` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `05-bases` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-public-key-authentication/src/tba_bases_public_key_authentication/__init__.py).
