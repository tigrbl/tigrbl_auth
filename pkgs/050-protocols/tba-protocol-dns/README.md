# tba-protocol-dns

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-protocol-dns</strong></p>
<p align="center">DNS zone transfers, updates, discovery, and authentication protocols.</p>
<p align="center">
<a href="https://pypi.org/project/tba-protocol-dns/"><img alt="pypi: tba-protocol-dns unpublished" src="https://img.shields.io/static/v1?label=pypi&amp;message=tba-protocol-dns%20unpublished&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-dns/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-dns/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-dns/pyproject.toml"><img alt="Layer: 050-protocols" src="https://img.shields.io/static/v1?label=Layer&amp;message=050-protocols&amp;labelColor=1E293B&amp;color=6D28D9"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-dns/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;labelColor=1E293B&amp;color=166534"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-dns/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;labelColor=1E293B&amp;color=86198F"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-dns/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;labelColor=1E293B&amp;color=86198F"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-protocol-dns/"><img alt="pypi downloads: tba-protocol-dns: unpublished" src="https://img.shields.io/static/v1?label=pypi%20downloads&amp;message=tba-protocol-dns%3A%20unpublished&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-dns/README.md"><img alt="README hits: tba-protocol-dns" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/050-protocols/tba-protocol-dns/README.md.svg?label=README%20hits&amp;labelColor=1E293B&amp;color=0E7490"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-dns/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-dns/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;labelColor=1E293B&amp;color=6D28D9"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

This package covers composing discovery and authenticated DNS protocol exchanges.

DNS zone transfers, dynamic updates, DNSSEC, ZONEMD, verified resolver
discovery, and GSS-TSIG negotiation. The package uses
[tba-provider-dns-resolver](../../20-providers/tba-provider-dns-resolver) for network exchange
and [tba-concrete-dns-zone](../../10-concrete/tba-concrete-dns-zone) for zone
state. Install `tba-protocol-dns[dnssec]` to sign and validate DNSSEC
records.

Import protocol modules from `tba_protocol_dns` and zones from
`tba_concrete_dns_zone.zone` or `tba_concrete_dns_zone.btreezone`. Use
`tba_protocol_dns.ddr.try_ddr(resolver)` or
`await tba_protocol_dns.ddr.try_ddr_async(resolver)` for verified discovery.

The [DNS interoperability suite](../../120-tests/tba-tests-interop-dns)
exercises GSS-TSIG against BIND and Kerberos.

### Why This Package

It gives dns discovery, zone transfers, and updates a separate boundary with independently verifiable behavior.

### When to Use

Use this package when a caller needs composing discovery and authenticated DNS protocol exchanges.

### Features

Use the package for composing discovery and authenticated DNS protocol exchanges. The authored notes above cover the supported behavior and examples.

### Non-Goals

Constructing an update does not send it or confer permission to update an authoritative server.

---

## Getting Started

### Prerequisites

Use Python 3.10–3.15 in the repository workspace. The examples use local inputs.

### Installation

#### uv

<!-- readme-standards:begin installation.uv -->
`tba-protocol-dns` is not declared published. From the source checkout:

```bash
uv pip install .
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
`tba-protocol-dns` is not declared published. From the source checkout:

```bash
python -m pip install .
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
`tba-protocol-dns` is not declared published. From a separate Poetry project, replace the path with your checkout:

```bash
poetry add /path/to/tba-protocol-dns
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-dns/docs/readme/quick_start.py).

```python
from tba_protocol_dns.update import Update

update = Update('example.com.')
assert update.changes == []
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The local example checks the declared interface without making a live DNS request.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-dns/docs/readme/usage.py).

```python
from tba_protocol_dns.update import Update

update = Update('example.com.')
update.add('www', 60, 'A', '192.0.2.10')
assert len(update.changes) == 1
```
<!-- readme-standards:end example.usage -->

### Configuration

Callers supply an origin, endpoint, and trust or signing material for operations that use it.

### Error Handling

Treat validation errors as failed operations. Inspect the original exception before choosing whether to retry.

### Best Practices

Keep the example inputs local when validating a new installation. Run the applicable integration tests separately.

---

## Package Boundary

### What It Owns

The owning boundary is composing discovery and authenticated DNS protocol exchanges.

### Public API and Import Surfaces

Start with the public interfaces imported in the maintained examples. They demonstrate composing discovery and authenticated DNS protocol exchanges.

### Entry Points

<!-- readme-standards:begin entry-points -->
- `tba.dns.inbound_xfr` → `protocol` → `tba_protocol_dns.xfr:inbound_xfr`
- `tba.dns.inbound_xfr` → `sync` → `tba_protocol_dns.xfr:inbound_xfr_sync`
- `tba.dns.inbound_xfr` → `xfr` → `tba_protocol_dns.xfr:xfr`
<!-- readme-standards:end entry-points -->

### Injected Dependencies

The calling code owns the external inputs. Callers supply an origin, endpoint, and trust or signing material for operations that use it.

### Protocol Consumers

DNS administration and resolver discovery can use this layer without owning wire codecs or client sockets.

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

Use this package when the application needs composing discovery and authenticated DNS protocol exchanges.

### How

Start with the local example and compare its result with the expected result before wiring it into a caller.

### When

Choose this boundary when the application needs composing discovery and authenticated DNS protocol exchanges.

---

## Documentation and Related Packages

### More Documentation

See the package notes in the Summary and the repository package standards.

### Related Packages

See [tba-provider-dns-resolver](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs) for the adjacent DNS boundary.

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-dns#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-dns#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-protocol-dns/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-dns)
- [pypi: tba-protocol-dns](https://pypi.org/project/tba-protocol-dns/)
<!-- readme-standards:end project-links -->

---

## Contributing

### How to Contribute

Keep proposed changes scoped to this package and include evidence for behavior changes.

### Development Setup

From the repository root, use the locked Python workspace and run the relevant DNS test selection.

### Notes for Maintainers

Keep the exported behavior for composing discovery and authenticated DNS protocol exchanges covered by ordinary DNS inputs in CI.

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
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-dns/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-dns/NOTICE) for attribution.
<!-- readme-standards:end notices -->
