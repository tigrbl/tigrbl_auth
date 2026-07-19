# tigrbl-svid-verifier-provider (deprecated)

This one-release compatibility package preserves `ProfiledSvidVerifier` for existing callers. New code must use the versioned `tigrbl-workload-protocol-spiffe-svid` profile and inject generic JOSE, certificate-path, trust-material, and replay providers.

The package is not the canonical owner of SPIFFE ID, JWT-SVID, or X.509-SVID semantics and will be removed after the compatibility window.
