# Face AMR Frontend UIX Brief

- **AMR:** `face`
- **Current delivery status:** Missing first-party face verifier and biometric lifecycle
- **Delivery target:** Complete first-party face authenticator, including native capture, liveness, template lifecycle, recovery, and evidence
- **Category:** Biometric method evidence
- **Primary implementation rule:** Never infer `face` from generic WebAuthn user verification
- **Target surfaces:** Public web, My Account web, Tenant Admin web, Platform Admin web, native platform authentication

## UIX delivery priority

**P0 — Actual authentication UIX (ship first):** method-aware login → Face method introduction → permission/sensor preflight → transaction-purpose confirmation → live face capture and liveness challenge → processing → quality retry/no-match/spoof-suspected/cancelled/blocked states → fallback or recovery handoff → success or next-factor result. The same ceremony must work for sign-in and step-up, across native and supported web-to-native handoff. This is the primary deliverable and release gate.

**P1 — Enrollment and user lifecycle:** consent, first enrollment capture, activation, backup-method confirmation, authenticator detail, retraining/replacement, suspension, revocation, recovery, consent withdrawal, and template deletion.

**P2 — Administration and operations:** tenant policy, verifier/provider configuration, health, conformance, analytics, audit investigation, and fleet/retention operations.

Do not treat P2 screens as evidence that the authenticator is delivered. The Face authenticator is not first class until the P0 authentication ceremony is interaction-complete, responsive, accessible, secure, and integrated end to end.

**Release gate:** P0 must be interaction-complete and validated before P2 administration/configuration/management UIX is treated as delivery. P2 screens cannot be used to claim first-class authenticator support.

## 1. Mandate

Deliver a complete first-party face authenticator product that enrolls an eligible user through an approved native capture boundary, performs liveness-protected facial verification, emits trusted `face` evidence, and supports the entire lifecycle through replacement, suspension, revocation, recovery, consent withdrawal, and biometric-template deletion.

The product must also consume trusted platform or federated face evidence, but those are additional adapters—not substitutes for the first-party implementation. Generic WebAuthn user verification must never be relabeled as `face`.

## 2. Users and jobs

- **Enrolling user:** understand the biometric purpose and data boundary, provide informed consent, complete capture/liveness, and activate recovery.
- **End user:** sign in or step up through first-party native facial verification, a trusted platform integration, or an approved upstream provider.
- **Account holder:** understand which authenticator was used and whether facial recognition was actually attested.
- **Tenant administrator:** decide whether trusted `face` evidence may satisfy a policy without treating it as universally phishing resistant.
- **Platform operator:** configure trusted evidence issuers, monitor failures, and prove that unsupported modality claims are rejected.
- **Native-app user:** complete permission, capture, liveness, verification, and recovery through approved native components.

## 3. Product boundaries

The generic web frontend may display `face` only when server evidence includes the AMR and its accepted provenance. Approved first-party native capture components may collect encrypted, ceremony-bound biometric samples directly into the verifier boundary. No general application screen may:

- persist, log, replay, analyze, or retain face images or biometric templates outside the approved verifier boundary;
- ask users to enroll through an untrusted generic browser camera flow;
- inspect platform prompt text to guess the biometric modality;
- substitute `face` for WebAuthn `user` or user-verification flags;
- promise hardware backing, liveness, phishing resistance, or identity proofing without separate evidence;
- expose raw upstream claims.

## 4. Screen inventory

| Screen | Platform | Purpose | Requirement |
|---|---|---|---|
| Eligibility and compatibility | Web/native | Confirm policy, jurisdiction, device, sensor/camera, verifier, and accessible alternatives | New screen |
| Biometric privacy and consent | Web/native | Explain purpose, processing boundary, retention, sharing, deletion, and alternatives | New screen |
| Camera/sensor permission | OS/native | Obtain platform permission only after informed user action | External system screen |
| Enrollment introduction | Native | Explain capture, positioning, lighting, liveness, retries, and recovery | New screen |
| Enrollment capture | Native/verifier | Capture server-directed samples inside approved boundary | New screen |
| Enrollment quality and liveness | Native/verifier | Provide safe corrective feedback and anti-spoof checks | New screen |
| Enrollment review and activation | Web/native | Confirm safe authenticator metadata, consent record, and recovery | New screen |
| Method-aware login | Web/native | Offer the first-party Face authenticator plus eligible passkey/provider adapters with distinct labels | Extend shared login |
| First-party face challenge | Native/verifier | Capture a fresh, transaction-bound liveness sample and verify it | New screen |
| Passkey assertion ceremony | Web/native | Launch OS/WebAuthn authentication | Shared screen |
| Federation redirect progress | Web | Transfer control to a trusted upstream provider | Shared screen |
| Federation callback processing | Web | Validate transformed upstream evidence | Shared screen |
| Step-up method chooser | Web/native | Offer an eligible method capable of satisfying policy | Shared screen |
| Native biometric prompt | OS/native | Perform local facial verification | External system screen |
| Ceremony success/result | Web/native | Confirm completion without overclaiming modality | Shared screen |
| Evidence detail | Web | Show validated `face` evidence, issuer, freshness, and limitations | New screen |
| Face authenticator detail | Web/native | Show status, consent, dates, verifier profile, and lifecycle actions | New screen |
| Retrain/replace authenticator | Native/verifier | Create and activate a replacement template safely | New screen |
| Suspend/revoke/remove | Web/native | Stop use immediately and protect last-factor access | New screen |
| Template deletion request/status | Web/native | Submit, track, retry, and prove deletion without exposing template data | New screen |
| Recovery and accessible alternative | Web/native | Regain access without weakening or bypassing controls silently | New screen |
| Session authentication context | Web | Show how the current session obtained the AMR | New screen |
| Tenant evidence policy | Web | Permit/prohibit issuers and define policy use | New screen |
| Trusted-provider configuration | Web | Configure issuer, transformation, and trust requirements | New screen |
| Evidence event detail | Web | Show redacted success/failure provenance | New screen |
| Provider health and conformance | Web | Monitor claim transformation and rejection behavior | New screen |
| Unsupported-evidence state | Web/native | Explain that the method cannot satisfy the requested policy | Shared ceremony state |

## 5. End-to-end flows

### 5.1 First-party enrollment flow

1. Add Authenticator shows Face only when tenant policy, regional rules, device capability, verifier health, and user eligibility permit it.
2. Privacy and consent explain the purpose, legal basis or consent model, capture boundary, retention, sharing, deletion, failure consequences, and equivalent alternative methods.
3. Explicit user action invokes the OS/native camera or sensor permission prompt.
4. Preflight checks camera/sensor availability, minimum security profile, lighting/environment, verifier connectivity, and accessible alternatives.
5. The native capture adapter obtains server-directed samples and streams them directly to the approved verifier boundary; general application state never receives them.
6. The verifier performs presentation-attack detection/liveness, quality evaluation, duplicate/cross-subject safeguards, and template creation.
7. Bounded corrective feedback handles positioning, lighting, occlusion, motion, and capture quality without revealing matching thresholds.
8. The server activates the authenticator only after accepted liveness, template binding, tenant/subject binding, consent recording, and recovery readiness.
9. Review shows a user-chosen label, verifier/profile, created date, consent version, retention/deletion information, and recovery method—never an image or template.
10. Completion notifies the user and offers enrollment of a backup authenticator.

### 5.2 First-party authentication and step-up flow

1. Login or step-up returns an eligible first-party Face method with ceremony purpose, expiry, and alternatives.
2. The user explicitly starts verification; the native adapter opens the approved capture surface.
3. The server issues a randomized or transaction-bound liveness challenge when the verifier profile requires it.
4. Native capture streams the fresh sample directly to the verifier boundary.
5. The server validates liveness, match result, template/authenticator binding, subject/tenant, challenge, purpose, freshness, replay, verifier signature, and policy.
6. An accepted result emits `face` evidence and either completes the action or advances to another factor.
7. Quality retry, liveness failure, no match, cancellation, camera denial, sensor outage, network interruption, and attempts exhausted each return a safe server-directed retry, fallback, recovery, or block.

### 5.3 Lifecycle, replacement, and deletion flow

1. Authenticator detail shows status, verifier/profile, consent version, created/last-used dates, re-enrollment deadline, and event history.
2. Retraining/replacement requires recent authentication, new consent where necessary, and a new enrollment ceremony.
3. The replacement template is verified and activated before the prior template is retired when overlap is policy-approved.
4. Suspension blocks new use without deleting recovery evidence; revocation blocks use permanently.
5. Removal warns about sessions, policies, and last-factor lockout.
6. Consent withdrawal or deletion submits a verifier deletion job and shows `pending`, `completed`, `failed`, and `manual_review` states with an audit reference.
7. Completion confirms what was deleted, what audit metadata remains, and which authenticator now protects the account.

### 5.4 Platform passkey flow

1. Login or step-up returns an eligible passkey method.
2. The user selects the passkey; the UI enters `awaiting_external_provider` before invoking WebAuthn.
3. The browser or OS displays its own authentication prompt.
4. The UI submits the assertion without attempting to determine whether face, fingerprint, PIN, or another local gesture was used.
5. The server validates the assertion and returns normalized evidence.
6. If accepted evidence contains `face`, the result and evidence views may show “Facial recognition reported by your authenticator.”
7. If evidence contains only user verification, the UI shows “User verified” and does not show `face`.
8. Cancellation, timeout, unsupported environment, and policy rejection return to the ceremony with an explicit switch-method action.

### 5.5 Federated evidence flow

1. The user chooses a trusted identity provider.
2. Redirect progress preserves the server transaction ID and safe provider label.
3. Callback processing sends the authorization response to the server; the browser never interprets raw upstream AMR values.
4. The server transforms and validates upstream evidence against provider policy.
5. Accepted `face` evidence appears with provider, authentication time, trust status, and limitations.
6. Rejected or unmapped evidence appears as generic upstream authentication and cannot satisfy a face-specific policy.

### 5.6 Evidence review flow

1. The account holder opens session context or an authentication event.
2. The detail screen shows method, provider/authenticator, time, purpose, confidence/trust classification, and whether the claim was direct or transformed.
3. Raw biometric material and unapproved provider claims are never rendered.
4. The user may report an unfamiliar event or revoke the underlying passkey/session/account link.

### 5.7 Administrative policy flow

1. An administrator selects `face` as an allowed evidence method.
2. The policy editor requires at least one trusted provider/evidence profile.
3. Impact preview lists affected applications, fallback methods, and lockout risk.
4. Simulation covers valid, absent, stale, transformed, conflicting, and untrusted evidence.
5. Publication requires confirmation and produces an auditable version.

## 6. Screen specifications

### Eligibility, privacy, and consent

- Eligibility is server-owned and combines tenant policy, age or population restrictions, jurisdiction, application purpose, verifier availability, device capability, and accessible alternatives.
- Consent content identifies controller/processor roles, capture purpose, sample/template handling, retention, sharing, withdrawal, deletion, audit retention, and consequences of declining.
- Declining must lead to an equivalent policy-approved method wherever required by law or accessibility policy.
- Consent is versioned, downloadable in a safe textual form, and never bundled into unrelated terms.

### Enrollment preflight and capture

- Request camera/sensor permission only after the consent action and never on page load.
- Preflight covers permission, device/verifier profile, connectivity, lighting, camera framing, accessibility, and unsupported-environment recovery.
- The capture surface provides textual and nonvisual equivalents for positioning, distance, lighting, occlusion, motion, and progress.
- Capture includes explicit start/cancel; no background or surprise recording.
- Quality retry and liveness failure are distinct. Neither exposes matcher thresholds, similarity scores, or anti-spoof rules.
- Raw samples stream directly to the approved verifier and clear immediately from transient native buffers after acknowledged transfer or cancellation.

### Enrollment review and activation

- Show label, verifier/profile, consent version/date, retention/deletion policy, recovery readiness, and safe device projection.
- Never display the captured face image as an account avatar or enrollment proof.
- Activation is disabled until verification and recovery requirements are met.
- Back navigation resumes server state and cannot duplicate template creation.

### Login and method chooser

- Label the first-party method “Use face recognition” with its approved verifier/device qualifier. Label adapters by their actual authenticator, such as “Use a passkey” or “Continue with Contoso.”
- For passkey adapters, supporting copy may say that the device might request face, fingerprint, PIN, or another unlock method; it must not imply that the passkey itself is the first-party Face authenticator.
- Eligibility, ordering, and fallback come from the server catalog.
- Loading must preserve layout; unavailable providers are disabled with a safe explanation.

### Native biometric prompt handoff

- Display a pre-prompt explanation only when it reduces surprise; never imitate the operating-system biometric UI.
- Invoke the native API only after explicit user action.
- Treat cancel, lockout, no enrollment, sensor unavailable, and system interruption as distinct local results mapped to safe server ceremony errors.
- On return, restore focus to the triggering control or the first error heading.

### First-party verification capture

- Show transaction purpose before capture so the user can detect an unexpected request.
- Use a fresh server challenge and approved liveness mode.
- Provide bounded attempts, cancel, alternative method, recovery, and safe support reference.
- On no-match, do not reveal whether another enrolled identity matched or expose confidence values.
- On suspected spoofing, fail safely and route according to policy without explaining detector rules.

### Federation callback

- Show provider branding only from approved configuration.
- Provide processing, delayed, retryable failure, terminal failure, identity mismatch, and takeover-risk states.
- Do not place tokens, claims, or error descriptions from the upstream provider into the URL or visible debug content.

### Evidence detail

- Display `face` as “Facial recognition” with an “Evidence supplied by…” qualifier.
- Show authentication time, freshness, provider/authenticator, ceremony purpose, evidence trust profile, and audit reference.
- Distinguish “reported by trusted upstream provider” from “verified through an approved native integration.”
- Explain that the application did not receive or store a face image.
- If modality confidence is insufficient, replace the value with “User verified.”

### Authenticator detail, replacement, and deletion

- Detail shows active/suspended/replacement-required/revoked/deletion-pending status, label, verifier/profile, consent, created/last-used dates, recovery posture, and audit timeline.
- Replacement is a complete enrollment ceremony and never edits a biometric template in browser state.
- Suspend, revoke, remove, and delete require recent authentication and proportional impact confirmation.
- Deletion status separates immediate authentication revocation from asynchronous template erasure.
- Failed deletion provides retry/escalation without restoring authenticator usability.

### Recovery

- Offer backup passkey/security key, recovery code, supervised recovery, or another policy-approved method.
- Recovery never reactivates an old face template; it leads to a new enrollment.
- Recovered sessions carry reduced/recovery assurance until required step-up is completed.
- Post-recovery checklist covers session review, notification review, and face re-enrollment.

### Policy and provider configuration

- Configure allowed issuers/integrations, required trust profiles, maximum evidence age, permitted applications, fallback methods, and assurance mapping.
- Require explicit acknowledgment before enabling face-specific policy because platform WebAuthn normally cannot prove modality.
- Prevent publication when no eligible fallback exists or the provider is unhealthy.
- Never offer an option to accept arbitrary raw `amr` strings.

## 7. Ceremony states

Every interactive flow must implement:

- initializing and eligibility loading;
- ready and explicit user start;
- awaiting OS or external provider;
- submitting and callback processing;
- retryable failure;
- biometric unavailable or not enrolled;
- consent required, declined, withdrawn, or outdated;
- permission required, denied, or permanently denied;
- preflight incompatible or degraded;
- enrollment capture, quality retry, and activation pending;
- liveness failure, no match, and suspected spoofing;
- active, suspended, replacement required, revoked, and compromised;
- deletion pending, completed, failed, or under manual review;
- user cancellation;
- timeout or expired ceremony;
- provider outage;
- untrusted or insufficient evidence;
- policy changed during ceremony;
- blocked or attempts exhausted;
- successful completion;
- successful completion requiring another factor;
- switch-method and safe exit.

Refresh must resume the server-owned ceremony and must not reopen a biometric prompt automatically.

## 8. Components

Reuse or extend:

- `CeremonyShell`, `AuthenticatorMethodPicker`, `PasskeyPrompt`, and `ProviderButton`;
- `CeremonyProgress`, `MethodSwitchMenu`, and `CeremonyResult`;
- `AuthenticationContextSummary`, `AssuranceSummary`, and `EvidenceFreshnessBadge`;
- `AuthenticatorEventTimeline`, `AuditReference`, and `PolicyImpactPreview`;
- `UnsupportedEnvironmentState`, `BlockedCeremonyState`, and `InlineMutationResult`.

Add:

- `BiometricEvidenceQualifier` for direct, transformed, and insufficient modality evidence;
- `BiometricPrivacyNotice` explaining local processing and data boundaries;
- `EvidenceProvenancePanel` with approved, redacted fields only.
- `BiometricConsentRecord`;
- `FaceCapturePreflight`;
- `FaceCaptureShell` for approved native/verifier implementations;
- `CaptureQualityGuidance` with nonvisual equivalents;
- `LivenessChallengeStatus`;
- `BiometricAuthenticatorLifecycle`;
- `BiometricDeletionStatus`.

## 9. Data and API expectations

The frontend requires server-owned fields for ceremony ID/state/purpose, eligibility, consent document/version/status, approved capture/verifier profile, permission/preflight requirements, capture step projection, liveness challenge/result class, enrollment/template reference projection, authenticator lifecycle, deletion job/status, trusted display name, evidence source, normalized AMRs, authentication time, freshness, trust profile, policy satisfaction, next step, safe error, audit reference, and allowed recovery actions.

The server must return a presentation-safe distinction among:

- `face_verified`;
- `user_verified_modality_unknown`;
- `upstream_face_trusted`;
- `upstream_face_untrusted`;
- `face_evidence_stale`.

Generic browser/application state must not receive biometric samples, templates, feature vectors, match/liveness scores, sensor data, or unrestricted upstream claims. Approved native capture code may handle samples only transiently and directly within the documented verifier transfer boundary.

## 10. Responsive and native behavior

- Narrow layouts use one primary action and stack evidence facts in definition-list order.
- Wide layouts may place safe help copy beside the ceremony but never beside a live OS prompt imitation.
- Long provider names wrap without moving the primary action off screen.
- Native applications use the platform authentication API and system prompt; web components must not be embedded to mimic it.
- First-party capture uses an approved native module or hardened capture application; ordinary web React components do not process biometric media.
- Native capture supports portrait/landscape changes, interruption, device lock, permission changes, and safe buffer clearing.
- Deep-link or app-resume handling must bind to the original ceremony and reject stale callbacks.

## 11. Accessibility

- Method controls expose authenticator name, not guessed modality.
- Status changes and callback completion are announced through a polite live region.
- Errors receive focus at the summary, with a direct retry or switch-method action.
- All evidence badges have text equivalents; color is never the only trust indicator.
- Support 200% zoom, forced colors, high contrast, reduced motion, and keyboard-only operation.
- Do not repeatedly trigger OS prompts for screen-reader users.
- Provide an equivalent alternative for users who cannot position, see, remain still, expose their face, or use the required sensor.
- Capture guidance must have spoken, textual, haptic where appropriate, and non-color equivalents.

## 12. Security and privacy

- No biometric material outside the approved transient native/verifier boundary, including application state, DOM, general storage, analytics, logs, URLs, screenshots, crash reports, or support payloads.
- Enforce origin, RP, transaction, tenant, subject, provider, nonce, and callback binding on the server.
- Redact provider claims and precise device details.
- Treat unexpected `face` claims as rejected evidence unless a configured transformation profile accepts them.
- Reauthentication is required before linking/unlinking providers or removing the last usable authenticator.
- Enrollment requires presentation-attack detection, duplicate/cross-subject safeguards, encrypted template storage, separation of duties, and signed verifier results.
- Consent withdrawal, revocation, and deletion have explicit server-enforced semantics and retention policy.

## 13. Analytics and audit

Allowed analytics: method offered, ceremony started, OS/provider handoff, safe error class, fallback selected, and completion. Analytics must not include biometric modality unless the event is an authorized security audit record.

Audit events cover accepted/rejected evidence, trust profile, provider, freshness decision, policy version, ceremony purpose, account-link changes, authenticator revocation, and administrator policy changes.

First-party audit additionally covers consent, enrollment start/completion, liveness result class, template reference creation, authentication result, suspension, replacement, revocation, recovery, deletion request/completion/failure, verifier/profile version, and privileged operator access without biometric material.

## 14. Test matrix

Required tests include:

- generic WebAuthn UV does not render `face`;
- trusted normalized evidence renders the qualified label;
- untrusted, stale, conflicting, and missing evidence cannot satisfy policy;
- OS cancellation, lockout, unavailable sensor, timeout, and resume;
- federation callback success, outage, mismatch, replay, and takeover block;
- policy change during ceremony;
- keyboard, screen reader, zoom, contrast, and reduced motion;
- no biometric data or raw claims in DOM, storage, logs, URLs, analytics, or error reports;
- cross-tenant and cross-subject evidence denial.
- consent accept/decline/withdraw/update and accessible-alternative routing;
- permission grant/deny/permanent deny and preflight incompatibility;
- enrollment capture, quality retry, liveness pass/fail, duplicate prevention, activation, and cancellation;
- first-party verification success, no match, spoof suspicion, attempts exhausted, and recovery;
- replacement overlap, suspension, revocation, last-factor removal prevention, and notification;
- deletion pending/completed/failed/manual-review and proof that revoked templates cannot authenticate;
- native buffer clearing and proof that media/templates/scores never enter general application or operational surfaces.

## 15. Acceptance criteria

- No UI calls a generic passkey “face authentication.”
- A user can enroll, activate, authenticate, step up, replace, suspend, revoke, recover, withdraw consent, and delete a first-party face authenticator end to end.
- `face` appears only with server-approved provenance and freshness.
- Login, step-up, callback, native handoff, result, evidence, policy, health, and audit states are complete.
- Every failure offers a safe retry, fallback, recovery, or terminal explanation.
- The flow works across web and native platforms without imitating system biometric prompts.
- Administrators can simulate and safely roll out face-specific evidence policy.
- Security tests demonstrate that biometric material never reaches generic browser/application UI, telemetry, or operational surfaces outside the approved transient native/verifier boundary.
- Approved native capture and verifier boundaries are explicit, tested, and operationally observable without exposing biometric material.

## 16. Dependencies and decisions

- Define and implement the first-party face capture, liveness, matcher, signed-result, template, consent, and deletion contracts.
- Define the trusted external biometric-evidence profile and transformation authority.
- Define retention and regional privacy requirements for biometric-related audit metadata.
- Correct static WebAuthn AMR assumptions before presenting modality or hardware claims.

## References

- [AMR screen support matrix](../../amr-screen-support-matrix.md)
- [Universal authenticator ceremony brief](../uix-pairing-briefs/40-authenticator-ceremony-api-universal-authenticator-pages-uix.md)
- [Canonical AMR vocabulary](../../../pkgs/10-concrete/tigrbl-jose-concrete/src/tigrbl_jose_concrete/amr.py)
