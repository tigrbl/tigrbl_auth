> [!WARNING]
> Non-authoritative supporting plan. For current feature truth, use `.ssot/registry.json` and live `uv run ssot feature list .` output.

# Remaining feature delivery plan - 2026-05-05

## Live planning basis

This plan is derived from the live feature registry on 2026-05-05.

- Remaining in-bounds features: `84`
- Remaining `partial` features: `26`
- Remaining `absent` features: `58`
- Explicit out-of-bounds features excluded from this plan: `4`

Excluded out-of-bounds features:

- `feat:cli-verb-adr-index`
- `feat:cli-verb-adr-list`
- `feat:cli-verb-adr-new`
- `feat:cli-verb-adr-show`

## Sequencing rules

1. Finish `partial` rows before starting new `absent` rows inside the same phase.
2. Do not move to the next phase until the current phase has implemented rows, linked claims/tests, and passing verification.
3. Keep API boundary work ahead of UIX work when the UIX depends on a governed contract or fail-closed behavior.
4. Keep release/provenance work after feature-surface closure so supply-chain proof reflects real implemented scope.

## Phase 1 - Surface boundary and applicability baseline

Goal: freeze the remaining surface boundaries and applicability semantics before broader feature expansion.

Features in this phase: `16`

Partial first:

- `feat:uix-admin-boundary`
- `feat:uix-public-boundary`

Then implement:

- `feat:surface-applicability-classification`
- `feat:api-admin-boundary`
- `feat:api-admin-contract-publication-boundary`
- `feat:api-admin-authz-gate`
- `feat:api-admin-resource-management-boundary`
- `feat:api-admin-policy-control-plane-boundary`
- `feat:api-admin-public-surface-exclusion`
- `feat:api-public-boundary`
- `feat:api-public-oauth-boundary`
- `feat:api-public-oidc-boundary`
- `feat:api-public-discovery-boundary`
- `feat:api-public-registration-boundary`
- `feat:api-public-logout-boundary`
- `feat:api-public-admin-surface-exclusion`

Exit criteria:

- boundary features are implemented
- admin/public API exclusion behavior is enforced
- applicability classification is encoded in authoritative repo truth

## Phase 2 - Public UIX and browser security completion

Goal: complete the public end-user UIX as a governed browser-facing surface over the public API.

Features in this phase: `15`

Partial first:

- `feat:uix-public-shell`
- `feat:uix-public-auth-session`
- `feat:uix-public-login-view`
- `feat:uix-public-logout-view`
- `feat:uix-public-registration-view`
- `feat:uix-public-recovery-view`
- `feat:uix-public-session-continuity`
- `feat:uix-public-openapi-contract-consumption`
- `feat:uix-public-browser-token-handling`
- `feat:uix-public-problem-details-rendering`
- `feat:uix-public-safe-error-disclosure`

Then implement:

- `feat:uix-public-consent-view`
- `feat:uix-public-cookie-session-model`
- `feat:uix-public-csrf-protection`
- `feat:uix-public-origin-and-redirect-constraints`

Exit criteria:

- public UIX shell and auth/session flows are implemented
- browser security controls are implemented and tested
- public UIX only consumes governed public API surfaces

## Phase 3 - Admin policy control plane and tenant-client normalization

Goal: complete the remaining administrator-facing authorization and cross-plane governance substrate.

Features in this phase: `15`

Partial first:

- `feat:f03-service-identities`
- `feat:f13-rbac`
- `feat:f14-abac`
- `feat:f16-policy-engine`
- `feat:f19-policy-simulation`
- `feat:f20-policy-audit`
- `feat:f24-fine-grained-permissions`
- `feat:f25-dynamic-conditions`
- `feat:f42-compliance-reporting`
- `feat:f45-delegated-admin`

Then implement:

- `feat:tenant-isolation-cross-plane`
- `feat:tenant-visibility-rules`
- `feat:client-policy-cross-plane`
- `feat:client-mutation-authority-rules`
- `feat:public-vs-admin-client-exposure`

Exit criteria:

- policy and delegated-admin surfaces are implemented end to end
- tenant/client visibility and mutation rules are normalized across planes
- compliance reporting is backed by real implemented state

## Phase 4 - Advanced authentication, federation, and graph authorization

Goal: implement the remaining higher-order identity and authorization capability set.

Features in this phase: `18`

Partial first:

- `feat:f08-sso`

Then implement:

- `feat:f05-passwordless-authentication`
- `feat:f06-mfa`
- `feat:f07-webauthn`
- `feat:f09-federation`
- `feat:f10-social-login`
- `feat:f11-device-identity`
- `feat:f12-workload-identity`
- `feat:f15-rebac`
- `feat:f17-policy-language`
- `feat:f18-policy-versioning`
- `feat:f21-access-decision-api`
- `feat:f22-graph-based-authorization`
- `feat:f23-relationship-modeling`
- `feat:f26-contextual-auth-time-location`
- `feat:f35-anomaly-detection-auth`
- `feat:f46-trust-federation-graphs`
- `feat:f47-cross-cloud-identity`

Exit criteria:

- advanced authn and federation capabilities are implemented
- graph and relationship-based authorization surfaces are implemented
- higher-order contextual and anomaly-aware controls are testable and governed

## Phase 5 - Provisioning, governance workflows, and ecosystem extension

Goal: complete the operator and integrator workflows that broaden adoption and enterprise governance.

Features in this phase: `5`

Partial first:

- `feat:f39-sdk-ecosystem`
- `feat:f40-extensibility-plugins`

Then implement:

- `feat:f33-scim-provisioning`
- `feat:f43-access-review-workflows`
- `feat:f44-entitlement-management`

Exit criteria:

- provisioning and entitlement lifecycle workflows are implemented
- ecosystem and plugin surfaces are governed and operational
- operator workflows are integrated with the broader authorization model

## Phase 6 - Transport, disclosure, and release provenance hardening

Goal: close the remaining posture, disclosure, and release-governance features after functional surface completion.

Features in this phase: `15`

Then implement:

- `feat:transport-http11-posture`
- `feat:transport-http2-posture`
- `feat:transport-http3-posture`
- `feat:transport-quic-posture`
- `feat:uix-schema-safe-disclosure`
- `feat:uix-jws-safe-disclosure`
- `feat:uix-jwe-safe-disclosure`
- `feat:uix-jwt-safe-disclosure`
- `feat:uix-jwks-safe-disclosure`
- `feat:release-ssdf-requirements`
- `feat:release-slsa-requirements`
- `feat:release-in-toto-requirements`
- `feat:release-sigstore-requirements`
- `feat:release-spdx-requirements`
- `feat:release-cyclonedx-requirements`

Exit criteria:

- transport posture is explicitly implemented and validated
- UIX disclosure boundaries are implemented and tested
- release provenance and SBOM requirements are implemented with reproducible evidence

## Coverage check

This plan must continue to cover exactly the live set of in-bounds `partial` and `absent` features. If feature status or horizon changes, regenerate this plan from `.ssot/registry.json` instead of hand-maintaining stale lists.
