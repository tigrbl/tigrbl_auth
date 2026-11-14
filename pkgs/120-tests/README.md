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
| `tba-tests-storage` | Storage components, migration portability, persistence durability, and table ownership and operations |
| `tba-tests-authorization` | Authorization invariants, policy evaluation and replay, delegation, and DID and workload policy contracts |
| `tba-tests-oauth` | OAuth grants, extensions, HTTP bindings, and security profiles |
| `tba-tests-oidc` | OpenID Connect discovery, ID tokens, UserInfo, and logout |
| `tba-tests-browser-session` | Browser login, cookies, consent, and session lifecycle |
| `tba-tests-platform-iam` | IAM contracts, conformance, policy decisions, RP sessions, performance, and UI wiring |
| `tba-tests-administration` | Admin authentication, identity and tenant operations, and account self service |
| `tba-tests-admin-uix` | Admin shell, access controls, resource views, and safe mutations |
| `tba-tests-runtime` | Server runners, runtime settings, and capability composition |
| `tba-tests-operator-cli` | CLI contracts, operator commands, and lifecycle conformance |
| `tba-tests-api-contracts` | OpenAPI, OpenRPC, route schemas, and router ownership |
| `tba-tests-certification` | Certification evidence, validated execution, and peer catalogs |
| `tba-tests-release` | Release gates, signing, package matrices, and installation checks |
| `tba-tests-architecture` | Package taxonomy, layer boundaries, and SSOT governance |
| `tba-tests-backend-apps` | Backend application package, realm, and live deployment checks |
| `tba-tests-jose` | JOSE/JWT and related signing, encryption, and key handling |
| `tba-tests-wire-codecs` | JSON canonicalization, multibase, CID, and DAG-CBOR |
| `tba-tests-did` | DID Core documents, resolution, dereferencing, and controller behavior |
| `tba-tests-gnap` | Grant Negotiation and Authorization Protocol versions and capability binding |
| `tba-tests-examples` | Device-login CLI and README usage tests. |
| `tba-tests-governance-composition` | Provisioning boundaries, entitlements, access reviews, and delivery summaries. |
| `tba-tests-scim` | Schema registration, PATCH operations, and group membership. |
| `tba-tests-ucan` | UCAN delegation and invocation verification |
| `tba-tests-zcap` | ZCAP delegation and HTTP invocation verification |
| `tba-tests-set` | Security Event Token claims, transmission, reception, and replay handling |
| `tba-tests-vcdm` | W3C Verifiable Credentials Data Model and presentation structure |
| `tba-tests-sd-jwt-vc` | SD-JWT VC format and versioned profile |
| `tba-tests-mdoc` | ISO mdoc structure, issuance, and verification |
| `tba-tests-vc-jose-cose` | Verifiable credential signing and verification over JOSE and COSE |
| `tba-tests-oid4vci` | OpenID for Verifiable Credential Issuance |
| `tba-tests-oid4vp` | OpenID for Verifiable Presentations |
| `tba-tests-haip` | OpenID High Assurance Interoperability Profile |
| `tba-tests-authzen` | AuthZEN access evaluation, batch evaluation, and search |
| `tba-tests-credential-composition` | Credential lifecycle, issuer and verifier dispatch, credential status, and issuer trust |
| `tba-tests-authentication` | Authentication backends, authenticator contracts, principal checks, and password hashing |
| `tba-tests-eat` | Entity Attestation Token claims, carriers, and evidence verification |
| `tba-tests-corim` | CoRIM model, reference material storage, and versioning |
| `tba-tests-attestation-composition` | Evidence appraisal and wallet, key, and platform attestation providers |
| `tba-tests-webauthn` | WebAuthn API, registration, authentication, and attestation formats |
| `tba-tests-totp` | Time-based one-time password generation and verification |
| `tba-tests-bimi` | BIMI discovery, DNS/DMARC readiness, VMC and CMC verification, and audit integration |
| `tba-tests-communications-identity` | Shared sending-domain assessment and auditing |
| `tba-tests-dns` | TXT record resolution and DNS contract compatibility |
| `tba-tests-x509` | X.509 logotype parsing and certificate path evidence |
| `tba-testkit-workload-credential-conformance` | Shared workload vectors, certificate fixtures and clean-wheel runner |
| `tba-testkit-wimse-cred-interop` | Opt-in Cred peer suite |
| `tba-testkit-identity` | Shared identity fixtures |

Run a native suite from the repository root with
`uv run --extra test pytest pkgs/120-tests/tba-tests-wimse/tests`.
The other native suites use the same command with their own paths.
Pass `--certification-lane all` to run the protocol suites across all lanes.
Run the BIMI suite with `uv run --extra test --extra bimi pytest pkgs/120-tests/tba-tests-bimi/tests`. The same extras cover its DNS, X.509, and communications identity dependencies.
The Cred package README documents its separate checkout and invocation.
