# Workload identity artifact evidence

This delivery has executable, repository-owned evidence for the following boundaries:

- deterministic JWS/JWE/JWT and COSE/CWT wire objects;
- capability-backed JOSE and COSE signing, encryption, decryption, and verification;
- versioned JWT, JWS, JWE, CWT, and COSE protocol mappings;
- canonical OIDC ID Token verification on the runtime path;
- canonical DID Document parsing, resolution, relationship validation, and verification;
- VC-JOSE-COSE credential issuance and verification with claims reconstructed only after cryptographic verification;
- fail-closed runtime feature composition for DID, VC-JOSE-COSE, and experimental CWT-SVID;
- negative confusion vectors for VC nesting, VP advertisement, DID relationships, ID Token token type, CWT carrier type, and CWT-SVID proof/replay;
- package-layer, dependency-direction, lockfile, and diff-integrity checks.

These are implementation and regression tests, not independent interoperability or certification evidence. No target is promoted above an implementation/test tier solely from constants, models, or repository-authored vectors. CWT-SVID remains a Tigrbl experiment and is explicitly not SPIFFE-conformant.

Outstanding independent evidence:

- generated official protobuf/gRPC bindings and wire compatibility for SPIFFE Workload/Broker APIs;
- a SPIRE or independent implementation interoperability run;
- independent JOSE, COSE, CWT, DID, and VC-JOSE-COSE vector/interoperability suites;
- production key custody, trust-path, time, replay, and cryptographic-provider integration tests;
- certification artifacts for OIDC, OAuth, W3C VC, or SPIFFE.
