# tba-capability-realm-administration

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-realm-administration/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-realm-administration/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-realm-administration%3D%3D0.4.0.dev3/pkgs/040-capabilities/tba-capability-realm-administration/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-realm-administration%3D%3D0.4.0.dev3/pkgs/040-capabilities/tba-capability-realm-administration/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/040-capabilities"><img alt="Layer: 040 capabilities" src="https://img.shields.io/badge/Layer-040%20capabilities-0a7f5a"></a>
<a href="https://pypi.org/project/tba-capability-realm-administration/"><img alt="PyPI version for tba-capability-realm-administration" src="https://img.shields.io/pypi/v/tba-capability-realm-administration?label=tba-capability-realm-administration%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-capability-realm-administration"><img alt="Monthly PyPI downloads for tba-capability-realm-administration" src="https://static.pepy.tech/badge/tba-capability-realm-administration/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-realm-administration/README.md"><img alt="README hits for tba-capability-realm-administration" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-realm-administration/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-realm-administration/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Realm lifecycle administration over injected durable operations.

## AEO Summary

- Package: `tba-capability-realm-administration`
- Layer: `040-capabilities`
- Responsibility: Realm administration capability over injected durable operations.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-realm-administration/src/tba_capability_realm_administration/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-capability-realm-administration` for this responsibility: Realm administration capability over injected durable operations. Its `040-capabilities` placement keeps use-case orchestration through explicit collaborators separate from HTTP wire schemas, direct table ownership, or hidden provider selection.

## Installation

Install the selected PyPI release of `tba-capability-realm-administration`:

```bash
uv pip install tba-capability-realm-administration
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/040-capabilities/tba-capability-realm-administration
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_capability_realm_administration import RealmAdministrationCapability

assert callable(RealmAdministrationCapability)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-capability-realm-administration==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the RealmAdministrationCapability entry point is available.

## Usage

The following public-entry-point example belongs to `tba-capability-realm-administration`. Realm administration capability over injected durable operations. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_capability_realm_administration import RealmAdministrationCapability

assert callable(RealmAdministrationCapability)
```

## Package Boundary

`tba-capability-realm-administration` belongs to `040-capabilities` and owns use-case orchestration through explicit collaborators: Realm administration capability over injected durable operations.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-realm-administration/src/tba_capability_realm_administration/__init__.py).

Keep HTTP wire schemas, direct table ownership, or hidden provider selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

- No package-mandated runtime dependency; callables are constructor-injected.

## Operations and readiness

- See the capability report for the effective operation registry and readiness.

## Protocol consumers

- Protocol-neutral; layer-50 packages may bind these operations.

## Non-goals

- No HTTP or protocol wire schemas.
- No direct layer-01 table access.
- No hidden mutable persistence or provider selection.

## Related Packages

Declared local runtime dependencies:

- [tba-concrete-capability](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-capability/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/README.md)

Direct downstream consumers:

- [tba-runtime-identity-administration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-administration/README.md)
- [tba-server-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/040-capabilities/tba-capability-realm-administration)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-realm-administration/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-realm-administration/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-realm-administration/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-capability-realm-administration/)

## Governance

`tba-capability-realm-administration` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `040-capabilities` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-realm-administration/src/tba_capability_realm_administration/__init__.py).
