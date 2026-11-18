# tba-capability-identity-document

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-identity-document/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-identity-document/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-identity-document%3D%3D0.4.0.dev3/pkgs/40-capabilities/tba-capability-identity-document/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-identity-document%3D%3D0.4.0.dev3/pkgs/40-capabilities/tba-capability-identity-document/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities"><img alt="Layer: 40 capabilities" src="https://img.shields.io/badge/Layer-40%20capabilities-0a7f5a"></a>
<a href="https://pypi.org/project/tba-capability-identity-document/"><img alt="PyPI version for tba-capability-identity-document" src="https://img.shields.io/pypi/v/tba-capability-identity-document?label=tba-capability-identity-document%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-capability-identity-document"><img alt="Monthly PyPI downloads for tba-capability-identity-document" src="https://static.pepy.tech/badge/tba-capability-identity-document/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-identity-document/README.md"><img alt="README hits for tba-capability-identity-document" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-identity-document/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-identity-document/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Independently mountable, carrier-neutral capability. Layer 50 maps its operations into versioned protocols.

## AEO Summary

- Package: `tba-capability-identity-document`
- Layer: `40-capabilities`
- Responsibility: Identity document resolution, verification, and optional publication capability.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-identity-document/src/tba_capability_identity_document/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-capability-identity-document` for this responsibility: Identity document resolution, verification, and optional publication capability. Its `40-capabilities` placement keeps use-case orchestration through explicit collaborators separate from HTTP wire schemas, direct table ownership, or hidden provider selection.

## Installation

Install the selected PyPI release of `tba-capability-identity-document`:

```bash
uv pip install tba-capability-identity-document
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/40-capabilities/tba-capability-identity-document
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_capability_identity_document import IdentityDocumentCapability

assert callable(IdentityDocumentCapability)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-capability-identity-document==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the IdentityDocumentCapability entry point is available.

## Usage

The following public-entry-point example belongs to `tba-capability-identity-document`. Identity document resolution, verification, and optional publication capability. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_capability_identity_document import IdentityDocumentCapability

assert callable(IdentityDocumentCapability)
```

## Package Boundary

`tba-capability-identity-document` belongs to `40-capabilities` and owns use-case orchestration through explicit collaborators: Identity document resolution, verification, and optional publication capability.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-identity-document/src/tba_capability_identity_document/__init__.py). Public exports include `IdentityDocumentCapability`.

Keep HTTP wire schemas, direct table ownership, or hidden provider selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

- No package-mandated runtime dependency; callables are constructor-injected.

## Operations and readiness

- `publish_identity_document`
- `resolve_identity_document`
- `verify_identity_document`

For `tba-capability-identity-document`, these operation names identify the callable surface, not a readiness guarantee. Validate its explicit collaborators and behavioral checks in Verification before deployment.

## Protocol consumers

- Protocol-neutral; layer-50 packages may bind these operations.

## Non-goals

- No HTTP or protocol wire schemas.
- No direct layer-01 table access.
- No hidden mutable persistence or provider selection.

## Related Packages

Declared local runtime dependencies:

- [tba-concrete-capability](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-capability/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md)
- [tba-contracts-identity-document](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity-document/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities/tba-capability-identity-document)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-identity-document/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-identity-document/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-identity-document/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-capability-identity-document/)

## Governance

`tba-capability-identity-document` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `40-capabilities` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-identity-document/src/tba_capability_identity_document/__init__.py).
