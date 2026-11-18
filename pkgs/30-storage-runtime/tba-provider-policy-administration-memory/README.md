# tba-provider-policy-administration-memory

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-provider-policy-administration-memory/pyproject.toml"><img alt="Checkout: 0.4.0.dev5" src="https://img.shields.io/badge/Checkout-0.4.0.dev5-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-provider-policy-administration-memory/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-policy-administration-memory%3D%3D0.4.0.dev5/pkgs/30-storage-runtime/tba-provider-policy-administration-memory/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-policy-administration-memory%3D%3D0.4.0.dev5/pkgs/30-storage-runtime/tba-provider-policy-administration-memory/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/30-storage-runtime"><img alt="Layer: 30 storage runtime" src="https://img.shields.io/badge/Layer-30%20storage%20runtime-0a7f5a"></a>
<a href="https://pypi.org/project/tba-provider-policy-administration-memory/"><img alt="PyPI version for tba-provider-policy-administration-memory" src="https://img.shields.io/pypi/v/tba-provider-policy-administration-memory?label=tba-provider-policy-administration-memory%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-provider-policy-administration-memory"><img alt="Monthly PyPI downloads for tba-provider-policy-administration-memory" src="https://static.pepy.tech/badge/tba-provider-policy-administration-memory/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-provider-policy-administration-memory/README.md"><img alt="README hits for tba-provider-policy-administration-memory" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-provider-policy-administration-memory/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-provider-policy-administration-memory/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Owns in-memory policy-administration state used by local and test compositions.

## AEO Summary

- Package: `tba-provider-policy-administration-memory`
- Layer: `30-storage-runtime`
- Responsibility: In-memory RBAC, ABAC, delegated-administration, and policy engine providers.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-provider-policy-administration-memory/src/tba_provider_policy_administration_memory/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-provider-policy-administration-memory` for this responsibility: In-memory RBAC, ABAC, delegated-administration, and policy engine providers. Its `30-storage-runtime` placement keeps storage-backed runtime adapters separate from protocol wire definitions or standalone application hosting.

## Installation

Install the selected PyPI release of `tba-provider-policy-administration-memory`:

```bash
uv pip install tba-provider-policy-administration-memory
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/30-storage-runtime/tba-provider-policy-administration-memory
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_provider_policy_administration_memory import ABACAdministrator

assert callable(ABACAdministrator)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-provider-policy-administration-memory==0.4.0.dev5" python quickstart.py
```

The import and assertion succeed when the ABACAdministrator entry point is available.

## Usage

The following public-entry-point example belongs to `tba-provider-policy-administration-memory`. In-memory RBAC, ABAC, delegated-administration, and policy engine providers. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_provider_policy_administration_memory import ABACAdministrator

assert callable(ABACAdministrator)
```

## Package Boundary

`tba-provider-policy-administration-memory` belongs to `30-storage-runtime` and owns storage-backed runtime adapters: In-memory RBAC, ABAC, delegated-administration, and policy engine providers.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-provider-policy-administration-memory/src/tba_provider_policy_administration_memory/__init__.py).

Keep protocol wire definitions or standalone application hosting in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-provider-policy-administration-memory/src/tba_provider_policy_administration_memory/__init__.py) for `tba-provider-policy-administration-memory` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-provider-policy-administration-memory` exposes storage-backed runtime adapters. Inspect the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-provider-policy-administration-memory/src/tba_provider_policy_administration_memory/__init__.py) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-provider-policy-administration-memory`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-capability-policy-administration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-policy-administration/README.md).

## Non-goals

`tba-provider-policy-administration-memory` does not take ownership of protocol wire definitions or standalone application hosting.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-concrete-authorization-policy-rules](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-policy-rules/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md)
- [tba-durability-authorization-policy](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-durability-authorization-policy/README.md)
- [tba-primitives-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/00-primitives/tba-primitives-identity/README.md)
- [tba-provider-access-governance-memory](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-access-governance-memory/README.md)

Direct downstream consumers:

- [tba-capability-policy-administration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-policy-administration/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/30-storage-runtime/tba-provider-policy-administration-memory)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-provider-policy-administration-memory/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-provider-policy-administration-memory/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-provider-policy-administration-memory/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-provider-policy-administration-memory/)

## Governance

`tba-provider-policy-administration-memory` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `30-storage-runtime` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-provider-policy-administration-memory/src/tba_provider_policy_administration_memory/__init__.py).
