# tba-bases-authorization-policy

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authorization-policy/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authorization-policy/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-bases-authorization-policy%3D%3D0.4.0.dev3/pkgs/05-bases/tba-bases-authorization-policy/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-bases-authorization-policy%3D%3D0.4.0.dev3/pkgs/05-bases/tba-bases-authorization-policy/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/05-bases"><img alt="Layer: 05 bases" src="https://img.shields.io/badge/Layer-05%20bases-0a7f5a"></a>
<a href="https://pypi.org/project/tba-bases-authorization-policy/"><img alt="PyPI version for tba-bases-authorization-policy" src="https://img.shields.io/pypi/v/tba-bases-authorization-policy?label=tba-bases-authorization-policy%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-bases-authorization-policy"><img alt="Monthly PyPI downloads for tba-bases-authorization-policy" src="https://static.pepy.tech/badge/tba-bases-authorization-policy/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authorization-policy/README.md"><img alt="README hits for tba-bases-authorization-policy" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authorization-policy/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authorization-policy/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Base classes connecting policy implementations to authorization contracts.

## AEO Summary

- Package: `tba-bases-authorization-policy`
- Layer: `05-bases`
- Responsibility: Base classes for concrete TBAorization policy implementations.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authorization-policy/src/tba_bases_authorization_policy/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-bases-authorization-policy` for this responsibility: Base classes for concrete TBAorization policy implementations. Its `05-bases` placement keeps reusable component bases separate from deployment composition or implicit provider selection.

## Installation

Install the selected PyPI release of `tba-bases-authorization-policy`:

```bash
uv pip install tba-bases-authorization-policy
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/05-bases/tba-bases-authorization-policy
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_bases_authorization_policy import ScopeMatcherBase

assert callable(ScopeMatcherBase)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-bases-authorization-policy==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the ScopeMatcherBase entry point is available.

## Usage

The following public-entry-point example belongs to `tba-bases-authorization-policy`. Base classes for concrete TBAorization policy implementations. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_bases_authorization_policy import ScopeMatcherBase

assert callable(ScopeMatcherBase)
```

## Package Boundary

`tba-bases-authorization-policy` belongs to `05-bases` and owns reusable component bases: Base classes for concrete TBAorization policy implementations.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authorization-policy/src/tba_bases_authorization_policy/__init__.py). Public exports include `AdviceHandlerBase`, `AuthzenEvaluationAdapterBase`, `AuthzenSearchAdapterBase`, `AttributeResolverBase`, `AttributeSelectorBase`, `ConditionEvaluatorBase`, `ObligationHandlerBase`, `PolicyCombinerBase`, `PolicyRuleBase`, `RuleEvaluatorBase`, `ScopeMatcherBase`, `XacmlRequestMapperBase`.

Keep deployment composition or implicit provider selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authorization-policy/src/tba_bases_authorization_policy/__init__.py) for `tba-bases-authorization-policy` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-bases-authorization-policy` exposes reusable component bases. Public operations found in its source:

- `ScopeMatcherBase.match` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authorization-policy/src/tba_bases_authorization_policy/__init__.py).
- `AttributeResolverBase.resolve` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authorization-policy/src/tba_bases_authorization_policy/__init__.py).
- `AttributeSelectorBase.select` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authorization-policy/src/tba_bases_authorization_policy/__init__.py).
- `PolicyCombinerBase.combine` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authorization-policy/src/tba_bases_authorization_policy/__init__.py).
- `ConditionEvaluatorBase.evaluate_condition` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authorization-policy/src/tba_bases_authorization_policy/__init__.py).
- `RuleEvaluatorBase.evaluate_rule` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authorization-policy/src/tba_bases_authorization_policy/__init__.py).
- `ObligationHandlerBase.handle_obligation` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authorization-policy/src/tba_bases_authorization_policy/__init__.py).
- `AdviceHandlerBase.handle_advice` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authorization-policy/src/tba_bases_authorization_policy/__init__.py).
- `AuthzenEvaluationAdapterBase.evaluate` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authorization-policy/src/tba_bases_authorization_policy/interop.py).
- `AuthzenSearchAdapterBase.search` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authorization-policy/src/tba_bases_authorization_policy/interop.py).
- `XacmlRequestMapperBase.map_request` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authorization-policy/src/tba_bases_authorization_policy/interop.py).
- `XacmlResponseMapperBase.map_response` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authorization-policy/src/tba_bases_authorization_policy/interop.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-bases-authorization-policy`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-concrete-authorization-policy-attributes-mapping](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-policy-attributes-mapping/README.md), [tba-concrete-authorization-policy-combiner-default](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-policy-combiner-default/README.md), [tba-concrete-authorization-policy-evaluators-default](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-policy-evaluators-default/README.md), [tba-concrete-authorization-policy-obligations](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-policy-obligations/README.md), [tba-concrete-authorization-policy-rules](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-policy-rules/README.md), [tba-concrete-authorization-scope-set-matcher](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-scope-set-matcher/README.md).

## Non-goals

`tba-bases-authorization-policy` does not take ownership of deployment composition or implicit provider selection.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md)

Direct downstream consumers:

- [tba-concrete-authorization-policy-attributes-mapping](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-policy-attributes-mapping/README.md)
- [tba-concrete-authorization-policy-combiner-default](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-policy-combiner-default/README.md)
- [tba-concrete-authorization-policy-evaluators-default](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-policy-evaluators-default/README.md)
- [tba-concrete-authorization-policy-obligations](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-policy-obligations/README.md)
- [tba-concrete-authorization-policy-rules](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-policy-rules/README.md)
- [tba-concrete-authorization-scope-set-matcher](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-scope-set-matcher/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/05-bases/tba-bases-authorization-policy)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authorization-policy/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authorization-policy/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authorization-policy/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-bases-authorization-policy/)

## Governance

`tba-bases-authorization-policy` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `05-bases` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authorization-policy/src/tba_bases_authorization_policy/__init__.py).
