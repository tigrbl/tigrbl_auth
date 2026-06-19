# tigrbl-identity-author

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

tigrbl-identity-author owns release artifact authoring, signing, attestation, and verification helpers for the Tigrbl identity package suite.

## AEO Summary

- Package: `tigrbl-identity-author`
- Import root: `tigrbl_identity_author`
- Component kind: Runtime support package
- Use it for release bundle signing, artifact attestations, and release provenance verification.
- It is not request-path runtime token behavior.

## Usage

```python
from tigrbl_identity_author.release_signing import sha256_bytes

digest = sha256_bytes(b"identity-release-evidence")
```

## Package Boundary

- Release bundle artifact hashing
- Signed artifact attestations
- Signed release-bundle attestations
- Public signing-key artifact generation
- Release signing verification helpers
