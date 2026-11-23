# tba-runtime-identity

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-runtime-identity</strong></p>
<p align="center">Runtime assembly, profile loading, feature flags, deployment resolution, runner adapters, and diagnostics for TBA identity apps.</p>
<p align="center">
<a href="https://pypi.org/project/tba-runtime-identity/"><img alt="pypi: tba-runtime-identity" src="https://img.shields.io/pypi/v/tba-runtime-identity"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/pyproject.toml"><img alt="Source version: 0.4.0.dev4" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev4&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/pyproject.toml"><img alt="Layer: 060-runtime" src="https://img.shields.io/static/v1?label=Layer&amp;message=060-runtime&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;color=525252"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-runtime-identity/"><img alt="Monthly PyPI downloads: tba-runtime-identity" src="https://img.shields.io/pypi/dm/tba-runtime-identity"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/README.md"><img alt="README hits: tba-runtime-identity" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/060-runtime/tba-runtime-identity/README.md.svg?label=README%20hits"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;color=525252"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

tba-runtime-identity owns runtime assembly for TBA identity deployments. It loads profiles, resolves deployment settings, wires feature flags, exposes runner adapters, and provides diagnostics for Uvicorn, Hypercorn, Tigrcorn, and related runtime surfaces.

- Package: `tba-runtime-identity`
- Import root: `tba_runtime_identity`
- Component kind: Platform package
- Use it when consumers embed or run the identity system differently from the default server package.
- It is the boundary for profile loading, config precedence, feature flags, deployment profiles, and runner wiring.
- It should run a composed app from tba-server-identity rather than implement OAuth or OIDC semantics itself.

### Why This Package

`tba-runtime-identity` isolates this responsibility: Runtime assembly, profile loading, feature flags, deployment resolution, runner adapters, and diagnostics for TBA identity apps. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/src/tba_runtime_identity/_deployment/defaults.py) exposes `CONFIG_PRECEDENCE`, `CapabilityFactory`, `CapabilityRegistry`, `ENGINE`, `LazyASGIApplication`, `ProtocolCapabilityBindingError`, `ReadinessDiagnostic`, `ReadinessStatus`, `RunnerAdapter`, `RuntimeCapabilityAssembly`, `RuntimePlan`, `RuntimeProfile`, `RuntimeStandard`, `STANDARD_OWNER_MODULES`, `WebAuthnComposition`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-runtime-identity` for this responsibility: Runtime assembly, profile loading, feature flags, deployment resolution, runner adapters, and diagnostics for TBA identity apps. Its `060-runtime` placement keeps runtime composition and operator entry points separate from duplicating protocol grammars, table declarations, or provider implementations.

### Features

- `ResolvedDeployment`: declared in src/tba_runtime_identity/_deployment/resolved_deployment.py
- `SurfaceBoundaryClassification`: declared in src/tba_runtime_identity/_surfaces/registries.py
- `ReadinessStatus`: declared in src/tba_runtime_identity/assembly.py
- `RuntimeProfile`: declared in src/tba_runtime_identity/assembly.py
- `ReadinessDiagnostic`: declared in src/tba_runtime_identity/assembly.py
- `AuthError`: declared in src/tba_runtime_identity/backends.py
- `PasswordBackend`: declared in src/tba_runtime_identity/backends.py
- `ApiKeyBackend`: declared in src/tba_runtime_identity/backends.py

### Non-Goals

`tba-runtime-identity` does not take ownership of duplicating protocol grammars, table declarations, or provider implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/pyproject.toml) declares runtime dependencies including `cryptography`, `tba-bases-certificate`, `tba-concrete-certificate-x509`, `tba-contracts-security-trust`, `tba-profile-workload-credential-wimse-wic`, `tba-profile-workload-credential-wimse-wit`, `tba-profile-workload-proof-wimse-wpt`, `tba-protocol-workload-wimse-identifier`, `tba-provider-jose-cryptography`, `tba-profile-workload-authentication-wimse-mtls`, `tba-provider-secret-hashing-bcrypt`, `tigrbl`. Read the example’s inputs and service requirements before execution.

### Installation

```bash
pip install tba-runtime-identity
# or
uv add tba-runtime-identity
```

Install the current `tba-runtime-identity` source checkout when working ahead of a PyPI release:

```bash
uv pip install ./pkgs/060-runtime/tba-runtime-identity
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-runtime-identity
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-runtime-identity
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-runtime-identity
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.


```bash
uv run --isolated --no-project --python 3.12 --with "tba-runtime-identity==0.4.0.dev4" python quickstart.py
```

The import and assertion succeed when the CapabilityRegistry entry point is available.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/docs/readme/quick_start.py).

```python
from tba_runtime_identity import CapabilityRegistry

assert callable(CapabilityRegistry)
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-runtime-identity` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/docs/readme/usage.py).

```python
from tba_runtime_identity.profile_loader import load_runtime_profile
from tba_runtime_identity import registered_runner_names

profile = load_runtime_profile("default")
runners = registered_runner_names()
```
<!-- readme-standards:end example.usage -->

### Configuration

The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/src/tba_runtime_identity/_deployment/defaults.py) references configuration keys `ASYNC_FALLBACK_DB`, `AUTHN_ISSUER`, `JWT_SECRET`, `LOG_LEVEL`, `PG_DB`, `PG_DSN`, `PG_HOST`, `PG_PASS`, `PG_USER`, `POSTGRES_URL`, `REDIS_HOST`, `REDIS_PASSWORD`. Consult the constructor or function signature before supplying them; a referenced key is not necessarily a global environment variable.

### Error Handling

The inspected `tba-runtime-identity` source raises `AttributeError`, `AuthError`, `KeyError`, `LookupError`, `ModuleNotFoundError`, `NotImplementedError`, `PermissionError`, `ProtocolCapabilityBindingError`, `RuntimeError`, `RuntimeProfileError`. Handle these at the calling boundary and consult the implementation for the triggering conditions.

### Best Practices

Use the explicit `tba-runtime-identity` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `CONFIG_PRECEDENCE`, `CapabilityFactory`, `CapabilityRegistry`, `ENGINE`, `LazyASGIApplication`, `ProtocolCapabilityBindingError`, `ReadinessDiagnostic`, `ReadinessStatus`, `RunnerAdapter`, `RuntimeCapabilityAssembly`, `RuntimePlan`, `RuntimeProfile`, `RuntimeStandard`, `STANDARD_OWNER_MODULES`, `WebAuthnComposition`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

- Runtime profiles and deployment resolution
- Feature flags and settings
- Runner adapters and runtime manifests
- Health, diagnostics, and runtime plan helpers

### Public API and Import Surfaces

Import namespace: `tba_runtime_identity`.

Source-declared exports or types: `CONFIG_PRECEDENCE`, `CapabilityFactory`, `CapabilityRegistry`, `ENGINE`, `LazyASGIApplication`, `ProtocolCapabilityBindingError`, `ReadinessDiagnostic`, `ReadinessStatus`, `RunnerAdapter`, `RuntimeCapabilityAssembly`, `RuntimePlan`, `RuntimeProfile`, `RuntimeStandard`, `STANDARD_OWNER_MODULES`, `WebAuthnComposition`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/src/tba_runtime_identity/_deployment/defaults.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

Explicit construction inputs and collaborators for `tba-runtime-identity`:

- `resolve_config` construction inputs: `defaults`, `profile`, `environment`, `explicit`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/src/tba_runtime_identity/assembly.py).
- `resolve_feature_flags` construction inputs: `defaults`, `profile`, `explicit`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/src/tba_runtime_identity/assembly.py).
- `LazyASGIApplication` construction inputs: `factory`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/src/tba_runtime_identity/base.py).
- `build_runtime_capability_assembly` construction inputs: `build_providers`, `build_storage_runtime`, `build_capabilities`, `build_protocols`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/src/tba_runtime_identity/capability_assembly.py).
- `CapabilityRegistry` construction inputs: `capabilities`, `factories`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/src/tba_runtime_identity/capability_registry.py).
- `build_webauthn_composition` construction inputs: `begin_registration`, `complete_registration`, `begin_authentication`, `complete_authentication`, `list_credentials`, `rename_credential`, `revoke_credential`, `configuration`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/src/tba_runtime_identity/composition/webauthn.py).
- `build_workload_identity_composition` construction inputs: `dependencies`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/src/tba_runtime_identity/composition/workload_identity.py).
- `build_runtime_plan` construction inputs: `deployment`, `runner`, `environment`, `app_factory`, `host`, `port`, `workers`, `uds`, `log_level`, `access_log`, `lifespan`, `graceful_timeout`, `pid_file`, `proxy_headers`, `require_tls`, `enable_mtls`, `cookies`, `health`, `metrics`, `public`, `admin`, `rpc`, `diagnostics`, `jwks_refresh_seconds`, `runner_options`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/src/tba_runtime_identity/plan.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

### Protocol Consumers

Direct consumers in this checkout’s package manifests include `tba-certification-release`, `tba-cli-identity`, `tba-plugin-tigrbl`, `tba-server-identity`, `tba-auth`, `tba-router-administration-gate`, `tba-router-wic-ca`, `tba-router-wit-issuance`, `tba-app-backend-core`, `tba-app-backend-wic-ca`, `tba-app-backend-wit-issuance`, `tba-workspace`. These edges describe declared dependencies, not protocol-conformance evidence.

### Extensions

For `tba-runtime-identity`, use the source-declared public interfaces (`CONFIG_PRECEDENCE`, `CapabilityFactory`, `CapabilityRegistry`, `ENGINE`, `LazyASGIApplication`, `ProtocolCapabilityBindingError`, `ReadinessDiagnostic`, `ReadinessStatus`, `RunnerAdapter`, `RuntimeCapabilityAssembly`, `RuntimePlan`, `RuntimeProfile`, `RuntimeStandard`, `STANDARD_OWNER_MODULES`, `WebAuthnComposition`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-runtime-identity` exposes runtime composition and operator entry points. Public operations found in its source:

- `ReadinessDiagnostic.ready` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/src/tba_runtime_identity/assembly.py).
- `resolve_config` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/src/tba_runtime_identity/assembly.py).
- `resolve_feature_flags` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/src/tba_runtime_identity/assembly.py).
- `provider_runtime_profile` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/src/tba_runtime_identity/assembly.py).
- `testkit_provider_runtime_profile` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/src/tba_runtime_identity/assembly.py).
- `readiness_diagnostic` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/src/tba_runtime_identity/assembly.py).
- `LazyASGIApplication.materialize` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/src/tba_runtime_identity/base.py).
- `RunnerAdapter.available_module_name` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/src/tba_runtime_identity/base.py).
- `RunnerAdapter.is_available` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/src/tba_runtime_identity/base.py).
- `RunnerAdapter.import_module` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/src/tba_runtime_identity/base.py).
- `RunnerAdapter.base_validation` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/src/tba_runtime_identity/base.py).
- `RunnerAdapter.validate` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/src/tba_runtime_identity/base.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-runtime-identity`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/src/tba_runtime_identity/_deployment/defaults.py). The `tba-runtime-identity` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-runtime-identity` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

When WIMSE WPT verification is enabled, workload composition also constructs
`wimse_wpt_issuer` if `wpt_signer`, `wpt_wit`, and
`wpt_workload_key_reference` are supplied together. Partial issuer configuration
is rejected. Existing verifier-only composition is unchanged; direct use of the
profile's `WptProofIssuer` remains available for sender-only processes.

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/src/tba_runtime_identity/__init__.py).

### Certification Status

No external certification is asserted for `tba-runtime-identity` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/src/tba_runtime_identity/_deployment/defaults.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-runtime-identity` provides runtime assembly, profile loading, feature flags, deployment resolution, runner adapters, and diagnostics for TBA identity apps; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-runtime-identity`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/src/tba_runtime_identity/_deployment/defaults.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-runtime-identity` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/src/tba_runtime_identity/_deployment/defaults.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/pyproject.toml) provide the supporting context for `tba-runtime-identity`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

- [tba-runtime-identity-administration](https://pypi.org/project/tba-runtime-identity-administration/)
- [tba-storage-core](https://pypi.org/project/tba-storage-core/)
- [tba-server-identity](https://pypi.org/project/tba-server-identity/)
- [tba-runtime-identity](https://pypi.org/project/tba-runtime-identity/)
- [tba-operator-identity](https://pypi.org/project/tba-operator-identity/)
- [tba-tests-identity](https://pypi.org/project/tba-tests-identity/)

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/060-runtime/tba-runtime-identity#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/060-runtime/tba-runtime-identity#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-runtime-identity/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [SSOT](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/060-runtime/tba-runtime-identity)
- [pypi: tba-runtime-identity](https://pypi.org/project/tba-runtime-identity/)
<!-- readme-standards:end project-links -->

- [PyPI package](https://pypi.org/project/tba-runtime-identity/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/060-runtime/tba-runtime-identity)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/060-runtime/tba-runtime-identity)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-runtime-identity/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-runtime-identity`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/060-runtime/tba-runtime-identity` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.1` without resolving unrelated runtime packages.

### Notes for Maintainers

**WIMSE workload identity**

The `workload.wic_service` and `workload.wit_token_service` modules expose
issuance to applications with an authenticated workload enrollment principal.
Each service resolves the authorized identity in its configured trust domain.

Receiving applications can call `build_workload_identity_composition()` with
`enable_wimse_wpt=True`. Supply `wit_trust_by_domain` and `wpt_replay_store`
along with the workload credential dependencies. Composition exposes
`wimse_wpt_verifier` for HTTP authentication and proof verification. Set the
expected recipient audience from application configuration. Use a shared
atomic replay store when multiple replicas receive the same audience.

---

## Governance

### Ownership and Decision Making

Changes to `tba-runtime-identity` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

This package is part of the SSOT-governed TBA identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.

`tba-runtime-identity` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `060-runtime` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-runtime-identity` source version is `0.4.0.dev4`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/NOTICE) for attribution.
<!-- readme-standards:end notices -->
