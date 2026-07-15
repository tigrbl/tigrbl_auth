# tigrbl-authenticator-attestation-capability

Mountable appraisal, metadata resolution, and reappraisal operations for authenticator attestations.

## Injected dependencies

An attestation appraiser plus optional metadata resolver and registered-authenticator reappraiser.

## Operations and readiness

Appraisal is required. Metadata resolution and reappraisal are optional and report unavailable when unbound.

## Protocol consumers

WebAuthn registration and the FIDO2 server profile consume normalized appraisal results.

## Non-goals

This package does not parse attestation formats, fetch metadata, validate certificate paths, or choose trust policy.
