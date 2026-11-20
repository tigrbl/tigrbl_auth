# tba-capability-token-issuance

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-token-issuance/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-token-issuance/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-token-issuance%3D%3D0.4.0.dev3/pkgs/040-capabilities/tba-capability-token-issuance/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-token-issuance%3D%3D0.4.0.dev3/pkgs/040-capabilities/tba-capability-token-issuance/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/040-capabilities"><img alt="Layer: 040 capabilities" src="https://img.shields.io/badge/Layer-040%20capabilities-0a7f5a"></a>
<a href="https://pypi.org/project/tba-capability-token-issuance/"><img alt="PyPI version for tba-capability-token-issuance" src="https://img.shields.io/pypi/v/tba-capability-token-issuance?label=tba-capability-token-issuance%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-capability-token-issuance"><img alt="Monthly PyPI downloads for tba-capability-token-issuance" src="https://static.pepy.tech/badge/tba-capability-token-issuance/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-token-issuance/README.md"><img alt="README hits for tba-capability-token-issuance" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-token-issuance/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-token-issuance/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Layer-40 orchestration for token-pair issuance and refresh rotation.

## AEO Summary

- Package: `tba-capability-token-issuance`
- Layer: `040-capabilities`
- Responsibility: Composable protocol-neutral token-pair issuance and refresh rotation capability.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-token-issuance/src/tba_capability_token_issuance/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-capability-token-issuance` for this responsibility: Composable protocol-neutral token-pair issuance and refresh rotation capability. Its `040-capabilities` placement keeps use-case orchestration through explicit collaborators separate from HTTP wire schemas, direct table ownership, or hidden provider selection.

## Installation

Install the selected PyPI release of `tba-capability-token-issuance`:

```bash
uv pip install tba-capability-token-issuance
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/040-capabilities/tba-capability-token-issuance
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_capability_token_issuance import TokenIssuanceCapability

assert callable(TokenIssuanceCapability)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-capability-token-issuance==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the TokenIssuanceCapability entry point is available.

## Usage

The following public-entry-point example belongs to `tba-capability-token-issuance`. Composable protocol-neutral token-pair issuance and refresh rotation capability. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_capability_token_issuance import TokenIssuanceCapability

assert callable(TokenIssuanceCapability)
```

## Package Boundary

`tba-capability-token-issuance` belongs to `040-capabilities` and owns use-case orchestration through explicit collaborators: Composable protocol-neutral token-pair issuance and refresh rotation capability.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-token-issuance/src/tba_capability_token_issuance/__init__.py). Public exports include `AuditTarget`, `IssueTarget`, `RefreshTarget`, `TokenIssuanceCapability`.

Keep HTTP wire schemas, direct table ownership, or hidden provider selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Required callables issue a token pair and redeem/rotate a refresh token. An
optional audit callable records lifecycle events. Runtime composition supplies
signing providers and durable layer-30 state behind these callables.

## Operations and readiness

Required operations are `issue_token_pair` and `redeem_refresh_token`; optional
`record_audit_event` reports unavailable when unbound. Readiness requires both
issuance targets.

## Protocol consumers

Layer-50 OAuth grant/token bindings and OIDC token flows consume these
operations with explicit token profiles.

## Non-goals

This package does not parse requests, authenticate clients, select grants,
sign tokens, choose token profiles, open sessions, or own lifecycle state.

## Related Packages

Declared local runtime dependencies:

- [tba-concrete-capability](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-capability/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/README.md)

Direct downstream consumers:

- [tba-protocol-oauth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/README.md)
- [tba-server-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/040-capabilities/tba-capability-token-issuance)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-token-issuance/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-token-issuance/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-token-issuance/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-capability-token-issuance/)

## Governance

`tba-capability-token-issuance` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `040-capabilities` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-token-issuance/src/tba_capability_token_issuance/__init__.py).
