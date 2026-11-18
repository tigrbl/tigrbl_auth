# tba-concrete-authorization-policy-obligations

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-policy-obligations/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-policy-obligations/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-authorization-policy-obligations%3D%3D0.4.0.dev4/pkgs/10-concrete/tba-concrete-authorization-policy-obligations/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-authorization-policy-obligations%3D%3D0.4.0.dev4/pkgs/10-concrete/tba-concrete-authorization-policy-obligations/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/10-concrete"><img alt="Layer: 10 concrete" src="https://img.shields.io/badge/Layer-10%20concrete-0a7f5a"></a>
<a href="https://pypi.org/project/tba-concrete-authorization-policy-obligations/"><img alt="PyPI version for tba-concrete-authorization-policy-obligations" src="https://img.shields.io/pypi/v/tba-concrete-authorization-policy-obligations?label=tba-concrete-authorization-policy-obligations%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-concrete-authorization-policy-obligations"><img alt="Monthly PyPI downloads for tba-concrete-authorization-policy-obligations" src="https://static.pepy.tech/badge/tba-concrete-authorization-policy-obligations/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-policy-obligations/README.md"><img alt="README hits for tba-concrete-authorization-policy-obligations" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-policy-obligations/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-policy-obligations/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

No-op and collecting authorization policy obligation and advice handlers.

Import root: `tba_concrete_authorization_policy_obligations`.

## AEO Summary

- Package: `tba-concrete-authorization-policy-obligations`
- Layer: `10-concrete`
- Responsibility: No-op and collecting authorization policy obligation and advice handlers.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-policy-obligations/src/tba_concrete_authorization_policy_obligations/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-concrete-authorization-policy-obligations` for this responsibility: No-op and collecting authorization policy obligation and advice handlers. Its `10-concrete` placement keeps focused concrete types and algorithms separate from application hosting or ownership of environment-specific providers.

## Installation

Install the selected PyPI release of `tba-concrete-authorization-policy-obligations`:

```bash
uv pip install tba-concrete-authorization-policy-obligations
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/10-concrete/tba-concrete-authorization-policy-obligations
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_concrete_authorization_policy_obligations import NoopObligationHandler

assert callable(NoopObligationHandler)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-concrete-authorization-policy-obligations==0.4.0.dev4" python quickstart.py
```

The import and assertion succeed when the NoopObligationHandler entry point is available.

## Usage

The following public-entry-point example belongs to `tba-concrete-authorization-policy-obligations`. No-op and collecting authorization policy obligation and advice handlers. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_concrete_authorization_policy_obligations import NoopObligationHandler

assert callable(NoopObligationHandler)
```

## Package Boundary

`tba-concrete-authorization-policy-obligations` belongs to `10-concrete` and owns focused concrete types and algorithms: No-op and collecting authorization policy obligation and advice handlers.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-policy-obligations/src/tba_concrete_authorization_policy_obligations/__init__.py). Public exports include `CollectingAdviceHandler`, `CollectingObligationHandler`, `NoopAdviceHandler`, `NoopObligationHandler`.

Keep application hosting or ownership of environment-specific providers in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-policy-obligations/src/tba_concrete_authorization_policy_obligations/__init__.py) for `tba-concrete-authorization-policy-obligations` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-concrete-authorization-policy-obligations` exposes focused concrete types and algorithms. Public operations found in its source:

- `NoopObligationHandler.handle_obligation` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-policy-obligations/src/tba_concrete_authorization_policy_obligations/__init__.py).
- `NoopAdviceHandler.handle_advice` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-policy-obligations/src/tba_concrete_authorization_policy_obligations/__init__.py).
- `CollectingObligationHandler.handle_obligation` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-policy-obligations/src/tba_concrete_authorization_policy_obligations/__init__.py).
- `CollectingAdviceHandler.handle_advice` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-policy-obligations/src/tba_concrete_authorization_policy_obligations/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-concrete-authorization-policy-obligations`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tba-auth/README.md).

## Non-goals

`tba-concrete-authorization-policy-obligations` does not take ownership of application hosting or ownership of environment-specific providers.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-bases-authorization-policy](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authorization-policy/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md)

Direct downstream consumers:

- [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tba-auth/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/10-concrete/tba-concrete-authorization-policy-obligations)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-policy-obligations/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-policy-obligations/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-policy-obligations/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-concrete-authorization-policy-obligations/)

## Governance

`tba-concrete-authorization-policy-obligations` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `10-concrete` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-policy-obligations/src/tba_concrete_authorization_policy_obligations/__init__.py).
