# Workload and identity artifact support

| Artifact or standard | Owner | Lifecycle | Delivered boundary | Not yet a conformance claim |
|---|---|---|---|---|
| JWT / JWS / JWE | `50-protocols/tigrbl-auth-protocol-jwt`, `tigrbl-security-protocol-jws`, `tigrbl-security-protocol-jwe` | RFC 7519 / 7515 / 7516 | deterministic compact/JSON objects, capability-backed signing/encryption, strict versioned profiles | independent JOSE interoperability and algorithm/provider certification |
| CWT / COSE | `50-protocols/tigrbl-auth-protocol-cwt`, `tigrbl-security-protocol-cose` | RFC 8392 / 9052 | tagged CWT claims, integer-label profiles, COSE_Sign1 issuance and cryptographic verification | independent COSE/CWT interoperability |
| OIDC ID Token | `50-protocols/tigrbl-auth-protocol-oidc` | OIDC Core 1.0 | signature verification followed by issuer, subject, audience, azp, time, nonce, algorithm, and type validation | canonical runtime regression suite and OP certification |
| OAuth JWT access token | `tigrbl-oauth-profile-jwt-access-token` | RFC 9068 | distinct `at+jwt` profile | resource-server certification |
| DID Document | `tigrbl-identity-protocol-did-core` | DID Core 1.0 Recommendation | canonical parse/resolve/verify path, document syntax, controllers, key material, and verification relationships | method-specific resolution and interoperability |
| VC-JOSE-COSE | `tigrbl-credential-profile-vc-jose-cose` | W3C Recommendation 2025-05-15 | VC issuance and verification over JOSE and COSE with claims reconstructed from verified bytes; unsupported VP formats are not advertised | independent VC-JOSE-COSE interoperability; VP delivery remains separate |
| X.509-SVID / JWT-SVID | `tigrbl-workload-protocol-spiffe-svid` | stable SPIFFE | SPIFFE ID and format-specific profile validation | SPIRE interoperability |
| WIT | `tigrbl-workload-credential-profile-wimse-wit` | IETF draft `-02` | confirmation-bound workload credential | standards-track stability |
| WPT | `tigrbl-workload-proof-profile-wimse-wpt` | IETF draft `-01` | audience/replay/WIT and context token hashes | standards-track stability |
| WIT-SVID | `tigrbl-workload-credential-profile-spiffe-wit-svid` | SPIFFE v1.15.1 Incubating | SPIFFE-subject WIT plus mandatory PoP input | stable SPIFFE conformance |
| CWT-SVID extension | `tigrbl-workload-credential-profile-cwt-svid-extension` | Tigrbl experiment 1 | CWT/COSE/RFC 8747 confirmation plus PoP | any SPIFFE conformance |
| Workload API | `tigrbl-workload-protocol-spiffe-workload-api` | stable service contract | exact closed RPC set and stream rules | generated protobuf/gRPC and SPIRE interop |
| Broker API | `tigrbl-workload-protocol-spiffe-broker-api` | v1.15.1 Incubating | exact closed RPC set, references, authorization | generated protobuf/gRPC and independent interop |

CWT-SVID is not an official SVID. WIT-SVID and Broker API remain disabled by default. Cryptographic validity, issuer trust, proof verification, replay state, and policy acceptance remain separate decisions.