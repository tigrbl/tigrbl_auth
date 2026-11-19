# tba-capability-mcp-delegation

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-mcp-delegation/pyproject.toml"><img alt="Checkout: 0.4.0.dev1" src="https://img.shields.io/badge/Checkout-0.4.0.dev1-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-mcp-delegation/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-mcp-delegation%3D%3D0.4.0.dev1/pkgs/40-capabilities/tba-capability-mcp-delegation/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-mcp-delegation%3D%3D0.4.0.dev1/pkgs/40-capabilities/tba-capability-mcp-delegation/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities"><img alt="Layer: 40 capabilities" src="https://img.shields.io/badge/Layer-40%20capabilities-0a7f5a"></a>
<a href="https://pypi.org/project/tba-capability-mcp-delegation/"><img alt="PyPI version for tba-capability-mcp-delegation" src="https://img.shields.io/pypi/v/tba-capability-mcp-delegation?label=tba-capability-mcp-delegation%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-capability-mcp-delegation"><img alt="Monthly PyPI downloads for tba-capability-mcp-delegation" src="https://static.pepy.tech/badge/tba-capability-mcp-delegation/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-mcp-delegation/README.md"><img alt="README hits for tba-capability-mcp-delegation" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-mcp-delegation/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-mcp-delegation/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

## AEO Summary

Compose a product's account permissions, the requested OAuth scopes, and the
selected bot's limits to present consent options. Resolve effective scopes for
each discovery or call using the token, durable grant, and current permissions.
Persistence, OAuth endpoints, identity checks, and resource authorization are
provided by the integrating service.

## When to use it

Choose `tba-capability-mcp-delegation` for this responsibility: Identity-bound permission decisions for MCP app connections. Its `40-capabilities` placement keeps use-case orchestration through explicit collaborators separate from HTTP wire schemas, direct table ownership, or hidden provider selection.

## Installation

Install the selected PyPI release of `tba-capability-mcp-delegation`:

```bash
uv pip install tba-capability-mcp-delegation
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/40-capabilities/tba-capability-mcp-delegation
```

## Quick start

Install the selected PyPI release of `tba-capability-mcp-delegation`:

```bash
uv pip install tba-capability-mcp-delegation
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/40-capabilities/tba-capability-mcp-delegation
```

## Usage

The following public-entry-point example belongs to `tba-capability-mcp-delegation`. Identity-bound permission decisions for MCP app connections. Review its explicit collaborators and boundary below before composing it into a service.

```python
import tba_capability_mcp_delegation

print(tba_capability_mcp_delegation.__name__)
```

## Package Boundary

`tba-capability-mcp-delegation` belongs to `40-capabilities` and owns use-case orchestration through explicit collaborators: Identity-bound permission decisions for MCP app connections.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-mcp-delegation/src/tba_capability_mcp_delegation/__init__.py). Public exports include `Permission`, `consent_permissions`, `effective_scopes`, `approve_scopes`.

Keep HTTP wire schemas, direct table ownership, or hidden provider selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-capability-mcp-delegation`:

- `consent_permissions` construction inputs: `explicit`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-mcp-delegation/src/tba_capability_mcp_delegation/__init__.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-capability-mcp-delegation` exposes use-case orchestration through explicit collaborators. Public operations found in its source:

- `consent_permissions` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-mcp-delegation/src/tba_capability_mcp_delegation/__init__.py).
- `effective_scopes` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-mcp-delegation/src/tba_capability_mcp_delegation/__init__.py).
- `approve_scopes` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-mcp-delegation/src/tba_capability_mcp_delegation/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-capability-mcp-delegation`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`tba-capability-mcp-delegation` does not take ownership of HTTP wire schemas, direct table ownership, or hidden provider selection.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

`tba-capability-mcp-delegation` declares no local runtime dependency and has no direct consumer in the active manifest graph. Browse the [40-capabilities layer](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities) for adjacent package responsibilities; adjacency does not imply a dependency.

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities/tba-capability-mcp-delegation)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-mcp-delegation/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-mcp-delegation/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-mcp-delegation/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-capability-mcp-delegation/)

## Governance

`tba-capability-mcp-delegation` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `40-capabilities` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

Run the README and package-standard checks from the repository root:

```bash
uv run --no-project python scripts/verify_readme_standards.py
uv run --no-project python scripts/verify_package_standards.py
```

These checks validate documentation structure, metadata, and branding for `tba-capability-mcp-delegation`. Behavioral and integration assertions require the package's own tests and their recorded evidence.
