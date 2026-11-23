# tba-example-oauth-device-authorization-cli

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-example-oauth-device-authorization-cli</strong></p>
<p align="center">Example consumer package showing CLI login against tba_auth device authorization.</p>
<p align="center">
<a href="https://pypi.org/project/tba-example-oauth-device-authorization-cli/"><img alt="pypi: tba-example-oauth-device-authorization-cli" src="https://img.shields.io/pypi/v/tba-example-oauth-device-authorization-cli"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli/pyproject.toml"><img alt="Source version: 0.1.1.dev1" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.1.1.dev1&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli/pyproject.toml"><img alt="Layer: 110-examples" src="https://img.shields.io/static/v1?label=Layer&amp;message=110-examples&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;color=525252"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-example-oauth-device-authorization-cli/"><img alt="Monthly PyPI downloads: tba-example-oauth-device-authorization-cli" src="https://img.shields.io/pypi/dm/tba-example-oauth-device-authorization-cli"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli/README.md"><img alt="README hits: tba-example-oauth-device-authorization-cli" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/110-examples/tba-example-oauth-device-authorization-cli/README.md.svg?label=README%20hits"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;color=525252"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

Try OAuth device login from a Python CLI against a configured TBA issuer.

- Package: `tba-example-oauth-device-authorization-cli`
- Layer: `110-examples`
- Responsibility: Example consumer package showing CLI login against tba_auth device authorization.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli/src/oauth_device_authorization_cli_example/__init__.py).
- Distribution: Python package on PyPI.

### Why This Package

`tba-example-oauth-device-authorization-cli` isolates this responsibility: Example consumer package showing CLI login against tba_auth device authorization. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli/src/oauth_device_authorization_cli_example/__init__.py) exposes `DeviceLoginError`, `DeviceAuthorizationPayload`, `DeviceLoginClient`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

For a live flow, register a client for the device authorization grant, substitute its ID and your issuer URL, and follow the browser instructions. The example caches returned tokens locally. Use a dedicated test account and protect the cache file.

### Features

- `DeviceLoginError`: Raised when the device login flow cannot complete.
- `DeviceAuthorizationPayload`: declared in src/oauth_device_authorization_cli_example/device_login.py
- `DeviceLoginClient`: Minimal client-side wrapper for RFC 8628 device authorization.

### Non-Goals

`tba-example-oauth-device-authorization-cli` does not take ownership of a production service guarantee or release certification.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli/pyproject.toml) declares runtime dependencies including `httpx`. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-example-oauth-device-authorization-cli`:

```bash
uv pip install tba-example-oauth-device-authorization-cli
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/110-examples/tba-example-oauth-device-authorization-cli
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-example-oauth-device-authorization-cli
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-example-oauth-device-authorization-cli
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-example-oauth-device-authorization-cli
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

Expect help for `--issuer`, `--client-id`, `--scope`, and `--token-cache`. This command uses the published package and needs no running issuer.

```bash
uvx --from tba-example-oauth-device-authorization-cli==0.1.1.dev1 oauth-device-login login --help
```

For a configured test deployment, replace the example issuer and client ID:

```bash
uvx --from tba-example-oauth-device-authorization-cli==0.1.1.dev1 oauth-device-login login --issuer https://issuer.example --client-id CLIENT_ID
```

The [device login guide](https://github.com/tigrbl/tigrbl_auth/blob/master/docs/examples/python-cli-device-login.md) explains discovery, browser approval, polling, and token storage.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli/docs/readme/quick_start.py).

```python
import oauth_device_authorization_cli_example

print(oauth_device_authorization_cli_example.__name__)
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-example-oauth-device-authorization-cli` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli/docs/readme/usage.py).

```python
import oauth_device_authorization_cli_example

print(oauth_device_authorization_cli_example.__name__)
```
<!-- readme-standards:end example.usage -->

The following public-entry-point example belongs to `tba-example-oauth-device-authorization-cli`. Example consumer package showing CLI login against tba_auth device authorization. Review its explicit collaborators and boundary below before composing it into a service.

### Configuration

Configure `tba-example-oauth-device-authorization-cli` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli/src/oauth_device_authorization_cli_example/__init__.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-example-oauth-device-authorization-cli` source raises `DeviceLoginError`, `SystemExit`. Handle these at the calling boundary and consult the implementation for the triggering conditions.

### Best Practices

Use the explicit `tba-example-oauth-device-authorization-cli` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `DeviceLoginError`, `DeviceAuthorizationPayload`, `DeviceLoginClient`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

`tba-example-oauth-device-authorization-cli` belongs to `110-examples` and owns executable integration examples: Example consumer package showing CLI login against tba_auth device authorization.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli/src/oauth_device_authorization_cli_example/__init__.py).

Keep a production service guarantee or release certification in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

### Public API and Import Surfaces

Import namespace: `oauth_device_authorization_cli_example`.

Source-declared exports or types: `DeviceLoginError`, `DeviceAuthorizationPayload`, `DeviceLoginClient`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli/src/oauth_device_authorization_cli_example/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
- `console_scripts` → `oauth-device-login` → `oauth_device_authorization_cli_example.main:main`
<!-- readme-standards:end entry-points -->

### Injected Dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli/src/oauth_device_authorization_cli_example/__init__.py) for `tba-example-oauth-device-authorization-cli` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

### Protocol Consumers

No direct package-manifest dependency on `tba-example-oauth-device-authorization-cli` was found in the audited three-repository inventory. External consumers may still use its documented imports or commands.

### Extensions

For `tba-example-oauth-device-authorization-cli`, use the source-declared public interfaces (`DeviceLoginError`, `DeviceAuthorizationPayload`, `DeviceLoginClient`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-example-oauth-device-authorization-cli` exposes executable integration examples. Inspect the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli/src/oauth_device_authorization_cli_example/__init__.py) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-example-oauth-device-authorization-cli`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli/src/oauth_device_authorization_cli_example/__init__.py). The `tba-example-oauth-device-authorization-cli` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-example-oauth-device-authorization-cli` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

See the [related repository tests](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-examples/tests/examples/test_python_cli_device_login.py) for the implementation scope covered by this example.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [tba-app-backend-public](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/090-backend-apps/tba-app-backend-public#readme) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)

### Certification Status

No external certification is asserted for `tba-example-oauth-device-authorization-cli` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli/src/oauth_device_authorization_cli_example/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-example-oauth-device-authorization-cli` provides example consumer package showing CLI login against tba_auth device authorization; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-example-oauth-device-authorization-cli`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli/src/oauth_device_authorization_cli_example/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-example-oauth-device-authorization-cli` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli/src/oauth_device_authorization_cli_example/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli/pyproject.toml) provide the supporting context for `tba-example-oauth-device-authorization-cli`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

`tba-example-oauth-device-authorization-cli` declares no local runtime dependency and has no direct consumer in the active manifest graph. Browse the [110-examples layer](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/110-examples) for adjacent package responsibilities; adjacency does not imply a dependency.

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-example-oauth-device-authorization-cli/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli)
- [pypi: tba-example-oauth-device-authorization-cli](https://pypi.org/project/tba-example-oauth-device-authorization-cli/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-example-oauth-device-authorization-cli/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-example-oauth-device-authorization-cli`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/110-examples/tba-example-oauth-device-authorization-cli` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.1` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-example-oauth-device-authorization-cli` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-example-oauth-device-authorization-cli` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

`tba-example-oauth-device-authorization-cli` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `110-examples` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-example-oauth-device-authorization-cli` source version is `0.1.1.dev1`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli/NOTICE) for attribution.
<!-- readme-standards:end notices -->
