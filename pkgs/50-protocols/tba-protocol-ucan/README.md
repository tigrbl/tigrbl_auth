# tba-protocol-ucan

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-ucan/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-ucan/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-ucan/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/50-protocols"><img alt="Layer: 50 protocols" src="https://img.shields.io/badge/Layer-50%20protocols-0a7f5a"></a>
<a href="https://pypi.org/project/tba-protocol-ucan/"><img alt="PyPI version for tba-protocol-ucan" src="https://img.shields.io/pypi/v/tba-protocol-ucan?label=tba-protocol-ucan%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-protocol-ucan"><img alt="Monthly PyPI downloads for tba-protocol-ucan" src="https://static.pepy.tech/badge/tba-protocol-ucan/month"></a>
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

## Quick start

Build the package from the repository root.

```bash
uv build --wheel pkgs/50-protocols/tba-protocol-ucan
```

## Verification

Check that the build produces a wheel with the package version declared in `pyproject.toml`.
