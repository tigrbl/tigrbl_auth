# tba-tests-interop-dns

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-tests-interop-dns</strong></p>
<p align="center">Independent DNS interoperability suite for Tigrbl Auth.</p>
<p align="center">
<a href="https://pypi.org/project/tba-tests-interop-dns/"><img alt="pypi: tba-tests-interop-dns unpublished" src="https://img.shields.io/static/v1?label=pypi&amp;message=tba-tests-interop-dns%20unpublished&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-dns/pyproject.toml"><img alt="Source version: 0.4.0.dev2" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev2&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-dns/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-dns/pyproject.toml"><img alt="Layer: 120-tests" src="https://img.shields.io/static/v1?label=Layer&amp;message=120-tests&amp;labelColor=1E293B&amp;color=6D28D9"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-dns/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;labelColor=1E293B&amp;color=166534"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-dns/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;labelColor=1E293B&amp;color=86198F"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-dns/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;labelColor=1E293B&amp;color=86198F"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-tests-interop-dns/"><img alt="pypi downloads: tba-tests-interop-dns: unpublished" src="https://img.shields.io/static/v1?label=pypi%20downloads&amp;message=tba-tests-interop-dns%3A%20unpublished&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-dns/README.md"><img alt="README hits: tba-tests-interop-dns" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/120-tests/tba-tests-interop-dns/README.md.svg?label=README%20hits&amp;labelColor=1E293B&amp;color=0E7490"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-dns/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-dns/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;labelColor=1E293B&amp;color=6D28D9"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

This package covers checking production wheels against BIND and a test Kerberos KDC.

Run the GSS-TSIG interoperability probe against BIND 9.20.31 and an MIT Kerberos
KDC. The container generates fixture credentials and exchanges DNS packets on
its loopback interface. The probe installs the production wheels from a
read-only mount.

Run from the repository root.

```bash
uv build --wheel --out-dir dist/dns pkgs/000-primitives/tba-primitives-dns-name
uv build --wheel --out-dir dist/dns pkgs/003-codecs/tba-codec-dns
uv build --wheel --out-dir dist/dns pkgs/010-concrete/tba-concrete-dns-zone
uv build --wheel --out-dir dist/dns pkgs/020-providers/tba-provider-dns-resolver
uv build --wheel --out-dir dist/dns pkgs/050-protocols/tba-protocol-dns
docker build -t tba-dns-gss-interop:local pkgs/120-tests/tba-tests-interop-dns
docker run --rm --network none --mount "type=bind,source=${PWD}/dist/dns,target=/wheels,readonly" tba-dns-gss-interop:local
```

The probe checks authenticated TKEY negotiation, a signed UPDATE and reply,
policy denial, and rejection of a tampered message.

### Why This Package

It gives source-only dns interoperability harness a separate boundary with independently verifiable behavior.

### When to Use

Use this package when a caller needs checking production wheels against BIND and a test Kerberos KDC.

### Features

Use the package for checking production wheels against BIND and a test Kerberos KDC. The authored notes above cover the supported behavior and examples.

### Non-Goals

The fixture is not a published library or a server configuration for production.

---

## Getting Started

### Prerequisites

Use Python 3.10–3.15 in the repository workspace. The examples use local inputs.

### Installation

#### uv

<!-- readme-standards:begin installation.uv -->
This is a source-only workspace or test harness, not an installable distribution. From its checkout, synchronize the declared environment:

```bash
uv sync
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
This is a source-only workspace or test harness, not an installable distribution. Use the uv checkout workflow above; this installer does not install the harness itself.
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
This is a source-only workspace or test harness, not an installable distribution. Use the uv checkout workflow above; this installer does not install the harness itself.
<!-- readme-standards:end installation.poetry -->

### Quick Start

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-dns/docs/readme/quick_start.py).

```python
from pathlib import Path

assert Path('pkgs/120-tests/tba-tests-interop-dns/Dockerfile').is_file()
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

This walkthrough checks the declared interface without making a live DNS request.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-dns/docs/readme/usage.py).

```python
from pathlib import Path

recipe = Path('pkgs/120-tests/tba-tests-interop-dns/Dockerfile').read_text()
assert 'FROM ' in recipe
```
<!-- readme-standards:end example.usage -->

### Configuration

The fixture requires the relevant built wheels and a Docker installation for its full interoperability run.

### Error Handling

Treat validation errors as failed operations. Inspect the original exception before choosing whether to retry.

### Best Practices

Keep the example inputs local when validating a new installation. Run the applicable integration tests separately.

---

## Package Boundary

### What It Owns

The owning boundary is checking production wheels against BIND and a test Kerberos KDC.

### Public API and Import Surfaces

Start with the public interfaces imported in the maintained examples. They demonstrate checking production wheels against BIND and a test Kerberos KDC.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

The calling code owns the external inputs. The fixture requires the relevant built wheels and a Docker installation for its full interoperability run.

### Protocol Consumers

This checkout harness verifies behavior of the DNS production distributions against an independent server.

### Extensions

Keep extensions at the package boundary. Use the documented inputs rather than replacing internal state.

---

## Operations and Readiness

### Operational Requirements

Run the nearest DNS tests in the repository before relying on this code in another environment.

### Health and Observability

The local examples verify a single operation. Use the owning application’s logs and integration tests for deployment readiness.

### Security and Resource Limits

Use trusted configuration and treat data from DNS peers or local files as input that needs validation.

### Compatibility

Run the workspace’s supported Python matrix when changing feature behavior or dependencies.

---

## Verification

### Tests

Run the repository’s DNS tests and the README example source checks.

### Certification Status

The package README and example checks are separate from interoperability or deployment certification.

### Evidence

Review the repository CI results and the DNS test suite for the actual checks run on a revision.

---

## FAQ

### Why

Use this package when the application needs checking production wheels against BIND and a test Kerberos KDC.

### How

Start with the local example and compare its result with the expected result before wiring it into a caller.

### When

Choose this boundary when the application needs checking production wheels against BIND and a test Kerberos KDC.

---

## Documentation and Related Packages

### More Documentation

See the package notes in the Summary and the repository package standards.

### Related Packages

See [tba-protocol-dns](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs) for the adjacent DNS boundary.

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/120-tests/tba-tests-interop-dns#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/120-tests/tba-tests-interop-dns#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/120-tests/tba-tests-interop-dns)
- [pypi: tba-tests-interop-dns](https://pypi.org/project/tba-tests-interop-dns/)
<!-- readme-standards:end project-links -->

---

## Contributing

### How to Contribute

Keep proposed changes scoped to this package and include evidence for behavior changes.

### Development Setup

From the repository root, use the locked Python workspace and run the relevant DNS test selection.

### Notes for Maintainers

Keep the exported behavior for checking production wheels against BIND and a test Kerberos KDC covered by ordinary DNS inputs in CI.

---

## Governance

### Ownership and Decision Making

The Tigrbl Auth repository maintains this package and its layer-specific contract.

### Standards and Policies

Follow the repository package-guide-v1 policy and current Apache attribution files.

### Lifecycle and Migration

Check the package manifest and workspace lock when updating a caller. Review source and wheel evidence separately.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-dns/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-dns/NOTICE) for attribution.
<!-- readme-standards:end notices -->
