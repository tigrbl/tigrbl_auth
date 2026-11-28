# MFA enrollment lifecycle

Planned acceptance. Each tier requires a recorded run against the candidate revision.

Governed by spc:1238.

## T0

Table-test scope and account binding, proof before activation, expiration, cancellation, replay, and replacement.

## T1

Integrate TOTP and WebAuthn verification with transactional storage. Concurrent completion activates one credential and a failed replacement preserves the prior factor.

## T2

Complete first enrollment and subsequent verification in the repository-owned browser fixture using synthetic accounts.

## Executable tests

- [Python tests](../../pkgs/120-tests/tba-tests-authentication/tests/unit/test_mfa_enrollment_step_up_runtime.py)
