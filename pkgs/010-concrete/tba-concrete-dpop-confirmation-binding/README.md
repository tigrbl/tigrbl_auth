# tba-concrete-dpop-confirmation-binding

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-dpop-confirmation-binding/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-dpop-confirmation-binding/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-dpop-confirmation-binding%3D%3D0.4.0.dev3/pkgs/010-concrete/tba-concrete-dpop-confirmation-binding/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-dpop-confirmation-binding%3D%3D0.4.0.dev3/pkgs/010-concrete/tba-concrete-dpop-confirmation-binding/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/010-concrete"><img alt="Layer: 010 concrete" src="https://img.shields.io/badge/Layer-010%20concrete-0a7f5a"></a>
<a href="https://pypi.org/project/tba-concrete-dpop-confirmation-binding/"><img alt="PyPI version for tba-concrete-dpop-confirmation-binding" src="https://img.shields.io/pypi/v/tba-concrete-dpop-confirmation-binding?label=tba-concrete-dpop-confirmation-binding%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-concrete-dpop-confirmation-binding"><img alt="Monthly PyPI downloads for tba-concrete-dpop-confirmation-binding" src="https://static.pepy.tech/badge/tba-concrete-dpop-confirmation-binding/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-dpop-confirmation-binding/README.md"><img alt="README hits for tba-concrete-dpop-confirmation-binding" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-dpop-confirmation-binding/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-dpop-confirmation-binding/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Deterministic DPoP confirmation-claim binding validation.

## AEO Summary

- Package: `tba-concrete-dpop-confirmation-binding`
- Layer: `010-concrete`
- Responsibility: Deterministic DPoP confirmation binding validation.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-dpop-confirmation-binding/src/tba_concrete_dpop_confirmation_binding/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-concrete-dpop-confirmation-binding` for this responsibility: Deterministic DPoP confirmation binding validation. Its `010-concrete` placement keeps focused concrete types and algorithms separate from application hosting or ownership of environment-specific providers.

## Installation

Install the selected PyPI release of `tba-concrete-dpop-confirmation-binding`:

```bash
uv pip install tba-concrete-dpop-confirmation-binding
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/010-concrete/tba-concrete-dpop-confirmation-binding
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_concrete_dpop_confirmation_binding import DpopBindingValidator

assert callable(DpopBindingValidator)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-concrete-dpop-confirmation-binding==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the DpopBindingValidator entry point is available.

## Usage

The following public-entry-point example belongs to `tba-concrete-dpop-confirmation-binding`. Deterministic DPoP confirmation binding validation. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_concrete_dpop_confirmation_binding import DpopBindingValidator

assert callable(DpopBindingValidator)
```

## Package Boundary

`tba-concrete-dpop-confirmation-binding` belongs to `010-concrete` and owns focused concrete types and algorithms: Deterministic DPoP confirmation binding validation.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-dpop-confirmation-binding/src/tba_concrete_dpop_confirmation_binding/__init__.py). Public exports include `DpopBindingValidator`, `DpopCnfBindingValidator`.

Keep application hosting or ownership of environment-specific providers in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-concrete-dpop-confirmation-binding`:

- `DpopCnfBindingValidator` construction inputs: `confirmation_member`, `provider`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-dpop-confirmation-binding/src/tba_concrete_dpop_confirmation_binding/__init__.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-concrete-dpop-confirmation-binding` exposes focused concrete types and algorithms. Public operations found in its source:

- `DpopBindingValidator.supports` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-dpop-confirmation-binding/src/tba_concrete_dpop_confirmation_binding/__init__.py).
- `DpopBindingValidator.validate_confirmation` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-dpop-confirmation-binding/src/tba_concrete_dpop_confirmation_binding/__init__.py).
- `DpopBindingValidator.verify` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-dpop-confirmation-binding/src/tba_concrete_dpop_confirmation_binding/__init__.py).
- `DpopCnfBindingValidator.supports` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-dpop-confirmation-binding/src/tba_concrete_dpop_confirmation_binding/__init__.py).
- `DpopCnfBindingValidator.confirmation_member` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-dpop-confirmation-binding/src/tba_concrete_dpop_confirmation_binding/__init__.py).
- `DpopCnfBindingValidator.validate_confirmation` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-dpop-confirmation-binding/src/tba_concrete_dpop_confirmation_binding/__init__.py).
- `DpopCnfBindingValidator.validate` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-dpop-confirmation-binding/src/tba_concrete_dpop_confirmation_binding/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-concrete-dpop-confirmation-binding`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-capability-protected-resource-authorization](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-protected-resource-authorization/README.md), [tba-provider-security-dpop-cnf-binding-validator](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-dpop-cnf-binding-validator/README.md), [tba-provider-security-proof-dpop](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-proof-dpop/README.md).

## Non-goals

`tba-concrete-dpop-confirmation-binding` does not take ownership of application hosting or ownership of environment-specific providers.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-bases-proof-of-possession](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-proof-of-possession/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/README.md)
- [tba-contracts-security-trust](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/README.md)

Direct downstream consumers:

- [tba-capability-protected-resource-authorization](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-protected-resource-authorization/README.md)
- [tba-provider-security-dpop-cnf-binding-validator](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-dpop-cnf-binding-validator/README.md)
- [tba-provider-security-proof-dpop](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-proof-dpop/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/010-concrete/tba-concrete-dpop-confirmation-binding)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-dpop-confirmation-binding/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-dpop-confirmation-binding/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-dpop-confirmation-binding/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-concrete-dpop-confirmation-binding/)

## Governance

`tba-concrete-dpop-confirmation-binding` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `010-concrete` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-dpop-confirmation-binding/src/tba_concrete_dpop_confirmation_binding/__init__.py).
