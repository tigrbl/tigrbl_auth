# tba-provider-dns-resolver

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-provider-dns-resolver</strong></p>
<p align="center">In-house DNS resolver and encrypted network transports.</p>
<p align="center">
<a href="https://pypi.org/project/tba-provider-dns-resolver/"><img alt="pypi: tba-provider-dns-resolver unpublished" src="https://img.shields.io/static/v1?label=pypi&amp;message=tba-provider-dns-resolver%20unpublished&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-dns-resolver/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-dns-resolver/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-dns-resolver/pyproject.toml"><img alt="Layer: 020-providers" src="https://img.shields.io/static/v1?label=Layer&amp;message=020-providers&amp;labelColor=1E293B&amp;color=6D28D9"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-dns-resolver/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;labelColor=1E293B&amp;color=166534"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-dns-resolver/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;labelColor=1E293B&amp;color=86198F"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-dns-resolver/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;labelColor=1E293B&amp;color=86198F"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-provider-dns-resolver/"><img alt="pypi downloads: tba-provider-dns-resolver: unpublished" src="https://img.shields.io/static/v1?label=pypi%20downloads&amp;message=tba-provider-dns-resolver%3A%20unpublished&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-dns-resolver/README.md"><img alt="README hits: tba-provider-dns-resolver" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/020-providers/tba-provider-dns-resolver/README.md.svg?label=README%20hits&amp;labelColor=1E293B&amp;color=0E7490"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-dns-resolver/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-dns-resolver/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;labelColor=1E293B&amp;color=6D28D9"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

This package covers native DNS resolution and encrypted client transports.

In-house synchronous and asynchronous DNS resolution, UDP and TCP query
transports, DoT, DoH, and DoQ.

```python
from tba_provider_dns_resolver import Resolver

answer = Resolver().resolve_answer("example.com.", "MX")
for record in answer.records:
    print(record.type, record.ttl)
```

The optional extras provide DoH over HTTP/2 (`http2`), DoQ and HTTP/3
(`quic`), and Trio support (`trio`).
The low-level HTTPS API runs HTTP/2 on asyncio and Trio and HTTP/3 on asyncio.
Discovered encrypted resolvers check the bootstrap address in the certificate
on the connection carrying the query. TCP and TLS queries can reuse connected
caller-owned sockets, and UDP also accepts a caller-owned datagram socket.
Use `transport.quic_session()` to send multiple DoQ queries on a single
verified connection. DoQ and HTTP/3 accept caller-supplied QUIC address tokens.

`AsyncResolver` autodetects asyncio or Trio. Its lookup methods also accept a
`backend=` implementing `asyncbackend.Backend`. For HTTP/1.1 and HTTP/2, pass
a configured `httpx.Client` or `httpx.AsyncClient` as `session=` to reuse the
caller's connection pool. The caller owns the session's lifetime and trust
settings.

Use `asyncquery.https(source=..., source_port=...)` to bind a new HTTP/1.1
or HTTP/2 connection to a local address and port. A borrowed client retains
its own connection configuration.

For native HTTP/3, pass a client `SSLContext` as `verify=`. The QUIC
transport uses its exportable CA certificates, hostname setting, compatible
TLS 1.3 cipher suites, and certificate verification flags. For revocation
checks, attach the CRL material explicitly because Python exposes CA
certificates from an `SSLContext` but does not expose loaded CRLs.

```python
import ssl

from tba_provider_dns_resolver import asyncquery

trust = ssl.create_default_context(cafile="ca.pem")
trust.verify_flags |= ssl.VERIFY_CRL_CHECK_CHAIN
asyncquery.configure_http3_crls(trust, "issuer-crls.pem")
answer = await asyncquery.https(query, endpoint, verify=trust, http_version=3)
```

For mutual TLS across HTTP versions, use `asyncquery.HTTP3SSLContext`.
Its `load_cert_chain()` method configures the same identity for TCP TLS
and native HTTP/3. Supply PEM files in leaf-first order. An encrypted
private key accepts a password or a password callback.

```python
trust = asyncquery.HTTP3SSLContext()
trust.load_verify_locations(cafile="ca.pem")
trust.load_cert_chain("client-chain.pem", "client-key.pem")
answer = await asyncquery.https(query, endpoint, verify=trust, http_version=3)
```

For an existing standard `ssl.SSLContext`, use
`asyncquery.configure_http3_client_identity()` with the original PEM files.
Python does not expose a private key previously loaded into a standard context.
The QUIC client verifies the server before sending its client certificate.

Use [tba-concrete-dns-zone](../../10-concrete/tba-concrete-dns-zone) for local
zones and [tba-protocol-dns](../../50-protocols/tba-protocol-dns) for discovery,
transfers, updates, and authentication. The [DNS tests](../../120-tests/tba-tests-dns)
cover the resolver and transports.

### Why This Package

It gives synchronous and asynchronous dns clients a separate boundary with independently verifiable behavior.

### When to Use

Use this package when a caller needs native DNS resolution and encrypted client transports.

### Features

Use the package for native DNS resolution and encrypted client transports. The authored notes above cover the supported behavior and examples.

### Non-Goals

The package provides outbound stub resolution and does not expose an authoritative listener.

---

## Getting Started

### Prerequisites

Use Python 3.10–3.15 in the repository workspace. The examples use local inputs.

### Installation

#### uv

<!-- readme-standards:begin installation.uv -->
`tba-provider-dns-resolver` is not declared published. From the source checkout:

```bash
uv pip install .
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
`tba-provider-dns-resolver` is not declared published. From the source checkout:

```bash
python -m pip install .
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
`tba-provider-dns-resolver` is not declared published. From a separate Poetry project, replace the path with your checkout:

```bash
poetry add /path/to/tba-provider-dns-resolver
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-dns-resolver/docs/readme/quick_start.py).

```python
from tba_provider_dns_resolver import Resolver

resolver = Resolver(configure=False)
assert not resolver.nameservers
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The local example checks the declared interface without making a live DNS request.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-dns-resolver/docs/readme/usage.py).

```python
from tba_provider_dns_resolver import AsyncResolver

resolver = AsyncResolver(configure=False)
resolver.nameservers = ['192.0.2.53']
assert resolver.nameservers == ('192.0.2.53',)
```
<!-- readme-standards:end example.usage -->

### Configuration

Supply resolver endpoints and timeouts explicitly when the deployment cannot rely on OS resolver settings.

### Error Handling

Treat validation errors as failed operations. Inspect the original exception before choosing whether to retry.

### Best Practices

Keep the example inputs local when validating a new installation. Run the applicable integration tests separately.

---

## Package Boundary

### What It Owns

The owning boundary is native DNS resolution and encrypted client transports.

### Public API and Import Surfaces

Start with the public interfaces imported in the maintained examples. They demonstrate native DNS resolution and encrypted client transports.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

The calling code owns the external inputs. Supply resolver endpoints and timeouts explicitly when the deployment cannot rely on OS resolver settings.

### Protocol Consumers

The TXT provider and DNS protocol packages delegate DNS exchanges to this resolver.

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

Use this package when the application needs native DNS resolution and encrypted client transports.

### How

Start with the local example and compare its result with the expected result before wiring it into a caller.

### When

Choose this boundary when the application needs native DNS resolution and encrypted client transports.

---

## Documentation and Related Packages

### More Documentation

See the package notes in the Summary and the repository package standards.

### Related Packages

See [tba-codec-dns](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs) for the adjacent DNS boundary.

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/020-providers/tba-provider-dns-resolver#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/020-providers/tba-provider-dns-resolver#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-provider-dns-resolver/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/020-providers/tba-provider-dns-resolver)
- [pypi: tba-provider-dns-resolver](https://pypi.org/project/tba-provider-dns-resolver/)
<!-- readme-standards:end project-links -->

---

## Contributing

### How to Contribute

Keep proposed changes scoped to this package and include evidence for behavior changes.

### Development Setup

From the repository root, use the locked Python workspace and run the relevant DNS test selection.

### Notes for Maintainers

Keep the exported behavior for native DNS resolution and encrypted client transports covered by ordinary DNS inputs in CI.

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
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-dns-resolver/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-dns-resolver/NOTICE) for attribution.
<!-- readme-standards:end notices -->
