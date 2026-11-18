# tba-capability-mfa-challenge

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-mfa-challenge/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-mfa-challenge/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-mfa-challenge%3D%3D0.4.0.dev3/pkgs/40-capabilities/tba-capability-mfa-challenge/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-mfa-challenge%3D%3D0.4.0.dev3/pkgs/40-capabilities/tba-capability-mfa-challenge/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities"><img alt="Layer: 40 capabilities" src="https://img.shields.io/badge/Layer-40%20capabilities-0a7f5a"></a>
<a href="https://pypi.org/project/tba-capability-mfa-challenge/"><img alt="PyPI version for tba-capability-mfa-challenge" src="https://img.shields.io/pypi/v/tba-capability-mfa-challenge?label=tba-capability-mfa-challenge%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-capability-mfa-challenge"><img alt="Monthly PyPI downloads for tba-capability-mfa-challenge" src="https://static.pepy.tech/badge/tba-capability-mfa-challenge/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-mfa-challenge/README.md"><img alt="README hits for tba-capability-mfa-challenge" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-mfa-challenge/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-mfa-challenge/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Coordinates begin and complete operations for a multi-factor challenge ceremony.

## AEO Summary

- Package: `tba-capability-mfa-challenge`
- Layer: `40-capabilities`
- Responsibility: Multi-factor challenge ceremony capability.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-mfa-challenge/src/tba_capability_mfa_challenge/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-capability-mfa-challenge` for this responsibility: Multi-factor challenge ceremony capability. Its `40-capabilities` placement keeps use-case orchestration through explicit collaborators separate from HTTP wire schemas, direct table ownership, or hidden provider selection.

## Installation

Install the selected PyPI release of `tba-capability-mfa-challenge`:

```bash
uv pip install tba-capability-mfa-challenge
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/40-capabilities/tba-capability-mfa-challenge
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_capability_mfa_challenge import MfaChallengeCapability

assert callable(MfaChallengeCapability)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-capability-mfa-challenge==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the MfaChallengeCapability entry point is available.

## Usage

The following public-entry-point example belongs to `tba-capability-mfa-challenge`. Multi-factor challenge ceremony capability. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_capability_mfa_challenge import MfaChallengeCapability

assert callable(MfaChallengeCapability)
```

## Package Boundary

`tba-capability-mfa-challenge` belongs to `40-capabilities` and owns use-case orchestration through explicit collaborators: Multi-factor challenge ceremony capability.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-mfa-challenge/src/tba_capability_mfa_challenge/__init__.py).

Keep HTTP wire schemas, direct table ownership, or hidden provider selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

- No package-mandated runtime dependency; callables are constructor-injected.

## Operations and readiness

- `begin_mfa_challenge`
- `complete_mfa_challenge`

For `tba-capability-mfa-challenge`, these operation names identify the callable surface, not a readiness guarantee. Validate its explicit collaborators and behavioral checks in Verification before deployment.

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

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities/tba-capability-mfa-challenge)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-mfa-challenge/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-mfa-challenge/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-mfa-challenge/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-capability-mfa-challenge/)

## Governance

`tba-capability-mfa-challenge` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `40-capabilities` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-mfa-challenge/src/tba_capability_mfa_challenge/__init__.py).
