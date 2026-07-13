# Layered identity migration and refactoring plan

Status: active implementation plan. This document describes target ownership and
delivery order; it is not certification evidence. Generated compliance reports
remain authoritative for conformance claims.

## 1. Target architecture

The ownership/composition direction is:

```text
00 primitives -> 01 durable schemas -> 30 durable Tigrbl table runtimes ---+
                                                                           |
00 primitives -> 02 semantic contracts -> 05 reusable behavioral bases    |
  -> 10 deterministic concrete objects -----------------------------------+
  -> 20 environment-backed providers -------------------------------------+
                                                                           |
                                      40 mountable capabilities <----------+
                                        -> 50 versioned protocols/profiles
  -> 60 runtime composition
  -> 70 public facade
  -> 80 HTTP/API products
  -> 90 reusable UIX core
  -> 95 product UIX applications and browser SDKs
```

Required ownership rules:

- Layer 01 defines tables, columns, relationships, constraints, indexes, and
  migrations. It does not define executable operations, hooks, HTTP routes,
  password verification, token logic, or use cases.
- Layer 02 defines immutable semantic values, requests, results, ports, and
  errors. It has no Tigrbl, SQLAlchemy, HTTP, cryptography, or provider imports.
- Layer 05 contains reusable abstract behavior only where multiple concrete or
  provider implementations share an extension point.
- Layer 10 contains deterministic, environment-free implementations. Each
  concrete identity, credential, and claim class has a standalone package.
- Layer 20 contains environment-backed implementations: keys, cryptography,
  trust lookup, clocks when externally governed, platform APIs, network clients,
  and vendor integrations. It does not own durable database tables.
- Layer 30 constructs executable Tigrbl table specifications with `make`,
  `define`, `derive`, and factories. It owns durable operations and hooks, but
  not protocol semantics or HTTP routes. It does not introduce repository or
  unit-of-work abstractions.
- Layer 40 exposes typed, reportable capabilities that compose/delegate to
  layer-10 algorithms, layer-20 providers, and layer-30 table operations.
- Layer 50 owns specification versions, feature matrices, compatibility,
  migration/upgrade rules, protocol claim sets, wire schemas, and protocol
  bindings. A specification with an independent version history gets its own
  package.
- Layers 60/70/80 compose, export, and mount lower-layer truth. They do not
  reimplement standards.

## 2. Completed checkpoints

- [x] `9e3d33e9` replaces parallel capability metadata/binding declarations with
  `CapabilityDefinition` and a single `CapabilityOperation` registry.
- [x] `170c17e8` introduces the layer-30 `make`/`define`/`derive`/factory surface.
- [x] `57104140` removes repository/store abstractions from the new layer-30
  table runtime.
- [x] `86af2a62` activates derived table operations on canonical models.
- [x] `383b5e0a` moves graph algorithms to layer 10 while leaving durable graph
  state construction in layer 30.
- [x] `608fd321` activates table runtimes during layer-60 startup.
- [x] `a5a7cdee` moves RBAC, ABAC, and delegated-administration mutations from
  layer 01 to layer 30.
- [x] `a8f124a5` moves OIDC back-channel logout replay mutation to layer 30.
- [x] `91d8be07` moves authorization-code persistence, client-registration
  upsert, and token-revocation ledger operations to layer 30.
- [x] `a50e6f68` moves session, consent, and logout-state mutations to layer 30
  and preserves member/collection arity in runtime operation construction.
- [x] `c7b0b5de` moves token-record persistence, rotation, family revocation, and
  introspection to a profiled layer-30 runtime family.
- [x] `6a03a8ba` and `f683cc2f` add shared-secret providers and composable
  password/client-secret authentication capabilities.
- [x] `89330723` routes runtime secret verification through those capabilities,
  and `1766a361` removes client-model authentication behavior.
- [x] `99e5b01`, `8994e5b8`, `5a7bbf1c`, and `85eb0d4f` move delegation,
  device-code, crypto-key, and audit lifecycles into layer-30 table runtimes.
- [x] `b5e74c46` centralizes durable handler execution in layer 30, and
  `952eefb8` makes the deprecated persistence facade delegate through runtime
  operation contexts.
- [x] `fb6be510` moves My Account session DTOs and HTTP handlers to the
  layer-80 My Account API package and leaves `AuthSession` as a mapped record.
- [x] `25815389` moves the remaining My Account profile, credential, consent,
  and route-composition HTTP surfaces into the layer-80 product; layer 30 now
  retains only the durable consent operations consumed by those routes.
- [x] Claim primitives, contracts, bases, `ClaimType`, `ClaimValueType`,
  `ClaimNameKind`, and standalone concrete claim packages exist.
- [x] Protocol-neutral scope matching exists as
  `tigrbl-authorization-scope-set-matcher-concrete`; the old OAuth package is a
  compatibility facade.
- [x] Protocol-neutral public and pairwise subject identifier strategies exist;
  the old OIDC package is a compatibility facade.
- [x] EAT is split into deterministic claim/evidence parsing at layer 10 and an
  integrity-verifying evidence provider at layer 20.

## 3. Layer 00: primitives

Owner: `pkgs/00-primitives/tigrbl-identity-core`.

### Retain and finish

- `artifacts.py`: `ArtifactKind`, `CredentialFormat`, `TokenKind`,
  `PresentationKind`, `AttestationKind`, `ManifestKind`,
  `VerificationOutcome`, and lifecycle values.
- `claims.py` or its current equivalent: `ClaimType`, `ClaimValueType`, and
  `ClaimNameKind`. These classify semantics; they must not enumerate every
  registered protocol claim name.
- `identifiers.py`/`primitives.py`: opaque IDs and references for identity,
  principal, credential, token, presentation, attestation, manifest,
  certificate, wallet, workload, trust domain, status list, transaction, and
  key.
- `protocol_tags.py`: canonical tags and aliases, including `oauth`, `oidc`,
  `authzen`, `xacml`, `did-core`, `oid4vci`, `oid4vp`, `w3c-vcdm`, `w3c-vp`,
  `sd-jwt`, `sd-jwt-vc`, `kb-jwt`, `iso-mdoc`, `haip`, `jwt`, `jws`, `jwe`,
  `jose`, `cwt`, `cose`, `cbor`, `x509`, `spiffe`, `svid`, `rats`, `eat`,
  `corim`, `comid`, `coswid`, `set`, `shared-signals`, `gnap`, `zta`,
  `webauthn`, `fido`, `dpop`, `pkce`, `rar`, `token-exchange`, and
  `identity-assurance`.
- `clock.py`: `utc_now()` and `utc_now_iso()`. Remove private `_utc_now` helpers
  from higher layers when no special clock semantics are required.
- `identifiers.py`: add a generic prefixed opaque-ID constructor if `_new_id`
  continues to appear in capabilities. Capability packages must request typed
  IDs rather than concatenate prefixes themselves.
- `versions.py`: version ordering and range checks used by layer-50 feature
  matrices.

### Prohibited

- Protocol request/response models, Pydantic, SQL, HTTP, crypto libraries,
  network access, trust resolution, issuer/verifier policy, and persistence.

## 4. Layer 01: durable schemas only

Owner: `pkgs/01-storage/tigrbl-identity-storage`.

### Keep

- `tables/**/_table.py`: mapped classes, constraints, relationships, schema
  names, indexes, column defaults that are truly storage defaults, and simple
  property accessors with no external dependencies.
- `migrations/versions/*.py`: schema creation and reversible migrations.
- Table registry/inventory metadata.

### Move to layer 30

The following remaining executable symbols must be removed from layer 01 after
equivalent runtime specs are active:

| Layer-01 source | Symbols to migrate | Layer-30 destination |
|---|---|---|
| `tables/delegation_grant/_table.py` | grant CRUD/transitions, edge linking, child deactivation, provenance, token links | `ops/delegation.py`, `tables/delegation.py` |
| `tables/device_code/_hooks.py` | approve/deny hooks | `hooks/device_code.py`, `tables/oauth.py` |
| `tables/crypto_key/_hooks.py` | normalization, primary-version seed, enabled check | `hooks/keys.py`, `tables/keys.py` |
| `tables/client/_table.py` | durable enable/disable/rotate operations | `ops/clients.py`, `tables/clients.py` |
| `tables/user/_table.py` | durable lookup operation | `ops/identities.py`, `tables/identities.py` |
| `tables/audit_event/__init__.py` | append/list wrappers | `ops/audit.py`, `tables/audit.py` |
| `tables/_ops.py` | generic table handler calls | consolidate into layer-30 `ops/common.py` |
| `tables/engine.py` | runtime engine/provider/session resolution | layer-30 engine/session composition |

Completed moves already removed executable operations from
`attribute_policy`, `delegated_admin_scope`, `tenant_membership`,
`backchannel_logout_replay`, `auth_code`, `client_registration`,
`revoked_token`, `auth_session`, `consent`, `logout_state`, and `token_record`
table modules.

### Move out of storage entirely

- `tables/auth_session/_table.py` account router and session HTTP handlers ->
  `pkgs/80-apis/tigrbl-auth-api-my-account`.
- `tables/realm/_table.py` admin router and realm/tenant HTTP handlers -> the
  appropriate layer-80 admin API package.
- `tables/user/_admin_identity_route.py` -> layer-80 admin API.
- `tables/user/_account_route.py` -> `tigrbl-auth-api-my-account`.
- Password and client-secret hashing/verification imports -> layer-20
  authenticator providers.
- `_persistence_extended.py` and `persistence.py` lifecycle/use-case facades ->
  layer-30 table runtimes or layer-40 capabilities. Leave one-release warning
  re-exports only after all internal callers migrate.
- `framework.py` must stop being a route/runtime dependency barrel. Split
  storage-safe mapped-table imports from runtime/API imports, then remove the
  higher-layer exports.

### Migrations

- Add schema migrations only when the model shape changes. Moving an operation
  between layers does not receive a database migration.
- Preserve existing table names, schemas, constraints, and migration revision
  identifiers during ownership moves.
- Every new credential, presentation, attestation, event, workload, DID, GNAP,
  and certificate table must have upgrade and downgrade tests.

## 5. Layer 02: contracts

Primary owners:

- `pkgs/02-contracts/tigrbl-identity-contracts`
- `pkgs/02-contracts/tigrbl-security-trust-contracts`

### Claims

Retain and finish `tigrbl_identity_contracts.claims`:

- `Claim`, `ClaimSet`, `ClaimDescriptor`, `ClaimProvenance`,
  `ClaimDisclosure`, `ClaimsRequest`, `ClaimsResult`.
- `ClaimValidatorPort`, `ClaimsProviderPort`, and `ClaimSetComposerPort`.
- `ClaimSet` is the ordered/validated collection; do not use bare
  `list[dict[str, Any]]` across package boundaries.
- A concrete claim class belongs in layer 10, not layer 02.

### Attestation/token/evidence separation

- `attestation/evidence.py`: `AttestationEvidence` and
  `VerifiedAttestationEvidence`.
- `attestation/results.py`: appraisal and evidence-verification results.
- `attestation/manifests.py`, `reference_values.py`, `endorsements.py`, and
  `appraisal.py`: reference material contracts.
- `tokens.py`: `ProtectedTokenEnvelope`, `VerifiedTokenEnvelope`,
  `TokenEnvelopeFormat`, `TokenProfile`, and profiled verification requests.
- An EAT instance is modeled as protected JWT/CWT token envelope carrying an
  EAT claim set and serving as attestation evidence. These are compositional
  facets, not inheritance aliases.
- `VerifiedAttestationEvidence` must contain a `VerifiedTokenEnvelope`; raw
  claims alone never prove integrity.

### Other contract families

- Digital credentials: issuance, presentations, status, assurance,
  verification, wallets, holder/transaction binding.
- Workloads: SPIFFE IDs, SVIDs, selectors, bundles, and provider/verifier ports.
- Security events: events, subjects, subscriptions, delivery, receiver and
  transmitter ports.
- DID: identifiers, documents, verification methods, services, resolution and
  dereferencing ports.
- Policy: representation-neutral AuthZEN/XACML entities, evaluations, search,
  capabilities, decisions, obligations, and advice.
- Delegation: actor chains, grants, attenuation constraints, proofs, and
  capability/delegation ports.
- Trust: certificate profiles, path validation, trust anchors, status,
  verification keys, and issuer trust.

## 6. Layer 05: bases

### Consolidate protocol-neutral bases

- Move reusable behavior from `tigrbl-oauth-bases` and `tigrbl-oidc-bases` into
  domain owners where the abstraction is not inherently protocol-specific:
  - claim composition/validation -> `tigrbl-identity-claims-bases`;
  - subject identifier strategy -> an identity-identifier base package;
  - authorization scope matching -> an authorization-scope base package;
  - profiled token verification -> `tigrbl-token-bases`;
  - authentication assurance evaluation ->
    `tigrbl-authentication-assurance-bases`.
- Keep an OAuth/OIDC base only when its method contract is defined by that
  protocol and has multiple implementations.

### EAT facets

- `tigrbl-token-bases`: protected token-envelope verification.
- `tigrbl-jose-bases`: EAT JWT coding only.
- `tigrbl-cose-bases`: EAT CWT coding only.
- `tigrbl-attestation-bases`: evidence verification, appraisal, reference
  material, and manifest behavior.
- `tigrbl-identity-claims-bases`: `ClaimBase` and claim-set composition.
- Do not create an `EatBase` that conflates all four facets.

### Base-class gate

Add a base only when two implementations share behavior or a provider contract
needs a stable extension point. Data objects do not receive ceremonial bases.

## 7. Layer 10: deterministic concrete packages

### Claim family

- Keep one distributable `tigrbl-claim-<name>-concrete` package per concrete
  claim class.
- Every class subclasses `ClaimBase` and declares canonical name/label,
  `ClaimType`, `ClaimValueType`, and name kind.
- Protocol packages assemble claim sets; standalone claim packages do not
  import layer 50.
- Remove the duplicate `tigrbl-claim-access-token-hash-oidc-concrete` after
  migrating consumers to the protocol-neutral access-token-hash class unless
  it encodes genuinely different semantics.
- Split remaining classes in `tigrbl-oidc-claims-concrete` into standalone,
  protocol-neutral packages. Convert the old package to a deprecation-only
  facade, then remove it after one release boundary.
- EAP ACR/AMR values belong to protocol/profile assembly at layer 50; their
  generic evidence evaluation belongs to authentication-assurance layer 10.

### Scope matcher rename

- Canonical package: `tigrbl-authorization-scope-set-matcher-concrete`.
- Canonical class: `ScopeSetMatcher`.
- Remove `DefaultScopeMatcher`; “default” is composition policy, not a concrete
  algorithm identity.
- Keep `tigrbl-oauth-scope-matcher` as a warning facade for one release; update
  all imports and root workspace metadata, then delete it.

### Subject strategy rename

- Canonical packages:
  `tigrbl-public-subject-identifier-concrete` and
  `tigrbl-pairwise-subject-identifier-concrete`.
- Canonical classes: `PublicSubjectIdentifierStrategy` and
  `PairwiseSubjectIdentifierStrategy`.
- Update `tigrbl-security-subject-pairwise-provider` and protocol imports.
- Keep `tigrbl-oidc-subject-strategy` as a warning facade for one release, then
  remove package, workspace entries, and lockfile records.

### EAT

- `tigrbl-eat-concrete/claims.py`: deterministic claim-set parsing.
- `profiles.py`: exact RFC/draft revision and profile identifiers.
- `submodules.py`: nested EAT submodule parsing.
- `evidence.py`: conversion to the representation-neutral evidence contract;
  no signature/trust claim.
- `validation.py`: structural and profile validation only.
- Keep individual EAT claims in standalone claim packages.
- No cryptographic validity, trust lookup, appraiser policy, network, or
  persistence in this package.

### Other concrete families

- Keep deterministic JOSE in `tigrbl-jose-concrete`.
- Keep SD-JWT, SD-JWT VC, mdoc, VCDM, CoRIM, SVID, DID, SET, identities, and
  credentials in their standalone layer-10 owners.
- Every concrete credential and identity class remains a standalone package.
- Exact draft/RFC/ISO revision constants must be exported and tested.

## 8. Layer 20: providers

### Provider responsibilities

- Environment-backed key loading/signing, HSM/cloud interaction, trust
  resolution, network clients, platform APIs, external clocks, vendor evidence,
  and policy-backed verification.
- Providers consume layer-02 ports and layer-10 deterministic behavior.
- Providers never own database table schemas or generic durable stores.

### Required corrections

- `tigrbl-eat-verifier-provider` must verify protected JWT/CWT integrity before
  returning `VerifiedAttestationEvidence`; then appraisers may evaluate claims
  against reference material.
- Split password/client-secret hashing out of `tigrbl-identity-jose` into the
  appropriate authenticator providers; JOSE is not password hashing.
- Update client/user call sites to provider ports instead of model methods.
- Replay memory remains a layer-20 provider because it is an environment-backed
  ephemeral implementation. Durable replay tables and operations remain in
  layers 01/30.
- Remove any package named `*-store-provider` when it merely wraps local SQL
  tables; use layer-30 operations. A remote vendor store client may remain a
  provider if it implements a layer-02 port.
- Certificate validation must require an explicit profile (`generic-pkix`,
  `oauth-mtls`, `x509-svid`, `mdoc-issuer`, `mdoc-reader`, `haip-issuer`,
  `haip-verifier`, `wallet-attestation`, or `eat-endorsement`).

## 9. Layer 30: durable Tigrbl table runtime

Owner: `pkgs/30-storage-runtime/tigrbl-identity-storage-runtime`.

### Canonical module shape

```text
src/tigrbl_identity_storage_runtime/
  make.py          # makeRuntimeOperation
  define.py        # reusable TableSpec definition classes
  derive.py        # overlay runtime specs on layer-01 models
  factories.py     # family factories
  inventory.py     # table/spec/operation indexes
  initialize.py    # explicit runtime activation
  ops/             # carrier-neutral durable operation bodies
  hooks/           # durable lifecycle hooks
  tables/          # one runtime spec module per table family
```

### Operation authoring rules

- An operation is created once with `makeRuntimeOperation`; its alias, handler,
  transaction scope, schemas, hooks, and owner metadata are one definition.
- `deriveRuntimeTableSpec` overlays it on the canonical layer-01 model.
- `initializeIdentityRuntimeTables` activates selected specs at composition
  time. Importing layer 01 must not activate runtime behavior.
- Operation bodies call canonical Tigrbl handlers through `ops/common.py`.
- Preserve alias, arity/target semantics, input materialization, response shape,
  transaction boundary, error behavior, and lifecycle hook order.
- Do not parse HTTP requests, choose protocol responses, load trust roots, or
  open network connections.

### Remaining runtime families

1. Sessions and OIDC logout.
2. Consent lifecycle.
3. Delegation grants, edges, proofs, and token links.
4. Token records and refresh-family rotation/reuse rejection.
5. Device-code approve/deny hooks.
6. Key/key-version normalization and lifecycle hooks.
7. Client/user durable lookup and state mutation.
8. Audit append/query operations.
9. Engine/session construction currently embedded in layer 01.

### Remove

- `Repository`, `Store`, and `UnitOfWork` classes.
- Protocol package imports from layer 30.
- Layer-60 server imports from operation bodies.
- HTTP routers and API response types.
- Deprecated layer-01 persistence imports after the compatibility window.

## 10. Layer 40: mountable capabilities

### Capability model

- `CapabilityDefinition`: `capability_id` and version only.
- `CapabilityOperation`: target plus required/optional and delegated state.
- `CapabilityState`: effective readiness and operation availability derived from
  the operation registry; a missing required target raises `NotImplementedError`
  during construction/validation.
- Remove guarantees, optional-features, limitations, unsupported,
  implementation, and free-standing dependency tuples.
- Capability reports derive operation names from the registry; there is no
  second literal operation list.

### Capability package behavior

- A capability composes/delegates to layer-10 algorithms, layer-20 providers,
  and layer-30 table operations.
- It can report its effective operation set and readiness without knowing HTTP
  or protocol wire syntax.
- It may subcall other capabilities through typed operations.
- It does not own protocol versions or mount routes.

### Required capability owners

- `tigrbl-digital-credential-issuance`
- `tigrbl-digital-credential-presentation`
- `tigrbl-attestation-appraisal`
- `tigrbl-security-events`
- `tigrbl-workload-identity`
- `tigrbl-replay-protection-capability`
- identity administration/control-plane capabilities
- protocol-artifact processing, with explicit token/credential/attestation
  profile dispatch.

HAIP composition belongs here: a HAIP issuer/verifier is a configured
credential/presentation capability meeting the profile’s required formats,
algorithms, trust, holder binding, and transaction behavior.

## 11. Layer 50: protocols, standards, and profiles

### Package rule

Each independently versioned specification/profile owns a separate layer-50
package with:

```text
versions.py       # supported/current/deprecated versions
features.py       # feature availability by version
compatibility.py  # backwards compatibility and negotiation
migrations.py     # request/config/metadata upgrades where possible
claims.py         # protocol claim-set assembly
schemas.py        # wire request/response models
bindings.py       # maps protocol actions to capability operations
errors.py         # protocol error mapping
```

### Existing/required packages

- OAuth, OIDC, JWT, CWT, RP/resource-server, AuthZEN, GNAP.
- OID4VCI and OID4VP.
- HAIP profile.
- SD-JWT VC profile.
- EAT and CoRIM attestation protocols.
- SET security-event protocol.

### Protocol responsibilities

- Import and configure protocol-neutral layer-10 and layer-20 packages.
- Import layer-40 capabilities and map their typed operations to the protocol.
- Assemble protocol claim sets from standalone claim packages.
- Record exact specification revision/status and expose feature flags by
  version.
- Own backward compatibility, wire migration, discovery/metadata, error codes,
  token profiles, nonce/replay semantics, and protocol-specific trust profiles.

### OIDC corrections

- EAP ACR values `phr`, `phrh`, and `pop` are owned and exported by OIDC/EAP
  profile modules, while evidence evaluation remains protocol-neutral below.
- Identity Assurance owns `verified_claims`, evidence/framework metadata, and
  its registered claims. Ordinary stored profile fields must never become
  `verified_claims` without evidence.
- OIDC protocol packages re-export selected stable claim/subject/scope APIs;
  they do not own their deterministic implementations.

## 12. Layers 60, 70, 80, 90, and 95

### Layer 60 runtime

- Select providers and capabilities.
- Activate layer-30 table runtime specs.
- Configure layer-50 protocol versions/features.
- Supply engine, sessions, keys, clocks, trust, and settings.
- Remove business logic and protocol algorithms from server modules.

### Layer 70 facade

- Re-export stable public APIs only.
- Maintain one-release deprecation aliases with warnings and removal dates.
- Do not trigger table activation or application startup on import.

### Layer 80 APIs

- Move account/admin routers out of layer 01.
- Mount layer-50 bindings and layer-40 capabilities.
- Translate HTTP authentication/context into typed calls and typed results into
  HTTP responses.
- Keep API schemas aligned with actual runtime handlers and generated OpenAPI.

### Layer 90 UIX core

- `pkgs/90-uix-core/uix-core` owns browser-safe, reusable React layout,
  authentication, API-client, form, table, and feedback primitives.
- It does not own product routes, protocol algorithms, server-side secrets, or
  durable state.

### Layer 95 product UIX

- `pkgs/95-ui/*` composes product-specific browser applications and SDKs from
  layer-90 UIX primitives and layer-80 API contracts.
- Each UIX package advertises only operations actually mounted by its paired
  API surface. Deployment manifests remain in their existing workspace owners;
  layer 95 is not the generic deployment/distribution layer.

## 13. Call-site migration order

For every moved symbol:

1. Add the new owner implementation and focused positive/negative tests.
2. Add a derived runtime spec or capability/protocol binding.
3. Activate it explicitly from layer 60.
4. Migrate internal imports and calls to the new owner.
5. Add a compatibility re-export at the old public path only when external
   compatibility is required.
6. Add a boundary test proving the old layer no longer contains the behavior.
7. Remove the old implementation and duplicate declarations.
8. Update package metadata, workspace editable sources, dependency-boundary
   expectations, lockfile, docs, compliance mappings, and facade exports.
9. Remove the compatibility package after one release boundary.

No compatibility alias may preserve an incorrect standards claim (for example,
SET as RFC 7952). Such errors are removed immediately, with configuration-only
migration warnings if necessary.

## 14. Verification and acceptance gates

Every checkpoint must pass:

- focused unit tests for new deterministic/provider/runtime behavior;
- positive and negative schema/claim tests;
- package-boundary and forbidden-import tests;
- runtime activation and product startup tests;
- operation equivalence tests for alias, target, schemas, lifecycle order,
  output envelope, errors, and transaction behavior;
- migration upgrade/downgrade tests when schemas change;
- nonce/replay and duplicate/reservation tests where relevant;
- explicit token profile and issuer/key/trust resolution tests for every
  JWT/CWT-like artifact;
- generated OpenAPI/OpenRPC equivalence where wire surfaces move;
- `ruff`, `git diff --check`, package import/export tests, and lock consistency;
- live compliance mappings to implementations and tests.

Certification is not granted from constants, models, or self-reported feature
flags. Tier-4 claims require independent interoperability evidence.

## 15. Delivery sequence

- [x] C0: capability operation definition correction.
- [x] C1: layer-30 Tigrbl construction/activation foundation.
- [x] C2: graph algorithm/runtime split.
- [ ] C3: finish all durable operations/hooks out of layer 01.
- [ ] C4: remove route/runtime/provider imports from layer 01 and move routers
  to layer 80.
- [ ] C5: finish claim package/facade cleanup and remove protocol-specific
  deterministic package names.
- [ ] C6: finish EAT token/evidence/appraisal/provider verification chain.
- [ ] C7: normalize bases and provider ownership, including password/client
  secret services.
- [ ] C8: make every layer-40 feature composable, delegated, and reportable.
- [ ] C9: complete per-specification layer-50 version/feature/compatibility and
  migration matrices.
- [ ] C10: update runtime/facade/API/app/deployment compositions.
- [ ] C11: remove compatibility packages after their release boundary.
- [ ] C12: full boundary, conformance, security-negative, migration, and
  interoperability audit.

## 16. Change notation and non-negotiable invariants

The file ledger below uses these actions:

- **ADD**: create a new owner or proof surface.
- **UPDATE**: retain the file and change its implementation or exports.
- **MOVE**: copy behavior to its correct owner, migrate callers, then delete the
  source behavior.
- **FACADE**: retain only warning re-exports for one published release.
- **REMOVE**: delete after all internal imports and compatibility commitments
  are satisfied.

Every moved operation must preserve the following equivalence contract:

1. the same semantic operation alias and collection/member arity;
2. the same request materialization and normalized typed input;
3. the same pre-handler, handler, persistence, and post-handler order;
4. the same transaction/commit/rollback boundary;
5. the same successful result and public error envelope;
6. the same replay, idempotency, and concurrency behavior;
7. the same protocol binding unless a separately reviewed protocol change is
   intentionally included.

The target import graph is enforced, not merely documented:

```text
00 -> 01 -> 30 ----------------+
                                 +-> 40 -> 50 -> 60 -> 70 -> 80 -> 90 -> 95
00 -> 02 -> 05 -> 10 ----------+
                 -> 20 --------+
```

Layer 20 may consume layer-01 mapped value types only when the provider is
explicitly an adapter for that type; it must not call table handlers, `_ops`,
sessions, or durable mutations. Durable reads and writes are injected from
layer 30 into layer-40 capabilities. Layer 50 calls capabilities, not layer-30
routers or persistence singletons.

## 17. C3: complete the layer-01 to layer-30 durable-runtime migration

### 17.1 Client records and client-secret lifecycle

| Action | File | Required change |
|---|---|---|
| ADD | `pkgs/30-storage-runtime/tigrbl-identity-storage-runtime/src/tigrbl_identity_storage_runtime/ops/clients.py` | Implement `lookup_client`, `set_client_enabled`, and `replace_client_secret_hash` using the common layer-30 table operations. The operation accepts an already-produced digest; it never hashes or verifies a secret. |
| ADD | `pkgs/30-storage-runtime/tigrbl-identity-storage-runtime/src/tigrbl_identity_storage_runtime/tables/clients.py` | Define `ClientRuntimeSpec` with aliases `lookup_client`, `enable`, `disable`, and `rotate_secret_hash`; preserve collection/member arity and read-only versus read-write transaction scope. |
| UPDATE | `.../tables/__init__.py`, `.../ops/__init__.py` | Export and activate the client runtime family. |
| UPDATE | `.../inventory.py` | Ensure the derived `ClientRuntimeSpec` is indexed by table and operation alias. Do not derive a second mapped class. |
| MOVE | `pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/client/_table.py` | Remove `verify_secret`, `rotate_secret`, `enable`, `disable`, `authenticate`, `op_ctx`, `_ops`, and `tigrbl_identity_jose` imports. Retain mapped fields, relationship, `_CLIENT_ID_RE`, and schema metadata. |
| UPDATE | `.../introspection.py`, `.../token_request.py` | Replace `client.verify_secret(...)` with an injected client-secret verification port; replace direct client lookup with the layer-30 operation. |
| UPDATE | tests and examples currently calling `Client.new(...)` | Use a provider-backed client-record factory that hashes before invoking the layer-30 create operation. Do not restore `Client.new` on the mapped model. |

The replacement call chain is:

```text
layer-50 token/introspection binding
  -> layer-40 ClientAuthenticationCapability.authenticate(request)
  -> layer-30 lookup_client(client_id, db)
  -> layer-20 ClientSecretLocalAuthenticator.verify(presented, stored_hash)
  -> typed ClientAuthenticationResult
```

### 17.2 User lookup and password lifecycle

| Action | File | Required change |
|---|---|---|
| ADD | `.../ops/identities.py` | Implement `lookup_identity_by_identifier`, `replace_password_hash`, `set_identity_enabled`, and password-reset state mutations. Reads filter active records and preserve username/email lookup semantics. |
| ADD | `.../tables/identities.py` | Define and derive `UserRuntimeSpec`; attach aliases without HTTP bindings. |
| MOVE | `pkgs/01-storage/.../tables/user/_table.py` | Remove request/response models, `TigrblRouter`, route imports, static route method attachment, `verify_password`, `lookup_by_identifier`, `op_ctx`, and JOSE password imports. Keep mapped columns, relationships, passive `roles`/`scopes` projections, and bootstrap identifiers. |
| MOVE | `pkgs/01-storage/.../tables/user/_account_route.py` | Move HTTP schemas and handlers to `pkgs/80-apis/tigrbl-auth-api-my-account/src/tigrbl_auth_api_my_account/identities.py`; call the password-authentication capability and identity runtime operations. |
| MOVE | `pkgs/01-storage/.../tables/user/_admin_identity_route.py` | Move to the appropriate tenant/platform admin API modules; delegate mutations to the identity-administration capability. |
| UPDATE | `.../login.py`, `pkgs/60-runtime/tigrbl-identity-server/src/tigrbl_identity_server/admin_auth.py` | Replace `row.verify_password(...)` with `PasswordAuthenticationCapability.authenticate(...)`. |
| UPDATE | bootstrap composition | Hash the initial superuser password through the configured password provider during bootstrap. `User.DEFAULT_ROWS` must not execute provider cryptography at import time. |
| REMOVE | old route files and layer-01 route exports | Delete only after OpenAPI equivalence and UI/API integration tests pass. |

### 17.3 Delegation-grant lifecycle

| Action | File | Required change |
|---|---|---|
| ADD | `.../ops/delegation.py` | Move `_create`, `_list`, `_read`, `_update`, `_create_grant`, transitions, recursive revoke, edge deactivation, provenance persistence, and token-link operations. Replace recursive dynamically attached model calls with direct local operation calls sharing one transaction. |
| ADD | `.../tables/delegation.py` | Define runtime specs for `DelegationGrant`, `DelegationGrantEdge`, `DelegationGrantProof`, and `DelegationGrantTokenLink`. Preserve aliases `create_grant`, `inspect_grant`, `list_grants`, `activate_grant`, `expire_grant`, `replace_grant`, `revoke_grant`, `link_edge`, `deactivate_children`, `persist_provenance`, `link_token`, and `list_for_grant`. |
| UPDATE | `.../tables/__init__.py`, `.../ops/__init__.py` | Export and include all four specs in `DURABLE_RUNTIME_TABLE_SPECS`. |
| MOVE | `pkgs/01-storage/.../tables/delegation_grant/_table.py` | Retain only mapped table classes, a storage-domain terminal-status invariant if needed, and the compatibility type alias. Remove helpers, operations, `op_ctx`, and runtime imports. |
| UPDATE | delegation providers/capabilities/protocol callers | Invoke typed delegation capability operations; no caller should call attached table methods directly. |

Add transaction tests proving replacement and recursive revocation are atomic,
descendants are collapsed once, terminal grants are not re-revoked, and token
links/provenance remain queryable.

### 17.4 Device-code and crypto-key hooks

| Action | File | Required change |
|---|---|---|
| ADD | `.../hooks/device_codes.py` | Move `approve_device_code` and `deny_device_code`; keep `HANDLER` stage, input identity rules, and default denial reason. |
| UPDATE | `.../tables/oauth.py` | Attach hooks to a derived `DeviceCodeRuntimeSpec` and include approve/deny operations if not already materialized by the canonical table spec. |
| REMOVE | `pkgs/01-storage/.../tables/device_code/_hooks.py` | Delete after hook-order equivalence tests pass; remove its imports/exports from `_table.py`. |
| ADD | `.../hooks/keys.py` | Move `normalize_key_usage_policy`, `seed_primary_key_version`, and `ensure_key_enabled`; retain PRE/POST stage ordering. |
| ADD | `.../tables/keys.py` | Derive `CryptoKeyRuntimeSpec` and `CryptoKeyVersionRuntimeSpec`; attach hooks to create/update/rotate operations. |
| MOVE | `pkgs/01-storage/.../tables/crypto_key/_usage.py` | Move deterministic normalization to a layer-10 key-policy concrete owner if used outside persistence; otherwise keep only a storage enum/value mapping. |
| REMOVE | `pkgs/01-storage/.../tables/crypto_key/_hooks.py` | Delete after primary-version idempotency, disabled-key rejection, and lifecycle-order tests pass. |

`scrub_key_material` belongs in the layer-20 key provider/serialization boundary,
not a durable hook. Layer 30 persists only already-separated public material and
opaque provider references.

### 17.5 Audit, engine, and generic storage helpers

| Action | File | Required change |
|---|---|---|
| ADD/UPDATE | `.../ops/audit.py`, `.../tables/audit.py` | Own append/list/filter operations and a typed audit-recorder adapter. |
| MOVE | `pkgs/01-storage/.../tables/audit_event/__init__.py` | Retain table export only; remove executable append/list wrappers. |
| UPDATE | `.../ops/common.py` | Become the only local adapter around canonical Tigrbl create/read/list/update/delete cores. Keep input/output unwrapping tested and private to layer 30. |
| REMOVE | `pkgs/01-storage/.../tables/_ops.py` | Migrate all callers, including provider packages, then delete. |
| MOVE | `pkgs/01-storage/.../tables/engine.py` | Move engine/session construction to layer-60 composition and layer-30 initialization. Layer 01 exposes mapped metadata only. |
| UPDATE/REMOVE | `pkgs/01-storage/.../framework.py` | Remove `TigrblApp`, `TigrblRouter`, `op_ctx`, `hook_ctx`, engine/session, and API imports. Retain a storage-safe barrel only if mapped tables still need it; otherwise import the framework owners directly and delete it. |
| FACADE | `pkgs/01-storage/.../persistence.py`, `_persistence_extended.py` | Warn and delegate to layer-30 operations for one release; prohibit new imports; then remove. |

No database migration is created for sections 17.1-17.5 unless a mapped column,
constraint, index, or relationship changes.

## 18. C4/C7: secret providers and authentication composition

### 18.1 New protocol-neutral contracts and provider

| Action | File/package | Required change |
|---|---|---|
| ADD | `pkgs/02-contracts/tigrbl-identity-contracts/src/tigrbl_identity_contracts/shared_secrets.py` | Define `SecretHash`, `SecretHashingPort.hash_secret`, `SecretVerificationPort.verify_secret`, `SecretHashPolicy`, and a typed verification result/error. The contract carries encoded bytes/string without choosing bcrypt/PBKDF2. |
| UPDATE | `.../authenticators.py` and package `__init__.py` | Reference the shared-secret ports from password/client-secret authenticator contracts and export them. |
| UPDATE | `pkgs/05-bases/tigrbl-identity-authenticator-bases/.../mixins.py` | Make `SecretVerifierMixin` an adapter over an injected `SecretVerificationPort`, or remove it if it remains a method that only raises `NotImplementedError`. |
| ADD | `pkgs/20-providers/tigrbl-secret-hashing-bcrypt-provider` | Add `BcryptSecretHasher` implementing hash/verify for the existing `LargeBinary(60)` representation, cost policy, malformed-hash rejection, and optional rehash-needed detection. |
| UPDATE | `tigrbl-authenticator-password-local` | `PasswordLocalAuthenticator` injects the hasher and implements typed authenticate/verify behavior; it does not query `User`. |
| UPDATE | `tigrbl-authenticator-client-secret-local` | `ClientSecretLocalAuthenticator` injects the hasher and implements typed verify behavior; remove OAuth-specific implementation semantics. |
| UPDATE | `tigrbl-authn-credentials/lifecycle.py` | Stop maintaining a competing PBKDF2 storage format unless explicitly supported as a versioned migration algorithm. Split deterministic lifecycle from provider hashing; remove `CredentialLedger` as an in-memory durable substitute. |

If legacy PBKDF2 hashes exist, add a layer-20 `CompositeSecretVerifier` that
recognizes both encodings, verifies with the correct provider, and requests a
bcrypt rehash after successful authentication. Never reinterpret one encoding
as another.

### 18.2 Authentication capabilities

ADD `pkgs/40-capabilities/tigrbl-principal-authentication` with:

- `PasswordAuthenticationCapability`: injected identity lookup operation and
  `PasswordLocalAuthenticator`; operation `authenticate_password`;
- `ClientSecretAuthenticationCapability`: injected client lookup operation and
  `ClientSecretLocalAuthenticator`; operation `authenticate_client_secret`;
- `ApiKeyAuthenticationCapability`: injected API/service-key lookup operations
  and API-key provider; operation `authenticate_api_key`;
- typed results that identify the authenticated principal and factor evidence
  without exposing stored digests.

MOVE the composition currently in
`pkgs/20-providers/tigrbl-authn-credentials/src/tigrbl_authn_credentials/backends.py`
to these capabilities. Remove imports of `tigrbl_identity_storage.tables`,
`tables._ops`, `User.lookup_by_identifier`, `Client.authenticate`, and
`tigrbl_identity_jose.key_management.verify_pw` from layer 20.

| Current call | Replacement |
|---|---|
| `login.py: row.verify_password(password)` | `PasswordAuthenticationCapability.call("authenticate_password", request)` |
| `admin_auth.py: user.verify_password(...)` | same capability, preserving current-password semantics |
| `token_request.py: client.verify_secret(...)` | `ClientSecretAuthenticationCapability.call("authenticate_client_secret", request)` |
| `introspection.py: client.verify_secret(...)` | same capability with the introspection client-auth profile |
| `PasswordBackend._get_user_candidates -> User.lookup_by_identifier` | injected layer-30 identity lookup operation |
| `ApiKeyBackend -> list_records/Client.authenticate` | layer-40 API-key/client-secret subcalls |

## 19. C5: claims, scope, subject, and base-package cleanup

### 19.1 Claims

- KEEP `tigrbl_identity_core` claim classifiers and
  `tigrbl_identity_contracts.claims` semantic objects/ports.
- KEEP `tigrbl-identity-claims-bases` as the protocol-neutral home of
  `ClaimBase`, `ClaimSetComposerBase`, and `ClaimsProviderBase`.
- REQUIRE every `pkgs/10-concrete/tigrbl-claim-*-concrete` class to subclass
  `ClaimBase` and declare canonical name, name kind, claim type, and value type.
- ADD a generated ownership test that discovers every standalone claim package,
  instantiates its exported claim class, rejects duplicate canonical names
  unless an explicit protocol label differs, and proves no package imports
  layer 50.
- REMOVE `tigrbl-claim-access-token-hash-oidc-concrete` after its users migrate
  to `tigrbl-claim-access-token-hash-concrete`.

`tigrbl-oidc-claims-concrete` becomes a FACADE only:

- MOVE `EapAcrValue`, `EapAmrValue`, and `satisfies_eap_acr` from `eap.py` to
  OIDC/EAP profile modules at layer 50 because these are registered OIDC values,
  not generic claim objects;
- MOVE `parse_verified_claims` and `serialize_verified_claims` from
  `identity_assurance.py` to `tigrbl-identity-assurance-concrete` because the
  evidence structure is reusable below the OIDC wire profile;
- UPDATE `tests/unit/test_protocol_neutral_reusable_ownership.py`,
  `test_standalone_concrete_ownership.py`, package-local tests, and imports;
- retain warning exports for one release, then REMOVE the package, root
  dependency/source entries, package tests, and lock record.

### 19.2 Scope and subject identifiers

- UPDATE callers/tests to import `ScopeSetMatcher` from
  `tigrbl-authorization-scope-set-matcher-concrete`; FACADE then REMOVE
  `tigrbl-oauth-scope-matcher` and `DefaultScopeMatcher`.
- UPDATE `tigrbl-security-subject-pairwise-provider` to import
  `PairwiseSubjectIdentifierStrategy` from
  `tigrbl-pairwise-subject-identifier-concrete`.
- UPDATE OIDC layer-50 composition to choose public versus pairwise strategy.
- FACADE then REMOVE `tigrbl-oidc-subject-strategy`.

### 19.3 Base ownership

- MOVE profiled token verification, rich-authorization validation, actor-chain
  validation, and step-up evaluation from `tigrbl-oauth-bases` to
  `tigrbl-token-bases`, authorization/delegation bases, and
  `tigrbl-authentication-assurance-bases` respectively.
- MOVE EAP/verified-claims evaluation from `tigrbl-oidc-bases` to
  authentication-assurance and identity-claims bases.
- retain only genuinely OAuth/OIDC-defined extension points with multiple
  implementations; if none remain, FACADE and REMOVE both protocol-named base
  packages.
- update `test_concrete_layer_taxonomy.py`, import-boundary tests, root
  `pyproject.toml`, affected package metadata, and `uv.lock`.

## 20. C6: finish the EAT token/evidence/attestation chain

The existing split is retained and hardened:

| Layer | Owner | Required final responsibility |
|---|---|---|
| 02 | `tokens.py` | `ProtectedTokenEnvelope`, `VerifiedTokenEnvelope`, and explicit `TokenProfile.ENTITY_ATTESTATION_TOKEN`. |
| 02 | `attestation/*` | Evidence, verified evidence, appraisal, reference values, endorsements, manifests, and result ports. |
| 05 | `tigrbl-token-bases` | Protected envelope verification extension point. |
| 05 | `tigrbl-jose-bases` / `tigrbl-cose-bases` | JWT and CWT integrity coding extension points. |
| 05 | `tigrbl-attestation-bases` | Evidence verification and appraisal extension points. |
| 10 | `tigrbl-eat-concrete` | Structural EAT claim parsing, submodules, profiles, detached-bundle structure, and evidence conversion only. |
| 20 | `tigrbl-eat-verifier-provider` | Choose JWT/CWT verifier by explicit envelope/profile, resolve issuer/key/trust, verify integrity, then return `VerifiedAttestationEvidence`. |
| 30 | attestation runtime tables | Persist protected artifact digest/locator, verification result, appraisal result, reference material, and replay state. |
| 40 | `tigrbl-attestation-appraisal` | Subcall evidence verification, reference resolution, appraisal, and durable result recording. |
| 50 | `tigrbl-attestation-protocol-eat` | Own exact RFC/profile versions, media types, claim labels, compatibility, feature flags, migrations, and capability bindings. |

UPDATE `EatVerifierProvider`: replace the untyped
`Callable[[bytes | str, str], bool]` with typed JWT/CWT token verifier ports;
never build `VerifiedTokenEnvelope` from the original claims until the verifier
returns authenticated claims. Verify expected profile, issuer, audience where
applicable, nonce/freshness, and trust result. Negative tests cover raw
claim-only input, missing verifier, invalid signature/MAC, wrong profile,
untrusted issuer, stale evidence, duplicate nonce, and modified submodules.

UPDATE `AttestationAppraisalCapability`: make `verify_evidence`,
`resolve_reference_material`, `appraise`, and `record_result` separate targets
or explicit subcalls. The appraiser accepts only `VerifiedAttestationEvidence`;
raw evidence cannot be appraised as trusted evidence.

## 21. C8: make layer-40 capabilities composable and reportable

### 21.1 Common capability corrections

- KEEP `CapabilityDefinition(capability_id, version)` and the single
  `Mapping[str, CapabilityOperation]` registry.
- KEEP construction-time `NotImplementedError` for a missing required target.
- KEEP `CapabilityState` only for effective runtime readiness/health, not static
  feature marketing metadata.
- UPDATE `Capability.call` to populate/validate `capability_id` and `operation`
  in call context, preserve deadlines, and expose a consistent typed failure.
- UPDATE `Capability.subcall` tests for parent/child IDs, trace and tenant
  propagation, authority narrowing, cycle rejection, and delegated results.
- ADD a layer-60 `CapabilityRegistry`/composer that indexes capability IDs,
  validates required operations once, and produces the effective report used
  by protocols and APIs.

### 21.2 Existing package corrections

| Package | Required change |
|---|---|
| `tigrbl-identity-admin-control-plane` | Replace in-memory `_metadata`, `_objects`, and `_audit_events` with injected layer-30 operations. Keep `_new_id`/`_utc_now` as layer-00 imports. Split resource operations if dependencies/readiness differ. |
| `tigrbl-digital-credential-issuance` | Replace in-memory `_configurations` with injected configuration/offer/transaction operations. Make wallet-attestation verification an optional operation and report it unavailable when unbound. |
| `tigrbl-digital-credential-presentation` | Inject replay and consent capabilities with async-safe operations; record presentation transaction/result durably. |
| `tigrbl-attestation-appraisal` | Use the verified-evidence chain in section 20 and durable recorder operations. |
| `tigrbl-security-events` | Inject durable event/subscription/delivery/replay operations; transmitter and receiver remain providers. |
| `tigrbl-workload-identity` | Expose fetch-X509-SVID, fetch-JWT-SVID, verify-SVID, resolve-bundle, and refresh operations as distinct targets. |
| `tigrbl-replay-protection-capability` | Keep memory provider support, bind durable reservations from layer 30 when selected, and derive persistence/provider reporting from the binding. |
| `tigrbl-protocol-artifact-processing` | Remove hard-coded ready state; derive readiness from bound operations and providers. |

Every layer-40 README must state injected dependencies, operation names,
readiness rules, non-goals, and consuming layer-50 packages.

## 22. C9: normalize layer-50 specification ownership and bindings

Every independently versioned specification package must contain, or explain
why it does not need, these modules:

```text
versions.py
features.py
compatibility.py
migrations.py
claims.py
schemas.py
bindings.py
errors.py
```

The live package audit requires these concrete updates:

- ADD the missing standard module set to `tigrbl-auth-protocol-cwt` and
  `tigrbl-auth-protocol-rp` where applicable.
- ADD `compatibility.py`, `claims.py`, `schemas.py`, `bindings.py`, and
  `errors.py` to EAT, CoRIM, HAIP, AuthZEN, GNAP, JWT, OID4VCI, OID4VP,
  SD-JWT VC, and SET packages as required by their wire surfaces.
- REPLACE generic generated `artifact.processing.validate` requirements with
  explicit `ProtocolCapabilityRequirement` rows mapping each wire operation to
  its actual layer-40 capability operation.
- MOVE HTTP/router construction currently exported from layer-30 modules
  (`token_endpoint`, `introspection`, `revocation`, `userinfo`, discovery,
  logout, PAR, and token exchange) into layer-50 bindings and layer-80 mounts.
  Layer 30 exports operations/specs only.
- REMOVE wildcard imports such as OAuth token exchange's `import *`; export a
  reviewed binding surface.
- MAKE OIDC claim sets import standalone claims and identity-assurance concrete
  behavior; make OAuth import the neutral scope matcher; make HAIP configure
  OID4VCI/OID4VP, SD-JWT VC/mdoc, trust, wallet/key attestation, replay, and
  holder binding through capabilities.
- RECORD exact published/draft revision, status, superseded revisions,
  supported features per revision, compatibility direction, and configuration
  migration functions. Draft support is labeled draft.

Protocol equivalence tests prove this chain:

```text
semantic operation -> binding spec -> runtime plan -> carrier dispatch
                   -> same typed capability call -> protocol envelope
```

Carriers may differ in envelopes, but must not fork semantic operation identity
or move carrier choices into handlers.

## 23. C10-C12: downstream migration, removals, and closure

### 23.1 Runtime, facade, APIs, and UIX

| Layer | Files/packages | Required change |
|---|---|---|
| 60 | `tigrbl-identity-server/api/lifecycle.py` | Build providers, layer-30 runtimes, capability registry, and selected protocols in that order; fail startup on missing required targets. |
| 60 | `tigrbl-identity-server/_surfaces/*.py` | Stop importing routers from layer 30. Import layer-80 API routers or mount layer-50 bindings. |
| 60 | `tigrbl-identity-runtime/token_service.py` | Consume typed capability/protocol services rather than persistence helpers directly. |
| 60 | CLI handlers | Call administration capabilities; remove direct `operator_store`, `resource_service`, and key-management mutations that bypass policy. |
| 70 | `tigrbl-auth` | Export stable contracts/capabilities/protocol configuration. Warn with removal versions for old scope, subject, claims, persistence, and model-method paths. |
| 80 | all `tigrbl-auth-api-*` packages | Own HTTP schemas/routes, translate request context to typed calls, mount selected layer-50 bindings, and generate OpenAPI/OpenRPC from mounted truth. |
| 90 | `uix-core` | Update shared generated clients/types only after layer-80 contracts stabilize. |
| 95 | product UIX packages | Update imports/endpoints and verify each package uses only its allowed layer-80 API surface. |

### 23.2 Workspace-wide metadata updates

Update in the same checkpoint as each package move:

- root `pyproject.toml` dependencies and `[tool.uv.sources]` entries;
- each affected package `pyproject.toml`;
- `uv.lock`, followed by `uv lock --check`;
- package `README.md`, `py.typed`, and stable `__init__.py` exports;
- package-boundary/forbidden-import inventories and taxonomy tests;
- compliance targets, feature/flag mappings, certification scope, and generated
  evidence only when they point to live implementations/tests;
- API OpenAPI/OpenRPC snapshots and UI generated clients when wire changes.

### 23.3 Explicit removal gates

REMOVE a legacy package/file only after `rg` finds no internal imports and its
published compatibility window has elapsed. Incorrect claims such as RFC 7952
being SET are removed immediately; no public alias preserves false attribution.

The final audit proves:

- layer 01 contains no `op_ctx`, `hook_ctx`, router, HTTP schema, hashing,
  provider, engine/session construction, or table-handler calls;
- layer 20 contains no SQL stores, repositories, table `_ops`, or direct durable
  mutations;
- layer 30 contains no routers, HTTP objects, protocol errors, or network/trust
  choices;
- layer 40 contains no in-memory substitute for state that must be durable;
- layer 50 owns every independently versioned specification and maps explicit
  capability requirements;
- every JWT/CWT/SET/EAT/SD-JWT-like artifact names an expected token profile and
  explicit issuer/key/trust resolution;
- every required claim/identity/credential concrete class has its standalone
  layer-10 owner;
- migrations upgrade/downgrade, boundary/full suites pass, generated API
  documents match runtime behavior, and compliance evidence is live.

## 24. Recommended checkpoint/commit sequence

1. **C3a clients and users**: runtime operations/specs, secret contracts and
   bcrypt provider, authentication capabilities, migrated calls/tests, stripped
   storage models.
2. **C3b delegation/device/key/audit**: move remaining operations/hooks and
   delete layer-01 `_ops` use.
3. **C4 routes/runtime barrels**: move user/session/realm routes to layer 80;
   remove runtime/API exports from layer 01.
4. **C5 neutral reusable ownership**: claims facade, scope matcher, subject
   strategy, OAuth/OIDC base cleanup.
5. **C6 EAT chain**: typed token verifiers, verified evidence, appraisal
   composition, durable recording, negative tests.
6. **C8 capability durability/composition**: remove in-memory durable
   substitutes and add registry/readiness/delegation proofs.
7. **C9 protocol normalization**: complete module sets and move routers/bindings
   out of layer 30.
8. **C10 downstream composition**: runtime, facade, APIs, UIX clients, metadata.
9. **C11 compatibility removal**: delete expired facades and lock/workspace
   entries.
10. **C12 closure audit**: full tests, migrations, carrier equivalence,
    security negatives, interop evidence, compliance regeneration, and final
    inventory.

Each checkpoint is committed only with a clean diff, focused proof, boundary
proof, and a recorded list of pre-existing failures not introduced by it.
