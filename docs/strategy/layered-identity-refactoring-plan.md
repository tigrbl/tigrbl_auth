# Layered identity migration and refactoring plan

Status: active implementation plan. This document describes target ownership and
delivery order; it is not certification evidence. Generated compliance reports
remain authoritative for conformance claims.

## 1. Target architecture

The dependency direction is:

```text
00 primitives
  -> 01 durable schemas / 02 semantic contracts
  -> 05 reusable behavioral bases
  -> 10 deterministic concrete objects / 20 environment-backed providers
  -> 30 durable Tigrbl table runtimes
  -> 40 mountable and composable capabilities
  -> 50 versioned protocols and profiles
  -> 60 runtime composition
  -> 70 public facade
  -> 80 HTTP/API products
  -> 90 deployable applications
  -> 95 distribution and deployment
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
| `tables/auth_session/_table.py` | `terminate`, `touch`, `get_active`, `rotate_cookie_secret`, `bind_client` | `ops/sessions.py`, `tables/sessions.py` |
| `tables/consent/_table.py` | `list_for_user`, `revoke_for_user`, `revoke_for_client` | `ops/consents.py`, `tables/consents.py` |
| `tables/logout_state/_table.py` | `latest_for_session`, `update_metadata`, `mark_channel`, `ensure_for_session` | `ops/oidc_logout.py`, extend `tables/oidc.py` |
| `tables/delegation_grant/_table.py` | grant CRUD/transitions, edge linking, child deactivation, provenance, token links | `ops/delegation.py`, `tables/delegation.py` |
| `tables/token_record/_operations.py` | `persist_issued`, `mark_rotated`, `revoke_family`, `introspect` | `ops/tokens.py`, `tables/tokens.py` |
| `tables/device_code/_hooks.py` | approve/deny hooks | `hooks/device_code.py`, `tables/oauth.py` |
| `tables/crypto_key/_hooks.py` | normalization, primary-version seed, enabled check | `hooks/keys.py`, `tables/keys.py` |
| `tables/client/_table.py` | durable enable/disable/rotate operations | `ops/clients.py`, `tables/clients.py` |
| `tables/user/_table.py` | durable lookup operation | `ops/identities.py`, `tables/identities.py` |
| `tables/audit_event/__init__.py` | append/list wrappers | `ops/audit.py`, `tables/audit.py` |
| `tables/_ops.py` | generic table handler calls | consolidate into layer-30 `ops/common.py` |
| `tables/engine.py` | runtime engine/provider/session resolution | layer-30 engine/session composition |

Completed moves already removed executable operations from
`attribute_policy`, `delegated_admin_scope`, `tenant_membership`,
`backchannel_logout_replay`, `auth_code`, `client_registration`, and
`revoked_token` table modules.

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

### Layer 90 applications

- Compose installable product surfaces from layer-80 APIs and layer-60 runtime
  configurations.
- Contain no reusable protocol/credential/claim algorithms.

### Layer 95 deployment/distribution

- Own packaging, images, charts, environment templates, and deployment policy.
- Validate that each application’s advertised capability/protocol set matches
  mounted routes and configured providers.

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

