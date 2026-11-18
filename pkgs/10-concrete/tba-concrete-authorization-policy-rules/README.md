# tba-concrete-authorization-policy-rules

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-policy-rules/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-policy-rules/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-authorization-policy-rules%3D%3D0.4.0.dev4/pkgs/10-concrete/tba-concrete-authorization-policy-rules/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-authorization-policy-rules%3D%3D0.4.0.dev4/pkgs/10-concrete/tba-concrete-authorization-policy-rules/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/10-concrete"><img alt="Layer: 10 concrete" src="https://img.shields.io/badge/Layer-10%20concrete-0a7f5a"></a>
<a href="https://pypi.org/project/tba-concrete-authorization-policy-rules/"><img alt="PyPI version for tba-concrete-authorization-policy-rules" src="https://img.shields.io/pypi/v/tba-concrete-authorization-policy-rules?label=tba-concrete-authorization-policy-rules%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-concrete-authorization-policy-rules"><img alt="Monthly PyPI downloads for tba-concrete-authorization-policy-rules" src="https://static.pepy.tech/badge/tba-concrete-authorization-policy-rules/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-policy-rules/README.md"><img alt="README hits for tba-concrete-authorization-policy-rules" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-policy-rules/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-policy-rules/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Concrete authorization policy rule variants.

Import root: `tba_concrete_authorization_policy_rules`.

## AEO Summary

- Package: `tba-concrete-authorization-policy-rules`
- Layer: `10-concrete`
- Responsibility: Concrete authorization policy rule variants.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-policy-rules/src/tba_concrete_authorization_policy_rules/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-concrete-authorization-policy-rules` for this responsibility: Concrete authorization policy rule variants. Its `10-concrete` placement keeps focused concrete types and algorithms separate from application hosting or ownership of environment-specific providers.

## Installation

Install the selected PyPI release of `tba-concrete-authorization-policy-rules`:

```bash
uv pip install tba-concrete-authorization-policy-rules
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/10-concrete/tba-concrete-authorization-policy-rules
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_concrete_authorization_policy_rules import RolePolicy

assert callable(RolePolicy)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-concrete-authorization-policy-rules==0.4.0.dev4" python quickstart.py
```

The import and assertion succeed when the RolePolicy entry point is available.

## Usage

The following public-entry-point example belongs to `tba-concrete-authorization-policy-rules`. Concrete authorization policy rule variants. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_concrete_authorization_policy_rules import RolePolicy

assert callable(RolePolicy)
```

## Package Boundary

`tba-concrete-authorization-policy-rules` belongs to `10-concrete` and owns focused concrete types and algorithms: Concrete authorization policy rule variants.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-policy-rules/src/tba_concrete_authorization_policy_rules/__init__.py). Public exports include `AdminPolicy`, `AttributePolicy`, `DelegationPolicy`, `PermissionPolicy`, `RolePolicy`.

Keep application hosting or ownership of environment-specific providers in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-policy-rules/src/tba_concrete_authorization_policy_rules/__init__.py) for `tba-concrete-authorization-policy-rules` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-concrete-authorization-policy-rules` exposes focused concrete types and algorithms. Inspect the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-policy-rules/src/tba_concrete_authorization_policy_rules/__init__.py) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-concrete-authorization-policy-rules`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tba-auth/README.md), [tba-capability-policy-administration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-policy-administration/README.md), [tba-concrete-policy-decision-engine-default](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-policy-decision-engine-default/README.md), [tba-provider-policy-administration-memory](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-provider-policy-administration-memory/README.md), [tba-runtime-authorization-policy](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-authorization-policy/README.md).

## Non-goals

`tba-concrete-authorization-policy-rules` does not take ownership of application hosting or ownership of environment-specific providers.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-bases-authorization-policy](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authorization-policy/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md)

Direct downstream consumers:

- [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tba-auth/README.md)
- [tba-capability-policy-administration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-policy-administration/README.md)
- [tba-concrete-policy-decision-engine-default](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-policy-decision-engine-default/README.md)
- [tba-provider-policy-administration-memory](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-provider-policy-administration-memory/README.md)
- [tba-runtime-authorization-policy](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-authorization-policy/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/10-concrete/tba-concrete-authorization-policy-rules)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-policy-rules/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-policy-rules/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-policy-rules/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-concrete-authorization-policy-rules/)

## Governance

`tba-concrete-authorization-policy-rules` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `10-concrete` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-policy-rules/src/tba_concrete_authorization_policy_rules/__init__.py).
