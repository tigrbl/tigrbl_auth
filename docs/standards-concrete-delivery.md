# Identity Standards Delivery Matrix

Updated: 2026-07-12

This is the durable implementation checklist for identity, credential, claim,
token, attestation, trust-material, and authorization standards. Structural
support is not described as protocol certification: certification additionally
requires complete normative coverage, negative and interoperability evidence,
and independently verifiable results.

## Layer delivery checklist

| Layer | Package or family | Delivered | Remaining |
|---|---|---|---|
| 00 | `tigrbl-identity-core` | Opaque IDs and refs; artifact, credential-format, token, presentation, attestation, manifest, lifecycle, media-type, nonce, digest, URI, protocol-tag, `ClaimType`, `ClaimValueType`, and `RegisteredClaim` primitives | Extend registries only when an implemented revision requires a new semantic value |
| 01 | `tigrbl-identity-storage` | Credential issuer/configuration/offer/issuance/status state; presentation transaction/consent/replay state; attestation evidence/results/reference material; SVID/trust bundles; SET delivery; optional DID/GNAP state; certificate records/trust anchors/status snapshots | Enforce deployment-specific retention, encryption, and deletion policies for sensitive payloads |
| 02 | `tigrbl-identity-contracts` | Neutral claim/claim-set, digital credential, presentation, wallet, attestation, workload/SVID, DID, security-event, policy/AuthZEN/XACML, delegation, EAP ACR, and Identity Assurance contracts | Continue removing wire-format dictionaries when stable neutral semantics exist |
| 02 | `tigrbl-security-trust-contracts` | Certificate profiles/path/status, trust anchors/bundles, issuer trust, and verification-key ports | Add profile contracts only with an implemented verifier |
| 05 | `tigrbl-identity-claims-bases` | `ClaimBase` and neutral provider base | None for current claim catalog |
| 05 | `tigrbl-digital-credential-bases` | Format, issuer, verifier, presentation, status, and wallet-attestation bases | Add bases only for multiple concrete implementations |
| 05 | attestation, JOSE, COSE, OAuth/OIDC compatibility, policy, resource-server, and trust bases | Shared deterministic/provider extension points | Finish removal of remaining protocol-named compatibility bases |
| 10 | standalone identity packages | One package per concrete user, admin, service, client, machine, workload, and device identity | Add identity classes only for distinct semantics/lifecycle |
| 10 | standalone authenticator-credential packages | One package per password, reset, API/service key, client secret, MFA/passkey/WebAuthn/passwordless, mTLS, and DPoP-key credential | Keep these distinct from issued digital credentials |
| 10 | standalone claim packages | One `ClaimBase` subclass per registered concrete claim package | Complete claim-name coverage as additional standards revisions are implemented |
| 10 | JOSE, SD-JWT, SD-JWT VC, mdoc, VCDM, EAT, CoRIM, SVID, DID, SET concrete packages | Deterministic parsing, validation, serialization, and format behavior | No filesystem, HTTP, database, HSM, or issuer-trust decisions |
| 20 | credential, presentation, COSE/mdoc, wallet/key/platform attestation, EAT/RATS/CoRIM, SPIFFE/SVID, DID, SET, certificate/trust providers | Environment-backed signing, verification, resolution, storage, appraisal, delivery, and trust behavior | Vendor-specific providers remain separate when dependencies or evidence differ |
| 30 | `tigrbl-identity-storage-runtime` | Repositories and transaction coordinators for new durable tables | Exercise every repository against production database backends |
| 40 | digital credential issuance/presentation, attestation appraisal, security events, workload identity | Capability orchestration over neutral ports | Add operational policy and transaction coordination without leaking wire formats |
| 50 | JWT, OAuth, OIDC, OID4VCI, OID4VP, HAIP, AuthZEN, GNAP, SET, EAT, SD-JWT VC | Independent version histories, revision feature gates, explicit migrations, and protocol/profile claim-set composition | Add normative endpoint coverage and independent interop evidence before certification |
| 60 | `tigrbl-identity-runtime` | Lazy installed-owner standards registry and exact runtime manifest | Remove older layer-50 imports of runtime settings by injecting deployment configuration |
| 70 | `tigrbl-auth` | Stable lazy exports for runtime standards discovery | Re-export additional APIs only after owner packages stabilize |
| 80 | public API contract | Declares standards-manifest capability and OID4VC/HAIP package consumption | Mount credential issuance, presentation, AuthZEN, GNAP, SET, and attestation routes from protocol/capability truth |
| Compliance | targets, mappings, claims, evidence, generated reports | RFC 8417 correction; live SET concrete/protocol owners; canonical registries regenerated and verified | Add new targets only when tests and independent evidence justify the claimed tier |

## Concrete object matrix

`01` means the object has independently useful durable lifecycle state; it does
not mean every encoded payload should be retained.

| Concrete object | Family | 00 primitive | 01 durable | 02 contract | 05 base | 10 concrete | 20 provider | Primary owner | Protocol tags |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| Principal | subject/authorization | yes | yes | yes | optional | yes | yes | neutral identity packages | oauth, oidc, authzen, xacml, zta |
| Identity | identity | yes | yes | yes | yes | standalone | source-dependent | standalone identity package | oidc, did-core, spiffe, zta |
| SPIFFE ID | workload identity | yes | yes | yes | yes | yes | resolver/provider | `tigrbl-svid-concrete` | spiffe, svid, x509, jwt |
| SVID | workload credential | yes | yes | yes | yes | JWT/X.509 | yes | SVID concrete/providers | spiffe, svid, jwt, x509 |
| Authenticator credential | authentication credential | yes | yes | yes | yes | standalone | yes | standalone credential package | oidc, oauth, webauthn, fido, x509, dpop |
| Digital credential | issued assertion | yes | yes | yes | yes | format-specific | issuer/verifier | digital credential families | oid4vci, oid4vp, haip, w3c-vcdm, sd-jwt-vc, iso-mdoc |
| W3C Verifiable Credential | digital credential data model | yes | yes | yes | yes | yes | issuer/verifier | `tigrbl-vcdm-concrete` | w3c-vcdm, w3c-vp, did-core |
| Verifiable Presentation | holder presentation | yes | transaction/replay | yes | yes | yes | verifier | VCDM/presentation packages | w3c-vp, oid4vp |
| SD-JWT VC | selective-disclosure credential | yes | yes | yes | yes | yes | issuer/verifier | SD-JWT VC packages | jwt, jws, sd-jwt, sd-jwt-vc, kb-jwt, oid4vci, oid4vp, haip |
| KB-JWT | holder-binding token | yes | replay state | yes | yes | yes | verifier | SD-JWT packages | jwt, jws, kb-jwt, sd-jwt, oid4vp |
| ISO mdoc | digital credential/document format | yes | yes | yes | yes | yes | issuer/verifier | mdoc packages | iso-mdoc, cbor, cose, oid4vci, oid4vp, haip |
| Claim | named assertion member | yes | owning artifact | yes | yes | standalone | source-dependent | standalone claim package | jwt, oauth, oidc, set, eat, sd-jwt-vc, oid4vc |
| ClaimSet | aggregate of claims | yes | owning artifact | yes | composer | payload/format model | provider | layer 50 protocol/profile | jwt, oauth, oidc, set, eat, sd-jwt-vc |
| Access token | authorization token | yes | yes | yes | yes | profile-specific | issuer/verifier | OAuth/resource-server | oauth, jwt, cwt, dpop, mtls, token-exchange |
| ID Token | authentication token | yes | replay/session | yes | yes | profile-specific | issuer/verifier | OIDC | oidc, jwt, jws, jwe |
| SET | security-event token | yes | delivery/replay | yes | yes | yes | transmitter/receiver | SET packages | set, jwt, jws, shared-signals |
| EAT | attestation evidence token | yes | evidence/result | yes | yes | yes | verifier/appraiser | EAT/RATS packages | eat, rats, jwt, cwt, cose, cbor |
| Attestation evidence | appraisal input | yes | policy-controlled | yes | yes | format-specific | verifier/appraiser | attestation packages | rats, eat, cose, x509, wallet-attestation, key-attestation |
| CoRIM | signed reference-material manifest | yes | yes | yes | yes | yes | store/trust verifier | CoRIM packages | corim, comid, coswid, cose, cbor, rats |
| CoMID | measurement/reference values | yes | yes | yes | yes | yes | reference provider | CoRIM packages | comid, corim, rats |
| X.509 certificate | public-key credential | yes | yes | yes | yes | profile structure | issuer/path/status | certificate/trust packages | x509, pkix, mtls, svid, iso-mdoc, haip |
| DID | identifier | yes | optional cache/history | yes | yes | yes | method resolver/controller | DID packages | did-core, w3c-vcdm, w3c-vp |
| DID Document | verification/service metadata | yes | optional authority/cache | yes | yes | yes | resolver/controller | DID packages | did-core |
| GNAP grant | authorization transaction | yes | yes | yes | yes | request model | grant/runtime provider | GNAP protocol | gnap |
| AuthZEN evaluation | authorization decision exchange | yes | audit-dependent | yes | yes | mapping | PDP adapter | AuthZEN protocol | authzen, xacml |
| XACML request/response | policy decision exchange | yes | audit-dependent | yes | yes | mapping | PDP/XML adapter | policy packages | xacml, authzen |

## Claim ownership rules

- `ClaimType` is a semantic family enum; `RegisteredClaim` is the concrete
  registered-name enum. Private and namespaced claims are not falsely treated
  as globally registered.
- Every concrete named claim implemented at layer 10 is a standalone package
  containing a `ClaimBase` subclass.
- Aggregate decoded structures use explicit names such as
  `EatClaimSetPayload`, `SdJwtVcClaimSetPayload`,
  `JwtSvidClaimSetPayload`, and `KeyBindingClaimSetPayload`; they are not
  individual claims.
- Layer 20 owns retrieval from databases, directories, user records, hardware,
  or external trust services. Layer 10 never owns a provider.
- Layer 50 owns revision-specific required/optional membership, aliases, wire
  names, feature flags, backwards compatibility, and migrations.

## Assurance vocabulary

- Authentication assurance uses ACR/AMR and evidence about the authentication
  event. OIDC EAP values `phr`, `phrh`, and `pop` are returned only when
  normalized authenticator evidence justifies them.
- Identity assurance uses `verified_claims`, trust-framework metadata,
  verification evidence, verification process, and verified person/entity
  claims. Ordinary stored profile fields are not promoted to verified claims.
- Credential assurance evaluates issuer trust, proof integrity, status,
  validity, schema/type, holder binding, and applicable profile constraints.
- Presentation assurance additionally evaluates verifier/request binding,
  audience, nonce, transaction, consent, replay, disclosure policy, and holder
  proof. A presentation is not a generic archive container like ASiC-E and is
  not reference material like CoRIM.

## Acceptance gates

- Exact implemented revisions are recorded and drafts are labeled as drafts.
- Every JWT-like artifact is verified under an explicit token profile.
- Key, issuer, certificate profile, and trust resolution are explicit.
- Nonce, replay, transaction, and holder/sender binding have positive and
  negative tests.
- Storage migrations upgrade and downgrade successfully.
- Package-boundary and import/export tests pass.
- Generated API contracts match runtime behavior before conformance is claimed.
- Compliance mappings reference live modules and tests.
- No active output identifies RFC 7952 as SET; SET is RFC 8417.
- Constants, models, or parsers alone never establish conformance.
- Tier 4/certification requires independent interoperability evidence.
