# tba-concrete-policy-decision-engine-default

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-policy-decision-engine-default/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-policy-decision-engine-default/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-policy-decision-engine-default%3D%3D0.4.0.dev3/pkgs/10-concrete/tba-concrete-policy-decision-engine-default/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-policy-decision-engine-default%3D%3D0.4.0.dev3/pkgs/10-concrete/tba-concrete-policy-decision-engine-default/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/10-concrete"><img alt="Layer: 10 concrete" src="https://img.shields.io/badge/Layer-10%20concrete-0a7f5a"></a>
<a href="https://pypi.org/project/tba-concrete-policy-decision-engine-default/"><img alt="PyPI version for tba-concrete-policy-decision-engine-default" src="https://img.shields.io/pypi/v/tba-concrete-policy-decision-engine-default?label=tba-concrete-policy-decision-engine-default%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-concrete-policy-decision-engine-default"><img alt="Monthly PyPI downloads for tba-concrete-policy-decision-engine-default" src="https://static.pepy.tech/badge/tba-concrete-policy-decision-engine-default/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-policy-decision-engine-default/README.md"><img alt="README hits for tba-concrete-policy-decision-engine-default" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-policy-decision-engine-default/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-policy-decision-engine-default/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Deterministic default RBAC, ABAC, PBAC, delegation, and administration decision engine.

## AEO Summary

- Package: `tba-concrete-policy-decision-engine-default`
- Layer: `10-concrete`
- Responsibility: Deterministic default authorization policy decision engine.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-policy-decision-engine-default/src/tba_concrete_policy_decision_engine_default/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-concrete-policy-decision-engine-default` for this responsibility: Deterministic default authorization policy decision engine. Its `10-concrete` placement keeps focused concrete types and algorithms separate from application hosting or ownership of environment-specific providers.

## Installation

Install the selected PyPI release of `tba-concrete-policy-decision-engine-default`:

```bash
uv pip install tba-concrete-policy-decision-engine-default
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/10-concrete/tba-concrete-policy-decision-engine-default
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_concrete_policy_decision_engine_default import AdminPolicy

assert callable(AdminPolicy)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-concrete-policy-decision-engine-default==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the AdminPolicy entry point is available.

## Usage

The following public-entry-point example belongs to `tba-concrete-policy-decision-engine-default`. Deterministic default authorization policy decision engine. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_concrete_policy_decision_engine_default import AdminPolicy

assert callable(AdminPolicy)
```

## Package Boundary

`tba-concrete-policy-decision-engine-default` belongs to `10-concrete` and owns focused concrete types and algorithms: Deterministic default authorization policy decision engine.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-policy-decision-engine-default/src/tba_concrete_policy_decision_engine_default/__init__.py).

Keep application hosting or ownership of environment-specific providers in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-policy-decision-engine-default/src/tba_concrete_policy_decision_engine_default/__init__.py) for `tba-concrete-policy-decision-engine-default` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-concrete-policy-decision-engine-default` exposes focused concrete types and algorithms. Inspect the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-policy-decision-engine-default/src/tba_concrete_policy_decision_engine_default/__init__.py) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-concrete-policy-decision-engine-default`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-provider-authorization-policy-decision-engine](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authorization-policy-decision-engine/README.md), [tba-runtime-authorization-policy](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-authorization-policy/README.md).

## Non-goals

`tba-concrete-policy-decision-engine-default` does not take ownership of application hosting or ownership of environment-specific providers.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-concrete-authorization-policy-rules](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-policy-rules/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md)
- [tba-primitives-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/00-primitives/tba-primitives-identity/README.md)

Direct downstream consumers:

- [tba-provider-authorization-policy-decision-engine](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authorization-policy-decision-engine/README.md)
- [tba-runtime-authorization-policy](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-authorization-policy/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/10-concrete/tba-concrete-policy-decision-engine-default)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-policy-decision-engine-default/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-policy-decision-engine-default/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-policy-decision-engine-default/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-concrete-policy-decision-engine-default/)

## Governance

`tba-concrete-policy-decision-engine-default` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `10-concrete` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-policy-decision-engine-default/src/tba_concrete_policy_decision_engine_default/__init__.py).
