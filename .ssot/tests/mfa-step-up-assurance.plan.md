# MFA step-up assurance

Planned acceptance. Each tier requires a recorded run against the candidate revision.

Governed by spc:1238.

## T0

Check scope, original subject, requested factor, purpose, and freshness rules for each proof outcome.

## T1

Use actual factor verifiers, a durable replay record, and two injected policies. Verify that only a fresh eligible proof upgrades assurance.

## T2

Show the synthetic relying party resumes the same subject at the required assurance.

## Executable tests

- [Python tests](../../pkgs/120-tests/tba-tests-authentication/tests/unit/test_mfa_enrollment_step_up_runtime.py)
