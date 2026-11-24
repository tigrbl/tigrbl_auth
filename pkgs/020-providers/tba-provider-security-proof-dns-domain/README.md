# tba-provider-security-proof-dns-domain

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-provider-security-proof-dns-domain</strong></p>
<p align="center">Exact DNS TXT ownership proof and CNAME target verification.</p>
<p align="center">
<a href="https://pypi.org/project/tba-provider-security-proof-dns-domain/"><img alt="pypi: tba-provider-security-proof-dns-domain" src="https://img.shields.io/pypi/v/tba-provider-security-proof-dns-domain?labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-proof-dns-domain/pyproject.toml"><img alt="Source version: 0.1.0" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.1.0&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-proof-dns-domain/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-proof-dns-domain/pyproject.toml"><img alt="Layer: 020-providers" src="https://img.shields.io/static/v1?label=Layer&amp;message=020-providers&amp;labelColor=1E293B&amp;color=6D28D9"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-proof-dns-domain/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;labelColor=1E293B&amp;color=166534"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-proof-dns-domain/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;labelColor=1E293B&amp;color=86198F"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-proof-dns-domain/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;labelColor=1E293B&amp;color=86198F"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-provider-security-proof-dns-domain/"><img alt="Monthly PyPI downloads: tba-provider-security-proof-dns-domain" src="https://img.shields.io/pypi/dm/tba-provider-security-proof-dns-domain?labelColor=1E293B&amp;color=0E7490"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-proof-dns-domain/README.md"><img alt="README hits: tba-provider-security-proof-dns-domain" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/020-providers/tba-provider-security-proof-dns-domain/README.md.svg?label=README%20hits&amp;labelColor=1E293B&amp;color=0E7490"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-proof-dns-domain/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-proof-dns-domain/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;labelColor=1E293B&amp;color=6D28D9"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

Verifies an exact TXT challenge and CNAME destination through a trusted HTTPS recursive resolver.

### Why This Package

Applications share DNS validation while retaining ownership of hostname claims.

### When to Use

Verify control of a hostname before turning on customer traffic.

### Features

Checks exact record owners, a TXT proof value, and the expected CNAME destination.

### Non-Goals

The calling application owns TLS provisioning, DNS changes, access decisions, and challenge storage.

---

## Getting Started

### Prerequisites

Use a supported Python version and an HTTPS recursive resolver with DNS JSON responses.

### Installation

Install the package using your project’s Python package manager.

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-provider-security-proof-dns-domain
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-provider-security-proof-dns-domain
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-provider-security-proof-dns-domain
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

Construct the verifier with the URL of a trusted DNS resolver.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-proof-dns-domain/docs/readme/quick_start.py).

```python
from tba_provider_security_proof_dns_domain import DnsDomainOwnershipVerifier

verifier = DnsDomainOwnershipVerifier("https://resolver.example/dns-query")
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The verifier is ready to check a challenge once the required DNS records exist.

---

## Usage

### Common Workflows

Generate a fresh challenge when a customer reserves a hostname.

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-proof-dns-domain/docs/readme/usage.py).

```python
from tba_provider_security_proof_dns_domain import DnsDomainOwnershipVerifier


def verify_claim(verifier: DnsDomainOwnershipVerifier, proof: str) -> bool:
    return verifier.verify(
        hostname="login.customer.example",
        record_name="_privpw.login.customer.example",
        proof=proof,
        cname_target="edge.provider.example",
    )
```
<!-- readme-standards:end example.usage -->

### Configuration

Provide the resolver URL, TXT owner, expected proof, and expected CNAME destination.

### Error Handling

A mismatch returns false. Catch `DomainProofUnavailable` for resolver errors or malformed responses.

### Best Practices

Persist each challenge with an expiration and replace it when a domain is reclaimed.

---

## Package Boundary

### What It Owns

DNS record matching and resolver error reporting.

### Public API and Import Surfaces

Import `DnsDomainOwnershipVerifier` and `DomainProofUnavailable` from `tba_provider_security_proof_dns_domain`.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

The caller supplies the resolver URL and can inject an HTTPX transport for tests.

### Protocol Consumers

Vanguard CIAM uses the verifier before enabling custom login domains.

### Extensions

The optional HTTPX transport supports deterministic tests.

---

## Operations and Readiness

### Operational Requirements

The caller needs HTTPS access to the configured recursive resolver.

### Health and Observability

Track verification outcomes and resolver errors at the application boundary.

### Security and Resource Limits

Configure the recursive resolver at deployment. Treat request inputs as the names and values to verify.

### Compatibility

The manifest declares supported Python and HTTPX versions.

---

## Verification

### Tests

The package tests cover exact matches, mismatches, and resolver failures.

### Certification Status

Package tests cover the DNS proof contract.

### Evidence

The package test directory contains deterministic resolver fixtures.

---

## FAQ

### Why

Matching a random TXT challenge proves control of the requested DNS record.

### How

The verifier requests TXT and CNAME answers through the configured recursive resolver.

### When

Verify the domain before enabling customer sign-in on it.

---

## Documentation and Related Packages

### More Documentation

See the package source and runnable usage example.

### Related Packages

`tba-provider-security-proof-pkce` handles PKCE in the same provider layer.

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/020-providers/tba-provider-security-proof-dns-domain#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/020-providers/tba-provider-security-proof-dns-domain#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-provider-security-proof-dns-domain/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [SSOT](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/020-providers/tba-provider-security-proof-dns-domain)
- [pypi: tba-provider-security-proof-dns-domain](https://pypi.org/project/tba-provider-security-proof-dns-domain/)
<!-- readme-standards:end project-links -->

---

## Contributing

### How to Contribute

Update examples and tests with changes to the public verifier.

### Development Setup

Install in editable mode and run pytest against the package tests.

### Notes for Maintainers

Regenerate the managed README sections after changing package metadata.

---

## Governance

### Ownership and Decision Making

Tigrbl Auth owns the DNS proof interface and test fixtures.

### Standards and Policies

The repository’s provider layer and README policies apply.

### Lifecycle and Migration

Pin the selected package release in downstream lockfiles.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-proof-dns-domain/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-proof-dns-domain/NOTICE) for attribution.
<!-- readme-standards:end notices -->
