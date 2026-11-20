# Layer 120: Tests

Layer 120 owns executable test suites and shared fixtures, vectors, and runners.
Production packages must not depend on this layer. Repository-wide suites move
here by capability. The root pytest configuration collects Layer 120.
The top-level `tests/` directory holds shared fixtures and support imports.

Use **governance certification** for claim and evidence checks and **release
certification** for release evidence and validation gates. Use **X.509
certificate** for parsing, trust, revocation, and path validation. Use the
protocol name with **mTLS** or **WIC** for certificate-based authentication
checks. The pytest option `--certification-lane` selects the evidence lane.

| Package | Scope |
| --- | --- |
| `tba-tests-wimse` | WIMSE identifiers, WIC certificate profiles, mTLS peer authentication, WIT, and WPT |
| `tba-tests-spiffe` | SPIFFE providers and SVID profiles, including the separately marked CWT extension module |
| `tba-tests-workload-composition` | Workload protocol boundaries, specification ownership and runtime composition |
| `tba-tests-storage` | Storage components, migration portability, persistence durability, and table ownership and operations |
| `tba-tests-authorization` | Authorization invariants, policy evaluation and replay, delegation, and DID and workload policy contracts |
| `tba-tests-oauth` | OAuth grants, HTTP bindings, security policies, and RFC 8705 mTLS client authentication |
| `tba-tests-oidc` | OpenID Connect discovery, ID tokens, UserInfo, and logout |
| `tba-tests-browser-session` | Browser login, cookies, consent, and session lifecycle |
| `tba-tests-platform-iam` | IAM contracts, conformance, policy decisions, RP sessions, performance, and UI wiring |
| `tba-tests-administration` | Admin authentication, identity and tenant operations, and account self service |
| `tba-tests-admin-uix` | Admin shell, access controls, resource views, and safe mutations |
| `tba-tests-runtime` | Server runners, runtime settings, and capability composition |
| `tba-tests-operator-cli` | CLI contracts, operator commands, and lifecycle conformance |
| `tba-tests-api-contracts` | OpenAPI, OpenRPC, route schemas, and router ownership |
| `tba-tests-governance-release-certification` | Governance claims, release certification evidence, validated execution, and peer catalogs |
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
| `tba-tests-x509-certificates` | X.509 certificate parsing, trust anchors, revocation status, and path validation |
| `tba-tests-workload-credential-conformance` | Shared workload vectors, certificate fixtures and clean-wheel runner |
| [`tba-tests-interop-wimse`](https://github.com/tigrbl/tba-tests-interop-wimse) | WIMSE interop matrices, factor rules, exclusions, and combination counter |
| `tba-tests-identity` | Shared identity fixtures and pytest suite selection |
| `tba-tests-interop-jose` | Bidirectional compact JWE tests for source checkouts and installed wheels |

Select a suite by its package name from the repository root.

```bash
uv run --extra test pytest --tba-suite tba-tests-wimse
```

Repeat `--tba-suite` to select multiple suites. Evidence commands can still
select suites by path, such as `pkgs/120-tests/tba-tests-wimse/tests`.
Use `--certification-lane all` to run cases across the certification lanes.
