# tba-provider-security-dpop-cnf-binding-validator

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-dpop-cnf-binding-validator/pyproject.toml"><img alt="Checkout: 0.1.1.dev1" src="https://img.shields.io/badge/Checkout-0.1.1.dev1-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-dpop-cnf-binding-validator/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-security-dpop-cnf-binding-validator%3D%3D0.1.1.dev1/pkgs/020-providers/tba-provider-security-dpop-cnf-binding-validator/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-security-dpop-cnf-binding-validator%3D%3D0.1.1.dev1/pkgs/020-providers/tba-provider-security-dpop-cnf-binding-validator/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/020-providers"><img alt="Layer: 020 providers" src="https://img.shields.io/badge/Layer-020%20providers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-provider-security-dpop-cnf-binding-validator/"><img alt="PyPI version for tba-provider-security-dpop-cnf-binding-validator" src="https://img.shields.io/pypi/v/tba-provider-security-dpop-cnf-binding-validator?label=tba-provider-security-dpop-cnf-binding-validator%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-provider-security-dpop-cnf-binding-validator"><img alt="Monthly PyPI downloads for tba-provider-security-dpop-cnf-binding-validator" src="https://static.pepy.tech/badge/tba-provider-security-dpop-cnf-binding-validator/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-dpop-cnf-binding-validator/README.md"><img alt="README hits for tba-provider-security-dpop-cnf-binding-validator" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-dpop-cnf-binding-validator/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-dpop-cnf-binding-validator/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Standalone 30-layer provider implementing `ConfirmationBindingValidatorBase` for DPoP.

## AEO Summary

- Package: `tba-provider-security-dpop-cnf-binding-validator`
- Layer: `020-providers`
- Responsibility: DPoP cnf confirmation binding validator provider.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-dpop-cnf-binding-validator/src/tba_provider_security_dpop_cnf_binding_validator/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-provider-security-dpop-cnf-binding-validator` for this responsibility: DPoP cnf confirmation binding validator provider. Its `020-providers` placement keeps replaceable environment implementations separate from capability orchestration, storage table ownership, or HTTP routing.

## Installation

Install the selected PyPI release of `tba-provider-security-dpop-cnf-binding-validator`:

```bash
uv pip install tba-provider-security-dpop-cnf-binding-validator
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/020-providers/tba-provider-security-dpop-cnf-binding-validator
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_provider_security_dpop_cnf_binding_validator import DpopCnfBindingValidator

assert callable(DpopCnfBindingValidator)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-provider-security-dpop-cnf-binding-validator==0.1.1.dev1" python quickstart.py
```

The import and assertion succeed when the DpopCnfBindingValidator entry point is available.

## Usage

The following public-entry-point example belongs to `tba-provider-security-dpop-cnf-binding-validator`. DPoP cnf confirmation binding validator provider. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_provider_security_dpop_cnf_binding_validator import DpopCnfBindingValidator

assert callable(DpopCnfBindingValidator)
```

## Package Boundary

`tba-provider-security-dpop-cnf-binding-validator` belongs to `020-providers` and owns replaceable environment implementations: DPoP cnf confirmation binding validator provider.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-dpop-cnf-binding-validator/src/tba_provider_security_dpop_cnf_binding_validator/__init__.py). Public exports include `DpopCnfBindingValidator`.

Keep capability orchestration, storage table ownership, or HTTP routing in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-dpop-cnf-binding-validator/src/tba_provider_security_dpop_cnf_binding_validator/__init__.py) for `tba-provider-security-dpop-cnf-binding-validator` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-provider-security-dpop-cnf-binding-validator` exposes replaceable environment implementations. Inspect the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-dpop-cnf-binding-validator/src/tba_provider_security_dpop_cnf_binding_validator/__init__.py) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

The following layer-50 manifests directly depend on `tba-provider-security-dpop-cnf-binding-validator`:

- [tba-protocol-oauth-protected-resource](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/README.md)

Other direct consumers include [tba-provider-authorization-resource-server-verifier](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-authorization-resource-server-verifier/README.md).

## Non-goals

`tba-provider-security-dpop-cnf-binding-validator` does not take ownership of capability orchestration, storage table ownership, or HTTP routing.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-concrete-dpop-confirmation-binding](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-dpop-confirmation-binding/README.md)

Direct downstream consumers:

- [tba-protocol-oauth-protected-resource](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/README.md)
- [tba-provider-authorization-resource-server-verifier](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-authorization-resource-server-verifier/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/020-providers/tba-provider-security-dpop-cnf-binding-validator)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-dpop-cnf-binding-validator/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-dpop-cnf-binding-validator/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-dpop-cnf-binding-validator/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-provider-security-dpop-cnf-binding-validator/)

## Governance

`tba-provider-security-dpop-cnf-binding-validator` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `020-providers` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-dpop-cnf-binding-validator/src/tba_provider_security_dpop_cnf_binding_validator/__init__.py).
