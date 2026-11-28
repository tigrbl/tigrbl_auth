# tba-middleware-policy-enforcement-asgi

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-middleware-policy-enforcement-asgi</strong></p>
<p align="center">ASGI policy enforcement point using an injected decision client.</p>
<p align="center">
<a href="https://pypi.org/project/tba-middleware-policy-enforcement-asgi/"><img alt="pypi: tba-middleware-policy-enforcement-asgi" src="https://img.shields.io/pypi/v/tba-middleware-policy-enforcement-asgi?labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/085-middleware/tba-middleware-policy-enforcement-asgi/pyproject.toml"><img alt="Source version: 0.4.0.dev4" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev4&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/085-middleware/tba-middleware-policy-enforcement-asgi/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/085-middleware/tba-middleware-policy-enforcement-asgi/pyproject.toml"><img alt="Layer: 085-middleware" src="https://img.shields.io/static/v1?label=Layer&amp;message=085-middleware&amp;labelColor=1E293B&amp;color=6D28D9"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/085-middleware/tba-middleware-policy-enforcement-asgi/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;labelColor=1E293B&amp;color=166534"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/085-middleware/tba-middleware-policy-enforcement-asgi/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;labelColor=1E293B&amp;color=86198F"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/085-middleware/tba-middleware-policy-enforcement-asgi/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;labelColor=1E293B&amp;color=86198F"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-middleware-policy-enforcement-asgi/"><img alt="Monthly PyPI downloads: tba-middleware-policy-enforcement-asgi" src="https://img.shields.io/pypi/dm/tba-middleware-policy-enforcement-asgi?labelColor=1E293B&amp;color=0E7490"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/085-middleware/tba-middleware-policy-enforcement-asgi/README.md"><img alt="README hits: tba-middleware-policy-enforcement-asgi" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/085-middleware/tba-middleware-policy-enforcement-asgi/README.md.svg?label=README%20hits&amp;labelColor=1E293B&amp;color=0E7490"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/085-middleware/tba-middleware-policy-enforcement-asgi/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/085-middleware/tba-middleware-policy-enforcement-asgi/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;labelColor=1E293B&amp;color=6D28D9"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

Apply a synchronous policy decision to HTTP requests at an ASGI boundary.

- Package: `tba-middleware-policy-enforcement-asgi`
- Layer: `085-middleware`
- Responsibility: ASGI policy enforcement point using an injected decision client.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/085-middleware/tba-middleware-policy-enforcement-asgi/src/tba_middleware_policy_enforcement_asgi/__init__.py).
- Distribution: Python package on PyPI.

### Why This Package

`tba-middleware-policy-enforcement-asgi` isolates this responsibility: ASGI policy enforcement point using an injected decision client. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/085-middleware/tba-middleware-policy-enforcement-asgi/src/tba_middleware_policy_enforcement_asgi/__init__.py) exposes `PolicyEnforcementMiddleware`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Inject a decision callable that returns an `allowed` field. The middleware sends 403 for a denied HTTP scope and forwards allowed requests and other scope types. The caller owns identity extraction, policy decisions, and handling transport failures.

### Features

- `PolicyEnforcementMiddleware`: declared in src/tba_middleware_policy_enforcement_asgi/__init__.py

### Non-Goals

`tba-middleware-policy-enforcement-asgi` does not take ownership of implicit key storage or a complete identity deployment.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/085-middleware/tba-middleware-policy-enforcement-asgi/pyproject.toml) declares runtime dependencies including `tba-client-policy-decision`. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-middleware-policy-enforcement-asgi`:

```bash
uv pip install tba-middleware-policy-enforcement-asgi
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/085-middleware/tba-middleware-policy-enforcement-asgi
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-middleware-policy-enforcement-asgi
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-middleware-policy-enforcement-asgi
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-middleware-policy-enforcement-asgi
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

Install the version used by this example.

```bash
python -m pip install "tba-middleware-policy-enforcement-asgi==0.4.0.dev4"
```

Save the following as `quickstart.py` and run `python quickstart.py`. The assertions should pass.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/085-middleware/tba-middleware-policy-enforcement-asgi/docs/readme/quick_start.py).

```python
import asyncio

from tba_middleware_policy_enforcement_asgi import PolicyEnforcementMiddleware


async def protected(scope, receive, send):
    raise AssertionError("a denied request reached the app")


messages = []


async def send(message):
    messages.append(message)


async def receive():
    raise AssertionError("a denied request read the body")


middleware = PolicyEnforcementMiddleware(protected, lambda scope: {"allowed": False})
asyncio.run(middleware({"type": "http"}, receive, send))
assert messages[0]["status"] == 403
assert messages[1]["body"] == b"Forbidden"
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-middleware-policy-enforcement-asgi` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/085-middleware/tba-middleware-policy-enforcement-asgi/docs/readme/usage.py).

```python
import asyncio

from tba_middleware_policy_enforcement_asgi import PolicyEnforcementMiddleware


async def protected(scope, receive, send):
    raise AssertionError("a denied request reached the app")


messages = []


async def send(message):
    messages.append(message)


async def receive():
    raise AssertionError("a denied request read the body")


middleware = PolicyEnforcementMiddleware(protected, lambda scope: {"allowed": False})
asyncio.run(middleware({"type": "http"}, receive, send))
assert messages[0]["status"] == 403
assert messages[1]["body"] == b"Forbidden"
```
<!-- readme-standards:end example.usage -->

The following public-entry-point example belongs to `tba-middleware-policy-enforcement-asgi`. ASGI policy enforcement point using an injected decision client. Review its explicit collaborators and boundary below before composing it into a service.

### Configuration

Configure `tba-middleware-policy-enforcement-asgi` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/085-middleware/tba-middleware-policy-enforcement-asgi/src/tba_middleware_policy_enforcement_asgi/__init__.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/085-middleware/tba-middleware-policy-enforcement-asgi/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-middleware-policy-enforcement-asgi` source does not establish a package-wide exception hierarchy. Preserve errors from its declared dependencies and validate inputs using the specific public contract in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/085-middleware/tba-middleware-policy-enforcement-asgi/src/tba_middleware_policy_enforcement_asgi/__init__.py).

### Best Practices

Use the explicit `tba-middleware-policy-enforcement-asgi` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `PolicyEnforcementMiddleware`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

`tba-middleware-policy-enforcement-asgi` belongs to `085-middleware` and owns request middleware integration: ASGI policy enforcement point using an injected decision client.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/085-middleware/tba-middleware-policy-enforcement-asgi/src/tba_middleware_policy_enforcement_asgi/__init__.py). Public exports include `PolicyEnforcementMiddleware`.

Keep implicit key storage or a complete identity deployment in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

### Public API and Import Surfaces

Import namespace: `tba_middleware_policy_enforcement_asgi`.

Source-declared exports or types: `PolicyEnforcementMiddleware`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/085-middleware/tba-middleware-policy-enforcement-asgi/src/tba_middleware_policy_enforcement_asgi/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

Explicit construction inputs and collaborators for `tba-middleware-policy-enforcement-asgi`:

- `PolicyEnforcementMiddleware` construction inputs: `app`, `decide`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/085-middleware/tba-middleware-policy-enforcement-asgi/src/tba_middleware_policy_enforcement_asgi/__init__.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

### Protocol Consumers

Direct consumers in this checkout’s package manifests include `tba-workspace`. These edges describe declared dependencies, not protocol-conformance evidence.

### Extensions

For `tba-middleware-policy-enforcement-asgi`, use the source-declared public interfaces (`PolicyEnforcementMiddleware`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-middleware-policy-enforcement-asgi` exposes request middleware integration. Inspect the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/085-middleware/tba-middleware-policy-enforcement-asgi/src/tba_middleware_policy_enforcement_asgi/__init__.py) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-middleware-policy-enforcement-asgi`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/085-middleware/tba-middleware-policy-enforcement-asgi/src/tba_middleware_policy_enforcement_asgi/__init__.py). The `tba-middleware-policy-enforcement-asgi` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-middleware-policy-enforcement-asgi` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

Run the example above to check the public API against the installed package. Its assertions describe the expected behavior.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [tba-client-policy-decision](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/075-clients/tba-client-policy-decision#readme) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)

### Certification Status

No external certification is asserted for `tba-middleware-policy-enforcement-asgi` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/085-middleware/tba-middleware-policy-enforcement-asgi/src/tba_middleware_policy_enforcement_asgi/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-middleware-policy-enforcement-asgi` provides aSGI policy enforcement point using an injected decision client; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-middleware-policy-enforcement-asgi`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/085-middleware/tba-middleware-policy-enforcement-asgi/src/tba_middleware_policy_enforcement_asgi/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-middleware-policy-enforcement-asgi` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/085-middleware/tba-middleware-policy-enforcement-asgi/src/tba_middleware_policy_enforcement_asgi/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/085-middleware/tba-middleware-policy-enforcement-asgi/pyproject.toml) provide the supporting context for `tba-middleware-policy-enforcement-asgi`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

Declared local runtime dependencies:

- [tba-client-policy-decision](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-policy-decision/README.md)

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/085-middleware/tba-middleware-policy-enforcement-asgi#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/085-middleware/tba-middleware-policy-enforcement-asgi#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-middleware-policy-enforcement-asgi/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/085-middleware/tba-middleware-policy-enforcement-asgi)
- [pypi: tba-middleware-policy-enforcement-asgi](https://pypi.org/project/tba-middleware-policy-enforcement-asgi/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/085-middleware/tba-middleware-policy-enforcement-asgi)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/085-middleware/tba-middleware-policy-enforcement-asgi/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/085-middleware/tba-middleware-policy-enforcement-asgi/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/085-middleware/tba-middleware-policy-enforcement-asgi/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-middleware-policy-enforcement-asgi/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-middleware-policy-enforcement-asgi`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/085-middleware/tba-middleware-policy-enforcement-asgi` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.3` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-middleware-policy-enforcement-asgi` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-middleware-policy-enforcement-asgi` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/085-middleware/tba-middleware-policy-enforcement-asgi/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

`tba-middleware-policy-enforcement-asgi` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `085-middleware` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-middleware-policy-enforcement-asgi` source version is `0.4.0.dev4`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/085-middleware/tba-middleware-policy-enforcement-asgi/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/085-middleware/tba-middleware-policy-enforcement-asgi/NOTICE) for attribution.
<!-- readme-standards:end notices -->
