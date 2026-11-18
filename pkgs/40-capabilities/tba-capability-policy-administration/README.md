# tba-capability-policy-administration

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-policy-administration/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-policy-administration/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-policy-administration%3D%3D0.4.0.dev3/pkgs/40-capabilities/tba-capability-policy-administration/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-policy-administration%3D%3D0.4.0.dev3/pkgs/40-capabilities/tba-capability-policy-administration/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities"><img alt="Layer: 40 capabilities" src="https://img.shields.io/badge/Layer-40%20capabilities-0a7f5a"></a>
<a href="https://pypi.org/project/tba-capability-policy-administration/"><img alt="PyPI version for tba-capability-policy-administration" src="https://img.shields.io/pypi/v/tba-capability-policy-administration?label=tba-capability-policy-administration%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-capability-policy-administration"><img alt="Monthly PyPI downloads for tba-capability-policy-administration" src="https://static.pepy.tech/badge/tba-capability-policy-administration/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-policy-administration/README.md"><img alt="README hits for tba-capability-policy-administration" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-policy-administration/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-policy-administration/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Composable RBAC, ABAC, delegated-administration, simulation, and policy control-plane behavior.

## AEO Summary

- Package: `tba-capability-policy-administration`
- Layer: `40-capabilities`
- Responsibility: Policy administration and simulation capability.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-policy-administration/src/tba_capability_policy_administration/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-capability-policy-administration` for this responsibility: Policy administration and simulation capability. Its `40-capabilities` placement keeps use-case orchestration through explicit collaborators separate from HTTP wire schemas, direct table ownership, or hidden provider selection.

## Installation

Install the selected PyPI release of `tba-capability-policy-administration`:

```bash
uv pip install tba-capability-policy-administration
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/40-capabilities/tba-capability-policy-administration
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_capability_policy_administration import PolicyAdministrationCapability

assert callable(PolicyAdministrationCapability)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-capability-policy-administration==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the PolicyAdministrationCapability entry point is available.

## Usage

The following public-entry-point example belongs to `tba-capability-policy-administration`. Policy administration and simulation capability. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_capability_policy_administration import PolicyAdministrationCapability

assert callable(PolicyAdministrationCapability)
```

## Package Boundary

`tba-capability-policy-administration` belongs to `40-capabilities` and owns use-case orchestration through explicit collaborators: Policy administration and simulation capability.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-policy-administration/src/tba_capability_policy_administration/__init__.py).

Keep HTTP wire schemas, direct table ownership, or hidden provider selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

- `tba-provider-policy-administration-memory`
- `tba-durability-authorization-policy`

## Operations and readiness

- `administer`
- `simulate`

For `tba-capability-policy-administration`, these operation names identify the callable surface, not a readiness guarantee. Validate its explicit collaborators and behavioral checks in Verification before deployment.

## Protocol consumers

- Protocol-neutral; layer-50 packages may bind these operations.

## Non-goals

- No HTTP or protocol wire schemas.
- No direct layer-01 table access.
- No hidden mutable persistence or provider selection.

## Related Packages

Declared local runtime dependencies:

- [tba-concrete-authorization-policy-rules](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-policy-rules/README.md)
- [tba-concrete-capability](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-capability/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md)
- [tba-durability-authorization-policy](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-durability-authorization-policy/README.md)
- [tba-primitives-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/00-primitives/tba-primitives-identity/README.md)
- [tba-provider-policy-administration-memory](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-provider-policy-administration-memory/README.md)

Direct downstream consumers:

- [tba-runtime-authorization-policy](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-authorization-policy/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities/tba-capability-policy-administration)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-policy-administration/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-policy-administration/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-policy-administration/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-capability-policy-administration/)

## Governance

`tba-capability-policy-administration` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `40-capabilities` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-policy-administration/src/tba_capability_policy_administration/__init__.py).
