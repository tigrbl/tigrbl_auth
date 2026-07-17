# Credential Verifier API + Verification Console UIX Requirements Brief

**Proposed pairing:** `tigrbl-auth-router-credential-verifier` + `@tigrbl-auth/credential-verifier-uix`<br>
**Status:** New product surface; planned verification-result/boundary work and reusable trust, JOSE, policy, status, audit, and API foundations exist<br>
**Prepared:** July 11, 2026<br>
**Proposed router owner:** `pkgs/80-routers/tigrbl-auth-router-credential-verifier`<br>
**Proposed protocol owner:** `pkgs/50-protocols/tigrbl-openid4vp-verifier`<br>
**Proposed UIX owner:** `pkgs/105-ui/credential-verifier-uix`

## 1. Product Decision

Create a digital credential verification and relying-party surface that defines purpose-bound presentation policies, generates secure OpenID4VP requests, receives wallet responses, validates protocol and credential-format protections, evaluates issuer/schema/status/holder/transaction trust, normalizes minimally disclosed claims, and produces a short-lived verification result for a separate business or authorization decision.

The product must distinguish:

- **Protocol validity:** request/response binding and transport are correct.
- **Credential/presentation validity:** cryptographic proof, issuer key, disclosure digests, holder/device proof, validity, and status pass.
- **Issuer/trust acceptance:** issuer is authorized for this credential type, jurisdiction, ecosystem, and purpose.
- **Claim/business policy:** disclosed claims satisfy the relying party's requirements.
- **Authorization/action:** the application or Policy Studio decides access, onboarding, transaction, or workflow outcome.

A successful verification is not universal identity proof, factual certainty, authorization, fraud clearance, consent for unrelated use, or permission to retain all disclosed data.

## 2. Current Repository Reality

Reusable foundations include:

- JOSE/JWT, key discovery/rotation, DPoP, mTLS, trust domains, federation graphs, resource-server validation, and policy engines;
- OAuth/OIDC/RP request/response, state, nonce, JAR/PAR, client metadata, session, and redirect patterns;
- credential/authenticator verification vocabulary, audit/provenance, evidence, storage, UIX core, and conformance infrastructure;
- proposed Credential Issuer, Wallet, Trust Registry, Attestation, and Security Signals surfaces;
- a planned `CredentialVerificationResult` identity-model test requiring representation, ownership, tenant isolation, lifecycle, and package-boundary checks;
- a planned policy-boundary test explicitly requiring credential verification to remain outside authorization packages.

No implementation evidence was found for:

- OpenID4VP Final request/response endpoints or Digital Credentials Query Language (DCQL);
- `vp_token` receipt, verifier metadata/client-identifier-prefix handling, request URI methods, or Digital Credentials API integration;
- SD-JWT VC, W3C VC 2.0 presentation, or mdoc verification;
- issuer/type/schema/status/trust-list appraisal;
- holder/key/device binding and transaction-data validation;
- credential verification result storage/API or Verification Console UIX.

The resource-server `VerificationResult` validates API access tokens and must not be reused as the digital credential verification result. The concepts have different inputs, trust models, evidence, privacy, and consumers.

## 3. Users and Jobs

### Relying-party/product administrator

1. define a business purpose and the minimum credential/claims needed.
2. choose accepted formats, credential types, trusted issuers/frameworks, status, holder binding, and freshness.
3. test same-device, cross-device, and API/browser presentation flows.
4. stage, publish, monitor, and supersede verification policies.
5. pass only necessary normalized facts/results to downstream applications.

### Risk, fraud, compliance, and privacy reviewer

1. inspect every verification stage and evidence source.
2. define issuer trust, status freshness, transaction binding, retention, and manual-review rules.
3. detect replay, over-disclosure, weak holder binding, malicious/unknown issuer, stale status, and policy drift.
4. prove why a result was accepted, rejected, or indeterminate without retaining unnecessary credential contents.

### Application developer

1. create a presentation transaction using a stable policy/template ID.
2. redirect/display QR or invoke a platform Digital Credentials API safely.
3. receive a normalized, audience-bound, short-lived result or callback.
4. handle cancel, no-match, invalid, expired, indeterminate, and error states.
5. avoid parsing wallet presentations or implementing issuer trust independently.

### Support/account team

1. locate a transaction by opaque reference/correlation without seeing raw credentials.
2. explain whether failure came from protocol, format, issuer trust, status, claim policy, holder proof, or system dependency.
3. export a redacted evidence bundle under authorization.

### Credential holder

1. see an accurate verifier identity, purpose, requested claims, and destination in the wallet.
2. disclose only necessary information.
3. decline without misleading claim-inference leakage.
4. understand the relying party's retention/use policy.

## 4. Architectural Ownership

### OpenID4VP protocol package owns

- verifier request object, metadata, client identifier prefixes, request URI methods, redirect/same/cross-device and Digital Credentials API flows;
- state, nonce, audience/origin, response URI/mode, encryption/signature, and response contracts;
- DCQL syntax/validation and protocol errors;
- exact OpenID4VP 1.0 Final behavior.

### Credential-format verifiers own

- SD-JWT VC disclosure/digest/key-binding/status verification;
- W3C VC/VP data-model and selected securing-mechanism verification;
- mdoc issuer/device authentication, session transcript, validity, certificate, namespace/element, and digest verification;
- format-specific normalization and test vectors;
- no generic "JWT verification" fallback for unknown credential formats.

### Credential Verifier API owns

- verifier/presentation policy, templates, trust, status, transactions, result, evidence, retention, incidents, and UI-facing schemas;
- protocol orchestration and format-provider selection;
- subject/claim normalization, business claim appraisal, relying-party result issuance, callbacks, metrics, privacy, and audit;
- integration with authorization/business applications without owning their decisions.

### Existing owners retain semantics

- Wallet owns credential selection and holder authorization;
- Issuer owns claims and credential status publication;
- Trust Registry owns issuer/framework lists and authority evidence;
- Attestation Center owns wallet/key/device attestation appraisal;
- Policy Studio consumes normalized result facts and decides access/action;
- Security Signals owns incident events and continuous response;
- storage owns durable minimal transaction/result/evidence metadata;
- UIX never validates presentations as the authority.

## 5. Verification Policy Model

Every active verification policy version defines:

- tenant/relying party, business purpose, legal/use basis, owner, lifecycle, locales, and holder-facing notice;
- accepted credential configurations/types/schemas and exact format/profile versions;
- DCQL query or governed template, credential sets, required/optional claims, allowed values/ranges/predicates, and minimization rules;
- accepted issuer/trust framework/authority criteria by type, purpose, jurisdiction, and time;
- issuer key discovery/algorithm policy and schema/type metadata/context integrity;
- credential/presentation validity, status mechanism/freshness, and offline/unknown behavior;
- holder/key/device binding, wallet attestation, user presence/authentication, nonce/freshness, and replay policy;
- transaction-data types/digests/semantics where used;
- normalized result claim schema, disclosure to downstream app, result lifetime/audience, retention, and evidence;
- manual review, retry, rate, incident, and fallback policy.

Policies are immutable after publication. A version change requires semantic diff, privacy review, holder-facing copy review, compatibility simulation, staged rollout, and rollback.

## 6. Request Creation and OpenID4VP Flows

The verifier creates presentation transactions from approved policy/template IDs, not arbitrary production DCQL supplied by a browser.

### Transaction creation

1. authenticate/authorize relying application and tenant;
2. resolve active policy/version and intended session/transaction/purpose;
3. create high-entropy state/nonce and opaque short-lived transaction ID;
4. bind callback/result audience, response URI/mode, verifier/client identity, origin, and one-time use;
5. construct minimal DCQL and recognized transaction data;
6. sign/encrypt/publish request object according to selected client identifier prefix/profile;
7. return same-device redirect, cross-device URI/QR, or platform Digital Credentials API input;
8. persist request digest/policy/context, not unnecessary claim values.

### Supported transports

- same-device redirect/app link;
- cross-device QR/deep link;
- request object by value or URI according to profile;
- request URI POST/capability negotiation where supported;
- W3C Digital Credentials API only on supported platforms with exact expected-origin and response-mode rules;
- no email/SMS embedding of long-lived bearer presentation requests.

### Request security

- short expiry and single-use;
- exact response URI allowlist, no open redirect;
- JAR/signature and metadata integrity where profile requires;
- QR contains no personal data and is resistant to session swapping;
- bind browser/application session without requiring third-party cookies;
- prevent a malicious site/app from replaying a request under a different origin.

## 7. DCQL and Data Minimization

### Policy-authoring requirements

- each credential and claim query has a stable semantic ID and documented purpose;
- required versus optional claims are explicit;
- credential sets express alternatives without forcing multiple credentials unnecessarily;
- trusted authority hints narrow likely acceptable credentials but do not replace server-side issuer trust verification;
- `values` constraints are used only when necessary and reviewed for probing/inference risk;
- prefer derived predicates (age-over, membership-valid, license-current) to raw dates/identifiers;
- avoid requesting name/address/identifier when a narrower eligibility fact suffices;
- transaction data references only credentials authorized for that transaction type.

### Runtime requirements

- validate final DCQL syntax and format-specific metadata constraints;
- accept only responses satisfying a defined query path and credential-set combination;
- reject extra credentials/claims unless the selected format necessarily includes them and policy explicitly permits processing;
- do not infer why a wallet returned no credential or holder declined;
- use indistinguishable user-facing/application errors where details could reveal possession or values;
- record requested/disclosed/retained claim categories and minimization delta without centralizing raw values.

## 8. Response and Presentation Validation Pipeline

1. resolve transaction atomically and reject unknown, expired, used, canceled, wrong-tenant, or context-mismatched responses;
2. validate state, nonce, response mode, origin, audience, response URI/channel, and encryption/signature container;
3. parse `vp_token` using only allowed format providers and bounded size/count/depth;
4. match presentations/credentials to DCQL IDs and allowed credential-set combination;
5. validate format-native credential/presentation cryptography, issuer key, type/schema/metadata, time, and critical fields;
6. validate selective-disclosure digests and reject unrequested/unknown disclosure handling according to policy;
7. validate holder/key/device binding and nonce/session transcript/transaction binding;
8. retrieve and validate status with required freshness/privacy/caching policy;
9. resolve issuer/trust framework/authority at the relevant time and purpose;
10. normalize allowed claims with provenance and evaluate claim/business constraints;
11. produce a result with explicit valid, invalid, indeterminate, canceled, or error status and stage reasons;
12. mark transaction consumed atomically, notify/callback relying application, and delete transient raw artifacts per retention.

No step may be skipped because a credential was produced by a known wallet or issuer.

## 9. Credential Format Verification

### SD-JWT VC

- pin the selected active draft/profile until standardized;
- validate issuer-signed JWT type/algorithm/key, type metadata, disclosures/digests, required claims, status, validity, and key binding;
- verify every disclosed digest and reject duplicate/conflicting/path-manipulated disclosures;
- validate key-binding JWT against holder key, verifier audience, nonce, issued time, and transaction context;
- treat decoy/undisclosed data safely and never log disclosures or salts;
- label production support according to the exact draft/profile evidence.

### W3C VC 2.0 / Verifiable Presentation

- validate conformance to VC Data Model 2.0 and selected securing mechanism;
- resolve issuer verification method and contexts/vocabularies/schema with pinned integrity and network safety;
- validate credential and presentation proofs, challenge/domain/audience, holder binding where required, validity, and status;
- distinguish proof authenticity from claim/trust/business validity;
- do not claim selective disclosure unless the selected cryptosuite/profile provides and proves it.

### mdoc

- validate CBOR/COSE structures, issuer authentication, MSO, digest mappings, certificate/path/profile, validity, requested namespaces/elements, device authentication/signature/MAC, session transcript, and reader/verifier binding;
- use exact ISO/HAIP profile rules and conformance vectors;
- reject JSON conversion as verification authority;
- retain only normalized allowed elements and minimum evidence.

## 10. Issuer Trust, Schemas, and Status

### Issuer trust

Trust policy answers: "Is this issuer authorized to assert this credential type for this purpose, jurisdiction, ecosystem, and time?"

- use direct configuration, trust registry, OpenID Federation, certificate chain, ecosystem list, or profile-specific method with explicit provenance;
- validate trust artifact signature/status/version/effective time and issuer/type scope;
- no transitive trust unless the framework explicitly defines and secures it;
- unknown/unreachable trust source yields indeterminate or fail-closed according to policy, never automatic acceptance.

### Schema/type metadata

- require exact type/configuration identifiers and compatible schema/type metadata;
- verify resource integrity and pin versions;
- do not dynamically execute JSON-LD/context/schema content;
- bound remote retrieval and protect against SSRF, context poisoning, semantic redefinition, oversized recursion, and stale cache;
- distinguish structural validation from semantic/business validation.

### Status

- support only status mechanisms declared by the format/profile and verifier policy;
- validate status resource authenticity, purpose, index, integrity, caching, and freshness;
- prevent per-holder correlation by preferring privacy-preserving list retrieval/caching;
- distinguish active, suspended, revoked, expired, superseded, unknown, source unavailable, and invalid status proof;
- do not accept cached good status beyond policy merely because the credential cryptography is valid.

## 11. Holder, Wallet, and Transaction Binding

- holder/key binding proves possession/control of a key associated with the credential/presentation; it does not independently identify a human;
- require fresh nonce and exact verifier/transaction audience/context;
- for mdoc, validate device authentication and session transcript;
- for SD-JWT VC, validate key-binding JWT when profile requires;
- for W3C presentations, validate holder proof/challenge/domain under selected suite;
- wallet/key attestation is appraised through Attestation Center and used only for declared assurance claims;
- avoid global wallet-instance identifiers and wallet-provider overtracking;
- validate recognized `transaction_data` type, canonical semantics, digest, credential binding, display text, and business transaction state;
- a presentation authorization must not be replayed for another amount/payee/order/purpose/session.

## 12. Verification Result Contract

Create a new `CredentialVerificationResult`, separate from API token `VerificationResult`.

Required fields:

- result ID/version, tenant, verifier/relying party, transaction, policy/version, purpose, and correlation;
- overall state: `verified`, `rejected`, `indeterminate`, `canceled`, or `error`;
- protocol, credential/presentation, issuer trust, schema/type, time, status, holder binding, transaction binding, and claim-policy stage results;
- normalized minimally necessary claims/facts with type, source credential query ID, provenance digest, and confidence/assurance labels supported by evidence;
- issuer/type/format/profile and safe subject/pseudonym reference where needed;
- issued/expiry times, audience, one-time/reuse rules, integrity signature/reference, and supersession/revocation;
- stable reason codes and redacted evidence references;
- retention/deletion classification.

Downstream applications should consume the result through a callback, one-time code exchange, signed result token/receipt, or authenticated query. A result token is audience-bound and non-bearer for unrelated APIs unless an explicit OAuth integration exchanges it under policy.

## 13. Relying-Party Integration

### Browser/app flow

- create transaction server-side;
- return redirect/QR/platform request to client;
- receive callback/webhook or poll safe transaction state;
- exchange a one-time result code through authenticated backend;
- use normalized result facts in business/policy decision;
- never send full raw presentation to the browser/business app by default.

### Authorization integration

- map result facts into a typed PolicyRequest context with policy/result version and maximum staleness;
- authorization policy determines allow/deny/step-up/manual review;
- result verification and authorization evidence remain linked but separate;
- no automatic account linking solely from email/name; use issuer/type/subject/pairwise binding policy;
- token issuance based on credential results must occur through Token Service/OAuth with explicit exchange/grant semantics.

### Webhooks/events

- signed/authenticated, replay-safe, ordered only per explicit sequence, and privacy-minimized;
- event indicates state transition/result reference, not raw claims;
- retry/idempotency/dead-letter and endpoint rotation;
- security events go through Security Signals where appropriate.

## 14. API Requirements

### Runtime transaction API

| Method | Proposed route | Purpose |
|---|---|---|
| `POST` | `/credential-verifier/v1/transactions` | Create a presentation transaction from an active policy/template. |
| `GET` | `/credential-verifier/v1/transactions/{id}` | Return safe state/next action to authorized caller. |
| `GET/POST` | profile-defined request URI | Serve or receive wallet capability/request interaction. |
| `POST` | profile-defined response endpoint | Receive OpenID4VP response. |
| `POST` | `/credential-verifier/v1/results:exchange` | Exchange one-time result code for minimal result. |
| `GET` | `/credential-verifier/v1/results/{id}` | Retrieve result under relying-party authorization. |
| `POST` | `/credential-verifier/v1/results/{id}:verify` | Validate result integrity/audience/current state. |
| `POST` | `/credential-verifier/v1/transactions/{id}:cancel` | Cancel unused transaction. |

Final public paths and methods must match OpenID4VP profile requirements; management convenience must not alter wire protocol.

### Management API

- `/admin/credential-verifier/policies`, `/templates`, `/relying-parties`, `/trust-sources`, `/issuers`, `/schemas`, `/status-providers`, `/formats`, `/keys`, `/transactions`, `/results`, `/incidents`, and `/reports`;
- validate/lint/simulate/submit/approve/publish/stage/rollback/supersede/suspend/retire;
- interoperability profiles and fixtures;
- privacy/retention/access/export policy;
- impact analysis for issuer/trust/schema/status/key/policy/profile changes.

### API invariants

- exact tenant/relying-party filtering before lookup;
- high-entropy single-use transaction/state/nonce/result codes;
- idempotent response handling and atomic consumption;
- raw presentations immutable and ephemeral/restricted;
- fail closed on unsupported critical format/transaction data/profile;
- stable reason codes with no holder-possession/claim-value oracle;
- no arbitrary production DCQL or trust override from browser clients.

## 15. Canonical Data Requirements

### Verification policy/version

- policy/template ID/version, tenant/relying party, purpose, lifecycle, locales, holder notice, owner, and legal/privacy basis;
- DCQL, formats/types/claims/sets, issuer/trust, schema, status, holder/wallet, transaction, result, retention, and failure policy;
- publication/approval/rollout/predecessor, fixtures, compatibility, and evidence.

### Presentation transaction

- transaction ID, tenant, relying party/session, policy, purpose, state/nonce digests, request digest/URI, origin/response mode/URI, created/expiry/consumed/canceled, and status;
- wallet capability/profile metadata only as needed;
- response/presentation digest/reference, stage results, result ID, errors, attempts, correlation, and audit;
- no raw state/nonce/result code after use and no holder inventory inference.

### Credential verification result

- contract from Section 12 with normalized claims encrypted/segmented by sensitivity;
- evidence digests/references and exact dependency versions;
- result access/audience, expiry, consumption, revocation/supersession, and deletion time;
- no unnecessary complete credential/presentation copy.

### Trust/schema/status cache

- source, resource identifier, type, version/digest, issuer/signature, effective/expiry/fetch/cache times, status, and validation;
- tenant/policy assignments, predecessor, provenance, and impact;
- sanitized parsed content and restricted raw artifact where needed.

## 16. Verification Console UIX

### Overview

- transactions/results by verified/rejected/indeterminate/canceled/error;
- stage failure trends, issuer/trust/status/schema/provider health, response latency, and privacy/retention posture;
- policy/version adoption and interoperability results;
- critical actions for compromised issuer/key/trust source, stale status, replay spike, overbroad policy, raw-evidence retention, and dependency outage.

### Request/policy builder

1. define relying party, business purpose, holder-facing notice, and downstream decision;
2. select accepted credential types/formats/trust frameworks;
3. build DCQL credential/claim/set requirements;
4. mark required/optional and minimize claims;
5. set status, holder/wallet/transaction binding and freshness;
6. define normalized result and retention;
7. simulate wallets/credentials and privacy/linkability impact;
8. review, approve, stage, publish.

### DCQL and disclosure preview

- semantic tree/table of requested credentials, alternatives, claims, values, and trusted-authority hints;
- holder-facing exact request preview;
- requested versus expected retained facts;
- warnings for raw identifiers, birth date instead of age predicate, address overreach, repeated `values` probes, small issuer cohort, mandatory format disclosures, and transaction ambiguity;
- code/raw JSON view secondary to guided semantic view.

### Verification inspector

- timeline: request created/served, response received, protocol validated, presentation parsed, format proof, issuer trust, schema/type, time, status, holder/transaction binding, claim appraisal, result issued/consumed;
- per-stage valid/invalid/indeterminate/error with key/source/version/time and stable reasons;
- disclosed claims masked and access-controlled;
- credential/presentation raw view restricted, audited, and retention-aware;
- result/downstream policy link without conflating decisions.

### Trust and incident operations

- issuer/type/purpose trust matrix and source provenance;
- schema/type/status/key cache health and semantic diffs;
- simulate and calculate affected policies/results/transactions before trust changes;
- suspend verifier policy/issuer/source, revoke results, notify relying parties, and trigger Security Signals;
- redacted evidence bundle and verified containment state.

### Interoperability lab

- exact OpenID4VP Final/HAIP/format/profile versions;
- reference wallet fixtures for same-device/cross-device/request URI/DC API;
- valid and adversarial presentations;
- capability badges tied to evidence, not vendor logo;
- no production holder credential upload to a casual decoder.

## 17. Security, Privacy, and Reliability

- Protect verifier signing/encryption keys in KMS/HSM and rotate with request/result compatibility.
- Validate request/response context to prevent replay, injection, mix-up, session swapping, malicious QR, open redirect, origin confusion, and response endpoint substitution.
- Harden request URI, metadata, trust, schema/context, status, and key retrieval against SSRF, DNS rebinding, redirect/downgrade, oversized content, stale cache, and compromised sources.
- Strictly type JWT/COSE/proof artifacts and reject algorithm/credential/token confusion.
- Bound request, response, credential, disclosure, CBOR/JSON/JSON-LD, claim, nesting, and cryptographic workloads.
- Do not expose distinct errors/timing that reveal credential possession, values, or holder decline.
- Encrypt raw presentations/claims at rest, keep them ephemeral by default, audit privileged reveal/export, and delete on schedule.
- Separate result facts by relying party/audience and use pairwise subject mapping where required.
- Prevent issuer/verifier collusion and cross-context correlation through unnecessary stable identifiers/logs.
- Use atomic one-time state and idempotent response/result processing.
- Define fail-closed versus indeterminate for status/trust dependencies; support circuit breakers, retry/backoff, queues, regional failover, and clock controls.
- Monitor repeated probing, verifier abuse, replay, invalid format, trust changes, status outages, and result misuse through Security Signals.

## 18. Stakeholder Requirements

### Technical marketing

- demonstrate minimal age/membership/license/eligibility verification, stage-by-stage trust, and downstream policy without retaining full credentials;
- explain cryptographic validity versus issuer trust versus business decision;
- show same/cross-device and privacy-friendly predicate use;
- prepare stories for onboarding/KYC support, hiring, education, professional licensing, healthcare eligibility, age assurance, travel/government, delegated authority, and device/workload compliance.

### Developer relations

- publish transaction creation, redirect/QR/DC API, callback/result exchange, DCQL, trust/status, and error quickstarts;
- provide reference wallet and credential fixtures for SD-JWT VC/W3C VC/mdoc only as implemented;
- include adversarial tests for wrong nonce/audience/origin/issuer/key/status, replay, extra disclosures, malformed digest, untrusted issuer, stale source, and claim probing;
- document exact profile versions, result schema, retention, webhook, and authorization integration.

### Sales and account management

- use an assessment for purpose, decisions, credentials/formats, issuers/trust, wallets, claims/minimization, status, holder binding, transaction data, volume, latency, retention, legal/privacy, region, and integrations;
- provide readiness report separating request, wallet, format, trust, status, result, decision, operations, and interoperability;
- define RACI for verifier, relying party, issuer, wallet, trust registry, status provider, policy owner, privacy owner, and incident support;
- avoid claiming full identity/KYC/legal assurance from one credential verification without program evidence.

### GTM strategist

- package Verification Policies/DCQL, Trust and Status, High-Assurance/HAIP, Transaction Authorization, and Verification Operations separately;
- lead with minimal claim/predicate verification for horizontal use cases;
- pair with Credential Issuer/Wallet, Trust Registry, Policy Studio, Token Service, and Security Signals;
- meter verification transactions, active policies/relying parties, trust sources, advanced formats, retention, or governance tier while discouraging neither minimization nor invalid rejection.

### Copywriter

- distinguish presentation request, credential, presentation, disclosure, holder proof, issuer trust, status, verification result, and business/authorization decision;
- say "verified under policy X" rather than "identity verified" without scope;
- label invalid, rejected, indeterminate, canceled, and system error accurately;
- state purpose, requested/retained claims, trust basis, status age, and result expiry;
- avoid inferring that decline/no-match means the holder lacks a credential or claim.

## 19. Delivery Instructions

### Frontend engineer

- generate typed management/transaction clients; all protocol/format/trust/status verification remains server-side;
- prevent raw credentials/presentations/disclosures/stable subject identifiers from URLs, analytics, browser logs, local storage, notifications, and ordinary exports;
- render server-returned DCQL semantics, stages, reasons, provenance, status freshness, trust, and result;
- support QR plus accessible link/code alternatives, background transaction state, expiration, callback races, stale policy, and partial dependency failure;
- add automated tests for no claim/credential telemetry and safe error indistinguishability;
- instrument stage latency/outcomes using opaque IDs and safe categories.

### UIX designer

- make requested, disclosed, retained, and derived claims visually distinct;
- separate protocol validity, credential validity, trust, status, holder binding, policy, and downstream decision;
- design empty, request ready/expired, waiting, response received, verifying, verified, rejected, indeterminate, canceled, dependency unavailable, result expired/revoked, and incident states;
- provide accessible DCQL tree/table, QR alternatives, claim masking, semantic diffs, and stage timelines;
- require privacy/impact review for claim expansion, `values`, transaction data, trust/status fallback, raw retention, and result reuse;
- meet WCAG 2.2 AA with keyboard operation, non-color status, focus, screen-reader privacy, localization, and reduced motion.

### Copywriter

- create purpose/request/DCQL, trust, status, verification-stage, result, error, remediation, confirmation, privacy, incident, and recovery catalogs;
- write holder-facing request copy separately from operator/developer copy;
- ensure errors do not leak possession/value/decline while still supporting authorized operators;
- explain status/trust dependency uncertainty and retry policy;
- calibrate interoperability/legal/assurance claims to evidence.

## 20. Delivery Phases

### Phase 1: Result contract and one verification profile

- canonical `CredentialVerificationResult`, policy, transaction, trust/status cache, evidence, reason, and retention contracts;
- OpenID4VP Final same/cross-device request/response and DCQL;
- one production credential-format verifier and reference wallet fixtures;
- minimal result exchange and downstream policy integration.

### Phase 2: Console, trust, and status

- policy builder/simulation, verifier metadata/keys, issuer/type trust, status, schema/type metadata, Verification Console, incidents, privacy/retention, and interoperability lab;
- Digital Credentials API where supported.

### Phase 3: High assurance/additional formats

- HAIP-selected profile, wallet/key attestation, SD-JWT VC stabilization, mdoc or W3C VC profile, transaction data, and certified ecosystem tests;
- result-to-OAuth exchange only through explicit Token Service integration.

### Phase 4: Vertical relying-party packs

- age/eligibility, workforce, education/license, healthcare, finance/onboarding, government/travel, delegated authority, and device/workload verification;
- jurisdiction-specific trust, claims, retention, accessibility, fraud, and legal evidence.

## 21. Acceptance Criteria

### API/runtime

- A reference wallet can complete supported OpenID4VP/DCQL flow and yield an audience/purpose-bound minimal result.
- Wrong/expired/replayed state/nonce/request/response/origin/audience/issuer/key/status/holder/transaction/context fails without result acceptance.
- Every accepted claim links to format proof, credential/type, issuer trust, status, policy constraint, and transaction.
- Extra disclosures are rejected or excluded according to explicit policy and never silently retained.
- Indeterminate dependency/unsupported states cannot become verified.
- Raw presentations are ephemeral/restricted and downstream apps receive only the defined result.
- Credential verification package boundaries remain outside authz decisions.

### UIX

- Admins can define and simulate a minimal purpose-bound policy without hand-authoring raw DCQL.
- Requested/disclosed/retained/derived facts and linkability are clear.
- Operators can locate the exact failing/indeterminate stage and source version.
- Trust/status/policy changes show affected transactions/results/relying parties before activation.
- Critical flows work accessibly without QR, graphs, raw JSON, or color alone.

### Evidence/business

- DevRel can run deterministic positive/adversarial OpenID4VP and format fixtures.
- Technical marketing can demonstrate minimal verification using synthetic credentials.
- Sales can provide readiness/RACI without raw holder presentations.
- OpenID4VP/HAIP/format/wallet/trust/legal-assurance claims link to pinned certified evidence.

## 22. Success Measures

- transaction creation, wallet response, protocol, format, trust, status, binding, policy, and result success by safe reason;
- time per verification stage and end-to-result latency;
- requested versus disclosed versus retained claim count;
- predicate versus raw-attribute use and privacy-review findings;
- replay/extra-disclosure/untrusted-issuer/stale-status/claim-probing detection;
- indeterminate/dependency outage/false rejection/manual override rate;
- result consumption/reuse/expiry/revocation posture;
- raw presentation retention/access/export and deletion compliance;
- wallet/issuer/format interoperability pass rate and support time;
- cross-tenant disclosure, false verification, or result misuse incidents.

Guardrails include false verification, trust overreach, stale status, holder-binding failure, transaction replay, overcollection, possession/value leakage, cross-context correlation, raw presentation sprawl, accessibility failure, and overstated assurance.

## 23. Source Evidence

### Repository

- `tests/planned/identity_model/credential-verification-result.md`;
- `tests/planned/policy_boundary/boundary-no-credential-verification.md`;
- `docs/architecture/AUTH_PACKAGE_TAXONOMY.md`;
- OAuth/OIDC/RP, JOSE, resource validation, trust/federation, policy, storage, audit/provenance, UIX core, attestation, and security-signal foundations;
- Credential Issuer and Wallet pairing briefs;
- repository scans showing no current OpenID4VP/DCQL/digital credential verifier implementation.

### Standards and primary sources

- [OpenID for Verifiable Presentations 1.0 Final](https://openid.net/specs/openid-4-verifiable-presentations-1_0-final.html)
- [OpenID4VC High Assurance Interoperability Profile 1.0 Final](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0-final.html)
- [OpenID for Verifiable Credential Issuance 1.0 Final](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0-final.html)
- [W3C Verifiable Credentials Data Model 2.0](https://www.w3.org/TR/vc-data-model-2.0/)
- [W3C Verifiable Credential Data Integrity 1.0](https://www.w3.org/TR/vc-data-integrity/)
- [W3C Bitstring Status List v1.0](https://www.w3.org/TR/vc-bitstring-status-list/)
- [RFC 9901: Selective Disclosure for JWTs](https://www.rfc-editor.org/rfc/rfc9901)
- [SD-JWT-based Verifiable Digital Credentials, active Internet-Draft](https://datatracker.ietf.org/doc/draft-ietf-oauth-sd-jwt-vc/)
- applicable ISO/IEC 18013-5 and 18013-7 documents for mdoc.

## 24. Explicit Non-Claims

This brief does not claim that the current repository:

- implements OpenID4VP, DCQL, `vp_token`, Digital Credentials API, or a credential verifier;
- verifies SD-JWT VC, W3C VC/VP, or mdoc presentations;
- has issuer trust registries, schema/type metadata, credential status, wallet/holder binding, or transaction verification;
- provides a digital `CredentialVerificationResult` implementation;
- can reuse API access-token verification as credential presentation verification;
- interoperates with production wallets/issuers/government or regulated ecosystems;
- makes a credential claim true or authorizes access solely because its cryptographic proof validates;
- provides anonymous, zero-knowledge, KYC, identity-proofing, or legal assurance by default.

Those claims require protocol/format implementations, issuer/status/trust policy, holder/transaction binding, privacy-minimized result contracts, adversarial/interoperability tests, legal/program analysis, operational proof, and release certification.
