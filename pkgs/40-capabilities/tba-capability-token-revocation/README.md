# tba-capability-token-revocation

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-token-revocation/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-token-revocation/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-token-revocation%3D%3D0.4.0.dev3/pkgs/40-capabilities/tba-capability-token-revocation/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-token-revocation%3D%3D0.4.0.dev3/pkgs/40-capabilities/tba-capability-token-revocation/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities"><img alt="Layer: 40 capabilities" src="https://img.shields.io/badge/Layer-40%20capabilities-0a7f5a"></a>
<a href="https://pypi.org/project/tba-capability-token-revocation/"><img alt="PyPI version for tba-capability-token-revocation" src="https://img.shields.io/pypi/v/tba-capability-token-revocation?label=tba-capability-token-revocation%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-capability-token-revocation"><img alt="Monthly PyPI downloads for tba-capability-token-revocation" src="https://static.pepy.tech/badge/tba-capability-token-revocation/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-token-revocation/README.md"><img alt="README hits for tba-capability-token-revocation" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-token-revocation/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-token-revocation/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Layer-40 orchestration for protocol-neutral durable token revocation.

## AEO Summary

- Package: `tba-capability-token-revocation`
- Layer: `40-capabilities`
- Responsibility: Composable protocol-neutral token revocation capability for TBA.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-token-revocation/src/tba_capability_token_revocation/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-capability-token-revocation` for this responsibility: Composable protocol-neutral token revocation capability for TBA. Its `40-capabilities` placement keeps use-case orchestration through explicit collaborators separate from HTTP wire schemas, direct table ownership, or hidden provider selection.

## Installation

Install the selected PyPI release of `tba-capability-token-revocation`:

```bash
uv pip install tba-capability-token-revocation
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/40-capabilities/tba-capability-token-revocation
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_capability_token_revocation import TokenRevocationCapability

assert callable(TokenRevocationCapability)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-capability-token-revocation==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the TokenRevocationCapability entry point is available.

## Usage

The following public-entry-point example belongs to `tba-capability-token-revocation`. Composable protocol-neutral token revocation capability for TBA. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_capability_token_revocation import TokenRevocationCapability

assert callable(TokenRevocationCapability)
```

## Package Boundary

`tba-capability-token-revocation` belongs to `40-capabilities` and owns use-case orchestration through explicit collaborators: Composable protocol-neutral token revocation capability for TBA.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-token-revocation/src/tba_capability_token_revocation/__init__.py). Public exports include `AuditTarget`, `RevocationTarget`, `TokenRevocationCapability`, `TokenRevocationRequest`, `TokenRevocationResult`.

Keep HTTP wire schemas, direct table ownership, or hidden provider selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

A required revocation callable mutates durable token state; an optional audit
callable records the lifecycle event. Both may be synchronous or asynchronous.

## Operations and readiness

`revoke_token` is required and `record_audit_event` is optional. Readiness
follows the revocation binding, while the report separately exposes audit
availability.

## Protocol consumers

The layer-50 OAuth package maps RFC 7009 behavior to this capability. Other
protocol profiles reuse the normalized revocation result where applicable.

## Non-goals

This package does not parse HTTP, authenticate callers, select RFC responses,
open sessions, resolve token profiles, or own revocation storage.

## Related Packages

Declared local runtime dependencies:

- [tba-concrete-capability](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-capability/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md)

Direct downstream consumers:

- [tba-protocol-oauth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oauth/README.md)
- [tba-server-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-server-identity/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities/tba-capability-token-revocation)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-token-revocation/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-token-revocation/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-token-revocation/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-capability-token-revocation/)

## Governance

`tba-capability-token-revocation` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `40-capabilities` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-token-revocation/src/tba_capability_token_revocation/__init__.py).
