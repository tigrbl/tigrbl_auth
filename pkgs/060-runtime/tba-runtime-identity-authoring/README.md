# tba-runtime-identity-authoring

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-runtime-identity-authoring</strong></p>
<p align="center">Release artifact authoring, signing, attestation, and verification helpers for the TBA identity suite.</p>
<p align="center">
<a href="https://pypi.org/project/tba-runtime-identity-authoring/"><img alt="pypi: tba-runtime-identity-authoring" src="https://img.shields.io/pypi/v/tba-runtime-identity-authoring"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-authoring/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-authoring/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-authoring/pyproject.toml"><img alt="Layer: 060-runtime" src="https://img.shields.io/static/v1?label=Layer&amp;message=060-runtime&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-authoring/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-authoring/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-authoring/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;color=525252"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-runtime-identity-authoring/"><img alt="Monthly PyPI downloads: tba-runtime-identity-authoring" src="https://img.shields.io/pypi/dm/tba-runtime-identity-authoring"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-authoring/README.md"><img alt="README hits: tba-runtime-identity-authoring" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/060-runtime/tba-runtime-identity-authoring/README.md.svg?label=README%20hits"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-authoring/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-authoring/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;color=525252"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

tba-runtime-identity-authoring owns release artifact authoring, signing, attestation, and verification helpers for the TBA identity package suite.

- Package: `tba-runtime-identity-authoring`
- Import root: `tba_runtime_identity_authoring`
- Component kind: Runtime support package
- Use it for release bundle signing, artifact attestations, and release provenance verification.
- It is not request-path runtime token behavior.

### Why This Package

`tba-runtime-identity-authoring` isolates this responsibility: Release artifact authoring, signing, attestation, and verification helpers for the TBA identity suite. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-authoring/src/tba_runtime_identity_authoring/__init__.py) exposes `DEFAULT_SIGNER_ID`, `LoadedSigner`, `SignerIdentity`, `VerificationResult`, `build_contract_set_manifest`, `load_signer`, `sha256_bytes`, `sha256_file`, `verify_bundle_attestations`, `verify_statement`, `write_artifact_attestation`, `write_attestation`, `write_bundle_attestation`, `write_public_key_artifacts`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-runtime-identity-authoring` for this responsibility: Release artifact authoring, signing, attestation, and verification helpers for the TBA identity suite. Its `060-runtime` placement keeps runtime composition and operator entry points separate from duplicating protocol grammars, table declarations, or provider implementations.

### Features

- `SignerIdentity`: declared in src/tba_runtime_identity_authoring/release_signing/models.py
- `LoadedSigner`: declared in src/tba_runtime_identity_authoring/release_signing/models.py
- `VerificationResult`: declared in src/tba_runtime_identity_authoring/release_signing/models.py

### Non-Goals

`tba-runtime-identity-authoring` does not take ownership of duplicating protocol grammars, table declarations, or provider implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-authoring/pyproject.toml) declares runtime dependencies including `cryptography`. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-runtime-identity-authoring`:

```bash
uv pip install tba-runtime-identity-authoring
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/060-runtime/tba-runtime-identity-authoring
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-runtime-identity-authoring
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-runtime-identity-authoring
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-runtime-identity-authoring
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.


```bash
uv run --isolated --no-project --python 3.12 --with "tba-runtime-identity-authoring==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the LoadedSigner entry point is available.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-authoring/docs/readme/quick_start.py).

```python
from tba_runtime_identity_authoring import LoadedSigner

assert callable(LoadedSigner)
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-runtime-identity-authoring` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-authoring/docs/readme/usage.py).

```python
from tba_runtime_identity_authoring.release_signing import sha256_bytes

digest = sha256_bytes(b"identity-release-evidence")
```
<!-- readme-standards:end example.usage -->

### Configuration

The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-authoring/src/tba_runtime_identity_authoring/__init__.py) references configuration keys `TBA_AUTH_RELEASE_SIGNER_ID`, `TBA_AUTH_RELEASE_SIGNING_KEY_FILE`, `TBA_AUTH_RELEASE_SIGNING_KEY_PEM`, `TBA_AUTH_RELEASE_SIGNING_SEED`. Consult the constructor or function signature before supplying them; a referenced key is not necessarily a global environment variable.

### Error Handling

The inspected `tba-runtime-identity-authoring` source raises `TypeError`. Handle these at the calling boundary and consult the implementation for the triggering conditions.

### Best Practices

Use the explicit `tba-runtime-identity-authoring` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `DEFAULT_SIGNER_ID`, `LoadedSigner`, `SignerIdentity`, `VerificationResult`, `build_contract_set_manifest`, `load_signer`, `sha256_bytes`, `sha256_file`, `verify_bundle_attestations`, `verify_statement`, `write_artifact_attestation`, `write_attestation`, `write_bundle_attestation`, `write_public_key_artifacts`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

- Release bundle artifact hashing
- Signed artifact attestations
- Signed release-bundle attestations
- Public signing-key artifact generation
- Release signing verification helpers

### Public API and Import Surfaces

Import namespace: `tba_runtime_identity_authoring`.

Source-declared exports or types: `DEFAULT_SIGNER_ID`, `LoadedSigner`, `SignerIdentity`, `VerificationResult`, `build_contract_set_manifest`, `load_signer`, `sha256_bytes`, `sha256_file`, `verify_bundle_attestations`, `verify_statement`, `write_artifact_attestation`, `write_attestation`, `write_bundle_attestation`, `write_public_key_artifacts`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-authoring/src/tba_runtime_identity_authoring/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

Explicit construction inputs and collaborators for `tba-runtime-identity-authoring`:

- `write_artifact_attestation` construction inputs: `signer`, `label`, `artifact_rel_path`, `package`, `version`, `profile`, `artifact_kind`, `media_type`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-authoring/src/tba_runtime_identity_authoring/release_signing/attestations.py).
- `write_bundle_attestation` construction inputs: `signer`, `package`, `version`, `profile`, `signed_artifacts`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-authoring/src/tba_runtime_identity_authoring/release_signing/attestations.py).
- `load_signer` construction inputs: `signing_key`, `signer_id`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-authoring/src/tba_runtime_identity_authoring/release_signing/keys.py).
- `verify_statement` construction inputs: `public_key_pem`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-authoring/src/tba_runtime_identity_authoring/release_signing/verification.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

### Protocol Consumers

Direct consumers in this checkout’s package manifests include `tba-cli-identity`, `tba-auth`, `tba-workspace`. These edges describe declared dependencies, not protocol-conformance evidence.

### Extensions

For `tba-runtime-identity-authoring`, use the source-declared public interfaces (`DEFAULT_SIGNER_ID`, `LoadedSigner`, `SignerIdentity`, `VerificationResult`, `build_contract_set_manifest`, `load_signer`, `sha256_bytes`, `sha256_file`, `verify_bundle_attestations`, `verify_statement`, `write_artifact_attestation`, `write_attestation`, `write_bundle_attestation`, `write_public_key_artifacts`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-runtime-identity-authoring` exposes runtime composition and operator entry points. Public operations found in its source:

- `build_contract_set_manifest` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-authoring/src/tba_runtime_identity_authoring/release_signing/attestations.py).
- `write_attestation` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-authoring/src/tba_runtime_identity_authoring/release_signing/attestations.py).
- `write_artifact_attestation` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-authoring/src/tba_runtime_identity_authoring/release_signing/attestations.py).
- `write_bundle_attestation` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-authoring/src/tba_runtime_identity_authoring/release_signing/attestations.py).
- `load_signer` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-authoring/src/tba_runtime_identity_authoring/release_signing/keys.py).
- `write_public_key_artifacts` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-authoring/src/tba_runtime_identity_authoring/release_signing/keys.py).
- `SignerIdentity.to_manifest` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-authoring/src/tba_runtime_identity_authoring/release_signing/models.py).
- `LoadedSigner.private_key_pem` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-authoring/src/tba_runtime_identity_authoring/release_signing/models.py).
- `LoadedSigner.sign_payload` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-authoring/src/tba_runtime_identity_authoring/release_signing/models.py).
- `LoadedSigner.sign_statement` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-authoring/src/tba_runtime_identity_authoring/release_signing/models.py).
- `VerificationResult.to_manifest` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-authoring/src/tba_runtime_identity_authoring/release_signing/models.py).
- `sha256_bytes` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-authoring/src/tba_runtime_identity_authoring/release_signing/utils.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-runtime-identity-authoring`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-authoring/src/tba_runtime_identity_authoring/__init__.py). The `tba-runtime-identity-authoring` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-runtime-identity-authoring` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-authoring/src/tba_runtime_identity_authoring/__init__.py).

### Certification Status

No external certification is asserted for `tba-runtime-identity-authoring` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-authoring/src/tba_runtime_identity_authoring/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-runtime-identity-authoring` provides release artifact authoring, signing, attestation, and verification helpers for the TBA identity suite; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-runtime-identity-authoring`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-authoring/src/tba_runtime_identity_authoring/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-runtime-identity-authoring` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-authoring/src/tba_runtime_identity_authoring/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-authoring/pyproject.toml) provide the supporting context for `tba-runtime-identity-authoring`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

Direct downstream consumers:

- [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/README.md)
- [tba-cli-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-cli-identity/README.md)

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/060-runtime/tba-runtime-identity-authoring#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/060-runtime/tba-runtime-identity-authoring#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-runtime-identity-authoring/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [SSOT](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/060-runtime/tba-runtime-identity-authoring)
- [pypi: tba-runtime-identity-authoring](https://pypi.org/project/tba-runtime-identity-authoring/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/060-runtime/tba-runtime-identity-authoring)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-authoring/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-authoring/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-authoring/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-runtime-identity-authoring/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-runtime-identity-authoring`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/060-runtime/tba-runtime-identity-authoring` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.1` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-runtime-identity-authoring` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-runtime-identity-authoring` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-authoring/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

`tba-runtime-identity-authoring` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `060-runtime` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-runtime-identity-authoring` source version is `0.4.0.dev3`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-authoring/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity-authoring/NOTICE) for attribution.
<!-- readme-standards:end notices -->
