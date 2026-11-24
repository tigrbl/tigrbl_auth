# tba-router-oauth-token

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-router-oauth-token</strong></p>
<p align="center">HTTP carrier binding for the OAuth token endpoint.</p>
<p align="center">
<a href="https://pypi.org/project/tba-router-oauth-token/"><img alt="pypi: tba-router-oauth-token" src="https://img.shields.io/pypi/v/tba-router-oauth-token?labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-token/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-token/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-token/pyproject.toml"><img alt="Layer: 080-routers" src="https://img.shields.io/static/v1?label=Layer&amp;message=080-routers&amp;labelColor=1E293B&amp;color=6D28D9"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-token/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;labelColor=1E293B&amp;color=166534"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-token/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;labelColor=1E293B&amp;color=86198F"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-token/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;labelColor=1E293B&amp;color=86198F"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-router-oauth-token/"><img alt="Monthly PyPI downloads: tba-router-oauth-token" src="https://img.shields.io/pypi/dm/tba-router-oauth-token?labelColor=1E293B&amp;color=0E7490"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-token/README.md"><img alt="README hits: tba-router-oauth-token" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/080-routers/tba-router-oauth-token/README.md.svg?label=README%20hits&amp;labelColor=1E293B&amp;color=0E7490"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-token/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-token/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;labelColor=1E293B&amp;color=6D28D9"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

This layer-80 package owns the OAuth token endpoint HTTP carrier: the POST
route, request/database dependency injection, and the protocol response model.

It receives the layer-60 token-request processor by injection. It does not
authenticate clients, evaluate grants, issue tokens, open storage sessions, or
own token lifecycle state.

- Package: `tba-router-oauth-token`
- Layer: `080-routers`
- Responsibility: HTTP carrier binding for the OAuth token endpoint.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-token/src/tba_router_oauth_token/__init__.py).
- Distribution: Python package on PyPI.

### Why This Package

`tba-router-oauth-token` isolates this responsibility: HTTP carrier binding for the OAuth token endpoint. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-token/src/tba_router_oauth_token/__init__.py) exposes `DatabaseDependency`, `TokenRequestTarget`, `build_token_router`, `include_token_endpoint`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-router-oauth-token` for this responsibility: HTTP carrier binding for the OAuth token endpoint. Its `080-routers` placement keeps transport-facing route composition separate from duplicating credential algorithms or storage ownership.

### Features

- Public source surface: `DatabaseDependency`, `TokenRequestTarget`, `build_token_router`, `include_token_endpoint`.
- Declared responsibility: HTTP carrier binding for the OAuth token endpoint.
- Versioned package metadata and maintained checkout examples.

### Non-Goals

`tba-router-oauth-token` does not take ownership of duplicating credential algorithms or storage ownership.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-token/pyproject.toml) declares runtime dependencies including `tigrbl`, `tba-protocol-oauth`. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-router-oauth-token`:

```bash
uv pip install tba-router-oauth-token
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/080-routers/tba-router-oauth-token
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-router-oauth-token
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-router-oauth-token
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-router-oauth-token
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.


```bash
uv run --isolated --no-project --python 3.12 --with "tba-router-oauth-token==0.4.0.dev3" python quickstart.py
```

The router registers `/token`. No request is sent and no database is opened.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-token/docs/readme/quick_start.py).

```python
from tba_router_oauth_token import build_token_router


async def handler(**kwargs):
    raise AssertionError("This example only registers routes")


def get_db():
    raise AssertionError("This example does not access storage")


router = build_token_router(
    token_request=handler,
    get_db=get_db,
)
paths = {
    getattr(route, "path", None) or getattr(route, "path_template", None)
    for route in router.routes
}
assert "/token" in paths
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-router-oauth-token` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-token/docs/readme/usage.py).

```python
from tba_router_oauth_token import build_token_router


async def handler(**kwargs):
    raise AssertionError("This example only registers routes")


def get_db():
    raise AssertionError("This example does not access storage")


router = build_token_router(
    token_request=handler,
    get_db=get_db,
)
paths = {
    getattr(route, "path", None) or getattr(route, "path_template", None)
    for route in router.routes
}
assert "/token" in paths
```
<!-- readme-standards:end example.usage -->

The following public-entry-point example belongs to `tba-router-oauth-token`. HTTP carrier binding for the OAuth token endpoint. Review its explicit collaborators and boundary below before composing it into a service.

### Configuration

Configure `tba-router-oauth-token` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-token/src/tba_router_oauth_token/__init__.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-token/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-router-oauth-token` source does not establish a package-wide exception hierarchy. Preserve errors from its declared dependencies and validate inputs using the specific public contract in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-token/src/tba_router_oauth_token/__init__.py).

### Best Practices

Use the explicit `tba-router-oauth-token` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `DatabaseDependency`, `TokenRequestTarget`, `build_token_router`, `include_token_endpoint`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

`tba-router-oauth-token` belongs to `080-routers` and owns transport-facing route composition: HTTP carrier binding for the OAuth token endpoint.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-token/src/tba_router_oauth_token/__init__.py). Public exports include `DatabaseDependency`, `TokenRequestTarget`, `build_token_router`, `include_token_endpoint`.

Keep duplicating credential algorithms or storage ownership in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

### Public API and Import Surfaces

Import namespace: `tba_router_oauth_token`.

Source-declared exports or types: `DatabaseDependency`, `TokenRequestTarget`, `build_token_router`, `include_token_endpoint`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-token/src/tba_router_oauth_token/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

Explicit construction inputs and collaborators for `tba-router-oauth-token`:

- `build_token_router` construction inputs: `token_request`, `get_db`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-token/src/tba_router_oauth_token/binding.py).
- `include_token_endpoint` construction inputs: `enabled`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-token/src/tba_router_oauth_token/binding.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

### Protocol Consumers

Direct consumers in this checkout’s package manifests include `tba-app-backend-core`, `tba-app-backend-public`, `tba-workspace`. These edges describe declared dependencies, not protocol-conformance evidence.

### Extensions

For `tba-router-oauth-token`, use the source-declared public interfaces (`DatabaseDependency`, `TokenRequestTarget`, `build_token_router`, `include_token_endpoint`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-router-oauth-token` exposes transport-facing route composition. Public operations found in its source:

- `build_token_router` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-token/src/tba_router_oauth_token/binding.py).
- `include_token_endpoint` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-token/src/tba_router_oauth_token/binding.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-router-oauth-token`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-token/src/tba_router_oauth_token/__init__.py). The `tba-router-oauth-token` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-router-oauth-token` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-token/src/tba_router_oauth_token/__init__.py).

### Certification Status

No external certification is asserted for `tba-router-oauth-token` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-token/src/tba_router_oauth_token/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-router-oauth-token` provides hTTP carrier binding for the OAuth token endpoint; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-router-oauth-token`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-token/src/tba_router_oauth_token/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-router-oauth-token` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-token/src/tba_router_oauth_token/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-token/pyproject.toml) provide the supporting context for `tba-router-oauth-token`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

Declared local runtime dependencies:

- [tba-protocol-oauth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/README.md)

Direct downstream consumers:

- [tba-app-backend-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/README.md)
- [tba-app-backend-public](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-public/README.md)

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/080-routers/tba-router-oauth-token#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/080-routers/tba-router-oauth-token#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-router-oauth-token/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/080-routers/tba-router-oauth-token)
- [pypi: tba-router-oauth-token](https://pypi.org/project/tba-router-oauth-token/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/080-routers/tba-router-oauth-token)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-token/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-token/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-token/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-router-oauth-token/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-router-oauth-token`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/080-routers/tba-router-oauth-token` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.3` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-router-oauth-token` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-router-oauth-token` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-token/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

`tba-router-oauth-token` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `080-routers` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-router-oauth-token` source version is `0.4.0.dev3`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-token/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-oauth-token/NOTICE) for attribution.
<!-- readme-standards:end notices -->
