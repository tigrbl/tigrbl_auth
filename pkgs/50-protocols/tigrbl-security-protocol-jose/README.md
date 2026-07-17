# tigrbl-security-protocol-jose

Version, compatibility, carrier-schema, and capability-binding ownership for
the JOSE RFC family. Deterministic JWS, JWE, JWK, and JWT algorithms remain in
tigrbl-jose-concrete; key loading and environment-backed cryptography remain
provider responsibilities.

JOSE headers are not application claims. JWT and other JOSE-using profiles own
their claim sets in their respective layer-50 packages.
