# tba-testkit-workload-credential-conformance

Reusable structural and negative vectors. Passing these vectors is not an independent interoperability or certification claim.

The workload suites also import certificate and TLS fixtures from `fixtures`,
profile exercises from `profiles`, and the clean-wheel runner from `wheels`.
The `runner` extra supplies their test tooling. The root test environment
supplies the protocol packages exercised by each suite.
