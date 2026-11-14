# Backend application tests

Each directory under `tests/packages/` uses the distribution name of the
backend application under test. Package and realm tests run against the local
workspace or an isolated wheel installed by the package test matrix. Live
deployment proofs keep their existing environment settings and readiness checks.

Run all backend application tests from the repository root with
`uv run --extra test pytest --certification-lane all pkgs/120-tests/tba-tests-backend-apps/tests`.
