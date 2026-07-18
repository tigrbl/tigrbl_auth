# Authenticator Ceremony API + Universal Authenticator Pages UIX

- **Pairing:** 40
- **Status:** Frontend and UIX delivery brief
- **Primary recipients:** Frontend/UIX engineer, UIX designer, accessibility engineer, API engineer, product copywriter
- **Primary surfaces:** Public UIX, My Account UIX, Tenant Admin UIX, Developer UIX, Service Admin UIX, Platform Admin UIX, shared `uix-core`
- **Adjacent pairing:** Authenticator Lifecycle API + Authenticator Center UIX

## 1. Delivery mandate

Deliver a coherent authenticator experience covering every supported human, recovery, federated, client, and workload authentication method without building one-off pages for each provider.

The frontend must use a universal ceremony framework backed by typed server state. Method-specific components plug into that framework, while the server remains authoritative for method eligibility, challenge state, assurance, policy, attempts, expiry, recovery, and lifecycle transitions.

The experience must:

- make passkeys and phishing-resistant methods the preferred path where available;
- preserve password, OTP, federation, and recovery compatibility without presenting them as equivalent assurance;
- give users complete enrollment, verification, replacement, removal, and recovery journeys;
- give administrators safe policy and lifecycle management without exposing secrets;
- give developers and service owners appropriate machine-authenticator management;
- express `acr`, `amr`, authentication age, evidence, and properties accurately;
- share one component library and visual language across every UIX surface;
- prevent account lockout, cross-tenant access, secret leakage, replay, and unsafe fallback.

## 2. Current repository reality

The canonical authenticator enum currently defines:

- `password_local`
- `api_key_local`
- `service_key_local`
- `client_secret_local`
- `session_local`
- `otp_local`
- `recovery_code_local`
- `webauthn_local`
- `mtls_client_cert`
- `dpop_proof`
- `remote_introspection`
- `federated_oidc`

Relevant foundations already exist:

- typed authenticator requests, challenge start/finish, metadata, evidence, result, factor class, and properties;
- concrete provider packages for all 12 enum values;
- password, passkey, MFA-factor, recovery-code, API-key, service-key, client-secret, mTLS, and DPoP credential models;
- durable WebAuthn passkey, MFA-factor, recovery-code, challenge, credential, key, and lifecycle tables;
- RFC 8176 AMR vocabulary validation;
- OpenID EAP `phr`, `phrh`, and `pop` contracts;
- credential lifecycle, rotation, revocation, audit, adaptive context, and tenant/realm foundations;
- Public UIX login, generic six-digit MFA, password recovery, email verification, and OIDC pages;
- My Account security and session pages;
- Developer client-credential pages;
- Service Admin API-key and service-key pages;
- shared `@tigrbl-auth/uix-core` components and tokens.

The shipped UI is incomplete and inconsistent:

- the generic MFA page assumes every factor is a six-digit code “sent to your registered device”;
- no complete TOTP enrollment exists;
- no recovery-code reveal, acknowledgment, rotation, or consumption UI exists;
- no WebAuthn registration/assertion UI exists;
- no authenticator inventory or detail page exists in My Account;
- federation linking/unlinking is absent;
- machine authentication is spread across different consoles;
- Public UIX uses a hard-coded indigo/slate language while shared `uix-core` uses deep green/neutral tokens;
- the older Admin UIX has an unrelated Parian/neumorphic language;
- provider metadata currently defaults WebAuthn AMR to `hwk` and `user`, which can overstate synced or unverified passkeys.

The frontend must not compensate for missing contracts with local assumptions. Methods remain visibly unavailable or preview-only until the API supplies complete, evidence-backed capability.

## 3. Required taxonomy in the frontend

Do not render every backend enum value as an equivalent “authentication method.” Introduce display categories:

### Human authenticators

- password;
- TOTP;
- WebAuthn passkey;
- WebAuthn security key;
- federated OIDC;
- future email OTP, email link, SMS OTP, push, HOTP, smart card, and SAML methods when their capability records are production-ready.

### Recovery methods

- recovery code;
- backup passkey/security key;
- governed email/phone recovery;
- enterprise or supervised recovery.

### Machine/client authenticators

- client secret;
- `private_key_jwt` when added;
- mTLS client certificate;
- API key;
- service key;
- SPIFFE X.509/JWT SVID when added.

### Supporting mechanisms

- session evidence;
- DPoP sender constraint;
- mTLS token binding;
- remote token introspection;
- risk, device, and workload attestation.

Supporting mechanisms may appear in evidence, session, client, or validation views but not in the user’s “Add authenticator” catalog unless a separately defined profile makes them user-manageable.

## 4. Surface ownership

### Public UIX

Owns:

- identifier-first or method-aware sign-in;
- password entry;
- authenticator selection;
- OTP challenge;
- passkey assertion;
- federated redirect/callback;
- step-up authentication;
- recovery initiation and challenge;
- password reset and forced change;
- expired, cancelled, blocked, and unsupported ceremony states.

Public UIX must not own persistent authenticator inventory, policy editing, provider configuration, or credential secrets after ceremony completion.

### My Account UIX

Owns:

- My Authenticators overview;
- add authenticator;
- method-specific enrollment;
- authenticator detail;
- rename, replace, suspend/remove, and revoke where allowed;
- recovery center;
- recovery-code generation and rotation;
- federated account linking/unlinking;
- authenticator event history;
- session authentication-context detail.

### Tenant Admin UIX

Owns:

- allowed/required/prohibited method policy;
- assurance and step-up policy;
- attestation and algorithm policy;
- recovery policy and enrollment grace periods;
- user enrollment posture;
- safe authenticator inventory;
- require re-enrollment, suspend, revoke, and initiate supervised recovery;
- policy preview, lockout impact, approval, version diff, and rollout.

### Developer UIX

Owns:

- client authentication-method selection;
- client-secret lifecycle;
- `private_key_jwt` public-key/JWKS configuration;
- DPoP capability and proof validation tools;
- mTLS client certificate binding;
- redirect/resource/authentication profile compatibility;
- example requests and validation diagnostics.

### Service Admin UIX

Owns:

- service and workload authenticators;
- API/service keys;
- mTLS and SPIFFE bindings;
- one-time key reveal;
- rotation, overlap, revocation, last use, and dependent-service impact;
- workload authentication evidence and validation tools.

### Platform Admin UIX

Owns:

- authenticator provider catalog;
- global capability and maturity state;
- provider health and outage posture;
- platform-wide algorithm/attestation restrictions;
- policy-pack and profile publication;
- evidence and conformance status;
- no routine end-user credential manipulation.

## 5. Route map

Routes are proposed and should remain configurable under each UI application.

### Public routes

- `/login`
- `/login/method`
- `/login/password`
- `/login/otp`
- `/login/passkey`
- `/login/federated/:provider`
- `/login/callback/:provider`
- `/login/recovery`
- `/login/recovery/code`
- `/step-up`
- `/step-up/method`
- `/step-up/:ceremonyId`
- `/ceremonies/:ceremonyId`
- `/ceremonies/:ceremonyId/expired`
- `/ceremonies/:ceremonyId/blocked`
- `/password/forgot`
- `/password/reset`
- `/password/change-required`

### My Account routes

- `/security/authenticators`
- `/security/authenticators/add`
- `/security/authenticators/enroll/:kind`
- `/security/authenticators/:authenticatorId`
- `/security/authenticators/:authenticatorId/replace`
- `/security/recovery`
- `/security/recovery/codes`
- `/security/federated-accounts`
- `/security/authentication-events`
- `/security/sessions/:sessionId/context`

### Tenant Admin routes

- `/security/authenticator-policy`
- `/security/authenticator-policy/versions`
- `/security/authenticator-policy/simulate`
- `/identities/:identityId/authenticators`
- `/identities/:identityId/authenticators/:authenticatorId`
- `/identities/:identityId/recovery`
- `/security/authenticator-events`

### Developer routes

- `/applications/:clientId/authentication`
- `/applications/:clientId/credentials`
- `/applications/:clientId/credentials/client-secret`
- `/applications/:clientId/credentials/private-key-jwt`
- `/applications/:clientId/credentials/mtls`
- `/applications/:clientId/sender-constraints/dpop`
- `/applications/:clientId/authentication/test`

### Service Admin routes

- `/services/:serviceId/authenticators`
- `/services/:serviceId/api-keys`
- `/services/:serviceId/service-keys`
- `/services/:serviceId/mtls`
- `/services/:serviceId/spiffe`
- `/services/:serviceId/authentication-events`

## 6. Universal ceremony architecture

Implement a single `CeremonyShell` with server-driven content and method adapters.

### Required ceremony states

- `initializing`
- `ready`
- `awaiting_user`
- `awaiting_external_provider`
- `submitting`
- `retryable_failure`
- `terminal_failure`
- `expired`
- `cancelled`
- `blocked`
- `succeeded`
- `requires_next_step`

### Server-owned ceremony fields

- ceremony ID and type;
- subject/tenant/realm binding represented only through authorized display projection;
- method and provider;
- purpose: sign-in, enrollment, verification, step-up, recovery, linking, replacement, removal, or reauthentication;
- lifecycle state and allowed transitions;
- challenge descriptor;
- expiry and server time;
- attempt budget and retry-after;
- method-switch eligibility;
- required and achieved authentication context;
- risk-safe user explanation;
- next action and callback target;
- cancellation policy;
- error code and safe recovery action;
- correlation/reference ID.

### Client-owned ephemeral state

- user-entered password or code until submission;
- browser WebAuthn response until submission;
- one-time secret display acknowledgment;
- local component focus and progress state;
- never authority, expiry truth, attempts remaining, or assurance result.

### Route restoration

On refresh or browser restoration, fetch the ceremony by ID and render the server’s current state. Never restart enrollment, issue another secret, or create another challenge automatically.

## 7. Shared component requirements

Build these in `@tigrbl-auth/uix-core`, with typed props and no provider business logic.

### Catalog and inventory

- `AuthenticatorCard`
- `AuthenticatorKindIcon`
- `AuthenticatorStatusBadge`
- `AuthenticatorRoleBadge`
- `AssurancePropertyBadge`
- `AuthenticatorMethodPicker`
- `AuthenticatorInventory`
- `AuthenticatorSummary`
- `AuthenticatorDetailPanel`
- `AuthenticatorEventTimeline`

### Ceremonies

- `CeremonyShell`
- `CeremonyHeader`
- `CeremonyProgress`
- `ChallengeCountdown`
- `MethodSwitchMenu`
- `RecentAuthenticationGate`
- `CeremonyResult`
- `ExpiredCeremonyState`
- `CancelledCeremonyState`
- `UnsupportedEnvironmentState`
- `BlockedCeremonyState`

### Method-specific inputs

- `PasswordField`
- `PasswordRequirements`
- `OtpInput`
- `QrEnrollmentPanel`
- `ManualSecretField`
- `PasskeyPrompt`
- `SecurityKeyPrompt`
- `CrossDeviceHandoff`
- `ProviderButton`
- `RecoveryCodeInput`
- `RecoveryCodeGrid`
- `OneTimeSecretReveal`
- `CertificateUploader`
- `CertificateFingerprint`
- `PublicKeySummary`
- `JwksEditor`

### Safety and evidence

- `CompatibilityNotice`
- `PrivacyNotice`
- `LockoutRiskNotice`
- `RecoveryImpactNotice`
- `AssuranceSummary`
- `AuthenticationContextSummary`
- `EvidenceFreshnessBadge`
- `AuditReference`
- `PolicyImpactPreview`
- `DangerZone`
- `ConfirmDialog`
- `InlineMutationResult`

Every component needs default, hover, focus, active, disabled, busy, success, warning, danger, expired, and unavailable behavior where applicable.

## 8. Human authenticator pages

### Password

Required screens:

1. password sign-in;
2. create password;
3. change password;
4. forced password change;
5. forgot-password request;
6. reset-password completion;
7. expired/used/invalid reset link;
8. compromised-password response;
9. password changed success.

Frontend requirements:

- allow paste and password managers;
- use `autocomplete="current-password"` and `new-password` correctly;
- show/hide is optional and must retain accessible naming;
- do not reveal which account exists;
- do not expose server-side password-policy internals that aid guessing;
- do not clear a valid field merely because an unrelated request fails;
- do not require arbitrary periodic change unless policy explicitly does.

### TOTP

Enrollment screens:

1. method introduction;
2. QR plus manual secret reveal;
3. initial-code verification;
4. authenticator naming;
5. recovery-method confirmation;
6. completion.

Challenge screens:

1. six/eight-digit input based on server descriptor;
2. retry and expiry;
3. drift/clock guidance only after safe generic failure thresholds;
4. switch method;
5. success.

Requirements:

- do not call TOTP “a code sent to your device”;
- QR and manual secret appear once and clear on acknowledgment, timeout, navigation, and unmount;
- full-code paste and one-time-code autofill must work;
- the server owns digit count, period, algorithm, attempts, replay, and drift;
- do not expose the seed after activation.

### Recovery codes

Required screens:

1. generate/rotate warning;
2. recent-authentication gate;
3. one-time reveal;
4. download/print/copy controls;
5. explicit acknowledgment;
6. remaining-code inventory;
7. recovery challenge;
8. consumed/invalid/exhausted state;
9. post-recovery secure-account checklist.

Requirements:

- display code values only in the one-time reveal response;
- never send codes to analytics, error reporters, URLs, logs, DOM snapshots, or clipboard telemetry;
- render remaining count after activation, not stored codes;
- recovery completion must retain reduced/recovery assurance until server policy upgrades it;
- rotate invalidates the previous set and clearly warns before execution.

### WebAuthn passkeys and security keys

Enrollment screens:

1. passkey/security-key introduction;
2. compatibility and policy check;
3. platform versus security-key choice where policy allows;
4. browser-mediated registration prompt;
5. cross-device/hybrid handoff if supported;
6. naming and safe metadata review;
7. backup/recovery guidance;
8. completion.

Authentication screens:

1. conditional or explicit passkey prompt;
2. browser-mediated assertion;
3. security-key insertion/touch guidance;
4. cross-device handoff;
5. retry/switch method;
6. success or safe error.

Requirements:

- isolate WebAuthn calls behind a tested adapter;
- decode/encode WebAuthn binary values correctly without persisting raw responses;
- bind calls to server options; never modify challenge, RP ID, allow/exclude lists, UV, attestation, or algorithm policy client-side;
- distinguish platform/cross-platform and backup eligible/backed-up only from returned evidence;
- do not infer hardware backing from method name;
- do not infer fingerprint, face, PIN, or exact device ownership from generic user verification;
- state clearly that biometric information stays on the device;
- handle `NotAllowedError`, cancellation, timeout, unsupported platform, invalid state, duplicate credential, and policy rejection separately where safe;
- never repeatedly reopen the browser prompt without explicit user action.

### Federated OIDC

Required screens:

1. provider chooser;
2. redirect progress;
3. callback processing;
4. upstream unavailable/error;
5. account-link confirmation;
6. recent-authentication gate before link/unlink;
7. identity mismatch or takeover-risk block;
8. linked-account detail and unlink warning.

Requirements:

- provider buttons come from server catalog and tenant policy;
- preserve transaction state without exposing tokens;
- never render raw upstream claims;
- do not promise upstream MFA merely from provider branding;
- show validated assurance only after server transformation;
- prevent accidental creation/linking ambiguity.

### Future lower-assurance and enterprise methods

The framework must support but not falsely activate:

- email OTP;
- email magic link;
- SMS OTP;
- push with number or transaction matching;
- HOTP/hardware OTP;
- SAML federation;
- PIV/CAC/smart card;
- CIBA/decoupled authentication.

Capability records must declare maturity, routes, enrollment/challenge support, assurance properties, compatibility, and UI adapter before the method appears.

## 9. Machine and workload pages

### Client secret

- select authentication method;
- issue secret;
- one-time reveal and acknowledgment;
- show identifier, created, expiry, status, last use, and safe prefix;
- overlapping rotation;
- activate replacement and retire prior secret;
- revoke with affected-client warning.

### `private_key_jwt`

- register JWKS or public key;
- validate algorithms and key use;
- display public fingerprint and key ID;
- generate example assertion requirements, not private keys by default;
- test exact `iss`, `sub`, audience, expiry, and `jti` behavior;
- support overlap, rotation, and revocation.

### mTLS client certificate

- upload certificate or CSR/public certificate information;
- validate chain, EKU/profile, subject/SAN, expiry, and thumbprint;
- show `cnf.x5t#S256` binding where applicable;
- manage overlap, replacement, and revocation;
- never accept or retain a client private key in ordinary browser workflows.

### API and service keys

- inventory and scope;
- one-time reveal;
- tenant/environment/resource binding;
- expiry and rotation;
- last use and safe anomaly status;
- revoke and dependent-service impact;
- validation examples without real secret values.

### DPoP

- display DPoP as a sender constraint, not an authenticator;
- show `jkt` thumbprint, supported algorithms, nonce policy, replay posture, and bound token types;
- provide proof-validation tooling with synthetic/redacted inputs;
- explain that DPoP is not client authentication by itself.

### Remote introspection

- place under validation/provider configuration;
- configure endpoint, client authentication, TLS, cache, timeout, and fail-open/fail-closed policy;
- test connectivity and response shape;
- never list it as a user authenticator.

## 10. ACR, AMR, AAL, and evidence presentation

### UI principles

- `acr` is the achieved authentication context for the whole event.
- `amr` lists validated methods actually used.
- AAL is a policy evaluation, not a visual score attached permanently to a credential.
- properties such as phishing resistant, hardware protected, user present, user verified, sender constrained, and replay resistant require evidence.
- recovery authentication must remain visibly distinct from ordinary authentication.

### Supported ACR display

- `phr`: “Phishing-resistant authentication”;
- `phrh`: “Phishing-resistant with verified hardware protection”;
- `urn:tigrbl:acr:aal1`: “Basic assurance profile”;
- `urn:tigrbl:acr:aal2`: “Multi-factor assurance profile”;
- `urn:tigrbl:acr:aal3`: “Hardware-backed high-assurance profile”;
- `urn:tigrbl:acr:recovery`: “Account recovery authentication”;
- unknown URI/value: render server-provided safe name or the value in technical details, never invent a label.

These labels describe configured profiles, not compliance certification.

### AMR display rules

- translate known values in technical detail only;
- preserve the exact value for developer/audit views;
- do not show `hwk` unless server evidence verified hardware protection;
- do not translate generic `user` into “biometric”;
- do not show `mfa` as proof of independent factors without a server assurance result;
- do not infer assurance by counting AMR strings;
- upstream AMR values appear as transformed/validated evidence, not raw provider claims.

### Authentication context summary

Show:

- requested context;
- achieved context;
- authentication time and permitted age;
- methods used;
- evidence-backed properties;
- recovery/degraded status;
- policy/decision reference in privileged views;
- clear “what this proves / does not prove” disclosure.

## 11. API contract expected by the frontend

The frontend requires generated clients for:

### Catalog

- list enabled authenticator methods;
- method compatibility and maturity;
- enrollment/challenge/recovery capabilities;
- safe display metadata;
- tenant/profile restrictions.

### Current-subject authenticators

- list and get;
- enrollment start/finish;
- verify;
- rename;
- replace start/finish;
- suspend/remove/revoke;
- recovery-code generation/acknowledgment/rotation;
- federation link/unlink;
- lifecycle events.

### Ceremonies

- create/start;
- retrieve/resume;
- finish;
- retry where allowed;
- switch method;
- cancel;
- acknowledge one-time material;
- retrieve result projection.

### Policy and administration

- get effective policy;
- list versions;
- draft/edit;
- validate/simulate impact;
- approve/activate/rollback;
- list a user’s safe authenticator projection;
- require re-enrollment;
- suspend/revoke;
- initiate governed recovery;
- retrieve events/evidence.

### Standard error shape

Require:

- stable code;
- safe title/message;
- field errors;
- ceremony ID and current state;
- retryable boolean;
- retry-after;
- attempts remaining only when disclosure policy allows;
- next allowed actions;
- correlation ID;
- no account enumeration or secret content.

## 12. Canonical design system

Use `@tigrbl-auth/uix-core` as the canonical system.

### Token direction

Retain the current shared foundation:

- neutral application background;
- white panels;
- deep green primary action;
- soft green primary tint;
- slate text;
- semantic red, amber, green, blue, and neutral states;
- 4px spacing scale;
- 8px standard radius and 6px compact radius;
- restrained border and shadow;
- visible three-pixel focus ring.

Replace hard-coded Public UIX indigo/slate tokens with semantic shared tokens:

- `--tigrbl-primary`
- `--tigrbl-primary-hover`
- `--tigrbl-primary-soft`
- `--tigrbl-bg`
- `--tigrbl-panel`
- `--tigrbl-border`
- `--tigrbl-text`
- `--tigrbl-muted`
- semantic success/warning/danger/info tokens;
- tenant-brand overrides with contrast validation.

Do not import the legacy Parian grid, animated arterial line, uppercase technical buttons, or neumorphic shadow language into authentication ceremonies.

### Typography

- one shared sans-serif stack across all UIX applications;
- Inter/system sans is the current recommended baseline;
- sentence case for headings, labels, and buttons;
- monospace only for recovery codes, fingerprints, key IDs, serials, and code samples;
- body text at least 16px in user ceremonies where practical;
- avoid all-caps security messages.

### Layout

- Public ceremony shell: centered, `28–32rem` maximum width;
- one primary task and one primary CTA per step;
- optional contextual/help panel on wide screens only;
- My Account: responsive inventory/detail layout;
- admin consoles: denser tables and detail drawers using shared components;
- secrets and destructive actions never depend on horizontal scrolling.

### Icons and imagery

- adopt one approved icon library;
- use consistent icons for password, code, passkey, security key, federation, recovery, certificate, API key, service key, warning, and success;
- no ad hoc inline SVG per page;
- do not depict biometrics as if Tigrbl receives biometric data;
- tenant logos are untrusted assets with validated dimensions, formats, and fallbacks.

## 13. Interaction requirements

- explicit user action starts browser/platform prompts;
- no repeated automatic WebAuthn prompt loops;
- preserve valid user input through unrelated failures;
- prevent double submission;
- show deterministic busy states;
- provide cancel and switch-method actions only when server allows them;
- show expiration as text and accessible announcement, not only animation;
- derive countdown from server time and refresh truth before terminal transition;
- support browser Back without duplicating ceremonies;
- handle network interruption and safe resume;
- do not auto-regenerate codes or secrets on refresh;
- use consequence-focused confirmations for removal, rotation, unlinking, and revocation;
- require recent authentication before sensitive lifecycle actions;
- warn and block final-factor deletion unless server returns an authorized safe path.

## 14. Responsive and accessibility requirements

Meet WCAG 2.2 AA.

- full keyboard operation;
- visible shared focus indicators;
- minimum 44×44px touch targets;
- programmatic labels and descriptions;
- `aria-live` announcements for errors, expiry, prompt completion, and method changes;
- field errors linked with `aria-describedby`;
- heading hierarchy and landmark structure;
- reduced-motion support;
- 200–400% zoom support without loss of the primary task;
- no status communicated by color alone;
- QR enrollment always includes an accessible manual secret;
- OTP accepts paste and mobile one-time-code input without six separate inaccessible labels;
- recovery-code groups work with screen readers and print/download;
- WebAuthn browser-prompt instructions remain useful when platform wording differs;
- long localization strings, RTL, non-Latin names, and translated provider names;
- timeout extensions where policy and security permit;
- errors do not blame users or reveal account existence.

## 15. Security and privacy constraints

The frontend must never persist or emit:

- passwords;
- OTP seeds;
- recovery-code values after reveal acknowledgment;
- private keys;
- client/API/service secrets;
- raw WebAuthn attestation/assertion blobs beyond immediate submission;
- bearer, refresh, reset, or linking tokens;
- raw upstream identity claims;
- detailed device identifiers;
- biometric modality inferred from WebAuthn;
- challenge payloads or identifiers in analytics;
- sensitive policy/risk reasons.

Prohibited locations include:

- localStorage/sessionStorage;
- IndexedDB unless a separately reviewed protocol requires it;
- URLs and query strings;
- browser history;
- console logs;
- telemetry breadcrumbs;
- analytics events;
- DOM snapshots/session replay;
- uncensored error reporting;
- clipboard analytics.

Use server-authorized projections and field-level redaction. Client-side hiding is not authorization or redaction.

## 16. Analytics

Allowed privacy-safe events:

- surface and method category;
- ceremony purpose and coarse stage;
- success, cancelled, expired, retryable failure, terminal failure;
- compatibility unavailable;
- method switch;
- recovery initiated/completed;
- policy preview/publish;
- duration buckets;
- stable non-sensitive error category.

Never include user, subject, tenant, email, phone, IP, credential, authenticator, device, challenge, secret, attestation, token, provider-subject, or recovery values.

## 17. Copy system

Use one controlled taxonomy:

- **Authenticator:** a method bound to an account or workload.
- **Passkey:** a WebAuthn credential that may be synced or device-bound.
- **Security key:** a roaming hardware authenticator.
- **Verification code:** only when transport/type is intentionally abstracted.
- **Authenticator app code:** TOTP.
- **Recovery code:** one-time account recovery secret.
- **Federated sign-in:** authentication through an upstream identity provider.
- **Client certificate:** mTLS client authentication/binding.
- **Sender constrained:** token must be used with a bound key/certificate.

Required copy families:

- catalog descriptions and compatibility;
- enrollment preparation;
- browser/device prompt guidance;
- expiry, retry, and attempt-limit messages;
- replacement and removal consequences;
- final-factor lockout warning;
- recovery and reduced-assurance restrictions;
- provider redirect/link/unlink;
- one-time secret handling;
- support escalation and correlation reference;
- assurance explanations and non-claims.

Avoid unsupported language:

- “unhackable”;
- “unphishable”;
- “biometric login” when the RP only sees WebAuthn UV;
- “hardware backed” without accepted evidence;
- “MFA” merely because two AMR strings exist;
- “trusted device” without a defined trust policy;
- “fully passwordless” when password/recovery fallback remains;
- “compliant with AAL3” without profile and deployment evidence.

## 18. State and fixture matrix

Every method must have deterministic fixtures for:

- eligible and ineligible;
- not enrolled;
- enrollment pending;
- active;
- suspended;
- revoked;
- expired;
- replacement required;
- recovery only;
- compromised;
- last usable authenticator;
- multiple devices/methods;
- no recovery method;
- challenge ready;
- invalid response;
- replayed response;
- expired challenge;
- attempts exhausted;
- rate limited;
- cancelled platform prompt;
- unsupported browser/device;
- provider unavailable;
- network interruption;
- cross-tenant/unauthorized access;
- policy changed during ceremony;
- successful completion with next step;
- reduced/recovery assurance;
- redacted evidence.

## 19. Test requirements

### Component tests

- all visual/interaction states;
- keyboard and focus behavior;
- accessible labels and announcements;
- secret clearing on acknowledgment, timeout, navigation, and unmount;
- long copy, RTL, zoom, and reduced motion;
- no sensitive props rendered into hidden/debug markup.

### Contract tests

- generated client matches API schema;
- stable error-code mapping;
- method capability/maturity gating;
- server state wins over stale browser state;
- no unsupported transition can be sent;
- no provider-specific assumptions leak into shared components.

### End-to-end tests

- password sign-in/change/reset;
- TOTP enrollment and replay-denied challenge;
- recovery-code reveal, acknowledgment, consumption, rotation, and replay denial;
- passkey enrollment and assertion with a virtual authenticator;
- platform and cross-platform WebAuthn profiles;
- cancelled/expired WebAuthn ceremony;
- federation redirect/callback/link/unlink takeover protections;
- step-up through RFC 9470 flow;
- final-factor deletion prevention;
- help-desk re-enrollment/recovery authority;
- client-secret and service/API-key one-time reveal and rotation;
- mTLS/DPoP public evidence rendering;
- cross-tenant and cross-subject denial;
- refresh/resume without duplicated secret or challenge.

### Security tests

- secret absence from storage, URL, logs, analytics, and error reports;
- challenge binding and replay;
- origin/RP mismatch;
- cross-account credential binding;
- account-link takeover;
- stale policy and ceremony version;
- unauthorized evidence fields;
- CSRF, XSS, clickjacking, and open redirect;
- rate-limit and enumeration-safe errors;
- clipboard and download handling;
- browser history/back-forward cache behavior.

### Visual tests

- mobile, tablet, and desktop;
- tenant theme variants;
- default, dark if later supported, high contrast, and forced colors;
- loading, empty, warning, danger, expired, blocked, and success states;
- consistent shared tokens and no legacy style leakage.

## 20. Delivery phases

### Phase 0 — Design system and contracts

- converge Public UIX onto `uix-core` semantic tokens;
- create shared authenticator components;
- define taxonomy and provider capability schema;
- define ceremony and error state machines;
- generate typed API clients;
- add route and maturity gates;
- correct static WebAuthn AMR/property assumptions in backend contracts before UI claims them.

### Phase 1 — Baseline human authentication

- authenticator chooser;
- password ceremonies;
- TOTP enrollment/challenge;
- recovery codes;
- My Authenticators inventory/detail;
- Recovery Center;
- tenant method policy baseline;
- lifecycle events and lockout safeguards.

### Phase 2 — Passkeys and phishing resistance

- WebAuthn adapter;
- passkey/security-key enrollment and assertion;
- conditional mediation where supported;
- cross-device flow;
- backup state and safe metadata;
- `phr`/`phrh` presentation;
- virtual-authenticator and negative security suite.

### Phase 3 — Federation and administration

- federated OIDC chooser/callback/linking;
- tenant policy versioning, simulation, and impact;
- help-desk suspension/re-enrollment/recovery;
- authentication context/session explorer;
- evidence and audit projections.

### Phase 4 — Machine/workload unification

- client-secret lifecycle;
- `private_key_jwt` when backend exists;
- API/service keys under shared components;
- mTLS and DPoP evidence/configuration;
- provider validation tools;
- SPIFFE profiles when backend exists.

### Phase 5 — Optional reach and enterprise profiles

- email OTP/link;
- SMS OTP;
- push number matching;
- HOTP;
- SAML;
- PIV/CAC;
- CIBA;
- wallet-based authentication only after separate security and privacy approval.

## 21. Acceptance criteria

### Architecture

- All authenticator screens use shared `uix-core` tokens and components.
- Public, My Account, Tenant Admin, Developer, and Service Admin reuse one typed ceremony/inventory model.
- Provider verification and policy do not execute in the browser.
- Supporting mechanisms are not misrepresented as authenticators.

### User experience

- Every enabled method has complete introduction, enrollment where applicable, challenge, success, failure, expiry, cancellation, replacement, and removal behavior.
- Users can understand method assurance, recovery effect, device dependence, and privacy without reading protocol vocabulary.
- Users cannot accidentally remove their final usable authenticator.
- Refresh, Back, interruption, and cancellation do not duplicate challenges or secrets.

### Assurance accuracy

- ACR, AMR, AAL, hardware, biometric, phishing-resistance, user-verification, and MFA labels come only from server evidence.
- Synced passkeys are not labeled hardware-backed by default.
- Recovery authentication is visibly and technically distinct.
- DPoP, mTLS token binding, sessions, and introspection are categorized correctly.

### Security and privacy

- No secret or raw sensitive ceremony material reaches persistent browser storage, URLs, logs, analytics, or uncensored telemetry.
- Cross-subject, cross-tenant, replayed, expired, and unauthorized operations fail safely.
- One-time reveal components clear material correctly.
- Recent authentication and permission checks protect sensitive lifecycle changes.

### Accessibility and responsiveness

- WCAG 2.2 AA checks pass.
- All core journeys work with keyboard and screen reader.
- Mobile and 400% zoom retain the complete primary task.
- QR, countdown, color, animation, and graphical states have accessible equivalents.

### Testing and maturity

- Component, contract, end-to-end, security, accessibility, and visual tests pass for every production-enabled method.
- Missing backend capability renders unavailable or preview—not production-ready.
- Stable fixtures support demos without real credentials or personal data.

## 22. Definition of done

This pairing is complete only when:

1. the backend taxonomy distinguishes authenticators, credentials, recovery, federation, session evidence, sender constraints, context, and token validation;
2. ceremony APIs are durable, resumable, versioned, replay-safe, tenant-bound, and typed;
3. the shared component library covers the full catalog and state matrix;
4. Public UIX supports production password, TOTP, recovery-code, passkey, federation, and step-up flows;
5. My Account supports full self-service lifecycle and recovery;
6. Tenant Admin supports safe policy, user posture, recovery, and audit;
7. Developer and Service Admin use the shared system for machine authenticators;
8. ACR/AMR/evidence claims are accurate and interoperable;
9. secrets do not leak through frontend or analytics surfaces;
10. accessibility, responsive, adversarial, and visual acceptance suites pass;
11. product copy and marketing claims match verified capability and maturity.

## 23. Standards baseline

- [NIST SP 800-63B-4, Authentication and Authenticator Management](https://pages.nist.gov/800-63-4/sp800-63b.html)
- [W3C Web Authentication Level 3](https://www.w3.org/TR/webauthn-3/)
- [RFC 8176, Authentication Method Reference Values](https://www.rfc-editor.org/rfc/rfc8176.html)
- [OpenID Connect Core 1.0](https://openid.net/specs/openid-connect-core-1_0-18.html)
- [OpenID EAP ACR Values 1.0](https://openid.net/specs/openid-connect-eap-acr-values-1_0-final.html)
- [RFC 9470, OAuth Step-Up Authentication Challenge Protocol](https://www.rfc-editor.org/rfc/rfc9470.html)
- [RFC 9449, OAuth DPoP](https://www.rfc-editor.org/rfc/rfc9449.html)
- [RFC 8705, OAuth Mutual TLS](https://www.rfc-editor.org/rfc/rfc8705.html)
- [RFC 7523, JWT Client Authentication](https://www.rfc-editor.org/rfc/rfc7523.html)
- [OpenID CIBA Core 1.0](https://openid.net/specs/openid-client-initiated-backchannel-authentication-core-1_0.html)

The implementation must pin supported profiles and test vectors rather than infer interoperability from a standard name alone.
