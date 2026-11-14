# tba-capability-policy-evaluation

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-policy-evaluation/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-policy-evaluation/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-policy-evaluation/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities"><img alt="Layer: 40 capabilities" src="https://img.shields.io/badge/Layer-40%20capabilities-0a7f5a"></a>
<a href="https://pypi.org/project/tba-capability-policy-evaluation/"><img alt="PyPI version for tba-capability-policy-evaluation" src="https://img.shields.io/pypi/v/tba-capability-policy-evaluation?label=tba-capability-policy-evaluation%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-capability-policy-evaluation"><img alt="Monthly PyPI downloads for tba-capability-policy-evaluation" src="https://static.pepy.tech/badge/tba-capability-policy-evaluation/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-policy-evaluation/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Layer-40 protocol-neutral composition for policy evaluation, batch evaluation,
entity search, and effective policy-service description.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_capability_policy_evaluation import PolicyEvaluationCapability

assert callable(PolicyEvaluationCapability)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-capability-policy-evaluation==0.4.0.dev2" python quickstart.py
```

The import and assertion succeed when the PolicyEvaluationCapability entry point is available.

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

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-policy-evaluation/src/tba_capability_policy_evaluation/__init__.py).
