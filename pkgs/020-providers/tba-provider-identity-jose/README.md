# tba-provider-identity-jose

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-provider-identity-jose</strong></p>
<p align="center">JOSE, JWT, JWS, JWE, JWK, JWKS, key rotation, and standards helpers for TBA identity tokens.</p>
<p align="center">
<a href="https://pypi.org/project/tba-provider-identity-jose/"><img alt="pypi: tba-provider-identity-jose" src="https://img.shields.io/pypi/v/tba-provider-identity-jose?labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/pyproject.toml"><img alt="Layer: 020-providers" src="https://img.shields.io/static/v1?label=Layer&amp;message=020-providers&amp;labelColor=1E293B&amp;color=6D28D9"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;labelColor=1E293B&amp;color=166534"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;labelColor=1E293B&amp;color=86198F"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;labelColor=1E293B&amp;color=86198F"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-provider-identity-jose/"><img alt="Monthly PyPI downloads: tba-provider-identity-jose" src="https://img.shields.io/pypi/dm/tba-provider-identity-jose?labelColor=1E293B&amp;color=0E7490"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/README.md"><img alt="README hits: tba-provider-identity-jose" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/020-providers/tba-provider-identity-jose/README.md.svg?label=README%20hits&amp;labelColor=1E293B&amp;color=0E7490"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;labelColor=1E293B&amp;color=1D4ED8"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;labelColor=1E293B&amp;color=0F766E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;labelColor=1E293B&amp;color=92400E"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;labelColor=1E293B&amp;color=4338CA"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;labelColor=1E293B&amp;color=6D28D9"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

tba-provider-identity-jose owns token cryptography and JOSE-related standards support for the TBA identity suite. It is the package for JWT coding, JWKS publication helpers, key rotation policy, and RFC-oriented JOSE modules.

- Package: `tba-provider-identity-jose`
- Import root: `tba_provider_identity_jose`
- Component kind: Provider package
- Use it when you need JOSE, JWT, JWK, JWS, JWE, JWKS, or key rotation behavior.
- It separates signing and verification material from OAuth and OIDC protocol decisions.
- It includes RFC-oriented modules for JOSE standards tracked by the identity suite.

### Why This Package

`tba-provider-identity-jose` isolates this responsibility: JOSE, JWT, JWS, JWE, JWK, JWKS, key rotation, and standards helpers for TBA identity tokens. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/src/tba_provider_identity_jose/__init__.py) exposes `DefaultJoseProviderSettings`, `EffectiveKeyRotationPolicy`, `JWEPolicy`, `JWK_PRIVATE_PARAMETERS`, `JWTCoder`, `JoseKey`, `JoseKeyRotationResult`, `JoseKeySet`, `JoseKeyStatus`, `JoseKeyUse`, `KeyRotationAdministration`, `KeyRotationPolicyGovernance`, `KeyRotationPolicyOverlapError`, `KeyRotationPolicyVersion`, `ML_DSA_65_ALG`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-provider-identity-jose` for this responsibility: JOSE, JWT, JWS, JWE, JWK, JWKS, key rotation, and standards helpers for TBA identity tokens. Its `020-providers` placement keeps replaceable environment implementations separate from capability orchestration, storage table ownership, or HTTP routing.

### Features

- `DefaultJoseProviderSettings`: declared in src/tba_provider_identity_jose/configuration.py
- `JWAAlg`: declared in src/tba_provider_identity_jose/framework.py
- `KeyAlg`: declared in src/tba_provider_identity_jose/framework.py
- `KeyClass`: declared in src/tba_provider_identity_jose/framework.py
- `KeyUse`: declared in src/tba_provider_identity_jose/framework.py
- `ExportPolicy`: declared in src/tba_provider_identity_jose/framework.py
- `KeySpec`: declared in src/tba_provider_identity_jose/framework.py
- `KeyReference`: declared in src/tba_provider_identity_jose/framework.py

### Non-Goals

`tba-provider-identity-jose` does not take ownership of capability orchestration, storage table ownership, or HTTP routing.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/pyproject.toml) declares runtime dependencies including `tba-concrete-jose`, `cryptography`, `tba-bases-jose`, `tba-contracts-security-key-rotation-policy`, `tba-provider-secret-hashing-bcrypt`, `tba-contracts-identity`, `tba-primitives-identity`, `tba-provider-security-signing-pqc`. Read the example’s inputs and service requirements before execution.

### Installation

```bash
pip install tba-provider-identity-jose
# or
uv add tba-provider-identity-jose
```

Install the current `tba-provider-identity-jose` source checkout when working ahead of a PyPI release:

```bash
uv pip install ./pkgs/020-providers/tba-provider-identity-jose
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-provider-identity-jose
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-provider-identity-jose
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-provider-identity-jose
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.


```bash
uv run --isolated --no-project --python 3.12 --with "tba-provider-identity-jose==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the DefaultJoseProviderSettings entry point is available.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/docs/readme/quick_start.py).

```python
from tba_provider_identity_jose import DefaultJoseProviderSettings

assert callable(DefaultJoseProviderSettings)
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-provider-identity-jose` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/docs/readme/usage.py).

```python
from tba_provider_identity_jose.key_rotation_policy import KeyRotationPolicyGovernance
```
<!-- readme-standards:end example.usage -->

### Configuration

The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/src/tba_provider_identity_jose/__init__.py) references configuration keys `JWT_ED25519_KEY_DIR`, `JWT_ML_DSA_65_KEY_PATH`, `JWT_RS256_KEY_PATH`, `TBA_JOSE_LOCAL_KEY_DIR`. Consult the constructor or function signature before supplying them; a referenced key is not necessarily a global environment variable.

### Error Handling

The inspected `tba-provider-identity-jose` source raises `InvalidTokenError`, `JWEPolicyError`, `RuntimeError`, `TypeError`, `ValueError`. Handle these at the calling boundary and consult the implementation for the triggering conditions.

### Best Practices

Use the explicit `tba-provider-identity-jose` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `DefaultJoseProviderSettings`, `EffectiveKeyRotationPolicy`, `JWEPolicy`, `JWK_PRIVATE_PARAMETERS`, `JWTCoder`, `JoseKey`, `JoseKeyRotationResult`, `JoseKeySet`, `JoseKeyStatus`, `JoseKeyUse`, `KeyRotationAdministration`, `KeyRotationPolicyGovernance`, `KeyRotationPolicyOverlapError`, `KeyRotationPolicyVersion`, `ML_DSA_65_ALG`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

- JWT and JOSE helpers
- JWK and JWKS services
- Key management and rotation policy
- RFC-oriented JOSE modules

### Public API and Import Surfaces

Import namespace: `tba_provider_identity_jose`.

Source-declared exports or types: `DefaultJoseProviderSettings`, `EffectiveKeyRotationPolicy`, `JWEPolicy`, `JWK_PRIVATE_PARAMETERS`, `JWTCoder`, `JoseKey`, `JoseKeyRotationResult`, `JoseKeySet`, `JoseKeyStatus`, `JoseKeyUse`, `KeyRotationAdministration`, `KeyRotationPolicyGovernance`, `KeyRotationPolicyOverlapError`, `KeyRotationPolicyVersion`, `ML_DSA_65_ALG`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/src/tba_provider_identity_jose/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

Explicit construction inputs and collaborators for `tba-provider-identity-jose`:

- `JWTCoder` construction inputs: `arg1`, `arg2`, `revocation_checker`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/src/tba_provider_identity_jose/jwt_coder.py).
- `jwk_thumbprint` construction inputs: `enabled`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/src/tba_provider_identity_jose/standards/rfc7638.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

### Protocol Consumers

The following layer-50 manifests directly depend on `tba-provider-identity-jose`:

- [tba-protocol-oauth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/README.md)
- [tba-protocol-oidc](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/README.md)

Other direct consumers include [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/README.md), [tba-credentials](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/README.md), [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/README.md), [tba-server-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/README.md).

### Extensions

For `tba-provider-identity-jose`, use the source-declared public interfaces (`DefaultJoseProviderSettings`, `EffectiveKeyRotationPolicy`, `JWEPolicy`, `JWK_PRIVATE_PARAMETERS`, `JWTCoder`, `JoseKey`, `JoseKeyRotationResult`, `JoseKeySet`, `JoseKeyStatus`, `JoseKeyUse`, `KeyRotationAdministration`, `KeyRotationPolicyGovernance`, `KeyRotationPolicyOverlapError`, `KeyRotationPolicyVersion`, `ML_DSA_65_ALG`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-provider-identity-jose` exposes replaceable environment implementations. Public operations found in its source:

- `configure_jose_provider` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/src/tba_provider_identity_jose/configuration.py).
- `jose_provider_source` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/src/tba_provider_identity_jose/configuration.py).
- `JWTCoder.default` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/src/tba_provider_identity_jose/jwt_coder.py).
- `JWTCoder.async_default` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/src/tba_provider_identity_jose/jwt_coder.py).
- `JWTCoder.async_sign` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/src/tba_provider_identity_jose/jwt_coder.py).
- `JWTCoder.sign` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/src/tba_provider_identity_jose/jwt_coder.py).
- `JWTCoder.async_sign_pair` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/src/tba_provider_identity_jose/jwt_coder.py).
- `JWTCoder.sign_pair` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/src/tba_provider_identity_jose/jwt_coder.py).
- `JWTCoder.async_verify` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/src/tba_provider_identity_jose/jwt_coder.py).
- `JWTCoder.verify` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/src/tba_provider_identity_jose/jwt_coder.py).
- `JWTCoder.async_decode` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/src/tba_provider_identity_jose/jwt_coder.py).
- `JWTCoder.decode` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/src/tba_provider_identity_jose/jwt_coder.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-provider-identity-jose`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/src/tba_provider_identity_jose/__init__.py). The `tba-provider-identity-jose` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-provider-identity-jose` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/src/tba_provider_identity_jose/__init__.py).

### Certification Status

No external certification is asserted for `tba-provider-identity-jose` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/src/tba_provider_identity_jose/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-provider-identity-jose` provides jOSE, JWT, JWS, JWE, JWK, JWKS, key rotation, and standards helpers for TBA identity tokens; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-provider-identity-jose`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/src/tba_provider_identity_jose/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-provider-identity-jose` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/src/tba_provider_identity_jose/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/pyproject.toml) provide the supporting context for `tba-provider-identity-jose`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

- [tba-primitives-identity](https://pypi.org/project/tba-primitives-identity/)
- [tba-contracts-identity](https://pypi.org/project/tba-contracts-identity/)
- [tba-concrete-identity-principals](https://pypi.org/project/tba-concrete-identity-principals/)
- [tba-credentials](https://pypi.org/project/tba-credentials/)
- [tba-provider-identity-jose](https://pypi.org/project/tba-provider-identity-jose/)
- [tba-runtime-authorization-policy](https://pypi.org/project/tba-runtime-authorization-policy/)

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/020-providers/tba-provider-identity-jose#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/020-providers/tba-provider-identity-jose#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-provider-identity-jose/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [SSOT](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/020-providers/tba-provider-identity-jose)
- [pypi: tba-provider-identity-jose](https://pypi.org/project/tba-provider-identity-jose/)
<!-- readme-standards:end project-links -->

- [PyPI package](https://pypi.org/project/tba-provider-identity-jose/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/020-providers/tba-provider-identity-jose)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/020-providers/tba-provider-identity-jose)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-provider-identity-jose/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-provider-identity-jose`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/020-providers/tba-provider-identity-jose` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.3` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-provider-identity-jose` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-provider-identity-jose` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

This package is part of the SSOT-governed TBA identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.

`tba-provider-identity-jose` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `020-providers` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-provider-identity-jose` source version is `0.4.0.dev3`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/NOTICE) for attribution.
<!-- readme-standards:end notices -->
