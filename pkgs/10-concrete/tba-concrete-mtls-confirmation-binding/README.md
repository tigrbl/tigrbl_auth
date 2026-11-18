# tba-concrete-mtls-confirmation-binding

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-mtls-confirmation-binding/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-mtls-confirmation-binding/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-mtls-confirmation-binding%3D%3D0.4.0.dev4/pkgs/10-concrete/tba-concrete-mtls-confirmation-binding/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-mtls-confirmation-binding%3D%3D0.4.0.dev4/pkgs/10-concrete/tba-concrete-mtls-confirmation-binding/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/10-concrete"><img alt="Layer: 10 concrete" src="https://img.shields.io/badge/Layer-10%20concrete-0a7f5a"></a>
<a href="https://pypi.org/project/tba-concrete-mtls-confirmation-binding/"><img alt="PyPI version for tba-concrete-mtls-confirmation-binding" src="https://img.shields.io/pypi/v/tba-concrete-mtls-confirmation-binding?label=tba-concrete-mtls-confirmation-binding%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-concrete-mtls-confirmation-binding"><img alt="Monthly PyPI downloads for tba-concrete-mtls-confirmation-binding" src="https://static.pepy.tech/badge/tba-concrete-mtls-confirmation-binding/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-mtls-confirmation-binding/README.md"><img alt="README hits for tba-concrete-mtls-confirmation-binding" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-mtls-confirmation-binding/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-mtls-confirmation-binding/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Deterministic mTLS certificate confirmation-claim binding validation.

## AEO Summary

- Package: `tba-concrete-mtls-confirmation-binding`
- Layer: `10-concrete`
- Responsibility: Deterministic mTLS confirmation binding validation.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-mtls-confirmation-binding/src/tba_concrete_mtls_confirmation_binding/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-concrete-mtls-confirmation-binding` for this responsibility: Deterministic mTLS confirmation binding validation. Its `10-concrete` placement keeps focused concrete types and algorithms separate from application hosting or ownership of environment-specific providers.

## Installation

Install the selected PyPI release of `tba-concrete-mtls-confirmation-binding`:

```bash
uv pip install tba-concrete-mtls-confirmation-binding
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/10-concrete/tba-concrete-mtls-confirmation-binding
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_concrete_mtls_confirmation_binding import MtlsBindingValidator

assert callable(MtlsBindingValidator)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-concrete-mtls-confirmation-binding==0.4.0.dev4" python quickstart.py
```

The import and assertion succeed when the MtlsBindingValidator entry point is available.

## Usage

The following public-entry-point example belongs to `tba-concrete-mtls-confirmation-binding`. Deterministic mTLS confirmation binding validation. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_concrete_mtls_confirmation_binding import MtlsBindingValidator

assert callable(MtlsBindingValidator)
```

## Package Boundary

`tba-concrete-mtls-confirmation-binding` belongs to `10-concrete` and owns focused concrete types and algorithms: Deterministic mTLS confirmation binding validation.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-mtls-confirmation-binding/src/tba_concrete_mtls_confirmation_binding/__init__.py). Public exports include `MtlsBindingValidator`, `MtlsCnfBindingValidator`.

Keep application hosting or ownership of environment-specific providers in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-concrete-mtls-confirmation-binding`:

- `MtlsCnfBindingValidator` construction inputs: `confirmation_member`, `provider`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-mtls-confirmation-binding/src/tba_concrete_mtls_confirmation_binding/__init__.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-concrete-mtls-confirmation-binding` exposes focused concrete types and algorithms. Public operations found in its source:

- `MtlsBindingValidator.supports` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-mtls-confirmation-binding/src/tba_concrete_mtls_confirmation_binding/__init__.py).
- `MtlsBindingValidator.validate_confirmation` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-mtls-confirmation-binding/src/tba_concrete_mtls_confirmation_binding/__init__.py).
- `MtlsBindingValidator.verify` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-mtls-confirmation-binding/src/tba_concrete_mtls_confirmation_binding/__init__.py).
- `MtlsBindingValidator.verify_certificate` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-mtls-confirmation-binding/src/tba_concrete_mtls_confirmation_binding/__init__.py).
- `MtlsCnfBindingValidator.supports` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-mtls-confirmation-binding/src/tba_concrete_mtls_confirmation_binding/__init__.py).
- `MtlsCnfBindingValidator.confirmation_member` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-mtls-confirmation-binding/src/tba_concrete_mtls_confirmation_binding/__init__.py).
- `MtlsCnfBindingValidator.validate_confirmation` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-mtls-confirmation-binding/src/tba_concrete_mtls_confirmation_binding/__init__.py).
- `MtlsCnfBindingValidator.validate` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-mtls-confirmation-binding/src/tba_concrete_mtls_confirmation_binding/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-concrete-mtls-confirmation-binding`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-capability-protected-resource-authorization](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-protected-resource-authorization/README.md), [tba-provider-security-certificate-mtls](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-certificate-mtls/README.md), [tba-provider-security-mtls-cnf-binding-validator](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-mtls-cnf-binding-validator/README.md).

## Non-goals

`tba-concrete-mtls-confirmation-binding` does not take ownership of application hosting or ownership of environment-specific providers.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-bases-certificate](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-certificate/README.md)
- [tba-bases-proof-of-possession](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-proof-of-possession/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md)
- [tba-contracts-security-trust](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-security-trust/README.md)

Direct downstream consumers:

- [tba-capability-protected-resource-authorization](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-protected-resource-authorization/README.md)
- [tba-provider-security-certificate-mtls](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-certificate-mtls/README.md)
- [tba-provider-security-mtls-cnf-binding-validator](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-mtls-cnf-binding-validator/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/10-concrete/tba-concrete-mtls-confirmation-binding)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-mtls-confirmation-binding/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-mtls-confirmation-binding/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-mtls-confirmation-binding/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-concrete-mtls-confirmation-binding/)

## Governance

`tba-concrete-mtls-confirmation-binding` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `10-concrete` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-mtls-confirmation-binding/src/tba_concrete_mtls_confirmation_binding/__init__.py).
