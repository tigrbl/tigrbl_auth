# Credential Wallet API + Wallet UIX/SDK Requirements Brief

**Proposed pairing:** `tigrbl-auth-api-wallet` + `@tigrbl-auth/wallet-uix` + wallet SDKs  
**Status:** New product surface; no wallet contracts, custody model, credential store, OpenID4VC client, or presentation UIX currently exists  
**Prepared:** July 11, 2026  
**Proposed API owner:** conditional on custody decision; hosted services under `pkgs/80-apis/tigrbl-auth-api-wallet`  
**Proposed protocol/SDK owners:** `pkgs/50-protocols/tigrbl-openid4vc-wallet` and platform/mobile/web SDKs  
**Proposed UIX owner:** `pkgs/95-ui/wallet-uix`

## 1. Product Decision Required Before Implementation

Tigrbl must choose a wallet product model before defining storage or APIs. These are separate products with different threat, privacy, compliance, recovery, and business consequences:

1. **Non-custodial wallet SDK/UIX (recommended first):** credentials and holder keys remain on the user's device or approved local secure storage. Tigrbl supplies protocol, format, policy, UI, backup adapters, and test components.
2. **Enterprise-managed wallet:** an organization manages wallet policy, devices, recovery, and approved credential programs while holder keys/credentials may remain device-bound. This needs administration without silent presentation control.
3. **Custodial hosted wallet:** Tigrbl stores credentials and/or controls keys server-side. This creates high-value centralized custody, transaction authorization, privacy, regulatory, breach, insider, recovery, and availability obligations.
4. **Issuer/verifier SDK only:** no end-user wallet product; Tigrbl provides test and integration components. Lowest custody risk but smaller product scope.

Recommended sequence: ship a non-custodial embeddable wallet SDK and reference UIX, plus a clearly isolated developer test wallet. Do not deploy a general custodial production wallet until a separate architecture, threat model, jurisdictional review, key-custody design, recovery model, and business decision are approved.

## 2. Product Boundary

The wallet product receives credentials from issuers, validates them for storage, protects holder keys, organizes credential copies, processes verifier requests, selects candidate credentials, obtains informed holder authorization, creates minimal presentations, transmits responses, refreshes status, and supports controlled backup/recovery/device migration.

The wallet is not:

- the credential issuer or source of truth for issuer claims;
- the verifier/relying party or its trust policy;
- a password/passkey/API-key vault by default;
- proof that the human holding the device is the credential subject;
- permission to present credentials silently;
- a blockchain requirement;
- a reason to upload all holder credentials and presentation history to Tigrbl.

The wallet must separate holder, subject, wallet instance, wallet provider, credential issuer, verifier, device, key, credential copy, and presentation transaction.

## 3. Current Repository Reality

The repository has reusable lower-level foundations:

- OAuth/OIDC clients, PKCE, authorization/token flows, JOSE, DPoP, mTLS, key lifecycle, secure credential concepts, and sessions;
- issuer, verifier/resource-server, federation/trust, attestation, policy, audit, consent-adjacent, UIX core, storage, and runtime patterns;
- proposed Credential Issuer and Credential Verifier pairings;
- WebAuthn/passkey, device authorization, encryption, key wrapping, and non-extractable/provider-controlled key contracts that may inform wallet design.

No implementation evidence was found for:

- wallet custody, credential store, holder-key store, or wallet instance/device records;
- OpenID4VCI wallet client;
- OpenID4VP wallet/authorization-server response behavior, DCQL evaluation, `vp_token`, or Digital Credentials API integration;
- SD-JWT VC disclosure, mdoc device response, W3C VP creation, credential status refresh, or trust registry use;
- presentation consent, verifier request rendering, backup/recovery, multi-device, wallet attestation, or wallet UIX.

Existing authentication `Credential` tables and browser/local session storage must not be reused as a digital wallet by convenience.

## 4. Users and Jobs

### Holder/end user

1. receive a credential from a recognizable issuer and understand what it contains.
2. protect it with device/user authentication and recover safely after loss.
3. see who is requesting which claims, for what purpose, and for what transaction.
4. disclose the minimum necessary claims and explicitly approve presentation.
5. inspect status/expiry, remove local copies, replace keys/credentials, and manage devices.

### Enterprise wallet administrator

1. define supported issuers, formats, profiles, wallet/device assurance, backup, and recovery policy.
2. distribute wallet configuration without reading holder credentials/presentations unnecessarily.
3. manage app versions, compromised devices, wallet attestation, and ecosystem interoperability.
4. support users without gaining unrestricted presentation authority.

### Wallet/application developer

1. integrate OpenID4VCI receipt and OpenID4VP presentation with stable SDK APIs.
2. use secure platform key/credential storage and lifecycle callbacks.
3. render requests, claims, purposes, and errors consistently.
4. test same-device, cross-device, redirects, and Digital Credentials API flows.
5. avoid implementing format crypto, DCQL, or trust validation independently.

### Privacy, compliance, and security teams

1. verify that credentials, identifiers, verifier requests, and history are minimized and protected.
2. audit wallet configuration/key/recovery changes without centralized behavior tracking.
3. detect malicious issuers/verifiers, overbroad requests, replay, phishing, key compromise, and backup abuse.
4. define when wallet provider attestation is appropriate without creating global tracking identifiers.

## 5. Architectural Ownership

### Wallet SDK/core owns

- local encrypted credential metadata/store abstraction and holder-key abstraction;
- OpenID4VCI client and OpenID4VP wallet protocol behavior;
- credential format parsing/validation/presentation adapters;
- DCQL evaluation and candidate selection;
- presentation planning, holder authorization, selective disclosure, proof creation, and response;
- issuer/verifier trust metadata integration;
- status refresh, local lifecycle, backup/recovery/device migration hooks;
- secure UI models that do not expose raw secrets.

### Wallet API owns only hosted/coordination concerns

- optional encrypted synchronization blobs, device registration, backup/recovery coordination, enterprise configuration, notification routing, and remote wipe/revocation signals;
- no plaintext credential or holder-key access in a non-custodial model;
- no presentation transaction log beyond holder-controlled/local or explicitly opted-in minimum support telemetry;
- wallet-provider metadata/attestation only under a selected profile.

### Other products retain ownership

- Issuer API owns offers and credential issuance/status;
- Credential Verifier owns requests and verification;
- Attestation Center appraises wallet/key/device attestations;
- Trust Registry governs recognized issuers/verifiers/ecosystems;
- Authenticator Center owns local user authentication methods;
- Security Signals communicates compromise/status changes;
- Policy Studio may supply enterprise policy but cannot override mandatory holder authorization silently;
- UIX presents core outputs and never reimplements protocol/crypto decisions.

## 6. Custody and Key Architecture

### Non-custodial default

- holder private keys are generated and used in device secure hardware/OS keystore where available;
- credentials are encrypted at rest with keys not available to Tigrbl's ordinary backend;
- raw keys/credentials do not enter application logs, crash reports, analytics, clipboard by default, screenshots where platform controls permit, or remote support bundles;
- key handles/fingerprints and safe metadata are exposed to UIX, never private key bytes;
- biometric/PIN/user-presence policy protects sensitive operations but is not claimed as remote identity proof by itself.

### Credential-to-key binding

- preserve exact issuer-bound key relationship per credential/profile;
- support one or multiple keys according to format and privacy policy;
- avoid reusing the same key across issuers/verifiers where it enables correlation;
- do not rotate keys independently when doing so invalidates credentials; trigger reissuance/migration;
- track device/key loss, compromise, replacement, and local credential copies.

### Custodial option requirements

If later approved, require tenant/holder-separated envelope encryption, HSM/KMS controls, transaction authorization independent from login, insider controls, quorum/step-up for recovery/export, immutable audit, data residency, breach response, availability/recovery objectives, and legal/regulatory review. Hosted custody must be labeled unmistakably and never inferred from enabling sync.

## 7. Credential Receipt via OpenID4VCI

The wallet client must support the exact OpenID4VCI 1.0 Final flow profile selected by the issuer/ecosystem:

1. accept offer by value/URI/deep link/QR under strict origin/scheme/size rules;
2. parse without trusting and retrieve issuer/authorization metadata securely;
3. identify issuer/configuration/format, render holder-facing issuer and claim information, and check supported profile;
4. choose authorization-code or pre-authorized-code flow;
5. use PKCE, state/nonce, redirect/app-link binding, hardened external user agent, and client/wallet authentication where required;
6. create/select holder key(s), obtain issuer nonce, and create exact proof/key attestation;
7. request credential/batch, handle deferred polling and notifications;
8. validate returned credential before storage: format/proof, issuer/key, configuration/type/schema, subject/key binding, validity, status metadata, and expected dataset context;
9. store atomically with provenance and delete transient tokens/codes/proofs;
10. notify holder of result and issuer only through allowed protocol event.

An issuer's signature makes the credential attributable to that issuer; wallet acceptance also requires the holder/ecosystem policy for issuer/type/format and safe metadata.

## 8. Presentation via OpenID4VP

Support OpenID4VP 1.0 Final for selected flows:

- same-device and cross-device redirect flows;
- signed request objects and supported client-identifier-prefix trust mechanisms;
- request URI retrieval/post behavior where enabled;
- wallet/verifier metadata negotiation;
- DCQL query parsing and deterministic candidate evaluation;
- `vp_token` response and response encryption/signing/profile behavior;
- nonce/state/origin/audience/client/request binding;
- transaction data only for recognized typed profiles with explicit holder authorization;
- W3C Digital Credentials API integration only through supported platform APIs and required expected-origin checks.

### Request validation pipeline

1. parse request/deep link/QR under strict limits without network side effects;
2. resolve client identifier prefix and authenticate verifier/request according to that method;
3. retrieve/validate metadata through hardened fetch and trust policy;
4. validate signature, issuer/client, audience, nonce, state/context, response URI/mode, expiry, origin, and replay;
5. parse DCQL and reject unsupported critical transaction data/format/features;
6. evaluate trusted-authority hints as candidate minimization, not final trust proof;
7. identify candidate credential combinations locally;
8. construct a minimal disclosure plan and render it for holder approval;
9. require local user authentication/presence according to policy;
10. create format-native presentations and send response only to the validated endpoint/context.

## 9. DCQL, Candidate Selection, and Minimization

- implement final DCQL credential/claim/set query semantics exactly;
- keep candidate matching local in a non-custodial wallet;
- return no observable difference that lets a verifier probe undisclosed claim values or credential possession before holder interaction;
- treat DCQL `values` matching as sensitive because match/non-match can leak claim values;
- never disclose more claims than the selected credential query and format require;
- prefer derived predicates such as age-over rather than raw source values when a trusted credential supports them;
- show alternative satisfying credential sets and default to the least identifying/minimal set;
- warn about repeated identifiers, mandatory credential fields, issuer/format correlation, verifier linkability, and transaction data;
- explain why a credential was or was not a candidate without revealing protected claim values to the verifier.

## 10. Holder Authorization Experience

Before every presentation, show:

- authenticated/validated verifier identity and trust basis, or a clear unverified/unknown warning;
- stated purpose, transaction data, request time/expiry, and response destination;
- each credential/issuer and each claim that will be disclosed;
- claims used only for local matching versus claims actually sent;
- holder-binding/pseudonym/identifier and linkability implications;
- optional versus required claims and alternative credential choices;
- whether the presentation is one-time, transaction-bound, reusable, or starts an API session;
- legal/privacy notice link without burying the disclosure summary.

Authorization must be specific, contemporaneous, and revocable before send. Enterprise policy may block unsafe presentations or set defaults, but cannot silently present personal credentials unless a narrowly defined, disclosed non-personal automation profile is explicitly authorized.

## 11. Credential Formats and Presentation Adapters

### SD-JWT VC

- validate issuer-signed JWT, type metadata, disclosures/digests, status, holder/key binding, and selected draft/profile;
- store issuer JWT and disclosures encrypted without reconstructing a permanently fully disclosed object unnecessarily;
- select only requested disclosures and generate fresh key-binding JWT where required;
- protect salts/disclosures and avoid analytics/logging of undisclosed data;
- label as draft-backed preview until the SD-JWT VC specification stabilizes/certifies.

### W3C VC 2.0

- validate conforming data model plus selected securing mechanism/context/vocabulary integrity;
- create a standards-conforming Verifiable Presentation under the selected proof suite;
- do not assume all W3C credentials support selective disclosure;
- avoid remote context fetch at presentation time unless pinned/cached/integrity-controlled.

### mdoc

- use ISO format-native issuer/device structures, namespaces/elements, MSO/digests, certificates, device authentication, session transcript, and proximity/online response profiles;
- protect device keys in secure hardware where required;
- render mandatory versus requested elements and prevent mdoc-to-JSON semantic shortcuts;
- license/use exact ISO requirements and conformance vectors.

## 12. Trust, Status, and Lifecycle

### Issuer trust

- validate credential cryptography and status, then apply holder/ecosystem trust policy for issuer, type, schema, jurisdiction, and purpose;
- use Trust Registry/Federation inputs with provenance/version/freshness;
- distinguish cryptographically valid, recognized issuer, trusted for credential type/purpose, current, and holder-accepted.

### Status refresh

- refresh status according to credential profile, privacy, cache, network, and expiry policy;
- batch/cache privacy-preserving lists rather than query per holder/credential where possible;
- show active/suspended/revoked/expired/superseded/unknown/offline distinctly;
- status unknown must not silently become active for high-risk presentations;
- minimize status endpoint correlation and never add wallet/holder authentication unless profile requires and privacy review permits.

### Local lifecycle

- states: pending import, active, expiring, expired, suspended, revoked, superseded, locally hidden/archived, deleted, backup-only, or recovery-pending;
- local deletion does not revoke issuer credential;
- issuer revocation does not necessarily erase the local record/evidence;
- replacement/reissuance links are local and privacy-safe;
- permit user labels/folders without modifying credential semantics.

## 13. Backup, Recovery, and Multi-Device

### Backup principles

- encrypted end-to-end before leaving device;
- backup provider cannot decrypt in non-custodial mode;
- bind backup metadata minimally and avoid global correlating wallet identifiers;
- separate credential blobs, key recovery capability, policy/config, and presentation history;
- some non-exportable keys/credentials require reissuance rather than backup.

### Recovery models

- device-to-device transfer with authenticated encrypted channel;
- recovery secret/key split or platform secure backup;
- enterprise recovery with explicit scope and no silent private-key takeover;
- issuer-assisted reissuance after fresh authentication/eligibility;
- custodial recovery only under separate approved model.

### Multi-device

- define per-credential whether copies, separate keys, or reissuance are allowed;
- avoid synchronizing one holder key to all devices when unlinkability/non-exportability is required;
- show device/key/credential-copy inventory and last local use without centralizing verifier history;
- revoke/remove lost device access and trigger status/reissuance as profile requires;
- protect against rollback of deleted/revoked credentials from stale backups.

## 14. Wallet Attestation and High Assurance

OpenID4VC HAIP 1.0 Final profiles high-assurance issuance/presentation using OpenID4VCI/VP with SD-JWT VC and mdoc, plus wallet/key attestation requirements.

If Tigrbl implements HAIP:

- implement a complete selected flow/profile, not isolated parameters;
- wallet attestations must not introduce a unique identifier for a wallet instance and must not be reused across issuers where prohibited;
- key attestations must bind the exact credential key and required storage/user-authentication properties;
- appraise evidence through Attestation Center and expose only required result claims;
- enforce wallet/client authentication at profiled OAuth endpoints;
- balance assurance with accessibility, device availability, recovery, vendor diversity, and privacy;
- maintain non-high-assurance profiles for valid lower-risk use cases.

Wallet provider reputation/attestation does not authorize presentation or prove all wallet-held claims.

## 15. Wallet API and SDK Requirements

### Core SDK interfaces

- `inspectOffer`, `acceptOffer`, `authorizeIssuance`, `requestCredential`, `pollDeferred`, `notifyIssuer`;
- `inspectPresentationRequest`, `evaluateDcql`, `buildDisclosurePlan`, `authorizePresentation`, `sendPresentation`;
- `listCredentials`, `getCredentialMetadata`, `refreshStatus`, `archive/deleteLocal`, `replace/reissue`;
- `create/list/rotate/revokeKey`, `listDevices`, `backup`, `restore`, `transfer`;
- result types preserve protocol stage, safe reason, retryability, user action, and evidence reference.

The SDK must use capability interfaces for key store, credential store, HTTP transport, deep links/QR, browser/platform authorization, user authentication, attestation, secure backup, trust registry, status, and telemetry.

### Optional hosted API

Under non-custodial mode, hosted routes may manage:

- wallet app/device registration and public attestation metadata;
- encrypted sync/backup blobs with opaque versioning and device authorization;
- enterprise policy/configuration and trusted ecosystem lists;
- push notification routing with opaque transaction handles;
- recovery coordination and remote device disable;
- no plaintext credential CRUD or generic presentation-history endpoint.

### Developer test wallet

- isolated environment and keys;
- explicit non-production banner/watermark;
- reset/export fixtures and protocol trace;
- never eligible for production high-assurance issuer/verifier trust;
- separate package/app from the holder production wallet.

## 16. Canonical Local Data Requirements

### Wallet instance/device

- local wallet/device ID, provider/app/version, platform, assurance/attestation result reference, lifecycle, created/last active, and recovery state;
- avoid stable cross-ecosystem identifiers in protocol messages;
- enterprise enrollment/config version and allowed profiles;
- local encrypted master-key handle and no server-readable key in non-custodial mode.

### Stored credential

- local ID, encrypted credential/reference, format/profile, issuer/configuration/type/schema, subject/key handle, issued/valid/expiry, and local status;
- safe display/claim index encrypted and minimized;
- issuer/status/trust metadata cache with version/freshness;
- receipt provenance, replacement lineage, backup/sync eligibility, and local labels;
- no central analytics copy.

### Presentation request/decision

- local transaction ID, request digest, verifier identity/trust, purpose, DCQL/transaction data digest, candidates, disclosure plan, holder decision, response result, and retention expiry;
- default short local retention and no hosted sync unless opted in/policy justified;
- no full claim values in generic audit/telemetry.

### Encrypted sync object

- opaque wallet/device namespace, ciphertext, version, predecessor, digest/MAC, size, created time, and device authorization;
- server cannot interpret credential count/type/issuer where padding/design can reasonably reduce leakage;
- replay/rollback/tamper detection and tombstones.

## 17. Wallet UIX

### Home and credential inventory

- active/expiring/status-unknown/revoked credentials, recent local activity, pending offers/requests, backup/device posture, and critical alerts;
- card/list views with accessible text parity;
- organize by purpose/category/issuer without implying issuer endorsement by Tigrbl;
- credential detail showing issuer, type, claims, validity, status, key/device binding, trust basis, receipt, privacy/linkability, and actions;
- mask sensitive claims by default and require local authentication to reveal where appropriate.

### Receive flow

1. scan/open/paste offer through safe system input;
2. show untrusted parsing state, then validated issuer/configuration details;
3. explain claims, issuer, purpose, binding, validity/status, storage, and privacy;
4. authenticate/authorize issuance and select/create key;
5. show progress through authorization/proof/deferred issuance;
6. validate credential and confirm storage;
7. offer accessible troubleshooting/retry/cancel.

### Present flow

1. scan/open request and validate verifier/request;
2. show verifier trust, purpose, transaction, requested claims, and warnings;
3. display candidate credential choices and minimal recommended disclosure;
4. show exact sent versus locally matched claims and linkability;
5. require holder approval and local authentication;
6. create/send response and show success/failure without storing unnecessary verifier history;
7. allow immediate incident/report/block action for suspicious requests.

### Keys, devices, backup, and recovery

- device/key inventory with public posture only;
- backup state, last successful encrypted sync, recoverability by credential/key type, and test-recovery guidance;
- lost-device removal, key compromise, credential reissuance, and remote disable actions;
- clearly explain which credentials cannot be restored and why;
- destructive local delete/reset requires credential/status/recovery impact summary.

### Privacy center

- per-presentation disclosure receipts stored locally by default;
- issuer/verifier trust decisions and blocks;
- telemetry, sync, backup, history retention, screenshot/clipboard, and notification controls;
- export/delete wallet data without exposing private keys casually;
- explain that issuer/verifier systems may retain their own records independently.

## 18. Security, Privacy, and Reliability

- Use platform secure key stores, non-exportable keys, app/device integrity, local user authentication, encrypted databases, and memory/clipboard/screenshot hygiene.
- Defend deep links/QR/request URIs against phishing, scheme hijacking, open redirects, request substitution, malicious metadata, SSRF, oversized payloads, and replay.
- Use exact issuer/verifier/client identity validation, signed requests where profile requires, expected origin for Digital Credentials API, nonce/state/audience/response-URI binding, and response encryption.
- Treat remote contexts/type metadata/status lists as untrusted and pin/cache with integrity/size/time/network controls.
- Prevent claim probing through DCQL values, silent requests, candidate count/timing, error differences, and repeated requests.
- Require holder interaction before responses, including non-match cases where the protocol could leak values.
- Keep credential/presentation processing local; minimize or disable centralized telemetry.
- Protect sync against server compromise, rollback, device cloning, recovery takeover, traffic analysis, and lost-device persistence.
- Ensure crash consistency/atomic storage so credentials/keys/status/backup state cannot diverge.
- Define offline behavior, clock skew, issuer/verifier/status outage, app upgrade/migration, OS restore, and storage corruption recovery.
- Support security signals for compromised issuer/key/device/wallet/version without revealing holder inventory.
- Conduct mobile/web platform-specific threat models, penetration tests, dependency/supply-chain review, and secure update/signing controls.

## 19. Stakeholder Requirements

### Technical marketing

- demonstrate receipt, local custody, minimal selective disclosure, suspicious-request warning, status, and recovery using synthetic credentials;
- show same-device and cross-device journeys and accessibility without QR;
- explain non-custodial versus custodial honestly;
- prepare stories for workforce, education, professional licensing, age assurance, healthcare eligibility, travel/government, financial onboarding, and enterprise apps.

### Developer relations

- publish mobile/web SDK quickstarts, secure-storage adapters, OpenID4VCI receipt, OpenID4VP/DCQL presentation, status, backup, recovery, and deep-link integration;
- provide reference apps and deterministic issuer/verifier fixtures;
- include adversarial tests for malicious QR/deep link, wrong issuer/verifier/origin/nonce, replay, overbroad DCQL, claim probing, revoked status, backup rollback, and compromised device;
- document platform limitations and no-production test-wallet boundaries.

### Sales and account management

- use a discovery worksheet for custody, platforms, users/devices, credential programs/formats, issuers/verifiers, trust framework, assurance, backup/recovery, enterprise policy, privacy, region, accessibility, and support;
- provide a readiness report separating SDK, custody, protocol, formats, trust, status, device security, recovery, and operations;
- define RACI for holder, enterprise, Tigrbl, OS/device vendor, issuer, verifier, trust framework, backup provider, and support;
- never promise universal wallet acceptance, anonymous presentations, or recoverability of non-exportable credentials without evidence.

### GTM strategist

- package Wallet SDK, Reference Wallet UIX, Enterprise Wallet Management, Secure Backup/Recovery, and High-Assurance Profile separately;
- lead with embeddable non-custodial components and issuer/verifier interoperability;
- postpone broad custodial wallet offering until market/regulatory justification and security investment are clear;
- monetize SDK/app deployment, managed devices, encrypted backup, enterprise policy, support, and certified profiles—not holder presentations or disclosure volume.

### Copywriter

- distinguish holder, subject, wallet, device, key, credential copy, issuer, verifier, presentation, disclosure, status, trust, backup, and custody;
- say exactly which claims leave the device and which are used only locally;
- avoid "anonymous" or "zero knowledge" without exact proof;
- explain verifier trust uncertainty, linkability, status unknown, backup limits, and deletion/revocation distinction;
- use calm, actionable language for suspicious requests and device loss.

## 20. Delivery Instructions

### Frontend/mobile engineer

- keep protocol/crypto/DCQL/format logic in audited core SDKs, not UI components;
- integrate OS secure key/credential storage and user-auth APIs through explicit capability adapters;
- prohibit credentials, disclosures, requests, responses, keys, and stable identifiers from generic logs/analytics/crash reports;
- render server/core-returned verifier/issuer trust, claim plan, status, reason, and warnings;
- support universal/app links, QR, external browser, platform DC API, background status/sync, offline, app lifecycle, and accessibility safely;
- add automated privacy snapshots and secret-scanning tests for UI state/telemetry.

### UIX designer

- design holder comprehension and minimization before card decoration;
- make issuer/verifier identity/trust, requested versus sent claims, and linkability prominent;
- cover empty, receiving, issuer unknown, authorization, proof, deferred, stored, expiring, status unknown/suspended/revoked, request invalid/suspicious, no candidate, disclosure approval, sending, failed, backup degraded, device lost, and recovery states;
- offer accessible alternatives to QR and biometric-only interaction;
- avoid dark patterns, preselected optional claims, urgency manipulation, and ambiguous approve buttons;
- meet WCAG 2.2 AA plus mobile accessibility, dynamic text, localization, reduced motion, screen-reader privacy, and high-contrast requirements.

### Copywriter

- build issuer/verifier trust, offer, credential, claim, request, disclosure, status, custody, backup, recovery, error, warning, and confirmation catalogs;
- write at multiple comprehension levels without hiding technical detail;
- clearly label test credentials/wallets and preview formats;
- explain what Tigrbl, issuer, verifier, enterprise, OS, and backup provider can see;
- provide lost device/key, suspicious verifier, revoked credential, failed restore, and compromised wallet-version guidance.

## 21. Delivery Phases

### Phase 0: Custody decision and threat model

- approve non-custodial SDK/reference wallet scope;
- define supported platforms, key stores, custody, telemetry, backup, recovery, trust, formats, and assurance;
- separate developer test wallet from production architecture.

### Phase 1: Receive and local custody

- wallet core/store/key abstractions, secure local database, one production format, OpenID4VCI client, credential validation/status, reference UIX, and issuer test harness;
- no hosted plaintext sync.

### Phase 2: Presentation and minimization

- OpenID4VP Final, DCQL, same/cross-device flows, verifier trust, holder authorization, selective disclosure/presentation adapter, local receipts, and verifier fixtures;
- Digital Credentials API only on supported platforms.

### Phase 3: Recovery and enterprise management

- end-to-end encrypted backup, device transfer, reissuance, rollback protection, enterprise config/policy, compromised-device response, and privacy-preserving operations;
- independent recovery exercise evidence.

### Phase 4: High assurance and additional formats

- HAIP-selected flow, wallet/key attestation, SD-JWT VC stabilization and mdoc profile, certified issuer/verifier interoperability;
- jurisdiction/vertical packs and custodial option only after separate approval.

## 22. Acceptance Criteria

### SDK/runtime

- A wallet can consume a supported OpenID4VCI offer, validate/store the credential locally, refresh status, process a valid OpenID4VP/DCQL request, obtain specific holder approval, create minimal presentation, and send it securely.
- Wrong issuer/verifier/origin/nonce/state/audience/response URI/key/status, replayed, malformed, unsupported, and cross-context artifacts fail without storage or disclosure.
- Private keys and plaintext credential values never reach hosted APIs in non-custodial mode.
- DCQL evaluation and claim matching do not leak possession/value information before holder interaction.
- Backup/restore rejects tamper/rollback and identifies credentials requiring reissuance.
- Local deletion, issuer revocation, device removal, and wallet reset have distinct semantics.

### UIX

- Holders understand issuer, verifier, purpose, exact disclosed claims, local-only matching, and linkability before action.
- Optional disclosure is not preselected through dark patterns.
- Receive/present flows work accessibly without QR and without biometric-only dependence.
- Suspicious/unverified requests produce calibrated warnings and safe cancellation/reporting.
- Device loss/recovery explains what is recoverable and what must be reissued.

### Evidence/business

- DevRel can run deterministic positive/adversarial issuer-wallet-verifier fixtures.
- Technical marketing can demonstrate non-custodial receipt/presentation without production holder data.
- Sales can produce custody/readiness/RACI documentation.
- OpenID4VCI/VP, HAIP, format, wallet/platform, privacy, and interoperability claims link to certified evidence.

## 23. Success Measures

- offer receipt, authorization, proof, storage, status, DCQL, approval, presentation, and response success by safe reason;
- time to receive/present and holder abandonment by stage;
- average requested versus disclosed claim count and optional-claim rejection;
- suspicious/untrusted verifier request block rate and false warnings;
- status freshness/unknown/revoked presentation prevention;
- key/device/backup/recovery success and credentials requiring reissuance;
- hosted telemetry/data minimization and raw credential/key leakage incidents;
- accessibility task completion and wallet interoperability pass rate;
- support and incident resolution time.

Guardrails include custody ambiguity, key/credential exfiltration, verifier phishing, claim probing, silent presentation, holder correlation, backup takeover/rollback, lost-device persistence, inaccessible consent, and overstated anonymity/interoperability.

## 24. Source Evidence

### Repository

- OAuth/OIDC client/protocol, JOSE, key, DPoP, mTLS, authenticator, device-flow, storage, UIX core, policy, attestation, federation/trust, and security-signal foundations;
- `docs/strategy/uix-pairing-briefs/10-additional-api-uix-opportunity-map.md`;
- `docs/strategy/uix-pairing-briefs/20-credential-issuer-api-issuer-studio-uix.md`;
- repository scans showing no current wallet/OpenID4VP/DCQL/credential-store implementation.

### Standards and primary sources

- [OpenID for Verifiable Credential Issuance 1.0 Final](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0-final.html)
- [OpenID for Verifiable Presentations 1.0 Final](https://openid.net/specs/openid-4-verifiable-presentations-1_0-final.html)
- [OpenID4VC High Assurance Interoperability Profile 1.0 Final](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0-final.html)
- [W3C Verifiable Credentials Data Model 2.0](https://www.w3.org/TR/vc-data-model-2.0/)
- [W3C Bitstring Status List v1.0](https://www.w3.org/TR/vc-bitstring-status-list/)
- [RFC 9901: Selective Disclosure for JWTs](https://www.rfc-editor.org/rfc/rfc9901)
- [SD-JWT-based Verifiable Digital Credentials, active Internet-Draft](https://datatracker.ietf.org/doc/draft-ietf-oauth-sd-jwt-vc/)
- applicable ISO/IEC 18013-5 and 18013-7 documents for mdoc.

## 25. Explicit Non-Claims

This brief does not claim that the current repository:

- implements a credential wallet, OpenID4VCI client, OpenID4VP wallet, DCQL, or Digital Credentials API integration;
- provides local/non-custodial or hosted/custodial credential storage;
- supports SD-JWT VC selective disclosure, W3C presentations, or mdoc;
- provides wallet/key attestation or HAIP conformance;
- offers encrypted backup, multi-device transfer, recovery, or remote wipe;
- interoperates with production issuers, verifiers, operating-system wallets, or government ecosystems;
- can use existing authentication credential tables/browser storage as a secure wallet;
- provides anonymous or unlinkable presentations by default.

Those claims require a custody decision, platform-specific secure implementation, protocol/format support, privacy analysis, adversarial and interoperability tests, recovery exercises, accessibility evidence, legal review, operations proof, and release certification.
