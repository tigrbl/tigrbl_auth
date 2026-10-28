# tba-provider-security-proof-pkce

Standalone RFC 7636 PKCE proof helper and verifier provider for the TBA package suite.

- Owns dependency-light verifier generation, S256 challenge derivation, and challenge verification.
- Exposes `PkceProofProvider` for the security trust domain provider surface.
- Protocol packages such as `tba-protocol-oidc-relying-party` and `tba-protocol-oauth` should import this package instead of duplicating PKCE primitives.
