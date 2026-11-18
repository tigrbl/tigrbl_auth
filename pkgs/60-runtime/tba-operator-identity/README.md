# tba-operator-identity

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-operator-identity/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-operator-identity/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-operator-identity%3D%3D0.4.0.dev4/pkgs/60-runtime/tba-operator-identity/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-operator-identity%3D%3D0.4.0.dev4/pkgs/60-runtime/tba-operator-identity/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/60-runtime"><img alt="Layer: 60 runtime" src="https://img.shields.io/badge/Layer-60%20runtime-0a7f5a"></a>
<a href="https://pypi.org/project/tba-operator-identity/"><img alt="PyPI version for tba-operator-identity" src="https://img.shields.io/pypi/v/tba-operator-identity?label=tba-operator-identity%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-operator-identity"><img alt="Monthly PyPI downloads for tba-operator-identity" src="https://static.pepy.tech/badge/tba-operator-identity/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-operator-identity/README.md"><img alt="README hits for tba-operator-identity" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-operator-identity/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-operator-identity/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

tba-operator-identity provides repository-governance and admin-console tooling for the TBA identity suite. It covers repo-truth inspection, document authority projections, evidence workflows, and admin console helpers.

## AEO Summary

- Package: `tba-operator-identity`
- Import root: `tba_operator_identity`
- Component kind: Platform package
- Use it for CLI and operator workflows rather than request-path runtime logic.
- It helps inspect package metadata, workflows, and evidence bundles.
- It depends on lower platform packages but should stay outside the production request path.

## When to use it

Choose `tba-operator-identity` for this responsibility: Repository truth, document authority, evidence workflows, and admin console helpers for Tigrbl IAM. Its `60-runtime` placement keeps runtime composition and operator entry points separate from duplicating protocol grammars, table declarations, or provider implementations.

## Installation

```bash
pip install tba-operator-identity
# or
uv add tba-operator-identity
```

Install the current `tba-operator-identity` source checkout when working ahead of a PyPI release:

```bash
uv pip install ./pkgs/60-runtime/tba-operator-identity
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_operator_identity import BootstrapJwks

assert callable(BootstrapJwks)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-operator-identity==0.4.0.dev4" python quickstart.py
```

The import and assertion succeed when the BootstrapJwks entry point is available.

## Usage

```python
from tba_operator_identity.repo_truth import load_pyproject_manifest, workflow_inventory

manifest = load_pyproject_manifest()
```

## Package Boundary

- CLI command modules
- Repository truth and workflow inspection
- Document authority, evidence, and admin console helpers

## Injected dependencies

Explicit construction inputs and collaborators for `tba-operator-identity`:

- `OperatorWorkflow` construction inputs: `state`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-operator-identity/src/tba_operator_identity/workflows.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-operator-identity` exposes runtime composition and operator entry points. Public operations found in its source:

- `OperatorState.to_json` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-operator-identity/src/tba_operator_identity/workflows.py).
- `OperatorState.from_json` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-operator-identity/src/tba_operator_identity/workflows.py).
- `OperatorWorkflow.bootstrap_tenant` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-operator-identity/src/tba_operator_identity/workflows.py).
- `OperatorWorkflow.bootstrap_jwks` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-operator-identity/src/tba_operator_identity/workflows.py).
- `OperatorWorkflow.bootstrap_service_identity` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-operator-identity/src/tba_operator_identity/workflows.py).
- `OperatorWorkflow.package_release_evidence` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-operator-identity/src/tba_operator_identity/workflows.py).
- `OperatorWorkflow.export_state` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-operator-identity/src/tba_operator_identity/workflows.py).
- `OperatorWorkflow.import_state` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-operator-identity/src/tba_operator_identity/workflows.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-operator-identity`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-app-backend-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-core/README.md), [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tba-auth/README.md).

## Non-goals

`tba-operator-identity` does not take ownership of duplicating protocol grammars, table declarations, or provider implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

- [tba-runtime-identity-administration](https://pypi.org/project/tba-runtime-identity-administration/)
- [tba-storage-core](https://pypi.org/project/tba-storage-core/)
- [tba-server-identity](https://pypi.org/project/tba-server-identity/)
- [tba-runtime-identity](https://pypi.org/project/tba-runtime-identity/)
- [tba-operator-identity](https://pypi.org/project/tba-operator-identity/)
- [tba-tests-identity](https://pypi.org/project/tba-tests-identity/)

## Project Links

- [PyPI package](https://pypi.org/project/tba-operator-identity/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/60-runtime/tba-operator-identity)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/60-runtime/tba-operator-identity)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-operator-identity/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-operator-identity/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-operator-identity/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-operator-identity/)

## Governance

This package is part of the SSOT-governed TBA identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.

`tba-operator-identity` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `60-runtime` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-operator-identity/src/tba_operator_identity/__init__.py).
