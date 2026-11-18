# tba-protocol-zcap

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-zcap/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-zcap/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-protocol-zcap%3D%3D0.4.0.dev3/pkgs/50-protocols/tba-protocol-zcap/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-protocol-zcap%3D%3D0.4.0.dev3/pkgs/50-protocols/tba-protocol-zcap/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/50-protocols"><img alt="Layer: 50 protocols" src="https://img.shields.io/badge/Layer-50%20protocols-0a7f5a"></a>
<a href="https://pypi.org/project/tba-protocol-zcap/"><img alt="PyPI version for tba-protocol-zcap" src="https://img.shields.io/pypi/v/tba-protocol-zcap?label=tba-protocol-zcap%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-protocol-zcap"><img alt="Monthly PyPI downloads for tba-protocol-zcap" src="https://static.pepy.tech/badge/tba-protocol-zcap/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-zcap/README.md"><img alt="README hits for tba-protocol-zcap" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-zcap/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-zcap/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

ZCAP-LD v0.4.0 delegation and HTTP invocation signing and verification for
the TBA Ed25519 development profile.

Use `ZcapRoot` to configure a trusted local root and `sign_delegation`
to grant a controller restricted actions at a target. A signed delegation
embeds its immediate delegated parent and references older ancestors by ID.
Use `sign_http_invocation` to present a root by ID or a leaf delegation as
gzip-compressed, base64url-encoded JSON.

Configure `ZcapVerifier` with a trusted local root lookup, an Ed25519 key
lookup, a revocation check, and a TBA replay reservation provider. The key
lookup takes the controller, verification method ID, and required proof
purpose. Return a key only if the method is authorized for that controller
and purpose. The revocation check takes the root and delegated capability IDs.
Supply the operation's trusted root, method, target, and action to
`verify_invocation`, then dispatch using the verified request.

Delegation proofs use `eddsa-jcs-2022`. The verifier hashes the canonical
proof options and the canonical unsigned document separately, then checks
the Ed25519 signature over their concatenated hashes. The two fixed
JSON-LD contexts are checked locally. This suite uses JSON canonicalization
and needs no remote context fetching or RDF canonicalization.

The HTTP profile uses one RFC 9421 signature named `zcap`. It signs the
method, full target URI, Capability-Invocation field, SHA-256 Content-Digest,
and Content-Type when present. The application supplies the externally
effective URL and unmodified body. Preserve repeated headers so the verifier
can reject duplicates. Each signature includes a creation time, an expiry,
and a nonce. Use shared atomic replay storage for a multi-worker deployment.

The profile accepts one controller per capability, explicit action
restrictions on delegations, simple HTTPS paths without query strings, and
up to eight delegated capabilities. It uses this exact Capability-Invocation
field syntax for root and delegated invocations, respectively.

```text
zcap id="<root-id>",action="read"
zcap capability=<base64url-gzip-json>,action="read"
```

This is a bounded profile. It does not implement JSON invocation proofs,
arbitrary JSON-LD contexts or caveats, query attenuation, or a revocation
endpoint.

- [ZCAP-LD v0.4.0](https://w3c-ccg.github.io/zcap-spec/v0.4.0/)
- [W3C EdDSA Data Integrity suites](https://www.w3.org/TR/vc-di-eddsa/#eddsa-jcs-2022)
- [RFC 9421 HTTP Message Signatures](https://www.rfc-editor.org/rfc/rfc9421.html)
- [RFC 9530 Digest Fields](https://www.rfc-editor.org/rfc/rfc9530.html)

## AEO Summary

- Package: `tba-protocol-zcap`
- Layer: `50-protocols`
- Responsibility: ZCAP-LD delegation and HTTP invocation verification for the TBA Ed25519 development profile.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-zcap/src/tba_protocol_zcap/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-protocol-zcap` for this responsibility: ZCAP-LD delegation and HTTP invocation verification for the TBA Ed25519 development profile. Its `50-protocols` placement keeps protocol semantics and projections separate from deployment hosting or ownership of persistence implementations.

## Installation

Install the selected PyPI release of `tba-protocol-zcap`:

```bash
uv pip install tba-protocol-zcap
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/50-protocols/tba-protocol-zcap
```

## Quick start

Build the package from the repository root.

```bash
uv build --wheel pkgs/50-protocols/tba-protocol-zcap
```

## Usage

The following public-entry-point example belongs to `tba-protocol-zcap`. ZCAP-LD delegation and HTTP invocation verification for the TBA Ed25519 development profile. Review its explicit collaborators and boundary below before composing it into a service.

```python
import tba_protocol_zcap

print(tba_protocol_zcap.__name__)
```

## Package Boundary

`tba-protocol-zcap` belongs to `50-protocols` and owns protocol semantics and projections: ZCAP-LD delegation and HTTP invocation verification for the TBA Ed25519 development profile.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-zcap/src/tba_protocol_zcap/__init__.py). Public exports include `CRYPTOSUITE`, `PROFILE`, `SPEC_VERSION`, `VerifiedZcapInvocation`, `ZcapDelegation`, `ZcapError`, `ZcapHttpInvocation`, `ZcapRoot`, `ZcapVerifier`, `sign_delegation`, `sign_http_invocation`.

Keep deployment hosting or ownership of persistence implementations in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-protocol-zcap`:

- `sign_http_invocation` construction inputs: `method`, `target`, `action`, `key_id`, `key`, `created`, `expires`, `nonce`, `body`, `content_type`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-zcap/src/tba_protocol_zcap/http.py).
- `sign_delegation` construction inputs: `verification_method`, `key`, `created`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-zcap/src/tba_protocol_zcap/proofs.py).
- `ZcapVerifier` construction inputs: `resolve_root`, `resolve_key`, `is_revoked`, `replay`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-zcap/src/tba_protocol_zcap/protocol.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-protocol-zcap` exposes protocol semantics and projections. Public operations found in its source:

- `sign_http_invocation` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-zcap/src/tba_protocol_zcap/http.py).
- `sign_delegation` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-zcap/src/tba_protocol_zcap/proofs.py).
- `ZcapVerifier.verify_invocation` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-zcap/src/tba_protocol_zcap/protocol.py).
- `ZcapRoot.id` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-zcap/src/tba_protocol_zcap/schemas.py).
- `ZcapRoot.to_document` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-zcap/src/tba_protocol_zcap/schemas.py).
- `ZcapDelegation.to_document` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-zcap/src/tba_protocol_zcap/schemas.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-protocol-zcap`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`tba-protocol-zcap` does not take ownership of deployment hosting or ownership of persistence implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-codec-jcs](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-jcs/README.md)
- [tba-codec-multibase](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-multibase/README.md)
- [tba-contracts-replay](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-replay/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/50-protocols/tba-protocol-zcap)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-zcap/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-zcap/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-zcap/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-protocol-zcap/)

## Governance

`tba-protocol-zcap` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `50-protocols` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

Check that the build produces a wheel with the package version declared in `pyproject.toml`.
