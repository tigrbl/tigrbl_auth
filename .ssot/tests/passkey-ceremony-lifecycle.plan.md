# Passkey ceremony composition

Planned acceptance. Each tier requires a recorded run against the candidate revision.

Governed by spc:1238.

## T0

Test challenge, RP ID, origin, user verification, and factor-purpose bindings.

## T1

Compose WebAuthn verifier, router and durable store for registration and assertion. Reject expired, mismatched and replayed challenges.

## T2

Use a browser virtual authenticator to prove registration and assertion of the same credential in a repository-owned synthetic app.
