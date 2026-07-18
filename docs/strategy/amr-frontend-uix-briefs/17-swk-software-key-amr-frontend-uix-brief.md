# Software-Secured Key AMR Frontend UIX Brief

- **AMR:** `swk`
- **Current delivery status:** Partial; key mechanisms exist but evidence-driven software-key classification/emission does not
- **Delivery target:** Complete first-party software-key creation, registration, proof, lifecycle, recovery, policy, SDK/CLI, and operations product
- **Category:** Possession/key-protection evidence
- **Platforms:** Web, native OS key stores, developer/service configuration, CLI/SDK, account/admin evidence

## UIX delivery priority

**P0 — Actual authentication/proof UIX (ship first):** software-key method/profile selection → transaction/proof requirement → native keystore authorization → signing/proof generation → submission → locked/missing/denied/stale/replayed/binding/algorithm failure states → reprovision/fallback → success evidence and continuation. Human, SDK, and CLI runtime proof paths are the release gate.

**P1 — Enrollment and lifecycle:** key creation/selection, public registration, ownership proof, activation, detail, rotation/overlap, compromise, revocation, and reprovisioning recovery.

**P2 — Administration and operations:** key-origin/algorithm/export policy, client/workload configuration, keystore/provider health, validation workbench, audit, and diagnostics.

Software-key configuration is not the primary UIX. First-class delivery requires a complete P0 local-key authorization and runtime proof experience.

**Release gate:** P0 must be interaction-complete and validated before P2 administration/configuration/management UIX is treated as delivery. P2 screens cannot be used to claim first-class authenticator support.

## 1. Mandate

Deliver complete registration, proof, evidence, lifecycle, rotation, compromise, policy, and diagnostic experiences for software-secured keys. Distinguish software-protected from hardware-backed and unknown key storage; never infer `swk` merely because a JWK or passkey exists.

### First-party enrollment semantics

Software-key creation, public-key registration, and ownership proof together form the enrollment ceremony. The first-party flow must generate or select a key in an approved software keystore, register public material, prove possession, classify key origin from accepted evidence, establish recovery/reprovisioning, and activate the credential. Browser-only public-key registration without local ownership proof is incomplete enrollment.

## 2. Required screens

| Screen | Purpose |
|---|---|
| Key/profile chooser | Select passkey, DPoP, `private_key_jwt`, signing, or workload profile |
| Software-key introduction | Explain storage boundary, backup, portability, compromise, and alternatives |
| Public-key/JWKS registration | Register public material only |
| Native software-key creation | Generate/import through approved OS/application keystore |
| Ownership-proof ceremony | Prove possession without exporting private key |
| Login/step-up handoff | Use approved key-based human profile when applicable |
| Signing/proof ceremony | Generate bound proof/assertion |
| Evidence detail | Show verified software-key classification, provenance, time, freshness |
| Key credential detail | Show public fingerprint, key ID, profile, storage class, status, dates |
| Rotation/overlap | Activate replacement before retirement |
| Compromise/revoke | Invalidate and explain dependent impact |
| Recovery/reprovision | Restore access without restoring a compromised key |
| Key-origin policy | Configure accepted software stores, algorithms, backup/export, app scope |
| Client/workload configuration | Configure JWKS, DPoP, assertions, or service proof |
| Validation workbench | Test synthetic proofs and public metadata |
| Provider/key-store health | Monitor integration and validator availability |
| Audit/diagnostics | Show redacted key-origin/proof/lifecycle events |
| CLI/SDK key tooling | Generate, reference, prove, rotate, and diagnose locally |

## 3. Registration flow

1. User/operator selects a supported profile.
2. Introduction explains whether software-key storage is acceptable and whether export/backup is permitted.
3. Native/CLI adapter creates or selects a key in the approved software keystore.
4. Public JWK/JWKS or equivalent is registered; private key stays local.
5. Server validates algorithm/use/identifier and issues ownership challenge.
6. Local key signs; server validates binding and key-origin evidence if available.
7. Activation displays `swk` only when accepted evidence proves software protection; otherwise show “Backing not verified.”

## 4. Proof and authentication flow

1. Server issues bound proof requirements including purpose, audience/endpoint, time, nonce/`jti`, and algorithm.
2. Native/CLI/app adapter requests local key authorization and signs.
3. Server validates signature, binding, freshness, replay, and policy.
4. Result provides normalized evidence and next step.
5. Locked/unavailable keystore, missing key, denied authorization, stale proof, replay, and unsupported algorithm route to retry/reprovision/recovery.

## 5. Lifecycle

- Detail shows safe public identifiers, storage classification/provenance, profile, created/last-used, status, backup/export posture, and dependencies.
- Rotation uses overlap, ownership proof, activation, traffic verification, and explicit retirement.
- Compromise revokes immediately and requires a newly generated key; restoring the same private key is not recovery.
- Human last-factor and machine outage safeguards are proportional to scope.

## 6. Screen behavior

- Never offer “download private key” as a routine browser action.
- Do not label unknown or platform-synced storage as `swk` without evidence.
- Show hardware/software/unknown classifications as mutually clear evidence results, not quality rankings without policy context.
- Examples use synthetic material.
- Diagnostics redact public identifiers where tenant policy requires it and never accept private keys in browser text areas.

## 7. States

Support no key, selecting store, generation pending, authorization required, public registration, ownership proof, active, backing verified/unverified, locked store, missing key, denied, algorithm rejected, replay/stale proof, overlap, replacement active, compromised, revoked, recovery/reprovision, provider unavailable, policy changed, success, and degraded evidence.

## 8. Components

Reuse `PublicKeySummary`, `JwksEditor`, `CertificateFingerprint` where relevant, `CeremonyShell`, `OneTimeSecretReveal` only for non-private recovery artifacts, `PolicyImpactPreview`, `DangerZone`, and audit/result components.

Add `KeyStorePicker`, `SoftwareKeyPrivacyNotice`, `KeyBackingBadge`, `OwnershipProofCeremony`, `KeyDependencyImpact`, `KeyRotationTimeline`, and native/CLI keystore adapters.

## 9. Data/API expectations

Server returns profile, public key projection, algorithms, ownership state, key-origin evidence/provenance, storage classification, lifecycle, dependency impact, proof result classes, policy version, and audit reference. Private keys, keystore credentials, reusable proofs, and unrestricted device details never enter frontend payloads.

## 10. Responsive, accessibility, and non-web

- Public-key facts reflow into semantic lists; code samples have labeled scroll/copy controls.
- Native key authorization uses platform prompts and returns focus/status accessibly.
- CLI uses secure keystore references and structured redacted output; private keys and PINs are never command arguments.
- Desktop/native resume is bound to the original ceremony.

## 11. Security

- Bind registration/proof to tenant, subject/client/service, key, purpose, ceremony, audience/endpoint, nonce/`jti`, and time.
- Prevent key substitution, replay, algorithm downgrade, audience confusion, cross-tenant binding, and unsafe export.
- Require recent authority for lifecycle actions.
- `swk` is server-derived from approved evidence, never client asserted.

## 12. Analytics and audit

Analytics records profile, registration/proof funnel, safe key-store class, rotation stage, and completion. Audit public registration, origin classification, ownership proof, use, replay rejection, rotation, compromise, revoke, reprovision, policy/provider changes, and operator actions.

## 13. Tests

- Generate/select, register, prove, authenticate, rotate, revoke, compromise, and reprovision pass across supported stores.
- Unknown origin does not render `swk`; accepted evidence does.
- Locked/missing store, denied authorization, replay, stale proof, key substitution, algorithm downgrade, and provider outage fail safely.
- No private material leaks to browser, telemetry, URLs, logs, or CLI history.
- Accessibility, responsive, native resume, cross-tenant, and dependency-impact tests pass.

## 14. Acceptance criteria

- All web, native, and CLI key flows are complete.
- Private keys stay in approved software-key boundaries.
- Software backing is evidence-derived.
- Rotation/revocation protects dependent clients/services and human recovery.
- Administrators can govern accepted stores, algorithms, backup/export, and assurance.

## 15. Dependencies

- Key-origin evidence and classification contract.
- Native/CLI software-keystore adapters.
- Profile-specific proof validators and replay protection.
- Key lifecycle/dependency inventory and recovery authority.

## References

- [AMR screen support matrix](../../amr-screen-support-matrix.md)
- [Universal authenticator ceremony brief](../uix-pairing-briefs/40-authenticator-ceremony-api-universal-authenticator-pages-uix.md)
- [Canonical AMR vocabulary](../../../pkgs/10-concrete/tigrbl-jose-concrete/src/tigrbl_jose_concrete/amr.py)
