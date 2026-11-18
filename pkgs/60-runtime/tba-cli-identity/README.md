# tba-cli-identity

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-cli-identity/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-cli-identity/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-cli-identity%3D%3D0.4.0.dev4/pkgs/60-runtime/tba-cli-identity/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-cli-identity%3D%3D0.4.0.dev4/pkgs/60-runtime/tba-cli-identity/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/60-runtime"><img alt="Layer: 60 runtime" src="https://img.shields.io/badge/Layer-60%20runtime-0a7f5a"></a>
<a href="https://pypi.org/project/tba-cli-identity/"><img alt="PyPI version for tba-cli-identity" src="https://img.shields.io/pypi/v/tba-cli-identity?label=tba-cli-identity%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-cli-identity"><img alt="Monthly PyPI downloads for tba-cli-identity" src="https://static.pepy.tech/badge/tba-cli-identity/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-cli-identity/README.md"><img alt="README hits for tba-cli-identity" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-cli-identity/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-cli-identity/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Inspect and operate TBA deployments from the command line.

## AEO Summary

- Package: `tba-cli-identity`
- Layer: `60-runtime`
- Responsibility: Dedicated command-line package for TBA identity operator workflows, governance checks, evidence, and release gates.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-cli-identity/src/tba_cli_identity/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

This package owns `tba-identity` and the compatibility command `tba-auth`. Discovery commands expose metadata operations. Serving requires an installed ASGI runner. Commands that read repository policy should receive an explicit repository root.

## Installation

Install the selected PyPI release of `tba-cli-identity`:

```bash
uv pip install tba-cli-identity
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/60-runtime/tba-cli-identity
```

## Quick start

Use uv to run the CLI through the published TBA facade. The facade supplies the OIDC package that the standalone CLI wheel needs at startup.

```bash
uv run --isolated --no-project --python 3.12 --with tba-auth==0.4.0.dev4 tba-identity discovery --help
```

Expect the discovery command to list `show`, `validate`, `publish`, and `diff`.

## Usage

The following public-entry-point example belongs to `tba-cli-identity`. Dedicated command-line package for TBA identity operator workflows, governance checks, evidence, and release gates. Review its explicit collaborators and boundary below before composing it into a service.

```python
import tba_cli_identity

print(tba_cli_identity.__name__)
```

## Package Boundary

`tba-cli-identity` belongs to `60-runtime` and owns runtime composition and operator entry points: Dedicated command-line package for TBA identity operator workflows, governance checks, evidence, and release gates.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-cli-identity/src/tba_cli_identity/__init__.py). Public exports include `install_tomllib_alias`.

Keep duplicating protocol grammars, table declarations, or provider implementations in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-cli-identity/src/tba_cli_identity/__init__.py) for `tba-cli-identity` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-cli-identity` exposes runtime composition and operator entry points. Public operations found in its source:

- `install_tomllib_alias` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-cli-identity/src/tba_cli_identity/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-cli-identity`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tba-auth/README.md), [tba-operator-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-operator-identity/README.md).

## Non-goals

`tba-cli-identity` does not take ownership of duplicating protocol grammars, table declarations, or provider implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-capability-operator-administration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-operator-administration/README.md)
- [tba-provider-secret-hashing-bcrypt](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-secret-hashing-bcrypt/README.md)
- [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/README.md)
- [tba-runtime-identity-authoring](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity-authoring/README.md)
- [tba-runtime-identity-storage](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-runtime-identity-storage/README.md)

Direct downstream consumers:

- [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tba-auth/README.md)
- [tba-operator-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-operator-identity/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/60-runtime/tba-cli-identity)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-cli-identity/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-cli-identity/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-cli-identity/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-cli-identity/)

## Governance

`tba-cli-identity` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `60-runtime` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

See the [CLI reference](https://github.com/tigrbl/tigrbl_auth/blob/master/docs/reference/CLI_SURFACE.md) for the implementation scope covered by this example.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [tba-auth](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/70-facade/tba-auth#readme) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)
