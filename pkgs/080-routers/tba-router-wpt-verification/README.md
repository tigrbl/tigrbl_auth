# tba-router-wpt-verification

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-router-wpt-verification</strong></p>
<p align="center">Authenticated remote WIT/WPT verification for a configured recipient.</p>
<p align="center">
<a href="https://pypi.org/project/tba-router-wpt-verification/"><img alt="pypi: tba-router-wpt-verification" src="https://img.shields.io/pypi/v/tba-router-wpt-verification?labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wpt-verification/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wpt-verification/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wpt-verification/pyproject.toml"><img alt="Layer: 080-routers" src="https://img.shields.io/static/v1?label=Layer&amp;message=080-routers&amp;labelColor=1E293B&amp;color=6D28D9"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wpt-verification/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;labelColor=1E293B&amp;color=166534"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wpt-verification/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;labelColor=1E293B&amp;color=86198F"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wpt-verification/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;labelColor=1E293B&amp;color=86198F"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-router-wpt-verification/"><img alt="Monthly PyPI downloads: tba-router-wpt-verification" src="https://img.shields.io/pypi/dm/tba-router-wpt-verification?labelColor=1E293B&amp;color=0E7490"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wpt-verification/README.md"><img alt="README hits: tba-router-wpt-verification" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/080-routers/tba-router-wpt-verification/README.md.svg?label=README%20hits&amp;labelColor=1E293B&amp;color=0E7490"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wpt-verification/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wpt-verification/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;labelColor=1E293B&amp;color=6D28D9"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

Authenticated remote WIT/WPT verification for a configured recipient.

- Package: `tba-router-wpt-verification`
- Layer: `080-routers`
- Responsibility: Authenticated remote WIT/WPT verification for a configured recipient.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wpt-verification/src/tba_router_wpt_verification/__init__.py).
- Distribution: Python package on PyPI.

### Why This Package

`tba-router-wpt-verification` isolates this responsibility: Authenticated remote WIT/WPT verification for a configured recipient. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wpt-verification/src/tba_router_wpt_verification/binding.py) exposes `TokenHeader`, `WptVerificationRequest`, `WptVerificationResponse`, `build_wpt_verification_router`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-router-wpt-verification` for this responsibility: Authenticated remote WIT/WPT verification for a configured recipient. Its `080-routers` placement keeps transport-facing route composition separate from duplicating credential algorithms or storage ownership.

### Features

- `TokenHeader`: declared in src/tba_router_wpt_verification/schemas.py
- `WptVerificationRequest`: declared in src/tba_router_wpt_verification/schemas.py
- `WptVerificationResponse`: declared in src/tba_router_wpt_verification/schemas.py

### Non-Goals

`tba-router-wpt-verification` does not take ownership of duplicating credential algorithms or storage ownership.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wpt-verification/pyproject.toml) declares runtime dependencies including `tigrbl`, `pydantic`, `tba-concrete-jwt`, `tba-profile-workload-proof-wimse-wpt`. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-router-wpt-verification`:

```bash
uv pip install tba-router-wpt-verification
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/080-routers/tba-router-wpt-verification
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-router-wpt-verification
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-router-wpt-verification
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-router-wpt-verification
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

Mount `build_wpt_verification_router(verifier=..., audience=...,
authenticate=..., authorize_verification=...)` on a `TigrblApp`.
`authenticate` identifies the calling recipient service; the separate
`authorize_verification` callback must explicitly allow that service to delegate
verification for the configured audience. These checks precede proof validation.

`POST /wpt/verify` accepts:

```json
{
  "workload_identity_token": "<original WIT>",
  "workload_proof_token": "<original WPT, without the WPT scheme prefix>",
  "token_headers": [{"name": "Txn-Token", "value": "<original token>"}]
}
```

`token_headers` is a list so duplicate original headers remain observable and
are rejected when used as bindings. Do not collapse duplicates before forwarding.
Caller authentication belongs in this API request's headers, separately from
the submitted workload proof. Submitted audiences and trust configuration are rejected.
The audience and `required_token_headers` are selected when mounting. Required
headers must be present and cryptographically bound; clients cannot disable this
policy by omitting a header. This strict presence policy is separate from the
profile's optional `bound_token_headers` binding selector.

A successful response contains `valid`, `subject`, `audience`, `proof_id`, and
`expires_at`. Missing/denied caller credentials return 401/403, malformed requests
return 400, and invalid or replayed workload proofs return 401. Responses disable
caching and do not echo tokens. An infrastructure exception fails the request;
it never returns a successful verification decision.

Verification **consumes replay state**. Use the result once for the original
request; do not preflight it and then verify the same proof again. The result
authenticates the workload; the recipient still applies resource authorization.
Transport this delegation over the deployment's authenticated confidential channel.

Build from the repository root:

```bash
uv build --wheel pkgs/080-routers/tba-router-wpt-verification
```

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wpt-verification/docs/readme/quick_start.py).

```python
import tba_router_wpt_verification

print(tba_router_wpt_verification.__name__)
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-router-wpt-verification` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wpt-verification/docs/readme/usage.py).

```python
import tba_router_wpt_verification

print(tba_router_wpt_verification.__name__)
```
<!-- readme-standards:end example.usage -->

The following public-entry-point example belongs to `tba-router-wpt-verification`. Authenticated remote WIT/WPT verification for a configured recipient. Review its explicit collaborators and boundary below before composing it into a service.

### Configuration

Configure `tba-router-wpt-verification` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wpt-verification/src/tba_router_wpt_verification/binding.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wpt-verification/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-router-wpt-verification` source raises `ValueError`. Handle these at the calling boundary and consult the implementation for the triggering conditions.

### Best Practices

Use the explicit `tba-router-wpt-verification` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `TokenHeader`, `WptVerificationRequest`, `WptVerificationResponse`, `build_wpt_verification_router`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

`tba-router-wpt-verification` belongs to `080-routers` and owns transport-facing route composition: Authenticated remote WIT/WPT verification for a configured recipient.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wpt-verification/src/tba_router_wpt_verification/__init__.py). Public exports include `TokenHeader`, `WptVerificationRequest`, `WptVerificationResponse`, `build_wpt_verification_router`.

Keep duplicating credential algorithms or storage ownership in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

### Public API and Import Surfaces

Import namespace: `tba_router_wpt_verification`.

Source-declared exports or types: `TokenHeader`, `WptVerificationRequest`, `WptVerificationResponse`, `build_wpt_verification_router`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wpt-verification/src/tba_router_wpt_verification/binding.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

Explicit construction inputs and collaborators for `tba-router-wpt-verification`:

- `build_wpt_verification_router` construction inputs: `verifier`, `audience`, `authenticate`, `authorize_verification`, `required_token_headers`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wpt-verification/src/tba_router_wpt_verification/binding.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

### Protocol Consumers

Direct consumers in this checkout’s package manifests include `tba-app-backend-wpt-verifier`, `tba-workspace`. These edges describe declared dependencies, not protocol-conformance evidence.

### Extensions

For `tba-router-wpt-verification`, use the source-declared public interfaces (`TokenHeader`, `WptVerificationRequest`, `WptVerificationResponse`, `build_wpt_verification_router`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-router-wpt-verification` exposes transport-facing route composition. Public operations found in its source:

- `build_wpt_verification_router` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wpt-verification/src/tba_router_wpt_verification/binding.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-router-wpt-verification`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wpt-verification/src/tba_router_wpt_verification/binding.py). The `tba-router-wpt-verification` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-router-wpt-verification` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

Run `python -m pytest docs/readme/test_examples.py` from the `tba-router-wpt-verification` package directory for the maintained example source checks (Python compilation and non-Python file presence). Behavioral tests may live in the repository’s shared suites; the new README syntax test is not presented as runtime coverage for authenticated remote WIT/WPT verification for a configured recipient.

The repository README gate also checks the required heading tree, metadata, managed fragments, and referenced files.

```bash
uv run --extra test pytest pkgs/120-tests/tba-tests-workload-composition/tests/test_wit_wpt_services.py
```

### Certification Status

No external certification is asserted for `tba-router-wpt-verification` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wpt-verification/src/tba_router_wpt_verification/binding.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-router-wpt-verification` provides authenticated remote WIT/WPT verification for a configured recipient; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-router-wpt-verification`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wpt-verification/src/tba_router_wpt_verification/binding.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-router-wpt-verification` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wpt-verification/src/tba_router_wpt_verification/binding.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wpt-verification/pyproject.toml) provide the supporting context for `tba-router-wpt-verification`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

Declared local runtime dependencies:

- [tba-concrete-jwt](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-jwt/README.md)
- [tba-profile-workload-proof-wimse-wpt](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-proof-wimse-wpt/README.md)

Direct downstream consumers:

- [tba-app-backend-wpt-verifier](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-wpt-verifier/README.md)

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/080-routers/tba-router-wpt-verification#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/080-routers/tba-router-wpt-verification#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-router-wpt-verification/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/080-routers/tba-router-wpt-verification)
- [pypi: tba-router-wpt-verification](https://pypi.org/project/tba-router-wpt-verification/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/080-routers/tba-router-wpt-verification)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wpt-verification/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wpt-verification/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wpt-verification/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-router-wpt-verification/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-router-wpt-verification`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/080-routers/tba-router-wpt-verification` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.3` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-router-wpt-verification` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-router-wpt-verification` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wpt-verification/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

`tba-router-wpt-verification` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `080-routers` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-router-wpt-verification` source version is `0.4.0.dev3`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wpt-verification/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-wpt-verification/NOTICE) for attribution.
<!-- readme-standards:end notices -->
