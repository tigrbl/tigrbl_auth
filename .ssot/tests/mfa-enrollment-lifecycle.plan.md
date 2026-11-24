# MFA enrollment lifecycle

Planned acceptance. Each tier requires a recorded run against the candidate revision.

Governed by spc:1238.

## T0

Verify pending, active, cancelled, and expired state transitions, scope and account binding, and the requirement for proof before activation.

## T1

Compose real TOTP and WebAuthn verifiers with transactional test storage. Verify single activation under concurrent completion and preservation of the active factor when replacement fails.

## T2

Run a synthetic hosted browser fixture through first enrollment, ensuing challenge, and factor replacement using isolated accounts. Exercise an actual browser passkey ceremony before claiming passkey coverage.
