# tba-capability-mcp-authorization

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-capability-mcp-authorization</strong></p>
<p align="center">MCP grant resolution, current scope authorization, and owned connection revocation.</p>
<p align="center">
<a href="https://pypi.org/project/tba-capability-mcp-authorization/"><img alt="pypi: tba-capability-mcp-authorization unpublished" src="https://img.shields.io/static/v1?label=pypi&amp;message=tba-capability-mcp-authorization%20unpublished&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-mcp-authorization/pyproject.toml"><img alt="Source version: 0.4.0.dev1" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev1&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-mcp-authorization/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-mcp-authorization/pyproject.toml"><img alt="Layer: 040-capabilities" src="https://img.shields.io/static/v1?label=Layer&amp;message=040-capabilities&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-mcp-authorization/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-mcp-authorization/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-mcp-authorization/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;color=525252"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-capability-mcp-authorization/"><img alt="pypi downloads: tba-capability-mcp-authorization: unpublished" src="https://img.shields.io/static/v1?label=pypi%20downloads&amp;message=tba-capability-mcp-authorization%3A%20unpublished&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-mcp-authorization/README.md"><img alt="README hits: tba-capability-mcp-authorization" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/040-capabilities/tba-capability-mcp-authorization/README.md.svg?label=README%20hits"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-mcp-authorization/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-mcp-authorization/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;color=525252"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

Resolve current owner and bot permissions for an approved MCP connection.

### Why This Package

A stored grant records consent. Each request still needs to check the account, acting identity, and resource at the time of use.

### When to Use

Use it between OAuth validation and the product's MCP resource policy.

### Features

- Check browser consent against requested and currently held scopes.
- Resolve a live principal from a grant bound to the client, resource, and tenant.
- Require a tool's scopes and the application's own resource check.
- Delegate owned connection revocation to the authoritative store.

### Non-Goals

OAuth transport, token validation and issuance, transaction management, and application resource policy are provided by the host.

---

## Getting Started

### Prerequisites

Python 3.10 or later, an authenticated OAuth integration, and an application grant and identity store.

### Installation

The package is pre-release. Build from the repository with its pinned dependency sources.

#### uv

<!-- readme-standards:begin installation.uv -->
`tba-capability-mcp-authorization` is not declared published. From the source checkout:

```bash
uv pip install .
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
`tba-capability-mcp-authorization` is not declared published. From the source checkout:

```bash
python -m pip install .
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
`tba-capability-mcp-authorization` is not declared published. From a separate Poetry project, replace the path with your checkout:

```bash
poetry add /path/to/tba-capability-mcp-authorization
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-mcp-authorization/docs/readme/quick_start.py).

```python
from tba_capability_mcp_authorization import MCPGrantBinding

binding = MCPGrantBinding(
    grant_id="g-123",
    tenant_id="example-tenant",
    client_id="example-client",
    resource="https://example.com/mcp",
)
assert binding.tenant_id == "example-tenant"
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The binding identifies one grant, client, tenant and MCP resource.

---

## Usage

### Common Workflows

Call `approve` after validating the browser principal and OAuth request. Persist consent and issue authorization codes through the product's transactional callback. Call `resolve` for live scope checks after OAuth validation, and `authorize_tool` to include the product's resource check.

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-mcp-authorization/docs/readme/usage.py).

```python
from collections.abc import Callable

from tba_capability_mcp_authorization import (
    MCPAuthorizationCapability,
    MCPGrantBinding,
    MCPResourceCheck,
    MCPPrincipal,
)


async def authorize_read(
    capability: MCPAuthorizationCapability,
    verified_binding: MCPGrantBinding,
    verified_token_scopes: frozenset[str],
    can_read_resource: MCPResourceCheck,
) -> MCPPrincipal | None:
    return await capability.authorize_tool(
        verified_binding,
        verified_token_scopes,
        required_scopes={"journal:read"},
        check_resource=can_read_resource,
    )


assert isinstance(authorize_read, Callable)
```
<!-- readme-standards:end example.usage -->

### Configuration

Inject a scoped grant store, a current subject lookup, and an optional clock. Use an absolute Unix timestamp for grant expiry.

### Error Handling

Invalid consent raises `PermissionError` or `ValueError`. An unavailable grant or failed tool check returns no principal. Infrastructure failures from injected operations propagate to the host.

### Best Practices

Build the binding from verified OAuth metadata and the expected resource. Use live subject snapshots for each check. Require scoped, atomic revocation and authorization-code redemption at the storage boundary.

---

## Package Boundary

### What It Owns

Grant and subject binding comparison, current scope intersection, tool-scope enforcement, and orchestration of an owned revoke operation.

### Public API and Import Surfaces

`tba_capability_mcp_authorization` exports `MCPAuthorizationCapability`, `MCPGrantBinding`, `MCPGrant`, `MCPSubject`, `MCPPrincipal`, and adapter types.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

`MCPGrantStore` loads a bound grant and revokes it with owner and binding checks inside the write. The subject lookup returns the currently active account or the owner's bot.

### Protocol Consumers

Use with a server-side MCP OAuth integration. Refresh adapters can use live scope resolution before calling the token rotation operation.

### Extensions

Use `tba-concrete-mcp-delegation` for the browser consent permission matrix. Product adapters supply tool-specific resource checks and response projection.

---

## Operations and Readiness

### Operational Requirements

OAuth and storage adapters enforce token validity, transactional issuance, current grant state and any product-specific mutation invariants.

### Health and Observability

The host owns adapter health, token lifecycles, audit events, and transport error responses.

### Security and Resource Limits

Only trusted callers construct the grant binding. Keep the mutation and its resource check consistent with the host transaction. Validate OAuth before delegating to this package.

### Compatibility

Scope and identifier strings are opaque to this package. Resource bindings are matched exactly. Adapters retain the product's existing credential and HTTP formats.

---

## Verification

### Tests

The package tests exercise journal and forum scope fixtures, live status changes, grant expiry and scoped revocation. The README examples are runnable.

### Certification Status

Consumer integration and certification are pending.

### Evidence

Unit tests verify the capability's decision boundary. Application tests cover routing, token storage and grant transaction guarantees.

---

## FAQ

### Why

Applications share the owner/bot scope intersection and enforce their own article, forum, or other resource rules.

### How

Pass the verified OAuth grant binding and scopes into the capability and supply the product's resource check before invoking a tool.

### When

Resolve current authorization at refresh, discovery, and tool invocation.

---

## Documentation and Related Packages

### More Documentation

The example files demonstrate grant binding and a tool authorization adapter.

### Related Packages

`tba-concrete-mcp-delegation`, `tba-durability-delegation`, and `tba-capability-token-issuance`.

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/040-capabilities/tba-capability-mcp-authorization#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/040-capabilities/tba-capability-mcp-authorization#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-capability-mcp-authorization/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/040-capabilities/tba-capability-mcp-authorization)
- [pypi: tba-capability-mcp-authorization](https://pypi.org/project/tba-capability-mcp-authorization/)
<!-- readme-standards:end project-links -->

---

## Contributing

### How to Contribute

Add fixtures for shared authorization semantics and verify the relevant application adapters.

### Development Setup

Use the repository's uv environment and package test suite.

### Notes for Maintainers

Keep the package free of product-specific roles and resource identifiers.

---

## Governance

### Ownership and Decision Making

Tigrbl Auth owns the shared decision boundary. Consumer maintainers own storage adapters and resource policy.

### Standards and Policies

Use the existing OAuth and delegation contracts when composing an integration.

### Lifecycle and Migration

Adopt behind the current application routes and storage contracts first.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-mcp-authorization/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-mcp-authorization/NOTICE) for attribution.
<!-- readme-standards:end notices -->
