# tba-capability-workload-credential-brokering

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-workload-credential-brokering/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-workload-credential-brokering/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-workload-credential-brokering%3D%3D0.4.0.dev3/pkgs/040-capabilities/tba-capability-workload-credential-brokering/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-workload-credential-brokering%3D%3D0.4.0.dev3/pkgs/040-capabilities/tba-capability-workload-credential-brokering/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/040-capabilities"><img alt="Layer: 040 capabilities" src="https://img.shields.io/badge/Layer-040%20capabilities-0a7f5a"></a>
<a href="https://pypi.org/project/tba-capability-workload-credential-brokering/"><img alt="PyPI version for tba-capability-workload-credential-brokering" src="https://img.shields.io/pypi/v/tba-capability-workload-credential-brokering?label=tba-capability-workload-credential-brokering%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-capability-workload-credential-brokering"><img alt="Monthly PyPI downloads for tba-capability-workload-credential-brokering" src="https://static.pepy.tech/badge/tba-capability-workload-credential-brokering/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-workload-credential-brokering/README.md"><img alt="README hits for tba-capability-workload-credential-brokering" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-workload-credential-brokering/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-workload-credential-brokering/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Independently mountable, carrier-neutral capability. Layer 50 maps its operations into versioned protocols.

## AEO Summary

- Package: `tba-capability-workload-credential-brokering`
- Layer: `040-capabilities`
- Responsibility: Delegated workload credential brokering capability.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-workload-credential-brokering/src/tba_capability_workload_credential_brokering/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-capability-workload-credential-brokering` for this responsibility: Delegated workload credential brokering capability. Its `040-capabilities` placement keeps use-case orchestration through explicit collaborators separate from HTTP wire schemas, direct table ownership, or hidden provider selection.

## Installation

Install the selected PyPI release of `tba-capability-workload-credential-brokering`:

```bash
uv pip install tba-capability-workload-credential-brokering
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/040-capabilities/tba-capability-workload-credential-brokering
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_capability_workload_credential_brokering import WorkloadCredentialBrokeringCapability

assert callable(WorkloadCredentialBrokeringCapability)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-capability-workload-credential-brokering==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the WorkloadCredentialBrokeringCapability entry point is available.

## Usage

The following public-entry-point example belongs to `tba-capability-workload-credential-brokering`. Delegated workload credential brokering capability. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_capability_workload_credential_brokering import WorkloadCredentialBrokeringCapability

assert callable(WorkloadCredentialBrokeringCapability)
```

## Package Boundary

`tba-capability-workload-credential-brokering` belongs to `040-capabilities` and owns use-case orchestration through explicit collaborators: Delegated workload credential brokering capability.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-workload-credential-brokering/src/tba_capability_workload_credential_brokering/__init__.py). Public exports include `WorkloadCredentialBrokeringCapability`.

Keep HTTP wire schemas, direct table ownership, or hidden provider selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

- No package-mandated runtime dependency; callables are constructor-injected.

## Operations and readiness

- `authorize_delegated_credential_access`
- `obtain_delegated_workload_credentials`
- `resolve_delegated_workload_trust`
- `resolve_workload_reference`
- `watch_delegated_workload_credentials`

For `tba-capability-workload-credential-brokering`, these operation names identify the callable surface, not a readiness guarantee. Validate its explicit collaborators and behavioral checks in Verification before deployment.

## Protocol consumers

- Protocol-neutral; layer-50 packages may bind these operations.

## Non-goals

- No HTTP or protocol wire schemas.
- No direct layer-01 table access.
- No hidden mutable persistence or provider selection.

## Related Packages

Declared local runtime dependencies:

- [tba-concrete-capability](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-capability/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/README.md)
- [tba-contracts-workload-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/040-capabilities/tba-capability-workload-credential-brokering)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-workload-credential-brokering/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-workload-credential-brokering/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-workload-credential-brokering/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-capability-workload-credential-brokering/)

## Governance

`tba-capability-workload-credential-brokering` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `040-capabilities` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-workload-credential-brokering/src/tba_capability_workload_credential_brokering/__init__.py).
