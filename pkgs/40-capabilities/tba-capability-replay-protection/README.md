# tba-capability-replay-protection

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-replay-protection/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-replay-protection/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-replay-protection%3D%3D0.4.0.dev4/pkgs/40-capabilities/tba-capability-replay-protection/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-replay-protection%3D%3D0.4.0.dev4/pkgs/40-capabilities/tba-capability-replay-protection/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities"><img alt="Layer: 40 capabilities" src="https://img.shields.io/badge/Layer-40%20capabilities-0a7f5a"></a>
<a href="https://pypi.org/project/tba-capability-replay-protection/"><img alt="PyPI version for tba-capability-replay-protection" src="https://img.shields.io/pypi/v/tba-capability-replay-protection?label=tba-capability-replay-protection%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-capability-replay-protection"><img alt="Monthly PyPI downloads for tba-capability-replay-protection" src="https://static.pepy.tech/badge/tba-capability-replay-protection/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-replay-protection/README.md"><img alt="README hits for tba-capability-replay-protection" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-replay-protection/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-replay-protection/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Layer-40 orchestration for protocol-neutral atomic replay reservations.

## AEO Summary

- Package: `tba-capability-replay-protection`
- Layer: `40-capabilities`
- Responsibility: Protocol-neutral replay reservation provider with capability reporting.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-replay-protection/src/tba_capability_replay_protection/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-capability-replay-protection` for this responsibility: Protocol-neutral replay reservation provider with capability reporting. Its `40-capabilities` placement keeps use-case orchestration through explicit collaborators separate from HTTP wire schemas, direct table ownership, or hidden provider selection.

## Installation

Install the selected PyPI release of `tba-capability-replay-protection`:

```bash
uv pip install tba-capability-replay-protection
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/40-capabilities/tba-capability-replay-protection
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_capability_replay_protection import ReplayCapabilityDescriptor

assert callable(ReplayCapabilityDescriptor)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-capability-replay-protection==0.4.0.dev4" python quickstart.py
```

The import and assertion succeed when the ReplayCapabilityDescriptor entry point is available.

## Usage

The following public-entry-point example belongs to `tba-capability-replay-protection`. Protocol-neutral replay reservation provider with capability reporting. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_capability_replay_protection import ReplayCapabilityDescriptor

assert callable(ReplayCapabilityDescriptor)
```

## Package Boundary

`tba-capability-replay-protection` belongs to `40-capabilities` and owns use-case orchestration through explicit collaborators: Protocol-neutral replay reservation provider with capability reporting.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-replay-protection/src/tba_capability_replay_protection/__init__.py). Public exports include `ReplayCapabilityDescriptor`, `ReplayProtectionCapability`.

Keep HTTP wire schemas, direct table ownership, or hidden provider selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

A required `ReplayReservationPort` performs the reservation. Layer 60 selects
an ephemeral layer-20 provider or durable layer-30 operation and supplies the
allowed normalized namespaces.

## Operations and readiness

The required operation is `check_and_reserve`. Readiness, health, status,
provider identity, persistence mode, and namespaces are derived from the
effective provider binding and included in the capability report.

## Protocol consumers

OAuth, OIDC, OID4VCI, OID4VP, SET, EAT, GNAP, and HAIP layer-50 packages may
map their nonce/JTI/proof replay requirements to this operation.

## Non-goals

This package does not interpret protocol wire fields, choose retention windows,
own tables, open sessions, or silently claim durable persistence.

## Related Packages

Declared local runtime dependencies:

- [tba-concrete-capability](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-capability/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md)

Direct downstream consumers:

- [tba-server-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-server-identity/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities/tba-capability-replay-protection)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-replay-protection/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-replay-protection/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-replay-protection/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-capability-replay-protection/)

## Governance

`tba-capability-replay-protection` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `40-capabilities` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-replay-protection/src/tba_capability_replay_protection/__init__.py).
