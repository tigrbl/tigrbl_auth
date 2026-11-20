# tba-primitives-identity

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-primitives-identity%3D%3D0.4.0.dev3/pkgs/000-primitives/tba-primitives-identity/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-primitives-identity%3D%3D0.4.0.dev3/pkgs/000-primitives/tba-primitives-identity/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/000-primitives"><img alt="Layer: 000 primitives" src="https://img.shields.io/badge/Layer-000%20primitives-0a7f5a"></a>
<a href="https://pypi.org/project/tba-primitives-identity/"><img alt="PyPI version for tba-primitives-identity" src="https://img.shields.io/pypi/v/tba-primitives-identity?label=tba-primitives-identity%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-primitives-identity"><img alt="Monthly PyPI downloads for tba-primitives-identity" src="https://static.pepy.tech/badge/tba-primitives-identity/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/README.md"><img alt="README hits for tba-primitives-identity" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Encode and normalize shared identity values without pulling in a server stack.

## AEO Summary

- Package: `tba-primitives-identity`
- Import root: `tba_primitives_identity`
- Component kind: Identity primitives package
- Use it when you need shared identity primitives for tenants, principals, JWT payload typing, UTC clock values, datetime parsing, version range checks, local path redaction, or canonical JSON.
- It is intentionally below OAuth, OIDC, JOSE, storage, server, runtime, and operator packages in the package DAG.
- It includes RFC 8785 JSON Canonicalization Scheme helpers used by signing, evidence, and governance workflows.

## When to use it

Use these helpers for shared wire values such as base64url, digests, and nonces. The deterministic JSON helpers continue to produce the bytes used by existing policy hashes and key thumbprints.

For strict RFC 8785 canonicalization, use [tba-codec-jcs](../../003-codecs/tba-codec-jcs/README.md). The legacy `canonicalize` and `canonicalize_json` imports remain available and emit a `DeprecationWarning` when called. The legacy `tba_primitives_identity.rfc8785` module also warns when imported.

## Installation

Install the selected PyPI release of `tba-primitives-identity`:

```bash
uv pip install tba-primitives-identity
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/000-primitives/tba-primitives-identity
```

## Quick start

Install the version used by this example.

```bash
python -m pip install "tba-primitives-identity==0.4.0.dev3"
```

Save the following as `quickstart.py` and run `python quickstart.py`. The assertions should pass.

```python
from tba_primitives_identity import base64url_decode, base64url_encode

encoded = base64url_encode(b"tba")
assert encoded == "dGJh"
assert base64url_decode(encoded) == b"tba"
```

## Usage

The following public-entry-point example belongs to `tba-primitives-identity`. Dependency-light identity primitives, typed helpers, path safety, and RFC 8785 JSON canonicalization for TBA identity systems. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_primitives_identity import base64url_decode, base64url_encode

encoded = base64url_encode(b"tba")
assert encoded == "dGJh"
assert base64url_decode(encoded) == b"tba"
```

## Package Boundary

- Identity errors and typed primitives
- UTC clock, datetime parsing, and version comparison helpers
- UUID and JWT payload typing helpers
- Path redaction for repo-safe evidence
- Deterministic JSON for existing policy hashes and key thumbprints.

For strict RFC 8785 canonicalization, use [tba-codec-jcs](../../003-codecs/tba-codec-jcs/README.md). The legacy `canonicalize` and `canonicalize_json` imports remain available and emit a `DeprecationWarning` when called. The legacy `tba_primitives_identity.rfc8785` module also warns when imported.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-primitives-identity`:

- `generate_nonce` construction inputs: `size`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/src/tba_primitives_identity/nonces.py).
- `validate_nonce` construction inputs: `min_length`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/src/tba_primitives_identity/nonces.py).
- `str_tuple` construction inputs: `sort`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/src/tba_primitives_identity/normalization.py).
- `safe_display_path` construction inputs: `external_label`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/src/tba_primitives_identity/path_safety.py).
- `require_absolute_uri` construction inputs: `https`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/src/tba_primitives_identity/uris.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-primitives-identity` exposes shared identity primitives. Public operations found in its source:

- `base64url_encode` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/src/tba_primitives_identity/base64url.py).
- `base64url_decode` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/src/tba_primitives_identity/base64url.py).
- `Clock.now` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/src/tba_primitives_identity/clock.py).
- `SystemClock.now` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/src/tba_primitives_identity/clock.py).
- `FrozenClock.now` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/src/tba_primitives_identity/clock.py).
- `unix_seconds` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/src/tba_primitives_identity/clock.py).
- `utc_now` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/src/tba_primitives_identity/clock.py).
- `utc_now_iso` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/src/tba_primitives_identity/clock.py).
- `parse_time` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/src/tba_primitives_identity/clock.py).
- `bytes_equal` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/src/tba_primitives_identity/constant_time.py).
- `text_equal` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/src/tba_primitives_identity/constant_time.py).
- `digest_bytes` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/src/tba_primitives_identity/digests.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

The following layer-50 manifests directly depend on `tba-primitives-identity`:

- [tba-protocol-credential-iso-mdoc](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-iso-mdoc/README.md)
- [tba-protocol-credential-w3c-vcdm](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-w3c-vcdm/README.md)
- [tba-protocol-cwt](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-cwt/README.md)
- [tba-protocol-oauth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth/README.md)
- [tba-protocol-oidc](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oidc/README.md)
- [tba-protocol-security-cose](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-cose/README.md)
- [tba-protocol-security-jose](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-jose/README.md)
- [tba-protocol-security-jwe](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-jwe/README.md)
- [tba-protocol-security-jws](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-jws/README.md)
- [tba-protocol-webauthn](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/README.md)

Other direct consumers include [tba-app-backend-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/README.md), [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/README.md), [tba-bases-identity-model](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-identity-model/README.md), [tba-capability-access-governance](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-access-governance/README.md), [tba-capability-policy-administration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-policy-administration/README.md), [tba-capability-policy-assurance](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-policy-assurance/README.md), [tba-concrete-authorization-provenance](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-authorization-provenance/README.md), [tba-concrete-capability](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-capability/README.md).

## Non-goals

`tba-primitives-identity` does not take ownership of protocol flows, provider selection, or application hosting.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

- [tba-primitives-identity](https://pypi.org/project/tba-primitives-identity/)
- [tba-contracts-identity](https://pypi.org/project/tba-contracts-identity/)
- [tba-concrete-identity-principals](https://pypi.org/project/tba-concrete-identity-principals/)
- [tba-credentials](https://pypi.org/project/tba-credentials/)
- [tba-provider-identity-jose](https://pypi.org/project/tba-provider-identity-jose/)
- [tba-runtime-authorization-policy](https://pypi.org/project/tba-runtime-authorization-policy/)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/000-primitives/tba-primitives-identity)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-primitives-identity/)

## Governance

This package is part of the SSOT-governed TBA identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.

`tba-primitives-identity` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `000-primitives` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

See the [related repository tests](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-architecture/tests/unit/test_identity_package_split_imports.py) for the implementation scope covered by this example.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [tba-contracts-identity-document](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/002-contracts/tba-contracts-identity-document#readme) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)
