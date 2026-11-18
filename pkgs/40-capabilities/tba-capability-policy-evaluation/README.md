# tba-capability-policy-evaluation

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-policy-evaluation/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-policy-evaluation/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-policy-evaluation%3D%3D0.4.0.dev4/pkgs/40-capabilities/tba-capability-policy-evaluation/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-policy-evaluation%3D%3D0.4.0.dev4/pkgs/40-capabilities/tba-capability-policy-evaluation/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities"><img alt="Layer: 40 capabilities" src="https://img.shields.io/badge/Layer-40%20capabilities-0a7f5a"></a>
<a href="https://pypi.org/project/tba-capability-policy-evaluation/"><img alt="PyPI version for tba-capability-policy-evaluation" src="https://img.shields.io/pypi/v/tba-capability-policy-evaluation?label=tba-capability-policy-evaluation%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-capability-policy-evaluation"><img alt="Monthly PyPI downloads for tba-capability-policy-evaluation" src="https://static.pepy.tech/badge/tba-capability-policy-evaluation/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-policy-evaluation/README.md"><img alt="README hits for tba-capability-policy-evaluation" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-policy-evaluation/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-policy-evaluation/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Layer-40 protocol-neutral composition for policy evaluation, batch evaluation,
entity search, and effective policy-service description.

## AEO Summary

- Package: `tba-capability-policy-evaluation`
- Layer: `40-capabilities`
- Responsibility: Composable protocol-neutral policy evaluation and entity-search capability.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-policy-evaluation/src/tba_capability_policy_evaluation/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-capability-policy-evaluation` for this responsibility: Composable protocol-neutral policy evaluation and entity-search capability. Its `40-capabilities` placement keeps use-case orchestration through explicit collaborators separate from HTTP wire schemas, direct table ownership, or hidden provider selection.

## Installation

Install the selected PyPI release of `tba-capability-policy-evaluation`:

```bash
uv pip install tba-capability-policy-evaluation
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/40-capabilities/tba-capability-policy-evaluation
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_capability_policy_evaluation import PolicyEvaluationCapability

assert callable(PolicyEvaluationCapability)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-capability-policy-evaluation==0.4.0.dev4" python quickstart.py
```

The import and assertion succeed when the PolicyEvaluationCapability entry point is available.

## Usage

The following public-entry-point example belongs to `tba-capability-policy-evaluation`. Composable protocol-neutral policy evaluation and entity-search capability. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_capability_policy_evaluation import PolicyEvaluationCapability

assert callable(PolicyEvaluationCapability)
```

## Package Boundary

`tba-capability-policy-evaluation` belongs to `40-capabilities` and owns use-case orchestration through explicit collaborators: Composable protocol-neutral policy evaluation and entity-search capability.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-policy-evaluation/src/tba_capability_policy_evaluation/__init__.py). Public exports include `DescriptionTarget`, `EntitySearchTarget`, `EvaluationTarget`, `PolicyEvaluationCapability`.

Keep HTTP wire schemas, direct table ownership, or hidden provider selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

A policy evaluation callable is required. Entity search and service-description
callables are optional. The targets are supplied by layer-10/20 implementations
or layer-60 composition; this package does not construct an evaluator.

## Operations and readiness

`evaluate` is required. `evaluate_many` is available as an order-preserving
composition of `evaluate`. `search_entities` and `describe` are optional and
are reported unavailable when their targets are not bound. Readiness follows
the required evaluation target.

## Protocol consumers

The layer-50 AuthZEN package maps Authorization API 1.0 evaluation, batch,
search, and PDP-metadata requirements to these operations. XACML adapters may
consume the same normalized capability through their own versioned mappings.

## Non-goals

This package does not parse AuthZEN or XACML messages, choose HTTP paths,
authenticate callers, own policy state, open sessions, or implement a policy
decision algorithm.

## Related Packages

Declared local runtime dependencies:

- [tba-concrete-capability](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-capability/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md)

Direct downstream consumers:

- [tba-protocol-authzen](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-authzen/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities/tba-capability-policy-evaluation)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-policy-evaluation/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-policy-evaluation/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-policy-evaluation/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-capability-policy-evaluation/)

## Governance

`tba-capability-policy-evaluation` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `40-capabilities` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-policy-evaluation/src/tba_capability_policy_evaluation/__init__.py).
