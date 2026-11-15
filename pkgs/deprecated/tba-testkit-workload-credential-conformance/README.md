# tba-testkit-workload-credential-conformance (deprecated)

Install [`tba-tests-workload-credential-conformance`](https://pypi.org/project/tba-tests-workload-credential-conformance/) and replace `tba_testkit_workload_credential_conformance` imports with `tba_tests_workload_credential_conformance`. Use `tba-tests-workload-credential-conformance[runner]` if you installed the old `runner` extra.

Existing installations can upgrade to this release using the original package name. Imports continue to work and emit `DeprecationWarning`. Use `python -W default` to display it.
