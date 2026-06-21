# tigrbl-security-proof-pkce

Standalone RFC 7636 PKCE proof helper and verifier provider for the Tigrbl auth package suite.

- Owns dependency-light verifier generation, S256 challenge derivation, and challenge verification.
- Exposes `PkceProofProvider` for the security trust domain provider surface.
- Protocol packages such as `tigrbl-auth-protocol-rp` and `tigrbl-auth-protocol-oauth` should import this package instead of duplicating PKCE primitives.
