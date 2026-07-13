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
| 20 | credential, presentation, COSE/mdoc, wallet/key/platform attestation, EAT/RATS/CoRIM, SPIFFE/SVID, DID, SET, certificate/trust, and replaceable infrastructure providers | Environment-backed signing, verification, resolution, appraisal, delivery, trust, and explicitly named external/ephemeral storage adapters | Rename ambiguous `*-store` packages as implementation-specific providers; no canonical durable schema or transaction ownership |
| 30 | `tigrbl-identity-storage-runtime` | Executable repositories, atomic reservations, database sessions, migrations, and transaction coordinators over layer-01 state | Add durable replay repositories and exercise every repository against production database backends |
| 40 | digital credential issuance/presentation, attestation appraisal, security events, workload identity | Multi-component use-case orchestration over neutral ports, with delegated subimplementations and machine-readable capability descriptors | Complete capability inventory/readiness/dependency reporting without leaking wire formats |
| 50 | JWT, OAuth, OIDC, OID4VCI, OID4VP, HAIP, AuthZEN, GNAP, SET, EAT, SD-JWT VC | Independent version histories, revision feature gates, compatibility/migrations, protocol claim-set composition, and traceable protocol-requirement-to-capability mappings | Remove embedded state-store implementations; add normative endpoint coverage and independent interop evidence before certification |
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

## Store, capability, and protocol ownership checklist

Canonical placement rule:

```text
01 durable schema and lifecycle record
02 storage/replay/capability contract
05 reusable provider/capability base when multiple implementations exist
20 replaceable implementation provider (memory, Redis, vendor service, HSM)
30 executable durable repository, session, transaction, and atomic coordination
40 mountable/composable capability and capability-set reporting
50 versioned protocol/specification mapping onto required capabilities
```

### General store rules

- [x] Layer 01 owns canonical durable tables, fields, constraints, retention
  references, and migration state.
- [x] Layer 02 owns representation-neutral ports rather than a database or
  vendor API.
- [x] Layer 20 may own an explicitly named replaceable backend provider.
- [x] Rename every ambiguous `*-store` layer-20 package to identify its actual
  implementation, such as `*-memory-provider` or `*-redis-provider`.
- [x] Move executable SQL repositories, sessions, and transaction coordination
  to layer 30.
- [x] Ensure no layer-50 protocol package silently creates production state or
  selects a default process-local store.
- [x] Require atomic `check_and_reserve(namespace, key, expires_at)` semantics
  for replay prevention; a separate read followed by write is insufficient.
- [x] Require explicit retention, namespace, tenant, expiry, purge, audit, and
  availability semantics in every production store descriptor.

### Replay protection delivery

- [x] Layer-01 tables exist for security-event, backchannel-logout, and
  presentation replay state.
- [x] Neutral replay contracts exist in `tigrbl-identity-contracts`.
- [x] Normalize the replay contract around an atomic reservation result and a
  protocol-neutral replay namespace/key/context.
- [x] Add a layer-05 replay base only for behavior genuinely shared by at least
  two providers.
- [x] Replace `tigrbl-security-event-replay-store` with
  `tigrbl-replay-memory-provider`, retain the old distribution only as a
  deprecated compatibility alias, and document it as
  non-durable, single-process, and unsuitable for horizontally scaled
  production deployments.
- [x] Add a layer-30 SQL replay repository backed by a layer-01 table whose
  unique digest constraint is the final concurrent duplicate arbiter.
- [x] Add separately packaged layer-20 Redis/vendor replay providers only when
  their dependencies and operational semantics differ.
  No Redis/vendor backend is selected in this delivery, so no speculative
  provider package is created; the rule is enforced by provider boundaries.
- [x] Add a layer-40 `tigrbl-replay-protection-capability` package that delegates to a
  selected provider/repository and reports operations, guarantees, namespaces,
  persistence class, health, and limitations.
- [x] Map SET `jti`, DPoP proof `jti`/nonce, OIDC backchannel logout token `jti`,
  OID4VP nonce/transaction binding, and other revision-specific replay rules to
  the layer-40 capability from their layer-50 packages.
- [x] Remove `StateNonceStore`, `TokenStore`, `DPoPReplayStore`, and
  `DPoPNonceStore` as implicit production implementations inside layer 50;
  retain only injected ports or explicitly named test fixtures.

### Reference-material stores

- [x] Layer-01 attestation reference-manifest/reference-value/endorsement state
  exists.
- [x] Layer-02 reference-material provider contracts and layer-05 bases exist.
- [x] Replace `tigrbl-corim-store-provider` with the implementation-specific
  `tigrbl-corim-reference-memory-provider`; retain the former only as a
  deprecated compatibility alias.
- [x] Put durable CoRIM/CoMID reference-material repositories and immutable
  publication transactions in layer 30.
- [x] Keep trust resolution/appraisal in layers 20/40 and keep CoRIM revision,
  encoding, and protocol mapping in layer 50.

### Capability-layer contract

- [x] Every layer-40 capability has a stable capability ID and version.
- [x] Every layer-40 capability reports supported operations, guarantees,
  optional features, selected provider identities, dependencies, readiness,
  health, limitations, and explicitly unsupported behavior.
- [x] Layer-40 capabilities accept normalized contracts and do not depend on
  protocol wire names such as `jti`, `nonce`, `state`, or HTTP parameters.
- [x] A capability may delegate to multiple layer-20 providers and layer-30
  repositories without exposing those implementation details to layer 50.
- [x] Capability mounting/composition is deterministic and its effective
  capability set is inspectable at runtime.

### Protocol-layer contract

- [x] Each protocol with independent history owns a distinct layer-50 package
  and version registry.
- [x] Layer 50 owns revision feature flags, compatibility rules, and migrations.
- [x] Each normative protocol requirement maps to a stable layer-40 capability
  operation or is explicitly reported unsupported.
- [x] Layer 50 reports the selected protocol revision, required capability set,
  effective implementation coverage, and conformance evidence links.
- [x] Layer 50 owns wire decoding/encoding and protocol error mapping but not
  databases, trust-anchor selection, key loading, or production state stores.
- [x] Layer 60 selects providers and deployment policy; layer 50 must not import
  runtime settings to make hidden implementation choices.

### EAT cross-aspect status

- [x] EAT is modeled as attestation evidence containing a claim set and carried
  in a protected JWT or CWT envelope; it is not treated as one claim.
- [x] Token-envelope verification, verified attestation evidence, and appraisal
  results are distinct contracts.
- [x] Claim, claim-set, token, evidence-verification, and appraisal bases exist.
- [x] EAT JWT and EAT CWT/COSE extension bases exist symmetrically.
- [x] `tigrbl-eat-concrete` specializes neutral `AttestationEvidence` without
  owning key resolution, trust selection, persistence, or appraisal.
- [x] The EAT verifier returns evidence-integrity verification separately from
  the reference-backed attestation appraisal decision.

### Verification snapshot (2026-07-12)

- [x] EAT cross-aspect contracts, bases, concrete specialization, JWT/CWT
  envelope symmetry, provider verification, and appraisal separation are
  implemented and covered by unit tests.
- [x] The complete unit suite passes: 1,078 tests.
- [x] Layer-boundary enforcement passes for the layered package tree.
- [x] SQLite and PostgreSQL migration upgrade/downgrade/reapply portability is
  preserved in validated-run evidence.
- [x] Artifact-to-route, route-to-contract, and runtime-plan-to-discovery truth
  checks pass.
- [x] RP state/token memory stores and DPoP replay/nonce memory stores are
  injected through neutral ports; explicit process-local implementations live
  in `tigrbl-replay-memory-provider`, and layer 60 selects them deliberately.
- [x] Layer-50 protocol packages consume the neutral injected protocol-settings
  proxy; layer 60 binds deployment settings and no layer-50 module imports the
  runtime settings module.
- [x] Layer-40 capability metadata is complete and operator-inspectable through
  the shared capability report, including bindings and delegated operations.
- [x] Every versioned layer-50 protocol/profile reports its selected revision,
  feature-derived normative requirements, stable capability mappings,
  effective coverage, explicit unsupported behavior, and conformance evidence
  links.

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
