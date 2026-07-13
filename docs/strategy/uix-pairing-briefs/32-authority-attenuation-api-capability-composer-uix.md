# Authority Attenuation API + Capability Composer UIX Requirements Brief

**Pairing:** `tigrbl-auth-api-authority-attenuation` + `@tigrbl-auth/capability-composer-uix`  
**Additional opportunity:** Authorization/delegation/sovereignty extension 3  
**Primary buyers:** authorization platform teams, security engineering, workload and agent platforms, API product teams, governance administrators, and high-assurance application owners  
**Status:** proposed product surface; scope coverage, wildcard narrowing, authority closure, monotonicity, least-authority diff, durable proof, and delegation lifecycle foundations exist

## 1. Product Decision

Build a dedicated attenuation service that can prove whether proposed authority is equal to or narrower than source authority across every supported authorization dimension.

The product must answer:

1. What authority does the source actually possess now?
2. What authority is proposed for the child grant, token, capability, session, task, or transaction?
3. Which dimensions were removed, narrowed, preserved, broadened, or left incomparable?
4. Can the narrowing be proven under versioned, typed semantics?
5. What is the minimum authority required for the intended operation?
6. Which constraints must the PEP enforce for the proof to remain valid?
7. When does source or context change invalidate the proof?

The API owns typed authority schemas, normalization, partial-order comparison, composition, minimization, proof generation, verification, and re-evaluation. The UIX helps authorized users compose safe capabilities and understand why a proposal is accepted, rejected, or incomparable.

## 2. Why This Is a Separate Pairing

Delegation Provenance owns grant and chain lifecycle. Policy Studio owns policy authoring. Authorization Provenance explains decisions. The Attenuation API owns the formal relationship:

`proposed authority <= source authority`

That relationship is reused by:

- delegated administration;
- token exchange and rich authorization requests;
- workload and service credentials;
- agent/sub-agent tasks and budgets;
- credential broker leases;
- device/fleet commands;
- transaction-specific approvals;
- cross-border and data-handling constraints;
- capability-style authorization;
- emergency and time-bound access.

Without a dedicated service, each product risks inventing incompatible narrowing rules or treating untyped JSON constraints as safely attenuated.

## 3. Current Repository Reality

The repository already provides:

- `AuthorityScope` with tenant, realm, action, and resource dimensions;
- exact and hierarchical `*`/`prefix.*` matching;
- `AuthorityScope.covers()` for scope inclusion;
- `DelegationGrantSpec` and `DelegationAttenuationProof`;
- `prove_delegation_attenuation()` with uncovered-scope reporting;
- checks for revoked/expired grants, known provenance, and allowed policy versions;
- multi-hop wildcard-narrowing and cross-tenant/realm rejection tests;
- durable proof rows with source/delegated scope hashes, proof result/version/hash, uncovered scopes, and evaluation time;
- authority graph reachability and effective-scope computation;
- monotonicity reports for grant/revoke/replace mutations;
- least-authority diffs with missing/excess scope attribution;
- durable grant constraints stored as JSON.

Current limits are material:

- attenuation semantics cover primarily tenant, realm, action, and resource;
- realm comparison permits an unspecified realm in some coverage cases and needs a deliberate product profile;
- arbitrary constraint JSON has no canonical type system or comparison semantics;
- time, audience, purpose, data class, region, amount, budget, count, assurance, device/workload posture, proof binding, and redelegation are not in the proof algebra;
- action/resource wildcard semantics are string-prefix based rather than catalog/version governed;
- no API/UIX exists for schema registration, safe composition, simulation, minimization, or proof verification;
- proof invalidation and PEP enforcement receipts are incomplete;
- no interoperable adapters exist for RAR, GNAP access rights, Macaroons, or other capability formats.

## 4. Product Principles

1. **Narrowing must be provable.** Unknown is not success.
2. **Constraints are typed.** Free-form values cannot participate in a proof.
3. **Conjunction narrows; disjunction may broaden.** Composition must preserve logic explicitly.
4. **Source authority is current and evidence-backed.** A child request cannot define its own parent.
5. **Least authority is purpose-specific.** Fewer strings are not necessarily safer if combinations broaden access.
6. **Proof and enforcement are separate.** A valid proof is useful only if the PEP understands and enforces its constraints.
7. **Formats are adapters.** A JWT, opaque handle, GNAP token, or Macaroon may carry authority, but none defines Tigrbl’s whole semantic model.
8. **Revocation remains necessary.** Attenuation reduces authority; it does not eliminate compromise or lifecycle risk.

## 5. Users and Jobs

### Security or authorization architect

- define authority types and constraint ordering;
- approve action/resource/data/purpose vocabularies;
- verify that downstream systems enforce every constraint;
- review ambiguous or non-monotonic constructs.

### Delegation or platform administrator

- start from effective source authority;
- select only the authority needed by a delegate;
- add time, purpose, resource, budget, region, and proof restrictions;
- preview proof and downstream impact before grant activation.

### Developer and API owner

- declare typed resource/action and rich authorization schemas;
- request minimized transaction authority;
- verify proof/constraints at the PEP;
- diagnose rejected or incompatible capability requests.

### Workload or agent platform engineer

- issue task-specific child authority;
- subdivide budgets and tools safely;
- prevent sub-agents from broadening scope or egress;
- refresh or revoke when source state changes.

### Reviewer and auditor

- compare parent and child authority dimension by dimension;
- verify the proof version, source evidence, and enforcement coverage;
- identify excess authority and unproven constraints.

## 6. Architectural Ownership

### Authority Attenuation API owns

- authority-type and constraint-schema registry;
- canonicalization and normalization;
- dimension-specific partial-order comparators;
- authority intersection, safe difference, and minimization;
- source-versus-proposed comparison;
- multi-hop proof composition;
- proof generation, verification, invalidation, and compatibility;
- PEP capability declarations and coverage checks;
- simulations and Capability Composer APIs.

### Delegation Provenance owns

- grants, parent/child edges, actors/subjects, approvals, lifecycle, token/action lineage, and revocation convergence;
- links to attenuation proof IDs.

### Policy Studio owns

- policies determining who may compose/approve authority;
- allowed profiles, maximums, and exception rules;
- not the comparison algorithms themselves.

### Authorization Decision and PEP own

- live contextual evaluation and enforcement;
- use of proof/constraints as verified inputs;
- enforcement receipts stating which constraints were applied.

## 7. Canonical Authority Object

An authority object requires:

- authority type URI/name and schema version;
- tenant, realm/trust domain, and environment;
- subject/delegate type where relevant;
- resource selectors;
- actions/operations;
- audiences/locations;
- data types/classifications;
- purposes/tasks/transactions;
- privileges/roles;
- time and usage bounds;
- value/count/budget limits;
- assurance, attestation, and proof-binding requirements;
- regional/residency/transfer constraints;
- redelegation constraints;
- obligations and enforcement profile;
- source authority and policy/provenance references;
- canonical digest.

Authority is represented as one or more clauses. Each clause is a conjunction of dimensions. Multiple clauses represent an explicit union. This avoids accidentally interpreting independent arrays as a broader Cartesian product.

## 8. Type and Schema Registry

Each authority type defines:

- stable type identifier and semantic version;
- owner and approved consumers;
- allowed/required dimensions;
- canonical JSON/data types;
- normalization rules;
- comparison operator for each dimension;
- clause/union semantics;
- wildcard/hierarchy/catalog behavior;
- unknown/missing/null meaning;
- safe display labels and sensitivity;
- PEP enforcement requirements;
- protocol-format mappings;
- test vectors and conformance status;
- lifecycle: draft, approved, deprecated, retired.

Type identifiers require exact comparison. Versions cannot silently change ordering semantics.

## 9. Partial-Order Semantics

For a proposed authority `C` and source authority `P`, attenuation passes only when every child clause is covered by a parent clause under every required dimension.

Possible comparison outcomes:

- `equal`;
- `narrower`;
- `broader`;
- `disjoint`;
- `incomparable`;
- `unknown`;
- `invalid`.

Only `equal` and `narrower` may pass. Profiles may require strictly narrower for redelegation.

Comparators must be reflexive, antisymmetric where applicable, and transitive over supported values. Property-based tests must verify these laws and reject counterexamples.

## 10. Set and Hierarchy Dimensions

Applicable to actions, resources, audiences, data types, regions, and allowed delegates.

Supported semantics may include:

- exact set inclusion;
- catalog hierarchy with immutable version;
- namespace/prefix inclusion;
- resource-tree descendant inclusion;
- CIDR/network subset;
- geographic/jurisdiction subset under a governed catalog.

Requirements:

- wildcard meaning is type-specific and visible;
- `*` never crosses tenant/realm/type boundaries;
- hierarchy changes invalidate or version proofs;
- aliases resolve before comparison and preserve original input;
- negative/deny sets require explicit algebra and cannot be inferred by subtraction;
- empty set means no authority, not unspecified authority.

## 11. Time and Usage Dimensions

### Time

- child `not_before` must be no earlier than parent;
- child expiry must be no later than parent;
- allowed time windows and schedules must be subsets;
- clock tolerance/profile must be explicit;
- timezone and calendar semantics are canonicalized.

### Usage

- one-use is narrower than bounded multi-use;
- smaller count/rate/concurrency limits are narrower;
- child cumulative consumption plus siblings must not exceed a shared parent budget;
- reservations and consumption require atomic ledgers;
- retry/idempotency semantics prevent double charge or double use.

Time passing may invalidate a proof without changing its digest. Verification always evaluates current validity.

## 12. Numeric, Monetary, and Budget Dimensions

Use typed units and interval/sub-budget semantics:

- amount/value maximum;
- transaction count;
- compute/token/storage/network budget;
- duration;
- geographic distance or other profile-specific bounded measure.

Requirements:

- canonical unit/currency and conversion policy;
- no floating-point ambiguity for money/security bounds;
- child interval is subset of parent interval;
- shared budgets use atomic allocation/reservation/consumption;
- currency conversion cannot prove attenuation without a pinned rate/time/source and approved policy;
- aggregate sibling allocation cannot exceed parent;
- refunds/releases are auditable and cannot create authority beyond the original parent.

## 13. Purpose, Task, and Transaction Dimensions

Purpose is not a free-text label. A type defines:

- purpose taxonomy/version;
- allowed sub-purposes;
- exact task/transaction binding;
- permitted data/actions/resources;
- reuse and redelegation rules;
- expiry and completion semantics.

Child purpose must equal or be a governed specialization of parent purpose. Adding a second purpose broadens authority unless separately authorized.

High-impact authority may bind to an immutable transaction digest so it cannot be replayed for a different operation.

## 14. Data and Regional Dimensions

Support:

- allowed data classifications/types;
- allowed operations on each class;
- source/destination/processing/storage regions;
- cross-border transfer authorization reference;
- disclosure recipients;
- retention and onward-use limits;
- de-identification or masking obligation.

Attenuation must preserve relationships among dimensions. “Read public and write confidential” cannot become a flat set of actions `{read, write}` and data types `{public, confidential}` because that Cartesian product wrongly permits writing confidential data.

Use separate clauses or relationship-preserving tuples.

## 15. Assurance, Attestation, and Proof Binding

Narrower authority may require stronger—not weaker—conditions:

- authentication assurance level;
- authentication age/recency;
- approved authenticator class;
- device/workload attestation profile and freshness;
- trusted environment/build/deployment;
- sender-constrained token/key/certificate;
- network or confidential-computing posture.

Comparator semantics for assurance are profile-governed. Different assurance schemes cannot be numerically compared without an approved mapping.

Removing a proof-binding requirement always broadens authority. Changing the bound key/client/workload is replacement, not attenuation.

## 16. Redelegation Dimensions

Child authority must not exceed parent limits for:

- redelegation allowed/forbidden;
- maximum depth and remaining depth;
- maximum children/fan-out;
- allowed delegate principal types;
- maximum child lifetime;
- minimum narrowing delta;
- permitted semantic modes;
- child approval/acceptance;
- downstream token/credential types;
- revocation and receipt obligations.

Remaining depth decreases at every hop. A child cannot reset it.

## 17. Predicate and Context Constraints

Arbitrary predicates are high risk because implication may be undecidable or dependent on mutable external state.

The service supports only registered predicate types with a safe comparator, such as:

- equality;
- finite set inclusion;
- numeric interval;
- time interval/schedule subset;
- prefix/tree descendant;
- CIDR subset;
- Boolean requirement strengthening;
- conjunction of registered predicates.

Unsupported code, scripts, regex without containment proof, general SQL, opaque policy expressions, and arbitrary functions yield `incomparable` and cannot produce an attenuation proof.

Context-dependent predicates may be preserved as runtime obligations but do not prove static attenuation unless implication is established.

## 18. Composition Rules

### Safe operations

- intersect source authority with a valid requested subset;
- add a conjunctive restriction;
- reduce set members, interval, count, rate, time, depth, or audience;
- strengthen assurance/proof requirements under a governed order;
- split one parent clause into narrower child clauses without increasing their union;
- allocate an atomic sub-budget.

### Unsafe or review-required operations

- union independent source grants;
- convert arrays into a Cartesian product;
- remove deny/exception conditions;
- substitute resource identifiers or bound keys;
- add alternative (`OR`) predicates;
- translate across incomparable schemas/profiles;
- extend time through renewal;
- use live mutable catalogs without version pinning;
- depend on unenforced constraints.

## 19. Minimum-Authority Synthesis

The API may propose authority from a typed operation template:

- required action/resource/data/purpose;
- target audience/location;
- exact transaction;
- required duration/count/value;
- required assurance and proof binding;
- regional/data obligations;
- allowed downstream behavior.

It returns:

- required authority clauses;
- missing source authority;
- excess source authority;
- proposed child authority;
- enforceability requirements;
- confidence/unsupported dimensions.

Synthesis is advisory until policy authorizes and proof verifies the result. It must not silently grant missing authority.

## 20. Multi-Source Authority

Default: one proof path must cover each child clause completely.

Combining authority from multiple parents is allowed only under a registered composition profile that defines:

- whether union is permitted;
- responsible/source authorities;
- conflict and deny precedence;
- shared constraints and budgets;
- revocation effect;
- proof construction and PEP semantics.

The service must never combine a parent’s resource permission with another parent’s action permission to synthesize authority neither granted.

## 21. Proof Model

An attenuation proof contains:

- proof ID/version/schema;
- authority type/version;
- source authority IDs and canonical hashes;
- child authority canonical hash;
- comparator registry/version and catalogs;
- per-clause/per-dimension comparison results;
- uncovered, broader, incomparable, and unknown dimensions;
- source fact/policy/provenance versions;
- evaluation time and validity/freshness bounds;
- PEP enforcement profile requirements;
- proof result and stable proof hash;
- optional integrity signature/seal;
- invalidation triggers.

Proofs are non-bearer evidence. Possessing a proof does not confer authority.

## 22. Proof Verification and Invalidation

Verification checks:

- canonical hashes and signature/seal;
- source authority status and current effective scope;
- type/comparator/catalog versions;
- child authority match;
- time and freshness;
- parent proof validity for multi-hop chains;
- PEP compatibility;
- revocation/replacement/suspension;
- budget/usage state where applicable.

Invalidate/re-evaluate on:

- parent authority change;
- policy/type/catalog/comparator change;
- source fact or trust change;
- time/usage/budget consumption;
- key/client/workload binding change;
- PEP capability downgrade;
- incident or risk signal;
- child replacement.

## 23. Protocol and Credential Adapters

### OAuth RAR

Map registered `authorization_details` types into typed clauses. Preserve relationship among fields and exact type semantics. Do not flatten rich authorization into OAuth scope strings.

### GNAP

Map access-right objects/strings, actions, locations, datatypes, identifiers, privileges, and API-specific fields through registered type definitions. GNAP arrays/objects may represent unions and cross-products; adapters must preserve their specified semantics.

### OAuth token exchange

Compare requested resource, audience, scope, actor/subject, token type, and proof binding against the canonical grant/source authority.

### Macaroons

An optional adapter may translate registered caveats into typed constraints and verify chained MACs. Macaroons demonstrate contextual caveat attenuation, but their bearer nature, verifier roots, third-party caveats, revocation, and caveat language require a separate threat model and conformance profile.

### Opaque capabilities/JWTs

Prefer opaque server-side handles or sender-constrained artifacts when possible. JWT claims are projections of authority, not the canonical proof or lifecycle store.

No new “Tigrbl capability token” should be invented unless an interoperability/profile need remains after these adapters.

## 24. PEP Capability and Enforcement Contract

Register each PEP’s:

- supported authority types/versions;
- understood dimensions/comparators;
- obligation support;
- token/credential formats;
- proof verification method;
- freshness/revocation sources;
- failure behavior;
- receipt capability.

Issuance/activation fails if the target PEP cannot enforce every material constraint. Ignoring unknown claims is prohibited.

Enforcement receipt records:

- authority/proof ID;
- decision/action/transaction;
- PEP identity/version;
- constraints evaluated and outcomes;
- usage/budget consumption;
- result and time;
- safe integrity reference.

## 25. API Requirements

Provide versioned endpoints for:

- `/authority-types`, schemas, dimensions, versions, and lifecycle;
- `/comparators`, catalogs, test vectors, and conformance;
- `/normalize` and `/validate`;
- `/compare` for source versus proposed authority;
- `/intersect`, bounded `/difference`, and `/minimize`;
- `/compose` with explicit union/conjunction semantics;
- `/proofs`, verification, refresh, and invalidation;
- `/multi-hop` proof composition;
- `/required-authority` synthesis from operation templates;
- `/simulations` and property/conformance reports;
- `/peps`, capabilities, coverage, and receipts;
- `/adapters/rar`, `/gnap`, `/token-exchange`, and approved formats;
- `/evidence-bundles` and integrity manifests.

API behavior:

- pure, deterministic evaluation for identical versioned inputs except declared current-state checks;
- canonical JSON and stable hashes;
- idempotent proof creation;
- explicit `incomparable`/`unknown` outcomes;
- no arbitrary code/policy execution;
- no grant activation or token issuance ownership;
- asynchronous jobs only for large graph/multi-proof analysis;
- tenant/realm/type authority and field-level redaction.

## 26. Capability Composer UIX

### Overview

Show proof volume/pass/fail/incomparable, unsupported constraint types, stale proofs, PEP coverage gaps, wildcard/excess authority, multi-source composition, budget allocation, and upcoming type/catalog deprecations.

### Source authority chooser

Resolve authorized source paths and display direct, inherited, delegated, relationship, and trust-framework authority separately. The user must select or accept an explicit source path/profile.

### Clause composer

Build authority using type-driven controls for resources, actions, data, audience, purpose, time, usage, budgets, assurance, region, and redelegation. Preserve relationships with clause groups rather than independent multi-select fields.

### Source-versus-child diff

For every dimension show removed, narrowed, unchanged, broader, incomparable, and unknown values. Explain wildcard expansion and catalog hierarchy. Highlight which PEP must enforce each constraint.

### Proof view

Show result, source/child hashes, type/comparator/catalog versions, per-dimension reasoning, uncovered authority, freshness/invalidation, and evidence—not a generic green check.

### Minimum-authority assistant

Start from an operation/task template and propose the smallest representable authority. Show assumptions, unsupported dimensions, missing source authority, and excess source authority. Require human/policy review before use.

### Multi-hop simulator

Compose child/grandchild authority and demonstrate remaining lifetime, budgets, depth, and constraints. Block reset or broadening at later hops.

### PEP compatibility

Before activation, show whether every target PEP understands and enforces all dimensions. Missing support blocks production activation or requires a separately approved fallback profile.

### Test and conformance studio

Run positive, negative, boundary, property-based, catalog-change, and PEP receipt fixtures. Compare comparator/type versions and reveal changed outcomes.

## 27. Security, Privacy, and Reliability

- Enforce tenant, realm, trust-domain, environment, authority type, and field isolation.
- Separate schema/comparator authoring, approval, proof generation, grant approval, PEP administration, and audit.
- Treat type/comparator/catalog changes as security-sensitive versioned releases.
- Defend normalization and comparator implementations against ambiguity, Unicode/confusable values, overflow, regex/algorithmic complexity, and resource exhaustion.
- Use exact decimal/integer semantics for money/count/security limits.
- Bound clauses, dimensions, set size, hierarchy depth, and proof-chain depth.
- Require canonical time, URI, identifier, unit, currency, region, and classification forms.
- Preserve sensitive resources, subjects, purposes, data classes, and budgets through authorized projections.
- Avoid embedding confidential authority into public/self-contained tokens when an opaque handle suffices.
- Fail closed on missing source, unknown type, unsupported comparator, stale catalog, or incompatible PEP.
- Use atomic budget/usage ledgers and idempotent receipts.
- Meet WCAG 2.2 AA for dense comparisons, clause builders, graphs, and proof details.

## 28. Stakeholder Requirements

### Technical marketing

Demonstrate wildcard-to-specific narrowing, transaction/time/budget restrictions, unsafe Cartesian-product prevention, multi-hop sub-agent attenuation, PEP incompatibility, and failed unknown predicate comparison. Explain that the product proves narrowing; it does not make all capability tokens safe.

### Developer relations

Deliver authority-type SDKs, comparator interfaces, RAR/GNAP/token-exchange adapters, PEP verifier examples, Macaroon experimental profile, property-based test kits, operation templates, and negative fixtures for broadening/incomparability/overflow/catalog drift.

### Sales and account management

Use discovery for resource/action vocabularies, delegation flows, tokens, transaction detail, budgets, agents, data/region constraints, PEPs, policy engines, credential formats, scale, and revocation. Distinguish supported comparators from arbitrary customer policy.

### GTM strategist

Position as a least-authority and safe sub-delegation layer across APIs, workloads, agents, and regulated transactions. Enter through explainable scope minimization and agent/workload controls; expand into regional/data and financial transaction constraints.

### Copywriter

Standardize `source authority`, `proposed authority`, `clause`, `dimension`, `constraint`, `narrower`, `broader`, `incomparable`, `unknown`, `attenuation proof`, `minimum authority`, and `PEP coverage`. Avoid `safe`, `least privilege`, or `cannot escalate` without a complete proof/enforcement chain.

## 29. Delivery Instructions

### Frontend engineer

- Generate controls from server-provided authority-type schemas, never client-hardcode security semantics.
- Preserve clause groupings and do not flatten relational dimensions.
- Render server comparison results and authorized projections.
- Provide accessible tables/text for graphs and set/interval visualizations.
- Use server-side search/pagination for catalogs and resources.
- Require preview/proof/PEP compatibility before sending a proposal to grant workflow.
- Keep authority details out of URLs, analytics, and session replay.
- Handle version conflicts, stale source authority, and proof invalidation explicitly.

### UIX designer

- Make source, proposed, and effective authority continuously distinguishable.
- Design a visual grammar for removed, narrowed, unchanged, broader, incomparable, unknown, and unsupported.
- Represent clauses/conjunctions/unions accurately; avoid misleading independent filters.
- Show wildcard and hierarchy expansion on demand.
- Keep proof reasoning understandable while retaining expert evidence.
- Design no-authority, no-access, stale, catalog-changed, PEP-incompatible, and partial-receipt states.

### Copywriter

- Explain each comparison in plain language tied to its dimension.
- State why incomparable/unknown fails activation and what remediation is possible.
- Explain that stricter conditions may reduce usability and require PEP support.
- Avoid mathematical certainty claims outside supported type/comparator versions.

## 30. Delivery Phases

### Phase 1: Generalize existing scope proof

- canonical authority object/type registry;
- tenant/realm/action/resource comparators with deliberate wildcard semantics;
- normalize/validate/compare/proof APIs;
- Capability Composer source/child diff and proof view;
- integrate Delegation Provenance grant lifecycle and existing durable proofs.

### Phase 2: Typed constraints and PEP coverage

- time, usage, audience, purpose, assurance, proof binding, and redelegation;
- PEP capability registry and enforcement receipts;
- operation templates/minimum-authority synthesis;
- comparator conformance/property test suite.

### Phase 3: Budgets, data, and regions

- numeric/monetary/compute budgets with atomic allocation;
- relational data/action clauses;
- classification, residency, transfer, recipient, and retention dimensions;
- multi-hop and sibling-budget proof composition.

### Phase 4: Protocol and ecosystem adapters

- RAR, GNAP, token exchange, credential broker, agent, device, and workload adapters;
- optional Macaroon experiment after threat model;
- external proof/evidence profiles, regional scale, and certification.

## 31. Acceptance Criteria

### Domain/API

- Every proof names exact authority type, schema, comparator, catalog, source, and child versions.
- Child authority passes only when every clause is equal/narrower across every required dimension.
- Broader, incomparable, unknown, invalid, missing, or stale dimensions fail closed.
- Wildcards cannot cross tenant, realm, type, or catalog boundaries.
- Clause relationships are preserved and Cartesian-product broadening is tested.
- Multi-hop proofs remain transitive under supported comparators.
- Parent time, budget, usage, and remaining-depth limits cannot be reset.
- Multiple source grants are not combined without an explicit composition profile.
- Proof is non-bearer and contains no raw credentials/secrets.
- Proof invalidation follows source/type/catalog/policy/PEP/lifecycle changes.

### PEP/enforcement

- Production activation requires a target PEP capable of enforcing every material dimension.
- Unknown claims cannot be ignored.
- Enforcement receipts link proof, action, PEP, constraints, usage, and result.
- Receipt absence is not displayed as successful enforcement.

### UIX

- Users can see source versus proposed authority by dimension before approval.
- Clause grouping prevents accidental broadened combinations.
- Incomparable and unknown states include precise remediation.
- Multi-hop views show remaining time, budget, depth, and constraints.
- Graphs/visual comparisons have accessible text/table equivalents.
- Core workflows meet WCAG 2.2 AA.

### Evidence/business

- Fixtures cover exact, subset, wildcard, tenant/realm violation, union/cross-product, time, count, money, purpose, data/action relationship, region, assurance, binding, depth, budget, multiple source, catalog drift, unknown predicate, and incompatible PEP.
- Marketing claims map to named dimensions, comparator versions, and PEP enforcement coverage.

## 32. Success Measures

- proposed child authorities passing, failing, or incomparable by dimension;
- wildcard authority reduced to specific resources/actions;
- median excess-authority reduction from source to child;
- grants blocked for unproven broadening;
- unsupported constraint and PEP coverage-gap rate;
- stale/invalidated proof count and age;
- multi-hop depth/fan-out and attenuation delta;
- budget over-allocation attempts prevented;
- enforcement receipt coverage and mismatch rate;
- time to compose/review a least-authority proposal;
- authorization failures caused by over-attenuation versus unsafe broadening prevented;
- comparator conformance/property test pass rate.

## 33. Source Evidence

### Repository

- `.ssot/specs/SPEC-1208-delegation-attenuation-proof-contract.yaml`
- `.ssot/specs/SPEC-1206-authority-derivation-graph-contract.yaml`
- `.ssot/specs/SPEC-1213-delegation-grant-lifecycle-contract.yaml`
- `pkgs/02-contracts/tigrbl-identity-contracts/src/tigrbl_identity_contracts/authority/graph.py`
- `pkgs/02-contracts/tigrbl-identity-contracts/src/tigrbl_identity_contracts/authority/semantics.py`
- `pkgs/02-contracts/tigrbl-identity-contracts/src/tigrbl_identity_contracts/delegation/proofs.py`
- `pkgs/20-providers/tigrbl-authz-policy/src/tigrbl_authz_policy/delegation.py`
- `pkgs/30-storage-runtime/tigrbl-authz-policy-authority-derivation-graph/`
- `pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/delegation_grant/`
- `tests/unit/test_delegation_attenuation_proof.py`
- `tests/unit/test_delegation_attenuation_robustness_t2.py`
- `tests/unit/test_authority_closure_monotonicity.py`
- `tests/unit/test_authority_closure_monotonicity_robustness_t2.py`
- `tests/unit/test_least_authority_minimality.py`
- `docs/strategy/uix-pairing-briefs/31-delegation-provenance-api-authority-chain-explorer-uix.md`

### Standards and primary research

- [RFC 9396, OAuth 2.0 Rich Authorization Requests](https://www.rfc-editor.org/rfc/rfc9396): typed authorization details for transaction/resource-specific access.
- [RFC 9635, GNAP](https://www.rfc-editor.org/rfc/rfc9635): structured resource access rights including actions, locations, datatypes, identifiers, privileges, and API-specific types.
- [RFC 8693, OAuth 2.0 Token Exchange](https://www.rfc-editor.org/rfc/rfc8693): subject/actor exchange with resource, audience, scope, delegation, and impersonation semantics.
- [Macaroons: Cookies with Contextual Caveats for Decentralized Authorization in the Cloud](https://research.google/pubs/macaroons-cookies-with-contextual-caveats-for-decentralized-authorization-in-the-cloud/): primary research on chained credentials and contextual caveat attenuation; use as an optional profile, not a universal format.
- [NIST least privilege definition](https://csrc.nist.gov/glossary/term/least_privilege): minimum necessary privileges for assigned tasks.
- [RFC 9449, DPoP](https://www.rfc-editor.org/rfc/rfc9449) and [RFC 8705, OAuth mTLS](https://www.rfc-editor.org/rfc/rfc8705): sender-constrained token enforcement inputs.

## 34. Explicit Non-Claims

- Fewer OAuth scope strings do not prove overall authority is narrower.
- A valid attenuation proof does not grant authority or prove the source authority is legitimate unless source verification succeeded.
- A proof does not establish that the PEP enforced every constraint.
- Unknown or opaque predicates are not safely attenuated merely because they were preserved.
- Adding caveats to a bearer credential does not eliminate theft, replay, root-key, verifier, or revocation risks.
- “Keyless” or opaque capabilities still depend on keys and trusted issuers/verifiers.
- Combining multiple narrow grants can create broader effective authority and requires explicit composition semantics.
- Least authority for one operation does not prove least privilege across a principal’s other grants or paths.
- Existing repository tests prove a valuable tenant/realm/action/resource slice, not the full typed constraint algebra proposed here.
