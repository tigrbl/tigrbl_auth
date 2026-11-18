# tba-protocol-ucan

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-ucan/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-ucan/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-protocol-ucan%3D%3D0.4.0.dev4/pkgs/50-protocols/tba-protocol-ucan/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-protocol-ucan%3D%3D0.4.0.dev4/pkgs/50-protocols/tba-protocol-ucan/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/50-protocols"><img alt="Layer: 50 protocols" src="https://img.shields.io/badge/Layer-50%20protocols-0a7f5a"></a>
<a href="https://pypi.org/project/tba-protocol-ucan/"><img alt="PyPI version for tba-protocol-ucan" src="https://img.shields.io/pypi/v/tba-protocol-ucan?label=tba-protocol-ucan%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-protocol-ucan"><img alt="Monthly PyPI downloads for tba-protocol-ucan" src="https://static.pepy.tech/badge/tba-protocol-ucan/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-ucan/README.md"><img alt="README hits for tba-protocol-ucan" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-ucan/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-ucan/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

UCAN delegation and invocation signing and verification for the TBA Ed25519
development profile. The wire tags are `ucan/dlg@1.0.0` and `ucan/inv@1.0.0`.

- [UCAN envelope](https://github.com/ucan-wg/spec/blob/8072f3f23f451eaa1271269fe763aebcf294f4db/README.md#envelope)
- [UCAN delegation](https://github.com/ucan-wg/delegation/blob/1cb32dbc9d4d15a23bf9844a02515d760b81e816/README.md)
- [UCAN invocation](https://github.com/ucan-wg/invocation/blob/0f4c11325af6aca298b565cc19e90009d10e0197/README.md)

This profile supports bare Ed25519 `did:key` identifiers, canonical DAG-CBOR
with integers in the interoperable 53-bit range, linear proof chains of up to
16 grants, finite expiries, and equality predicates on top-level arguments.
Invocations have a maximum remaining lifetime of five minutes. The profile
rejects unsupported algorithms, fields, and policy operators. It covers a
subset of the UCAN specifications.

## AEO Summary

- Package: `tba-protocol-ucan`
- Layer: `50-protocols`
- Responsibility: UCAN delegation and invocation verification for the TBA Ed25519 development profile.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-ucan/src/tba_protocol_ucan/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-protocol-ucan` for this responsibility: UCAN delegation and invocation verification for the TBA Ed25519 development profile. Its `50-protocols` placement keeps protocol semantics and projections separate from deployment hosting or ownership of persistence implementations.

## Installation

Install the selected PyPI release of `tba-protocol-ucan`:

```bash
uv pip install tba-protocol-ucan
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/50-protocols/tba-protocol-ucan
```

## Quick start

Build the package from the repository root.

```bash
uv build --wheel pkgs/50-protocols/tba-protocol-ucan
```

## Usage

The following public-entry-point example belongs to `tba-protocol-ucan`. UCAN delegation and invocation verification for the TBA Ed25519 development profile. Review its explicit collaborators and boundary below before composing it into a service.

```python
import tba_protocol_ucan

print(tba_protocol_ucan.__name__)
```

## Verifying a call

Use `sign_delegation` and `sign_invocation` with the issuer's Ed25519 private
key. Index signed delegations with `content_id` and list their CIDs in
`UcanInvocation.prf` from root to leaf. Configure `UcanVerifier` with a
proof lookup, a revocation check, and a TBA replay reservation provider.
Call `verify_invocation` with the trusted subject, the local executor, and the
expected command. Dispatch the command with the arguments in the returned
invocation. The verifier checks every delegation's policy against those
arguments and atomically reserves the invocation CID before returning.

The caller supplies the mapping from trusted subjects and commands to local
resources. A deployment with multiple workers needs a shared replay store
with atomic reservations. Revocation storage is supplied by the caller.

## Wire codec

**DAG-CBOR** produces deterministic binary bytes for the signed map. The
verifier rejects duplicate keys, noncanonical encodings, and values outside
the profile. **Varsig** is the header inside that map identifying Ed25519 and
DAG-CBOR. The signature covers both the header and the versioned payload.

A **CID** identifies the complete signed envelope. Its binary representation
contains CIDv1, the DAG-CBOR codec code, the SHA-256 multihash code and length,
and the digest. The text form uses base58btc. In the invocation proof list,
each CID is a DAG-CBOR tag 42 link with a leading zero byte followed by the
binary CID. The verifier recomputes the CID of every resolved proof before
accepting it.

See [DAG-CBOR](https://ipld.io/specs/codecs/dag-cbor/spec/) and
[Varsig](https://github.com/ChainAgnostic/varsig).

## Package Boundary

`tba-protocol-ucan` belongs to `50-protocols` and owns protocol semantics and projections: UCAN delegation and invocation verification for the TBA Ed25519 development profile.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-ucan/src/tba_protocol_ucan/__init__.py). Public exports include `DELEGATION_TAG`, `INVOCATION_TAG`, `PROFILE`, `UcanDelegation`, `UcanEnvelopeCodec`, `UcanError`, `UcanInvocation`, `UcanVerifier`, `VerifiedUcanInvocation`, `content_id`, `did_key`, `sign_delegation`.

Keep deployment hosting or ownership of persistence implementations in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-protocol-ucan`:

- `UcanVerifier` construction inputs: `resolve_proof`, `is_revoked`, `replay`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-ucan/src/tba_protocol_ucan/protocol.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-protocol-ucan` exposes protocol semantics and projections. Public operations found in its source:

- `did_key` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-ucan/src/tba_protocol_ucan/codec.py).
- `content_id` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-ucan/src/tba_protocol_ucan/codec.py).
- `UcanEnvelopeCodec.sign` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-ucan/src/tba_protocol_ucan/codec.py).
- `UcanEnvelopeCodec.verify` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-ucan/src/tba_protocol_ucan/codec.py).
- `sign_delegation` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-ucan/src/tba_protocol_ucan/protocol.py).
- `sign_invocation` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-ucan/src/tba_protocol_ucan/protocol.py).
- `UcanVerifier.verify_invocation` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-ucan/src/tba_protocol_ucan/protocol.py).
- `UcanDelegation.from_payload` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-ucan/src/tba_protocol_ucan/schemas.py).
- `UcanDelegation.to_payload` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-ucan/src/tba_protocol_ucan/schemas.py).
- `UcanInvocation.executor` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-ucan/src/tba_protocol_ucan/schemas.py).
- `UcanInvocation.from_payload` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-ucan/src/tba_protocol_ucan/schemas.py).
- `UcanInvocation.to_payload` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-ucan/src/tba_protocol_ucan/schemas.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-protocol-ucan`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`tba-protocol-ucan` does not take ownership of deployment hosting or ownership of persistence implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-codec-cid](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-cid/README.md)
- [tba-codec-dag-cbor](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-dag-cbor/README.md)
- [tba-codec-multibase](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-multibase/README.md)
- [tba-contracts-replay](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-replay/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/50-protocols/tba-protocol-ucan)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-ucan/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-ucan/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-ucan/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-protocol-ucan/)

## Governance

`tba-protocol-ucan` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `50-protocols` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

Check that the build produces a wheel with the package version declared in `pyproject.toml`.
