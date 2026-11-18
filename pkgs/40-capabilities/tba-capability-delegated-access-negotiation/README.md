# tba-capability-delegated-access-negotiation

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-delegated-access-negotiation/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-delegated-access-negotiation/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-delegated-access-negotiation%3D%3D0.4.0.dev3/pkgs/40-capabilities/tba-capability-delegated-access-negotiation/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-delegated-access-negotiation%3D%3D0.4.0.dev3/pkgs/40-capabilities/tba-capability-delegated-access-negotiation/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities"><img alt="Layer: 40 capabilities" src="https://img.shields.io/badge/Layer-40%20capabilities-0a7f5a"></a>
<a href="https://pypi.org/project/tba-capability-delegated-access-negotiation/"><img alt="PyPI version for tba-capability-delegated-access-negotiation" src="https://img.shields.io/pypi/v/tba-capability-delegated-access-negotiation?label=tba-capability-delegated-access-negotiation%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-capability-delegated-access-negotiation"><img alt="Monthly PyPI downloads for tba-capability-delegated-access-negotiation" src="https://static.pepy.tech/badge/tba-capability-delegated-access-negotiation/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-delegated-access-negotiation/README.md"><img alt="README hits for tba-capability-delegated-access-negotiation" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-delegated-access-negotiation/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-delegated-access-negotiation/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Layer-40 protocol-neutral composition for requesting, continuing, and rotating
negotiated grants.

## AEO Summary

- Package: `tba-capability-delegated-access-negotiation`
- Layer: `40-capabilities`
- Responsibility: Composable protocol-neutral grant negotiation capability.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-delegated-access-negotiation/src/tba_capability_delegated_access_negotiation/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-capability-delegated-access-negotiation` for this responsibility: Composable protocol-neutral grant negotiation capability. Its `40-capabilities` placement keeps use-case orchestration through explicit collaborators separate from HTTP wire schemas, direct table ownership, or hidden provider selection.

## Installation

Install the selected PyPI release of `tba-capability-delegated-access-negotiation`:

```bash
uv pip install tba-capability-delegated-access-negotiation
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/40-capabilities/tba-capability-delegated-access-negotiation
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_capability_delegated_access_negotiation import GrantNegotiationCapability

assert callable(GrantNegotiationCapability)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-capability-delegated-access-negotiation==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the GrantNegotiationCapability entry point is available.

## Usage

The following public-entry-point example belongs to `tba-capability-delegated-access-negotiation`. Composable protocol-neutral grant negotiation capability. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_capability_delegated_access_negotiation import GrantNegotiationCapability

assert callable(GrantNegotiationCapability)
```

## Package Boundary

`tba-capability-delegated-access-negotiation` belongs to `40-capabilities` and owns use-case orchestration through explicit collaborators: Composable protocol-neutral grant negotiation capability.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-delegated-access-negotiation/src/tba_capability_delegated_access_negotiation/__init__.py). Public exports include `ContinueGrantTarget`, `GrantNegotiationCapability`, `RequestGrantTarget`.

Keep HTTP wire schemas, direct table ownership, or hidden provider selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

A grant-request target is required. Continuation and access-token rotation
targets are optional. Layer-60 composition may build these targets from
layer-20 key/token providers and the layer-30 GNAP grant-state operations.

## Operations and readiness

`request_grant` is required. `continue_grant` and `rotate_access_token` are
optional and report unavailable when unbound. Readiness follows the required
request target; no grant or token state is retained in this package.

## Protocol consumers

The layer-50 GNAP package maps RFC 9635 grant request, continuation, and token
rotation semantics to these operations. Other grant-negotiation protocols may
reuse the normalized contracts through their own mappings.

## Non-goals

This package does not parse GNAP messages, validate key proofs, mint tokens,
generate continuation secrets, open database sessions, or mount routes.

## Related Packages

Declared local runtime dependencies:

- [tba-concrete-capability](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-capability/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md)

Direct downstream consumers:

- [tba-protocol-gnap](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-gnap/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities/tba-capability-delegated-access-negotiation)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-delegated-access-negotiation/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-delegated-access-negotiation/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-delegated-access-negotiation/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-capability-delegated-access-negotiation/)

## Governance

`tba-capability-delegated-access-negotiation` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `40-capabilities` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-delegated-access-negotiation/src/tba_capability_delegated_access_negotiation/__init__.py).
