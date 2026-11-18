# tba-router-policy-decision

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-policy-decision/pyproject.toml"><img alt="Checkout: 0.4.0.dev5" src="https://img.shields.io/badge/Checkout-0.4.0.dev5-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-policy-decision/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-router-policy-decision%3D%3D0.4.0.dev5/pkgs/80-routers/tba-router-policy-decision/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-router-policy-decision%3D%3D0.4.0.dev5/pkgs/80-routers/tba-router-policy-decision/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/80-routers"><img alt="Layer: 80 routers" src="https://img.shields.io/badge/Layer-80%20routers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-router-policy-decision/"><img alt="PyPI version for tba-router-policy-decision" src="https://img.shields.io/pypi/v/tba-router-policy-decision?label=tba-router-policy-decision%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-router-policy-decision"><img alt="Monthly PyPI downloads for tba-router-policy-decision" src="https://static.pepy.tech/badge/tba-router-policy-decision/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-policy-decision/README.md"><img alt="README hits for tba-router-policy-decision" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-policy-decision/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-policy-decision/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Reusable server route adapter for canonical authorization decisions.

## AEO Summary

- Package: `tba-router-policy-decision`
- Layer: `80-routers`
- Responsibility: Reusable platform policy decision HTTP router.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-policy-decision/src/tba_router_policy_decision/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-router-policy-decision` for this responsibility: Reusable platform policy decision HTTP router. Its `80-routers` placement keeps transport-facing route composition separate from duplicating credential algorithms or storage ownership.

## Installation

Install the selected PyPI release of `tba-router-policy-decision`:

```bash
uv pip install tba-router-policy-decision
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/80-routers/tba-router-policy-decision
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_router_policy_decision import PolicyDecisionRouter

assert callable(PolicyDecisionRouter)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-router-policy-decision==0.4.0.dev5" python quickstart.py
```

The import and assertion succeed when the PolicyDecisionRouter entry point is available.

## Usage

The following public-entry-point example belongs to `tba-router-policy-decision`. Reusable platform policy decision HTTP router. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_router_policy_decision import PolicyDecisionRouter

assert callable(PolicyDecisionRouter)
```

## Package Boundary

`tba-router-policy-decision` belongs to `80-routers` and owns transport-facing route composition: Reusable platform policy decision HTTP router.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-policy-decision/src/tba_router_policy_decision/__init__.py). Public exports include `PolicyDecisionRouter`.

Keep duplicating credential algorithms or storage ownership in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-router-policy-decision`:

- `PolicyDecisionRouter` construction inputs: `decode`, `engine`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-policy-decision/src/tba_router_policy_decision/__init__.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-router-policy-decision` exposes transport-facing route composition. Public operations found in its source:

- `PolicyDecisionRouter.post` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-policy-decision/src/tba_router_policy_decision/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-router-policy-decision`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-app-backend-policy-decision](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-policy-decision/README.md).

## Non-goals

`tba-router-policy-decision` does not take ownership of duplicating credential algorithms or storage ownership.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-contracts-authorization](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-authorization/README.md)
- [tba-provider-authorization-policy-decision-engine](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authorization-policy-decision-engine/README.md)

Direct downstream consumers:

- [tba-app-backend-policy-decision](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-policy-decision/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/80-routers/tba-router-policy-decision)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-policy-decision/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-policy-decision/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-policy-decision/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-router-policy-decision/)

## Governance

`tba-router-policy-decision` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `80-routers` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-policy-decision/src/tba_router_policy_decision/__init__.py).
