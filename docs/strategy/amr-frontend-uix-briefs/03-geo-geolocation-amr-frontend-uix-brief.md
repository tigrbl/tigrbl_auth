# Geolocation AMR Frontend UIX Brief

- **AMR:** `geo`
- **Current delivery status:** Derived/contextual capability is not productized
- **Delivery target:** Complete first-party geolocation evidence, consent, policy, step-up, provenance, privacy, and operations service
- **Category:** Authentication context evidence
- **Primary implementation rule:** Location may influence authentication but must not be presented as an identity proof by itself
- **Platforms:** Web, native mobile/desktop, tenant/platform administration, audit and diagnostics

## UIX delivery priority

**P0 — Actual authentication UIX (ship first):** login context evaluation → precise-location purpose/consent when required → browser/OS permission handoff → collecting/evaluating state → denied/unavailable/low-accuracy/stale/conflicting evidence states → risk-triggered authenticator chooser and step-up → blocked/review/fallback → success and return to the original transaction. This contextual authentication sequence is the primary deliverable and release gate.

**P1 — User evidence and consent lifecycle:** session-context detail, consent review/withdrawal, managed-device/location-source enrollment, unfamiliar-event response, and recovery from location-driven blocks.

**P2 — Administration and operations:** zones, source/provider registration, risk policy, simulation, datasets, privacy/retention controls, health, and diagnostics.

`geo` is not a standalone credential, but its first-party UIX is still judged by the P0 authentication experience—not by whether an administrator can draw zones or configure providers.

**Release gate:** P0 must be interaction-complete and validated before P2 administration/configuration/management UIX is treated as delivery. P2 screens cannot be used to claim first-class authenticator support.

## 1. Mandate

Deliver the complete user and administrative experience needed to collect or consume approved location evidence, apply it to authentication policy, trigger proportionate step-up, explain decisions safely, and audit provenance. The UI must distinguish precise device location, coarse network-derived location, trusted enterprise-zone evidence, and unverified upstream claims.

`geo` is not offered in the authenticator chooser as a method. It appears in authentication context and policy evaluation and may cause another authenticator ceremony.

### First-party enrollment and lifecycle applicability

There is no user authenticator enrollment for `geo`. The first-party equivalent is enrollment of evidence sources and consent grants: device-location permission/consent, managed-device posture registration, enterprise network-zone configuration, network-geolocation provider registration, and trusted upstream source registration. Each source has draft, active, degraded, suspended, revoked, expired, and deleted lifecycle states. Users can review and withdraw precise-location consent; administrators can rotate provider credentials/datasets and disable a source without deleting audit provenance.

## 2. Users and jobs

- End users understand when location permission is requested and recover when it is denied or unavailable.
- Account holders inspect coarse, privacy-safe location context for their sessions and events.
- Tenant administrators define location conditions, allowed sources, step-up responses, and fallbacks.
- Platform operators configure signal providers, geographic datasets, privacy controls, and health.
- Support/security analysts investigate anomalies using redacted evidence and policy versions.

## 3. Required screens

| Screen | Platform | Purpose |
|---|---|---|
| Login eligibility/loading | Web/native | Evaluate context without presenting location as a method |
| Location consent explainer | Web/native | Request precise location only when necessary and lawful |
| Browser/OS permission prompt | Browser/OS | Obtain device permission through the platform |
| Risk-triggered step-up | Web/native | Explain that additional verification is required without exposing detection logic |
| Universal ceremony states | Web/native | Run the selected authenticator after the context decision |
| Location unavailable/denied | Web/native | Offer retry, alternate evidence, or another method |
| Session context detail | Web | Show privacy-safe source, granularity, time, and policy outcome |
| Authentication event detail | Web | Show redacted location evidence and audit reference |
| Location/risk policy editor | Web | Define sources, zones, actions, freshness, and fallbacks |
| Policy simulator | Web | Test representative and boundary conditions |
| Provider/data configuration | Web | Configure source priority, dataset version, privacy, and fail behavior |
| Provider health/diagnostics | Web | Monitor latency, staleness, lookup failure, and disagreement |
| Native permission settings help | Native | Explain how to restore denied permissions without impersonating OS settings |

## 4. End-to-end flows

### Passive coarse-location flow

1. Login begins without asking for location permission.
2. Server-side network or enterprise-zone context is evaluated.
3. If policy is satisfied, authentication continues normally.
4. If risk requires step-up, the UI shows a safe explanation and eligible methods.
5. Result evidence records source, granularity, freshness, policy version, and action.

### Precise-location flow

1. The server returns `location_permission_required` with purpose and alternatives.
2. The consent screen states why location is needed, requested precision, retention, and what happens if declined.
3. Explicit user action launches the browser/OS permission prompt.
4. The client submits only the approved location payload to the bound ceremony.
5. The server validates freshness, accuracy, integrity signals, and policy.
6. Success proceeds; denied, unavailable, spoof-suspected, stale, or low-accuracy results offer policy-approved alternatives.

### Administrative flow

1. Choose approved location sources and granularity.
2. Define named zones, confidence thresholds, freshness, and resulting actions.
3. Configure fail-closed/fail-to-step-up behavior; silent fail-open is prohibited for required controls.
4. Simulate boundaries, dataset changes, VPN/proxy uncertainty, absent permission, source disagreement, and provider outage.
5. Review privacy and lockout impact, publish a version, and monitor outcomes.

## 5. Screen specifications

### Consent and permission

- Do not request precise location on page load.
- State purpose, precision, retention, sharing, and fallback before the OS prompt.
- Primary action: “Share location and continue.” Secondary action: policy-approved alternative.
- A denial must not loop or repeatedly open the permission prompt.
- “Open device settings” appears only when the platform supports a safe settings deep link.

### Step-up and blocked states

- Use safe copy such as “We need another verification step for this sign-in.”
- Do not reveal exact risk score, geofence shape, fraud rule, IP intelligence, or bypass hints.
- Show method chooser, expiry, cancel/back behavior, and support/recovery paths.
- Distinguish temporary provider outage from policy prohibition.

### Context and evidence detail

- Show source class, collection time, freshness, coarse region or named enterprise zone, and policy effect.
- Never show precise coordinates to ordinary users or administrators unless a separately authorized incident workflow requires them.
- Label inferred network location as approximate.
- Show conflicts and uncertainty without exposing sensitive detection internals.

### Policy and provider configuration

- Source types: network inference, device permission, enterprise network zone, managed-device signal, trusted upstream evidence.
- Controls: tenant/app scope, freshness, accuracy, source priority, zone membership, required response, fallbacks, retention, and regional restrictions.
- Preview affected users/apps and lockout risk.
- Provider health includes dataset age, last refresh, error rate, response time, and fail behavior.

## 6. States

Support initializing, evaluating, consent required, awaiting permission, permission granted, denied, unavailable, low accuracy, stale, source conflict, spoof suspected, submitting, step-up required, provider unavailable, retryable failure, blocked, expired, cancelled, success, and success requiring another step.

Refresh resumes server state and does not request permission again automatically.

## 7. Components

Reuse `CeremonyShell`, `CeremonyProgress`, `AuthenticatorMethodPicker`, `AuthenticationContextSummary`, `EvidenceFreshnessBadge`, `PolicyImpactPreview`, `AuditReference`, and shared blocked/expired/error states.

Add:

- `LocationConsentPanel`;
- `LocationEvidenceSummary`;
- `LocationSourceBadge` with accessible text;
- `ZonePolicyEditor` and boundary-condition simulator;
- `SignalProviderHealthCard`;
- native/browser permission adapter.

## 8. Data/API contract

The server owns purpose, required precision, allowed source, ceremony binding, maximum age, minimum accuracy, retention notice, eligible alternatives, safe reason, policy version, and result.

Presentation data must distinguish exact-device, coarse-network, enterprise-zone, upstream, unavailable, uncertain, and conflicting evidence. Precise coordinates and raw IP intelligence are excluded from ordinary frontend payloads.

## 9. Responsive and non-web behavior

- Consent copy remains readable at 200% zoom and does not bury the decline/fallback action.
- Native applications use platform permission APIs and lifecycle callbacks.
- Background/resume must reject stale location challenges.
- Desktop applications support managed-zone context without requesting irrelevant GPS permission.
- CLI/service flows use noninteractive workload policy and diagnostics; they do not present user location prompts.

## 10. Accessibility

- Permission purpose and alternatives are announced before handoff.
- Focus returns to the correct status heading after the OS prompt.
- Maps are not required; any future map must have a complete textual/table equivalent.
- Color is not the only signal for allowed, uncertain, or blocked zones.
- Keyboard, screen reader, reduced motion, forced colors, and reflow are required.

## 11. Security and privacy

- Collect the minimum precision needed and only after explicit action where permission is required.
- Never expose coordinates, IP reputation, device identifiers, or fraud rules in URLs, analytics, logs, DOM snapshots, or generic support payloads.
- Bind evidence to tenant, subject, session, ceremony, purpose, timestamp, and policy version.
- Treat client-submitted coordinates as untrusted without server verification.
- Apply configured deletion/retention and regional restrictions.

## 12. Analytics and audit

Analytics may record permission requested/granted/denied, source class, step-up required, safe error class, fallback, and completion. Do not collect coordinates or precise zones in product analytics.

Audit source, granularity class, freshness, confidence classification, policy version, decision, fallback, provider/dataset version, and administrative changes.

## 13. Tests

- Permission is never requested without explicit action.
- Denial, permanent denial, low accuracy, stale evidence, source disagreement, spoof suspicion, and provider outage have safe paths.
- Step-up does not disclose rule internals.
- Precise data never appears in URLs, analytics, logs, or unauthorized UI.
- Boundary, timezone, VPN/proxy, dataset update, cross-tenant, replay, and policy-change cases pass.
- Web/native permission resume, accessibility, reflow, and reduced-motion tests pass.

## 14. Acceptance criteria

- `geo` never appears as an addable authenticator.
- Every collection path has purpose, consent where required, minimization, and fallback.
- Context can trigger and complete an end-to-end step-up ceremony.
- Users can inspect privacy-safe session evidence.
- Administrators can configure, simulate, version, and monitor location policy.
- Provider outages and uncertain evidence fail according to explicit policy.

## 15. Dependencies

- Canonical location-evidence and provenance contract.
- Privacy/retention rules by deployment region.
- Approved source providers and dataset lifecycle.
- Risk-policy integration and safe-reason taxonomy.

## References

- [AMR screen support matrix](../../amr-screen-support-matrix.md)
- [Universal authenticator ceremony brief](../uix-pairing-briefs/40-authenticator-ceremony-api-universal-authenticator-pages-uix.md)
- [Canonical AMR vocabulary](../../../pkgs/10-concrete/tigrbl-jose-concrete/src/tigrbl_jose_concrete/amr.py)
