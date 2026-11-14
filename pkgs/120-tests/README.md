# Layer 120: Tests

Layer 120 owns executable test suites and shared fixtures, vectors, and runners.
Production packages must not depend on this layer. Repository-wide suites move
here by capability. During migration the root pytest configuration collects both
the migrated suites and the remaining root tests.

| Package | Scope |
| --- | --- |
| `tba-tests-wimse` | WIMSE identifiers, WIC, mTLS, WIT, WPT, and workload proof claims |
| `tba-tests-spiffe` | SPIFFE providers and SVID profiles, including the separately marked CWT extension module |
| `tba-tests-workload-composition` | Workload protocol boundaries, specification ownership and runtime composition |
| `tba-tests-storage` | Workload artifact durability and WIMSE/SPIFFE storage migrations |
| `tba-tests-authorization` | DID and workload policy contracts |
| `tba-tests-oauth` | OAuth grants, extensions, HTTP bindings, and security profiles |
| `tba-tests-oidc` | OpenID Connect discovery, ID tokens, UserInfo, and logout |
| `tba-tests-jose` | JOSE/JWT and related signing, encryption, and key handling |
| `tba-testkit-workload-credential-conformance` | Shared workload vectors, certificate fixtures and clean-wheel runner |
| `tba-testkit-wimse-cred-interop` | Opt-in Cred peer suite |
| `tba-testkit-identity` | Shared identity fixtures |

Run a native suite from the repository root with
`uv run --extra test pytest pkgs/120-tests/tba-tests-wimse/tests`.
The other native suites use the same command with their own paths.
Pass `--certification-lane all` to run the protocol suites across all lanes.
The Cred package README documents its separate checkout and invocation.
