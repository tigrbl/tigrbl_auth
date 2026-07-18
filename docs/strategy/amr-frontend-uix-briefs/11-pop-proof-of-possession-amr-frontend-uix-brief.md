# Proof-of-Possession AMR Frontend UIX Brief

- **AMR:** `pop`
- **Current delivery status:** Partial; contract exists, DPoP/mTLS do not currently advertise `pop`
- **Delivery target:** Complete first-party proof-of-possession registration, validation, evidence, lifecycle, policy, and tooling product
- **Category:** Key possession evidence
- **Primary rule:** Proof of possession is server-verified evidence, not a user-selectable authenticator label
- **Platforms:** Developer/service web, tenant/platform policy, native key stores, hardware devices, CLI/SDK diagnostics

## UIX delivery priority

**P0 — Actual authentication/proof UIX (ship first):** runtime proof requirement → local key authorization → proof generation → submission/handshake → nonce-required retry → malformed/signature/binding/audience/freshness/replay/policy failure states → success evidence and continuation. For machine identities, the primary P0 surface may be native SDK/CLI plus a web validation result rather than a human login page. This is the release gate.

**P1 — Enrollment and lifecycle:** public-key/certificate registration, ownership proof, activation, evidence detail, rotation/overlap, compromise, revocation, and reprovisioning recovery.

**P2 — Administration and operations:** DPoP/mTLS/assertion policy, validation workbench, verifier/nonce/replay health, dependency impact, audit, and diagnostics.

Configuration screens do not make PoP first class. The runtime P0 proof ceremony and its client-facing failure/retry UX must work first.

**Release gate:** P0 must be interaction-complete and validated before P2 administration/configuration/management UIX is treated as delivery. P2 screens cannot be used to claim first-class authenticator support.

## 1. Mandate

Deliver complete configuration, proof, evidence, lifecycle, rotation, policy, and diagnostic experiences for proof-of-possession profiles including DPoP, mTLS, `private_key_jwt`, and approved workload-key mechanisms. The UI must explain that DPoP is a sender constraint and is not client authentication by itself.

### First-party enrollment and recovery semantics

Registration plus ownership proof is the `pop` enrollment ceremony. It creates a bound public-key/certificate credential only after the client proves control of the private key. Recovery never restores or exports a lost private key: a human, client, or workload follows an authorized reprovisioning flow, registers a new key, proves ownership, activates overlap where safe, and revokes the missing/compromised binding. Recovery screens must show dependent tokens/services, reduced/degraded operation, emergency authority, notifications, and completion evidence.

## 2. Users and jobs

- Developers register public keys/certificates and validate exact proof requirements.
- Service operators rotate keys/certificates without downtime and inspect binding evidence.
- Administrators define algorithms, nonce, audience, replay, freshness, and profile requirements.
- Platform operators manage validators, trust, conformance, and outages.
- Native/CLI clients generate proofs using local keys without exposing private material.

## 3. Required screens

| Screen | Purpose |
|---|---|
| Authentication-profile chooser | Select DPoP, mTLS, `private_key_jwt`, or workload profile |
| Public-key/JWKS registration | Register public material and metadata |
| Certificate/CSR registration | Configure mTLS public certificate/profile |
| Ownership-proof ceremony | Prove control of the registered key |
| DPoP configuration | Show algorithms, nonce policy, token binding, and endpoints |
| mTLS configuration | Show chain/profile, SAN/EKU, thumbprint, and binding |
| Assertion configuration | Explain `iss`, `sub`, audience, expiry, `jti`, and algorithm |
| Synthetic validation tool | Test proofs with synthetic/redacted requests |
| Evidence detail | Show proof type, key binding, time, freshness, replay outcome |
| Credential detail | Show public fingerprint, key ID, status, dates, and usage |
| Rotation/overlap | Add replacement, activate, verify traffic, retire old key |
| Revoke/compromise | Revoke safely and explain dependent impact |
| Policy editor | Configure permitted profiles/algorithms and assurance mapping |
| Provider/validator health | Monitor nonce, replay, certificate, and proof validation |
| Audit/diagnostics | Correlate proof failures without logging proof secrets |
| Native key-store prompt | Authorize signing or certificate selection |
| CLI/SDK output | Generate/test proof locally with redacted diagnostics |

## 4. Registration and ownership flow

1. Select profile based on server capability and application/service compatibility.
2. Register public JWK/JWKS, certificate, CSR information, or attested public key; private keys are never uploaded.
3. Validate algorithm, key use, size/profile, identifiers, chain, expiry, and duplicates.
4. Server issues a bound ownership challenge.
5. Client signs or performs the required handshake using its local key.
6. Server validates and activates the binding.
7. Completion shows public fingerprint, key ID, binding type, status, next rotation date, and example requirements.

## 5. Proof-validation flow

1. Configuration page shows endpoint-specific proof requirements.
2. Synthetic tool creates a safe request descriptor or accepts a redacted public proof fixture.
3. Native/CLI client generates proof locally.
4. Server validates signature, key binding, method/URI or audience, time, nonce, `jti`, replay, and policy.
5. Result separates malformed, signature, binding, nonce, freshness, replay, certificate, and policy failures.
6. Successful evidence may include `pop` only when the profile's authentication context permits it.

## 6. Rotation and revocation

1. Add replacement public material without changing the active key.
2. Prove ownership and validate profile.
3. Start overlap and show both bindings with traffic/last-use projections.
4. Activate replacement and test production-safe validation.
5. Retire/revoke prior key after confirmation.
6. Emergency compromise skips ordinary overlap but requires impact confirmation, notification, and audit.

## 7. Screen behavior

- Clearly separate client authentication, token sender constraint, and resource proof.
- Show public identifiers only; mask safe prefixes where useful.
- Example requests use synthetic keys/tokens and never interpolate real secrets.
- DPoP displays `jkt`, algorithms, nonce posture, replay posture, and bound token types.
- mTLS displays `x5t#S256`, chain/profile result, SAN/EKU, expiry, and trust source.
- Evidence detail shows verifier, profile, proof time, freshness, key binding, replay result, policy version, and audit reference.
- Destructive actions show affected apps/services/tokens and require typed or explicit confirmation proportional to impact.

## 8. States

Support no key, draft, validation pending, ownership proof required, active, overlap, replacement active, retiring, expired, suspended, compromised, revoked, algorithm rejected, certificate invalid, nonce required, nonce stale, proof malformed, signature invalid, binding mismatch, replay detected, provider unavailable, rate limited, policy changed, success, and degraded validation.

## 9. Components

Reuse `CertificateUploader`, `CertificateFingerprint`, `PublicKeySummary`, `JwksEditor`, `OneTimeSecretReveal` where appropriate, `PolicyImpactPreview`, `DangerZone`, `AuditReference`, and shared async/result states.

Add `ProofProfilePicker`, `OwnershipProofCeremony`, `DpopBindingSummary`, `MtlsBindingSummary`, `AssertionRequirements`, `ProofValidationWorkbench`, `KeyOverlapTimeline`, and `DependentTrafficImpact`.

## 10. Data/API expectations

Server fields include profile, public key/certificate projection, fingerprints, algorithms, binding identifiers, nonce policy, replay posture, ownership status, validation result classes, lifecycle actions, dependent-resource impact, policy version, and audit reference.

Private keys, real bearer tokens, reusable proofs, client secrets, unrestricted certificates, and replay-store internals never enter frontend telemetry or persisted state.

## 11. Responsive, accessibility, and non-web

- Dense public-key/certificate facts become semantic definition lists at narrow widths.
- Code/examples wrap or scroll within labeled regions and have accessible copy controls.
- Native prompts identify the requesting application and purpose before signing.
- CLI defaults to redacted structured output, reads sensitive material through secure key-store references, and never encourages private keys on command lines.
- All configuration and diagnostic actions support keyboard, screen reader, high contrast, zoom, and reduced motion.

## 12. Security

- Prove ownership before activation and bind proof to tenant, client/service, key, challenge, purpose, and time.
- Prevent replay, algorithm downgrade, key substitution, audience/method/URI confusion, certificate confusion, and cross-tenant binding.
- Rotation never reuses private material generated by the server unless an explicitly governed HSM workflow owns it.
- Validation tools accept synthetic/redacted data only.

## 13. Analytics and audit

Analytics records profile selection, registration stage, safe validation class, rotation stage, and completion. Audit public-key/certificate registration, ownership proof, activation, validation result, replay rejection, rotation, revocation, compromise, policy/provider changes, and administrator identity.

## 14. Tests

- Registration, ownership proof, activation, validation, overlap, rotation, retirement, revoke, and compromise flows pass.
- DPoP method/URI, nonce, `jti`, time, and replay failures are distinct and safe.
- mTLS chain/profile/binding failures are safe.
- No private keys or reusable secrets reach browser storage, logs, URLs, analytics, or support payloads.
- Cross-tenant, key substitution, algorithm downgrade, audience confusion, accessibility, responsive, native key-store, and CLI tests pass.

## 15. Acceptance criteria

- Every profile has complete setup, proof, evidence, lifecycle, rotation, policy, diagnostics, and non-web tooling.
- DPoP is never described as sufficient client authentication by itself.
- `pop` is emitted only from accepted server evidence.
- Private keys remain in client/device/key-store boundaries.
- Rotation and emergency revocation clearly protect dependent services.

## 16. Dependencies

- Profile-specific proof verifiers and replay/nonce stores.
- Public key/certificate repositories and lifecycle APIs.
- Evidence mapping that determines when `pop` is appropriate.
- SDK/CLI and native key-store adapters.

## References

- [AMR screen support matrix](../../amr-screen-support-matrix.md)
- [Universal authenticator ceremony brief](../uix-pairing-briefs/40-authenticator-ceremony-api-universal-authenticator-pages-uix.md)
- [Canonical AMR vocabulary](../../../pkgs/10-concrete/tigrbl-jose-concrete/src/tigrbl_jose_concrete/amr.py)
