# tba-codec-dns

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-codec-dns</strong></p>
<p align="center">DNS wire messages and type-specific resource record data codecs.</p>
<p align="center">
<a href="https://pypi.org/project/tba-codec-dns/"><img alt="pypi: tba-codec-dns unpublished" src="https://img.shields.io/static/v1?label=pypi&amp;message=tba-codec-dns%20unpublished&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dns/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dns/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dns/pyproject.toml"><img alt="Layer: 003-codecs" src="https://img.shields.io/static/v1?label=Layer&amp;message=003-codecs&amp;labelColor=1E293B&amp;color=6D28D9"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dns/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;labelColor=1E293B&amp;color=166534"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dns/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;labelColor=1E293B&amp;color=86198F"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dns/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;labelColor=1E293B&amp;color=86198F"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-codec-dns/"><img alt="pypi downloads: tba-codec-dns: unpublished" src="https://img.shields.io/static/v1?label=pypi%20downloads&amp;message=tba-codec-dns%3A%20unpublished&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dns/README.md"><img alt="README hits: tba-codec-dns" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/003-codecs/tba-codec-dns/README.md.svg?label=README%20hits&amp;labelColor=1E293B&amp;color=0E7490"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dns/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dns/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;labelColor=1E293B&amp;color=6D28D9"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

This package covers DNS wire-message and record-data encoding.

Use `wire` for complete DNS messages and `rdata` for individual resource record
payloads. The package also provides RRsets, EDNS options, and DNS presentation
formats.

```python
from tba_codec_dns import rdata, wire

query = wire.make_query("example.com.", "MX")
assert wire.Message.from_wire(query.to_wire()) == query

record = rdata.from_text("IN", "MX", "10 mail.example.com.")
assert rdata.from_wire("IN", "MX", record.to_wire()) == record
```

Use `rdata.get_rdata_class()` for type-specific constructors and field access.
DNS messages support opt-in TSIG signing and parser verification with a key or
keyring. Pass `continue_on_error=True` to collect recoverable errors with
their byte offsets, or use `Message.rrsets()` for grouped records.

```python
from tba_codec_dns.tsig import TsigKey

key = TsigKey((b"key", b"example"), b"example shared secret")
outgoing = query.use_tsig(key).to_wire()
incoming = wire.from_wire(outgoing, keyring=key)
assert incoming.had_tsig
```

Omitting the wire parser's keyring retains the parse-only behavior of existing
callers. Supply a key or keyring when the caller requires authentication.

Verify with the codec cases in [the DNS test suite](../../120-tests/tba-tests-dns).

### Why This Package

It gives dns messages and record encodings a separate boundary with independently verifiable behavior.

### When to Use

Use this package when a caller needs DNS wire-message and record-data encoding.

### Features

Use the package for DNS wire-message and record-data encoding. The authored notes above cover the supported behavior and examples.

### Non-Goals

Encoding a packet does not send it, establish peer trust, or interpret a resolver result.

---

## Getting Started

### Prerequisites

Use Python 3.10–3.15 in the repository workspace. The examples use local inputs.

### Installation

#### uv

<!-- readme-standards:begin installation.uv -->
`tba-codec-dns` is not declared published. From the source checkout:

```bash
uv pip install .
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
`tba-codec-dns` is not declared published. From the source checkout:

```bash
python -m pip install .
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
`tba-codec-dns` is not declared published. From a separate Poetry project, replace the path with your checkout:

```bash
poetry add /path/to/tba-codec-dns
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dns/docs/readme/quick_start.py).

```python
from tba_codec_dns.wire import make_query

query = make_query('example.com.', 'A')
assert query.to_wire()
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The local example checks the declared interface without making a live DNS request.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dns/docs/readme/usage.py).

```python
from tba_codec_dns.wire import Message, make_query

query = make_query('example.com.', 'TXT')
assert Message.from_wire(query.to_wire()).questions == query.questions
```
<!-- readme-standards:end example.usage -->

### Configuration

Callers choose the name, record type, class, and optional EDNS settings.

### Error Handling

Treat validation errors as failed operations. Inspect the original exception before choosing whether to retry.

### Best Practices

Keep the example inputs local when validating a new installation. Run the applicable integration tests separately.

---

## Package Boundary

### What It Owns

The owning boundary is DNS wire-message and record-data encoding.

### Public API and Import Surfaces

Start with the public interfaces imported in the maintained examples. They demonstrate DNS wire-message and record-data encoding.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

The calling code owns the external inputs. Callers choose the name, record type, class, and optional EDNS settings.

### Protocol Consumers

The resolver, zone, and protocol packages share these question and record representations.

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

Use this package when the application needs DNS wire-message and record-data encoding.

### How

Start with the local example and compare its result with the expected result before wiring it into a caller.

### When

Choose this boundary when the application needs DNS wire-message and record-data encoding.

---

## Documentation and Related Packages

### More Documentation

See the package notes in the Summary and the repository package standards.

### Related Packages

See [tba-primitives-dns-name](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs) for the adjacent DNS boundary.

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/003-codecs/tba-codec-dns#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/003-codecs/tba-codec-dns#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-codec-dns/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/003-codecs/tba-codec-dns)
- [pypi: tba-codec-dns](https://pypi.org/project/tba-codec-dns/)
<!-- readme-standards:end project-links -->

---

## Contributing

### How to Contribute

Keep proposed changes scoped to this package and include evidence for behavior changes.

### Development Setup

From the repository root, use the locked Python workspace and run the relevant DNS test selection.

### Notes for Maintainers

Keep the exported behavior for DNS wire-message and record-data encoding covered by ordinary DNS inputs in CI.

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
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dns/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/003-codecs/tba-codec-dns/NOTICE) for attribution.
<!-- readme-standards:end notices -->
