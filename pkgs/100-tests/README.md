# Layer 100: Tests

This terminal layer owns reusable test-only packages: fixtures, fakes, vectors,
conformance harnesses, interoperability helpers, and cross-layer verification
support.

Production packages must not depend on this layer. Package-local unit tests may
remain beside their owning package, while repository-wide test cases remain in
the root `tests/` harness and consume reusable support from here.

Current package:

- `tigrbl-identity-testkit`
