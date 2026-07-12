# Identity, Authorization, Credential, and Attestation Vocabulary Gap Audit

Status: repository audit and implementation-planning document

Date: 2026-07-11

Scope: `tigrbl_auth` OAuth, OpenID Connect, identity-assurance, authorization-policy, verifiable-credential, decentralized-identity, zero-trust, workload-identity, and attestation vocabulary

## Executive summary

The repository has substantial OAuth 2.0, OpenID Connect, JOSE, and JWT coverage. Its retained certification boundary includes OAuth authorization-server behavior, bearer tokens, PKCE, metadata, revocation, introspection, dynamic client registration, native and device flows, token exchange, mTLS, resource indicators, JWT access tokens, JAR, PAR, issuer identification, Rich Authorization Requests, DPoP, protected-resource metadata, the OAuth Security BCP, OIDC Core, Discovery, UserInfo, session management, and the principal logout specifications.

The repository does not yet have equivalent standards surfaces for:

- XACML or the OpenID AuthZEN Authorization API;
- zero-trust architecture vocabulary;
- DIDs and DID resolution;
- eKYC and identity assurance;
- OIDC EAP ACR values;
- W3C Verifiable Credentials Data Model 2.0;
- SD-JWT and SD-JWT VC;
- ISO mdoc;
- OpenID4VCI, OpenID4VP, or HAIP;
- CWT/COSE credential and attestation profiles;
- EAT and CoRIM;
- SPIFFE SVID workload identity; or
- complete SET, GNAP, and adjacent shared-signals protocol surfaces.

These technologies are not interchangeable. They occupy different layers: cryptographic envelopes, claims containers, credentials, event messages, attestation evidence, workload identities, authorization protocols, and trust documents. The repository should model those layers explicitly rather than treating every signed object as a JWT variation inside the OAuth/OIDC boundary.

### Immediate correctness defect

The repository currently labels the Security Event Token as **RFC 7952**. This is incorrect:

- Security Event Token (SET) is **RFC 8417**.
- RFC 7952 is **Defining and Using Metadata with YANG**.

The incorrect association originates in `compliance/targets/extension-targets.yaml` and is propagated through certification scope, target mappings, feature flags, runtime product surfaces, and claims/evidence registries. It should be corrected as a dedicated change before SET coverage is expanded. A migration or compatibility alias may be necessary for stored feature/claim identifiers, but no compliance output should continue to claim that RFC 7952 defines SET.

## 1. How the standards fit together

### 1.1 Layer model

| Layer | Purpose | Representative technologies |
|---|---|---|
| Cryptographic primitive or envelope | Sign, MAC, or encrypt bytes and bind protected headers | JWS/JWE, COSE, X.509 signatures |
| General claims container | Carry named claims in a signed or encrypted object | JWT, CWT |
| Selective-disclosure credential | Let a holder disclose only selected issuer-signed claims | SD-JWT VC, ISO mdoc |
| General credential data model | Describe issuers, subjects, holders, credentials, presentations, status, and schemas | W3C VC Data Model |
| Issuance protocol | Authorize and deliver credentials to a wallet | OpenID4VCI |
| Presentation protocol | Request and return credentials or presentations | OpenID4VP |
| Interoperability profile | Select algorithms, flows, formats, and security requirements | OpenID4VC HAIP |
| Security-event message | Notify receivers that a security event occurred | SET |
| Attestation evidence | Report device, workload, software, or boot-state claims | EAT |
| Attestation reference/endorsement material | Describe expected measurements or endorsed characteristics | CoRIM/CoMID |
| Workload identity | Identify a workload in a trust domain | X.509-SVID, JWT-SVID |
| Authorization protocol | Negotiate or convey delegated access | OAuth, GNAP |
| Authorization decision API/model | Ask whether a subject may perform an action on a resource | AuthZEN, XACML |
| Decentralized identifier document | Resolve controllers, verification methods, and services | DID/DID document |
| Public-key trust credential | Bind a public key to an identity under a PKI | X.509 certificate |

### 1.2 Why “any signed token suffices” is unsafe

A valid signature answers only a limited question: whether the protected bytes validate under a particular key and algorithm. It does not establish:

- that the token type is acceptable in the current protocol;
- that the issuer is trusted for the asserted subject or claim;
- that the audience, nonce, transaction, or channel binding is correct;
- that required disclosure, holder-binding, or device-binding rules were followed;
- that the credential is currently valid and not revoked or suspended;
- that attestation evidence was appraised against trusted reference values;
- that an X.509 chain satisfies the intended EKU, name constraints, policy, or trust domain; or
- that an authorization grant or policy decision exists.

Every accepted object therefore needs an explicit type/profile discriminator, validation policy, trust-resolution mechanism, replay policy, and protocol context.

## 2. Terminology

### 2.1 SET — Security Event Token

A SET is a JWT whose claims describe one or more security events. Typical uses include account disablement, session revocation, credential compromise, device events, and risk-state changes. Its important vocabulary includes:

- `events`: a JSON object keyed by event-type URI;
- event type and event-specific payload;
- `iss`, `aud`, `iat`, and `jti` delivery/security claims;
- subject identifiers, often represented using the Subject Identifiers for Security Event Tokens specification;
- transmitter and receiver;
- push and polling delivery profiles;
- acknowledgement, retry, deduplication, replay, and retention policy.

A SET is not an access token and should not be accepted by an OAuth resource server merely because it is a valid JWT.

### 2.2 EAT — Entity Attestation Token

An Entity Attestation Token carries claims about an entity and its execution environment. The entity can be a device, hardware component, workload, enclave, or software instance. Relevant concepts include:

- attester, verifier, relying party, and endorser;
- evidence, attestation result, endorsements, and reference values;
- nonce/freshness;
- UEID and other entity identifiers;
- boot and debug state;
- hardware, software, OEM, model, and lifecycle claims;
- submodules and layered/composite environments;
- measurements and measurement results;
- JWT and CWT serializations;
- appraisal policy and trustworthiness vector.

EAT proves neither user identity nor authorization by itself. A verifier appraises EAT evidence and produces a result that a relying party can use in a separate decision.

### 2.3 CoRIM and CoMID

CoRIM means **Concise Reference Integrity Manifest**. It packages signed attestation reference material. CoMID means **Concise Module Identifier** and represents measurements, reference values, endorsements, and related triples for environments or components.

Important vocabulary includes:

- CoRIM signer and signed manifest;
- CoMID tag;
- environment, class, instance, and group identity;
- measurement maps;
- reference values;
- endorsed values;
- verification keys;
- conditional endorsement series;
- validity period;
- dependency and supply-chain relationships.

CoRIM is not normally presented as the live evidence from a device. It is trusted reference or endorsement material used while appraising evidence such as EAT claims.

### 2.4 GNAP

GNAP is the **Grant Negotiation and Authorization Protocol**. It is adjacent to OAuth, not an OAuth grant type. Its model includes:

- grant request and continuation;
- client instance and client key;
- proof methods;
- requested access rights;
- resource server;
- interaction start and finish modes;
- user-facing and redirect interaction;
- subject information;
- access-token response and token management;
- token rotation and continuation access token;
- detached JWS and HTTP message proof considerations.

GNAP should be tracked as its own protocol family, with the resource-server profile represented separately from the authorization-server negotiation flow.

### 2.5 SVID and SPIFFE

An SVID is a **SPIFFE Verifiable Identity Document**. It identifies a workload within a SPIFFE trust domain.

- A SPIFFE ID is a URI such as `spiffe://example.org/service/api`.
- An X.509-SVID is an X.509 certificate containing the SPIFFE ID and an associated private key and trust bundle.
- A JWT-SVID is a JWT containing the SPIFFE ID as subject and an explicitly requested audience.
- The Workload API delivers identities and bundles to workloads.
- A trust domain and trust bundle establish workload-identity trust roots.
- Federation connects trust domains.

JWT-SVID and X.509-SVID are alternative workload-identity presentations for particular channels; they are not general replacements for user ID Tokens, VC credentials, or OAuth access tokens.

### 2.6 XACML spelling

The correct acronym is **XACML**, the eXtensible Access Control Markup Language. “XCAML” is a transposition and should not be introduced into package, target, or public API names.

### 2.7 “W3C VCD” ambiguity

There is no principal W3C identity specification commonly abbreviated “VCD.” The intended term is likely one of:

- **VCDM** — Verifiable Credentials Data Model;
- **VC Data Integrity** — the securing-mechanism framework for linked-data proofs; or
- **VC DI** — informal shorthand for Verifiable Credential Data Integrity.

This audit covers both VCDM 2.0 and the need to select one or more securing mechanisms.

## 3. Existing repository coverage

The retained OAuth/OIDC/JOSE boundary is represented primarily in:

- `compliance/targets/rfc-targets.yaml`;
- `compliance/targets/oidc-targets.yaml`;
- `compliance/targets/extension-targets.yaml`;
- `compliance/targets/alignment-targets.yaml`;
- `pkgs/50-protocols/tigrbl-auth-protocol-oauth`;
- `pkgs/50-protocols/tigrbl-auth-protocol-oidc`; and
- the associated compliance mappings, tests, evidence, and generated reports.

Implemented/tracked OAuth vocabulary includes authorization and token endpoints, bearer-token use, PKCE, authorization-server metadata, protected-resource metadata, revocation, introspection, dynamic registration and registration management, native apps, device authorization, token exchange, mTLS client authentication and certificate-bound tokens, resource indicators, JWT access tokens, JAR, PAR, issuer identification, RAR `authorization_details`, DPoP, assertion grants/client authentication, and the OAuth Security BCP.

Implemented/tracked OIDC vocabulary includes Core, ID Tokens, Discovery, UserInfo, session management, RP-initiated logout, front-channel logout, and back-channel logout.

Some generic federation storage/contracts exist, and an OIDC federation provider abstraction exists, but this is not yet evidence of complete OpenID Federation protocol or conformance coverage.

## 4. XACML vocabulary gap

### 4.1 Core architectural roles

Add explicit concepts for:

- **Policy Administration Point (PAP):** creates and manages policy;
- **Policy Decision Point (PDP):** evaluates a request against policy;
- **Policy Enforcement Point (PEP):** intercepts an attempted operation and enforces the decision;
- **Policy Information Point (PIP):** supplies attributes needed for evaluation;
- **Context Handler:** converts native requests and responses to and from the XACML context model.

### 4.2 Policy language

Add:

- `PolicySet`, `Policy`, and `Rule`;
- policy/rule identifiers and versions;
- `Target`, `AnyOf`, `AllOf`, and `Match`;
- `Condition`;
- `Effect`: `Permit` or `Deny`;
- expressions, functions, bags, and higher-order functions;
- attribute values and data types;
- `AttributeDesignator` and `AttributeSelector`;
- variable definitions and references;
- policy and policy-set references;
- combining algorithms and combining parameters;
- `ObligationExpression` and `AdviceExpression`.

### 4.3 Request/response context

Add:

- request categories for subject/access-subject, resource, action, and environment;
- `Attributes`, `Attribute`, issuer, value, category, and inclusion in result;
- single and multiple-decision requests;
- `RequestReference` and `AttributesReference`;
- decision values `Permit`, `Deny`, `NotApplicable`, and `Indeterminate`;
- response `Result`, `Status`, obligations, advice, attributes, and policy identifier list;
- missing-attribute, syntax-error, and processing-error status detail.

### 4.4 Boundary guidance

XACML is a policy language and evaluation model. The repository should not require XML throughout its internal authorization interfaces. Internal subject/resource/action/context contracts can be representation-neutral, while an XACML adapter owns XML parsing, policy semantics, combining behavior, and XACML response serialization.

## 5. AuthZEN vocabulary gap

OpenID AuthZEN Authorization API 1.0 standardizes communication between PEPs and PDPs without requiring a common internal policy language.

Add:

- subject, resource, action, and context entities;
- entity type and ID conventions;
- access-evaluation request and response;
- Boolean decision and optional evaluation context;
- multiple/boxcar evaluation requests;
- subject search, resource search, and action search;
- search semantics when the queried entity identifier is omitted;
- pagination request, limit, continuation/next token, and stable subsequent-page parameters;
- API versioning;
- PDP metadata discovery;
- PDP capability registry values;
- `authzen` well-known URI and URN vocabulary;
- authentication and authorization of PEP-to-PDP calls;
- error responses, invalid requests, unavailable attributes, and partial failure policy.

AuthZEN and XACML overlap at the PDP/PEP boundary but are not synonyms. AuthZEN can front an XACML PDP, a relationship-based engine, an attribute-based engine, or application-specific policy logic.

## 6. OAuth vocabulary gap

### 6.1 Current strengths

The repository already covers most modern OAuth authorization-server fundamentals. New work should preserve the existing RFC-target structure rather than duplicate constants in a parallel vocabulary module.

### 6.2 Missing or incomplete targets

Candidate additions include:

- OAuth step-up authentication challenge, including `insufficient_user_authentication`, `acr_values`, and `max_age`;
- JWT Secured Authorization Response Mode (JARM);
- CIBA where its grant and token behavior intersects OAuth;
- attestation-based client authentication and client-instance identity;
- browser-based application terminology, backend-for-frontend, and token-mediating backend patterns;
- transaction tokens and transaction-scoped authorization context;
- token status lists where required by credential ecosystems;
- ACE-OAuth profiles if constrained-device support is in scope;
- CWT access-token profiles if CBOR ecosystems are in scope;
- richer authorization-detail type registration and per-type validation;
- authorization-server and protected-resource metadata extensions required by OID4VCI/OID4VP;
- explicit sender-constraint negotiation and downgrade prevention across mTLS and DPoP.

### 6.3 OAuth versus GNAP

Do not represent GNAP concepts as OAuth extension grants. GNAP has a different request, client-instance, interaction, continuation, and key-proof model. Shared internal abstractions may include access rights, resources, subject information, keys, and issued tokens, but each protocol owns its wire vocabulary and state machine.

## 7. OpenID Connect vocabulary gap

### 7.1 Core vocabulary that should be made explicit

Even where behavior exists, the public standards vocabulary should consistently expose:

- issuer, subject, audience, authorized party, nonce, authentication time;
- `acr`, `amr`, `max_age`, prompt, login hint, and ID token hint;
- essential versus voluntary claims;
- aggregated and distributed claims;
- pairwise versus public subject identifiers;
- sector identifier;
- claims and UI locales;
- signed/encrypted UserInfo and ID Tokens;
- request object and request URI;
- client authentication methods;
- OP and RP roles;
- front-channel, back-channel, and RP-initiated logout distinctions.

### 7.2 Missing extension families

Add separate targets or profiles for:

- JARM;
- CIBA;
- OpenID Federation, including entity statements, trust anchors, trust chains, metadata policy, federation endpoints, and subordinate/superior relationships;
- FAPI profiles;
- Shared Signals, RISC, and CAEP;
- Security Event Token subject identifiers and delivery;
- OIDC EAP ACR Values;
- eKYC and Identity Assurance;
- Self-Issued OpenID Provider and wallet/provider attestation;
- native SSO where required;
- OpenID4VCI and OpenID4VP;
- HAIP.

## 8. Zero Trust Architecture vocabulary gap

Zero trust is an architectural decision model, not a token format or synonym for mTLS.

### 8.1 Entities and roles

Add:

- subject, user, workload, service, device, asset, and enterprise resource;
- policy engine;
- policy administrator;
- policy enforcement point;
- identity provider and credential authority;
- continuous diagnostics and mitigation system;
- security analytics and threat-intelligence sources;
- data-access policy and resource owner;
- control plane and data plane.

### 8.2 Signals and decisions

Add:

- identity assurance;
- authenticator assurance;
- device identity, inventory state, configuration, compliance, and health;
- workload identity and software provenance;
- location, network, time, behavioral, threat, and environmental signals;
- resource sensitivity and requested action;
- risk score and confidence;
- trust algorithm;
- policy input, decision, obligation, and enforcement action;
- continuous evaluation, session reauthorization, and revocation;
- signal freshness, provenance, integrity, and failure policy.

### 8.3 Deployment models

Represent:

- identity-governed access;
- microsegmentation;
- software-defined perimeter;
- identity-aware proxy;
- resource portal/gateway;
- agent/gateway and enclave models;
- least privilege, just-in-time access, and just-enough access.

No component should claim “zero trust compliance” solely because it validates JWTs, uses TLS, or supports DPoP.

## 9. DID vocabulary gap

### 9.1 Identifier model

Add:

- DID;
- DID scheme;
- DID method;
- method-specific identifier;
- DID URL;
- path, query, fragment, and DID parameters;
- relative DID URL.

### 9.2 DID document model

Add:

- DID subject;
- controller;
- DID document;
- verification method;
- verification material, including multibase/JWK forms selected by supported suites;
- service and service endpoint;
- `alsoKnownAs`;
- verification relationships: `authentication`, `assertionMethod`, `keyAgreement`, `capabilityInvocation`, and `capabilityDelegation`.

### 9.3 Resolution and lifecycle

Add:

- DID resolution and DID URL dereferencing;
- resolution input metadata;
- DID document metadata;
- resolution metadata;
- representation and media type;
- method operations: create, read/resolve, update, and deactivate;
- `created`, `updated`, `deactivated`, `nextUpdate`, `versionId`, and `nextVersionId`;
- equivalent ID and canonical ID;
- key rotation, recovery, delegation, and controller authorization;
- method-specific trust and security policy.

DID Core does not define a universal registry, credential issuance protocol, wallet, proof suite, or trust policy. Those must be selected independently.

## 10. OIDC Extended Authentication Profile ACR Values 1.0

This final specification defines interoperable requests for phishing-resistant authentication and phishing-resistant authentication using hardware-protected keys, plus a related proof-of-possession authentication-method value.

Required repository additions include:

- constants for the registered ACR values;
- the registered proof-of-possession AMR value;
- discovery publication through `acr_values_supported`;
- client request support through `acr_values` and the claims parameter;
- policy mapping from local authentication ceremonies to each requested ACR;
- ID Token `acr` and `amr` emission;
- failure/downgrade behavior when the requested class cannot be satisfied;
- validation that “phishing resistant” and “hardware protected” are backed by authenticator evidence rather than configuration labels;
- positive and negative tests for WebAuthn/FIDO or other satisfying authenticators.

Authentication context is not identity-proofing assurance. EAP ACR answers how the current authentication was performed; Identity Assurance describes how identity claims were verified and maintained.

## 11. eKYC and Identity Assurance

The OIDF Identity Assurance work consists of three complementary final specifications:

1. OpenID Identity Assurance Schema Definition 1.0;
2. OpenID Connect for Identity Assurance Claims Registration 1.0; and
3. OpenID Connect for Identity Assurance 1.0.

### 11.1 Identity Assurance Claims Registration

Add the registered natural-person claims defined by the claims-registration specification, covering categories such as:

- person name and name components;
- birth name and place/date of birth;
- sex/gender claims where applicable;
- address and locality claims;
- nationality and citizenship;
- personal identifiers;
- identity-document-related identifiers;
- jurisdiction-specific claims.

The implementation should preserve exact registered spellings and types from the final specification. It should not invent near-synonyms or silently map jurisdictional identifiers into generic `sub`.

### 11.2 Identity Assurance Schema Definition

Add:

- `verified_claims`;
- claims coupled with assurance metadata;
- assurance level;
- trust framework;
- verification process;
- verification time;
- evidence;
- verification method/check;
- identity-document evidence and document details;
- electronic record/eID evidence;
- utility-bill, voucher, or attestation evidence when supported;
- issuer, verifier, organization, country, and jurisdiction details;
- document type, number, issuer, issue date, expiry date, and validity checks;
- evidence attachments/references where selected by profile;
- extensible predefined-value registries.

### 11.3 OIDC protocol integration

Add:

- requesting verified claims through the OIDC claims parameter;
- returning verified claims in ID Token or UserInfo as permitted;
- OP metadata advertising support;
- client metadata and registration controls;
- transaction-specific purpose;
- consent and purpose limitation;
- claim minimization;
- handling essential requested assurance details;
- error behavior when requested evidence or assurance cannot be supplied;
- privacy controls around document numbers and evidence artifacts.

Identity Assurance metadata should be reusable from OID4VC credential payloads without making the OIDC protocol package the owner of the schema.

## 12. W3C Verifiable Credentials Data Model 2.0

### 12.1 Roles and objects

Add:

- issuer;
- holder;
- verifier;
- credential subject;
- verifiable credential;
- verifiable presentation;
- verifiable data registry as an abstract role;
- claim, property, value, and graph.

### 12.2 Core credential properties

Add:

- `@context`;
- `id`;
- `type`;
- `name` and `description` with language/direction support;
- `issuer`;
- `credentialSubject`;
- `validFrom` and `validUntil`;
- `credentialStatus`;
- `credentialSchema`;
- securing mechanism/proof representation;
- `relatedResource` and integrity metadata;
- `refreshService`;
- `termsOfUse`;
- `evidence`.

### 12.3 Presentation properties

Add:

- presentation holder;
- embedded `verifiableCredential` graph/container semantics;
- presentation type and identifier;
- presentation securing mechanism;
- audience/domain/challenge binding as defined by the selected securing mechanism or presentation protocol;
- verification of every embedded credential independently from verification of the presentation.

### 12.4 Processing requirements

Add:

- VC context v2 handling;
- protected JSON-LD term behavior;
- type-specific credential processing;
- unknown context/type policy;
- JSON-LD expansion/canonicalization only where required by the chosen securing mechanism;
- `application/vc` and `application/vp` media types;
- schema, status, validity, issuer trust, and fitness-for-purpose checks;
- Data Integrity and JOSE/COSE securing-mechanism adapters;
- privacy protections against identifier and signature correlation.

VCDM defines a data model. It does not itself prescribe OID4VCI, OID4VP, DID, SD-JWT VC, or ISO mdoc.

## 13. SD-JWT

### 13.1 Core selective-disclosure vocabulary

Add:

- issuer-signed JWT;
- disclosure;
- salt, claim name, and claim value disclosure forms;
- disclosure digest;
- `_sd` digest arrays;
- `_sd_alg`;
- array-element disclosure marker;
- decoy digest;
- combined serialization using issuer JWT, disclosures, and optional key-binding JWT;
- undisclosed, disclosed, and always-visible claims;
- disclosure selection;
- disclosure verification;
- duplicate digest and collision handling;
- recursive disclosure processing;
- key-binding JWT;
- `sd_hash`;
- nonce and audience binding;
- holder key and `cnf` binding.

### 13.2 Validation pipeline

A verifier must:

1. parse the combined serialization;
2. validate the issuer-signed JWT and its explicit token type/profile;
3. hash each disclosure using the declared/allowed algorithm;
4. match disclosures to digest locations without reuse or ambiguity;
5. reconstruct the disclosed claims;
6. reject forbidden or conflicting claim shapes;
7. validate key binding when policy requires it;
8. validate nonce, audience, time, issuer trust, status, and credential profile.

SD-JWT is a selective-disclosure envelope. SD-JWT VC adds credential-specific typing, metadata, trust, and validation rules.

## 14. SD-JWT VC

Add:

- `application/vc+sd-jwt` and the current registered/profile media-type rules;
- credential token-type marker required by the final/current profile;
- `vct` credential type;
- VCT metadata discovery;
- metadata integrity protection;
- display metadata;
- claim metadata and selective-disclosure policy;
- issuer identification and issuer-key resolution;
- `cnf` holder-key confirmation;
- credential status;
- reserved claims and collision rules;
- validity claims and clock handling;
- issuer-signed versus holder-bound validation;
- key-binding requirements selected by use case;
- integration with OID4VCI issuance and OID4VP presentation.

Because SD-JWT VC was still an IETF draft during parts of the repository’s earlier compliance work, its target must record the exact draft or RFC revision implemented. Do not emit an RFC compliance claim until the relevant document is an RFC and the implementation is updated to it.

## 15. ISO mdoc

ISO/IEC 18013-5 defines the mobile-document structures and exchange mechanisms used by mobile driving licences and generalized by related mdoc profiles.

### 15.1 Document vocabulary

Add:

- mdoc and mDL;
- document type (`docType`);
- namespace;
- data element identifier and value;
- issuer-signed item;
- issuer-signed namespaces;
- issuer authentication;
- Mobile Security Object (MSO);
- digest algorithm, digest ID, and value digest;
- validity information;
- device key information;
- device-signed namespaces;
- device authentication;
- document errors.

### 15.2 Session and exchange vocabulary

Add:

- device engagement;
- reader engagement;
- handover;
- session establishment;
- session transcript;
- ephemeral keys;
- reader authentication;
- items request;
- document request;
- requested data elements and intent to retain;
- `DeviceRequest` and `DeviceResponse`;
- status codes;
- online and offline retrieval modes;
- proximity and remote-presentation profile distinctions.

### 15.3 Validation requirements

Add:

- deterministic CBOR processing required by the profile;
- COSE signature/MAC validation;
- MSO-to-issuer-signed-item digest verification;
- issuer certificate-path and profile validation;
- namespace and element authorization;
- validity checking;
- session-transcript binding;
- reader-authentication validation when present;
- device-authentication and device-key validation;
- replay prevention;
- selective-release and user-consent policy.

ISO standards text is licensed. Repository documentation and tests should use independently authored summaries and permissible test vectors, not copy normative ISO text or tables wholesale.

## 16. OpenID for Verifiable Credential Issuance

OpenID4VCI defines an API and OAuth-based authorization mechanisms for issuing credentials.

### 16.1 Discovery and configuration

Add:

- credential issuer identifier;
- credential issuer metadata;
- authorization-server metadata and selection;
- credential endpoint;
- nonce endpoint where applicable;
- deferred credential endpoint;
- notification endpoint;
- batch credential endpoint/support;
- credential configurations supported;
- credential configuration identifier;
- format-specific parameters for SD-JWT VC and mdoc;
- display, locale, claim, binding method, proof type, signing algorithm, and encryption metadata.

### 16.2 Credential offer and authorization

Add:

- credential offer by value or URI;
- offered credential configuration IDs;
- authorization code grant;
- pre-authorized code grant;
- pre-authorized code;
- transaction code;
- issuer state;
- `authorization_details` credential authorization detail;
- scope-to-credential mapping;
- redirect, wallet, and issuer correlation protections.

### 16.3 Proof and issuance

Add:

- proof object and proof type;
- proof JWT and supported alternatives;
- issuer nonce/freshness;
- wallet/holder key proof;
- credential request;
- credential response;
- response encryption;
- batch issuance;
- deferred issuance and transaction identifier;
- notification events;
- invalid-proof and nonce-refresh behavior;
- replay and duplicate issuance prevention.

### 16.4 Wallet and client trust

Add:

- wallet instance;
- wallet attestation;
- wallet-attestation proof of possession;
- client attestation and key binding where profiled;
- issuer policy for public/native wallets;
- key rotation and wallet-instance lifecycle;
- privacy-preserving client identification.

OpenID4VCI should reuse OAuth endpoint and authorization primitives, but credential issuance state and format validation need dedicated owners.

## 17. OpenID for Verifiable Presentations

OpenID4VP defines an OAuth-based mechanism for requesting and delivering credential presentations.

### 17.1 Request vocabulary

Add:

- verifier/client identifier and identifier scheme;
- wallet authorization endpoint/invocation;
- `vp_token` response type;
- nonce;
- state;
- response mode, including direct-post variants;
- request object and request URI;
- verifier metadata;
- presentation definition where supported;
- Digital Credentials Query Language (DCQL) query where supported by the selected revision;
- requested credential format, type, claims, alternatives, and trusted authorities;
- transaction data.

### 17.2 Response vocabulary

Add:

- `vp_token`;
- presentation submission when Presentation Exchange is used;
- encrypted authorization response;
- direct-post response endpoint;
- response code where the selected mode uses one;
- format-specific SD-JWT VC presentation;
- format-specific mdoc device response;
- error response and user-declined/unsatisfied request distinctions.

### 17.3 Validation and privacy

Add:

- request-object authenticity and verifier identity;
- nonce, state, audience/client, and transaction binding;
- response encryption requirements;
- credential query satisfaction;
- credential issuer trust;
- holder/device key binding;
- SD-JWT key-binding validation;
- mdoc session-transcript and device-authentication validation;
- replay detection;
- credential status;
- minimization, user consent, and over-disclosure detection;
- verifier/client-ID scheme policy.

OpenID4VP does not define credential semantics. Each accepted credential format needs an independent validator.

## 18. OpenID4VC High Assurance Interoperability Profile

HAIP selects constrained combinations of OpenID4VCI, OpenID4VP, SD-JWT VC, and ISO mdoc for high-assurance interoperability.

Add:

- explicit `haip-vci` and `haip-vp` conformance configurations;
- mandatory issuer, wallet, and verifier capabilities;
- permitted credential formats;
- required algorithms, curves, and key sizes;
- wallet-attestation support;
- holder/device key binding;
- proof and nonce rules;
- encrypted response requirements;
- request-object and metadata integrity requirements;
- certificate and trust-chain validation profiles;
- SD-JWT VC typing, key-binding, and metadata constraints;
- mdoc issuer authentication, device authentication, and transcript binding;
- credential-offer and authorization flow restrictions;
- verifier/client identifier scheme restrictions;
- replay, downgrade, and algorithm-confusion protections;
- interoperability and negative-test vectors.

HAIP is a profile, not a fifth implementation of issuance, presentation, SD-JWT, or mdoc. HAIP conformance should be computed from underlying target evidence plus HAIP-specific constraints.

## 19. CWT and COSE

If constrained-device or CBOR ecosystems are in scope, add:

- CWT integer and text claim labels;
- CBOR tag handling;
- COSE Sign1, Sign, Encrypt0, Encrypt, MAC0, and key structures as required;
- protected versus unprotected COSE headers;
- algorithm and key identifiers;
- external additional authenticated data;
- countersignatures where selected;
- CWT confirmation/key-binding claims;
- deterministic CBOR profile requirements;
- CWT access-token profile;
- EAT CWT profile;
- COSE-based VC securing mechanisms if supported.

Do not round-trip CBOR objects through generic JSON if that loses integer labels, byte strings, tags, ordering/canonicalization requirements, or protected-header distinctions.

## 20. X.509 vocabulary

X.509 support should distinguish generic certificate processing from mTLS OAuth, mdoc issuer authentication, workload identity, and attestation endorsement use.

Add or make explicit:

- trust anchor and certification path;
- subject and issuer distinguished names;
- Subject Alternative Name;
- basic constraints and path length;
- key usage and extended key usage;
- name constraints;
- certificate policies and policy constraints;
- authority and subject key identifiers;
- validity period;
- revocation through CRL/OCSP and failure policy;
- certificate transparency where applicable;
- algorithm constraints;
- SPIFFE URI SAN validation for X.509-SVID;
- profile-specific EKUs and chain rules for mdoc or attestation.

Successful generic path validation is necessary but may not satisfy the application profile.

## 21. Proposed package and target ownership

The repository should keep abstractions with the package that owns their semantics and keep protocol-carrier behavior in protocol packages.

Suggested conceptual ownership:

| Surface | Suggested owner |
|---|---|
| Shared credential/assurance/attestation data contracts | contracts layer, independent of OAuth/OIDC |
| JWT/SD-JWT primitives | standards/crypto or token package |
| CWT/COSE primitives | standards/crypto or token package |
| VCDM structures and validation | credential-model package |
| SD-JWT VC validation | credential-format package |
| ISO mdoc CBOR/COSE validation | credential-format package |
| OID4VCI endpoints and state machine | protocol package |
| OID4VP endpoints and state machine | protocol package |
| HAIP constraints | conformance/profile package consuming underlying capabilities |
| DID parsing/resolution contracts | decentralized-identifier package |
| XACML language/adapter | authorization-policy adapter package |
| AuthZEN wire API | authorization protocol package |
| ZTA signals and decision context | policy/security contracts layer |
| EAT appraisal and CoRIM reference material | attestation packages |
| SPIFFE/SVID workload identity | workload-identity package |
| SET events and delivery | shared-signals/security-events package |
| GNAP | independent authorization protocol package |

The existing `tigrbl-auth-protocol-oauth` and `tigrbl-auth-protocol-oidc` packages should expose integration points, not become owners of every credential, policy, DID, and attestation schema.

## 22. Compliance-target model

Create distinct target families or manifests rather than adding all items to `rfc-targets.yaml`:

- `oauth-targets.yaml` or retained RFC targets for OAuth RFCs;
- `oidc-targets.yaml` for OIDC/OIDF identity protocols;
- `openid4vc-targets.yaml` for OID4VCI, OID4VP, and HAIP;
- `vc-targets.yaml` for W3C VCDM and securing mechanisms;
- `credential-format-targets.yaml` for SD-JWT VC and mdoc;
- `authorization-policy-targets.yaml` for XACML and AuthZEN;
- `did-targets.yaml`;
- `attestation-targets.yaml` for EAT and CoRIM;
- `workload-identity-targets.yaml` for SPIFFE/SVID;
- `security-event-targets.yaml` for SET, RISC, CAEP, and delivery profiles;
- `zta-alignment-targets.yaml` for architecture alignment rather than protocol certification;
- `gnap-targets.yaml`.

Each target should record:

- standards organization;
- exact title and version/date;
- RFC number or stable specification URL;
- status: final, recommendation, RFC, implementer’s draft, or tracked draft;
- claimability policy;
- owning modules;
- public endpoints or data formats;
- feature flags;
- normative requirement inventory;
- positive, negative, interop, and security tests;
- evidence tier and unresolved gaps.

Draft targets must not be emitted as final/RFC compliance claims.

## 23. Recommended delivery sequence

### Phase 0 — Correctness and inventory

1. Replace the erroneous RFC 7952 SET mapping with RFC 8417.
2. Audit generated claims, evidence mappings, feature flags, and persisted identifiers affected by the correction.
3. Add a standards-version registry so draft/final revisions cannot be conflated.
4. Inventory existing generic identity, federation, policy, credential, device, and trust-graph contracts before creating packages.

### Phase 1 — Vocabulary and contracts

1. Introduce representation-neutral contracts for credentials, presentations, assurance, policy evaluation, attestation evidence/results, trust material, and workload identity.
2. Add target manifests for all new standards families without claiming runtime conformance.
3. Add exact constants/enums/schema models with normative-source references.
4. Establish media-type and explicit token/profile dispatch.

### Phase 2 — Near-adjacent OIDC work

1. OIDC EAP ACR Values.
2. Identity Assurance Claims Registration.
3. Identity Assurance Schema Definition.
4. OIDC for Identity Assurance.
5. AuthZEN evaluation API if centralized policy decisions are a product priority.

These additions reuse existing OIDC discovery, claims, ID Token, UserInfo, metadata, and authorization-policy surfaces.

### Phase 3 — Credential foundations

1. SD-JWT primitives.
2. SD-JWT VC profile.
3. W3C VCDM 2.0 model and selected securing mechanisms.
4. Credential status, schema, trust, and key-resolution interfaces.
5. Format-independent issuer/holder/verifier contracts.

### Phase 4 — Credential protocols

1. OpenID4VCI discovery, offers, authorization, proof, issuance, deferred/batch, and notification flows.
2. OpenID4VP requests, query handling, response modes, wallet invocation, and validation.
3. ISO mdoc model, CBOR/COSE processing, and device/session binding.
4. HAIP constraints and conformance composition.

### Phase 5 — Attestation and workload identity

1. CWT/COSE foundations.
2. EAT claims and appraisal contracts.
3. CoRIM/CoMID reference and endorsement processing.
4. SPIFFE IDs, X.509-SVID, JWT-SVID, workload API, bundles, and federation.
5. Integrate attestation/workload signals into ZTA and AuthZEN contexts without equating them to authorization decisions.

### Phase 6 — Security events and alternative authorization

1. SET core and subject identifiers.
2. SET push/poll delivery.
3. RISC and CAEP event profiles.
4. GNAP core and resource-server behavior.
5. XACML adapter and expanded AuthZEN search/capability surfaces where required.

## 24. Definition of done for any standards target

A target is not complete merely because constants or Pydantic models exist. Completion requires:

- exact versioned normative source;
- owned public API and package boundary;
- complete required vocabulary;
- parser and serializer where applicable;
- positive validation behavior;
- negative validation behavior;
- explicit trust and key resolution;
- replay/freshness/channel/transaction binding where applicable;
- privacy and minimization policy;
- discovery and metadata integration;
- runtime protocol behavior where applicable;
- conformance tests and independent interoperability evidence;
- generated OpenAPI/OpenRPC/schema updates where public surfaces change;
- compliance mappings and evidence without overstated claims;
- operator documentation and feature lifecycle controls.

## 25. Primary references

- IETF, JSON Web Token: <https://www.rfc-editor.org/rfc/rfc7519>
- IETF, CBOR Web Token: <https://www.rfc-editor.org/rfc/rfc8392>
- IETF, Security Event Token: <https://www.rfc-editor.org/rfc/rfc8417>
- IETF, Grant Negotiation and Authorization Protocol: <https://www.rfc-editor.org/rfc/rfc9635>
- IETF, Entity Attestation Token: <https://www.rfc-editor.org/rfc/rfc9711>
- OpenID Foundation specifications index: <https://openid.net/developers/specs/>
- OpenID Connect EAP ACR Values 1.0: <https://openid.net/specs/openid-connect-eap-acr-values-1_0.html>
- OpenID eKYC and Identity Assurance specifications: <https://openid.net/wg/ekyc-ida/specifications/>
- OpenID AuthZEN specifications: <https://openid.net/wg/authzen/specifications/>
- OpenID Authorization API 1.0: <https://openid.net/specs/authorization-api-1_0.html>
- OpenID4VC HAIP 1.0: <https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0-final.html>
- W3C DID Core: <https://www.w3.org/TR/did-core/>
- W3C Verifiable Credentials Data Model 2.0: <https://www.w3.org/TR/vc-data-model/>
- W3C Verifiable Credential Data Integrity 1.0: <https://www.w3.org/TR/vc-data-integrity/>
- W3C Verifiable Credentials Vocabulary 2.0: <https://www.w3.org/2018/credentials/>
- OASIS XACML 3.0 Core: <https://docs.oasis-open.org/xacml/3.0/xacml-3.0-core-spec-cos01-en.html>
- NIST SP 800-207, Zero Trust Architecture: <https://csrc.nist.gov/publications/detail/sp/800-207/final>
- SPIFFE specifications: <https://github.com/spiffe/spiffe/tree/main/standards>

ISO/IEC 18013-5 and related mdoc standards should be consulted from licensed ISO copies. Exact mdoc requirements, identifiers, and test vectors must be verified against the revision selected for implementation and the applicable OID4VC/HAIP profile.
