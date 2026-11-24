# Hosted authorization continuation

Planned acceptance. Each tier requires a recorded run against the candidate revision.

Governed by spc:1239.

## T0

Test resume, restart and unavailable for valid, expired, mismatched and consumed requests. Preserve issuer, client, exact redirect, state, nonce and PKCE when applicable.

## T1

Use durable transaction adapters through email verification and first MFA enrollment. Concurrent attempts produce at most one resume.

## T2

Use a synthetic relying party and installed packages to resume the original callback after first enrollment, and verify a separately registered restart after expiry.
