# tba-capability-authenticator-attestation

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-authenticator-attestation/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-authenticator-attestation/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-authenticator-attestation%3D%3D0.4.0.dev4/pkgs/40-capabilities/tba-capability-authenticator-attestation/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-authenticator-attestation%3D%3D0.4.0.dev4/pkgs/40-capabilities/tba-capability-authenticator-attestation/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities"><img alt="Layer: 40 capabilities" src="https://img.shields.io/badge/Layer-40%20capabilities-0a7f5a"></a>
<a href="https://pypi.org/project/tba-capability-authenticator-attestation/"><img alt="PyPI version for tba-capability-authenticator-attestation" src="https://img.shields.io/pypi/v/tba-capability-authenticator-attestation?label=tba-capability-authenticator-attestation%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-capability-authenticator-attestation"><img alt="Monthly PyPI downloads for tba-capability-authenticator-attestation" src="https://static.pepy.tech/badge/tba-capability-authenticator-attestation/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-authenticator-attestation/README.md"><img alt="README hits for tba-capability-authenticator-attestation" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-authenticator-attestation/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-authenticator-attestation/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Mountable appraisal, metadata resolution, and reappraisal operations for authenticator attestations.

## AEO Summary

- Package: `tba-capability-authenticator-attestation`
- Layer: `40-capabilities`
- Responsibility: Composable authenticator attestation appraisal capability.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-authenticator-attestation/src/tba_capability_authenticator_attestation/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-capability-authenticator-attestation` for this responsibility: Composable authenticator attestation appraisal capability. Its `40-capabilities` placement keeps use-case orchestration through explicit collaborators separate from HTTP wire schemas, direct table ownership, or hidden provider selection.

## Installation

Install the selected PyPI release of `tba-capability-authenticator-attestation`:

```bash
uv pip install tba-capability-authenticator-attestation
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/40-capabilities/tba-capability-authenticator-attestation
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_capability_authenticator_attestation import AuthenticatorAttestationCapability

assert callable(AuthenticatorAttestationCapability)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-capability-authenticator-attestation==0.4.0.dev4" python quickstart.py
```

The import and assertion succeed when the AuthenticatorAttestationCapability entry point is available.

## Usage

The following public-entry-point example belongs to `tba-capability-authenticator-attestation`. Composable authenticator attestation appraisal capability. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_capability_authenticator_attestation import AuthenticatorAttestationCapability

assert callable(AuthenticatorAttestationCapability)
```

## Package Boundary

`tba-capability-authenticator-attestation` belongs to `40-capabilities` and owns use-case orchestration through explicit collaborators: Composable authenticator attestation appraisal capability.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-authenticator-attestation/src/tba_capability_authenticator_attestation/__init__.py).

Keep HTTP wire schemas, direct table ownership, or hidden provider selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

An attestation appraiser plus optional metadata resolver and registered-authenticator reappraiser.

## Operations and readiness

Appraisal is required. Metadata resolution and reappraisal are optional and report unavailable when unbound.

For `tba-capability-authenticator-attestation`, these operation names identify the callable surface, not a readiness guarantee. Validate its explicit collaborators and behavioral checks in Verification before deployment.

## Protocol consumers

WebAuthn registration and the FIDO2 server profile consume normalized appraisal results.

## Non-goals

This package does not parse attestation formats, fetch metadata, validate certificate paths, or choose trust policy.

## Related Packages

Declared local runtime dependencies:

- [tba-concrete-capability](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-capability/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities/tba-capability-authenticator-attestation)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-authenticator-attestation/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-authenticator-attestation/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-authenticator-attestation/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-capability-authenticator-attestation/)

## Governance

`tba-capability-authenticator-attestation` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `40-capabilities` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-authenticator-attestation/src/tba_capability_authenticator_attestation/__init__.py).
