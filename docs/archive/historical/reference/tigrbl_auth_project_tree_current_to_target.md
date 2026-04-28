> **Historical / non-authoritative** — This document is retained for planning or provenance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# tigrbl_auth — Current Tree and Sustainable Target Tree

## Basis

This document is based on:

- the uploaded `tigrbl_auth.zip` package archive,
- the revised standards / compliance matrix,
- the requirement to adhere to the Swarmauri monorepo and Tigrbl framework model,
- the requirement to introduce ADRs, release gates, and certifiable standards evidence.

The standards matrix requires explicit certification tiers through an **independent peer claim** tier and separates implementation s from claim maturity. That means the package tree cannot be runtime-only; it needs governance, gate, spec, and evidence planes as first-class repository structure.

---

## 1. Current package tree (observed)

```text
tigrbl_auth/
├── Dockerfile
├── LICENSE
├── README.md
├── pyproject.toml
├── tests/
│   ├── conftest.py
│   ├── examples/
│   │   └── test_readme_usage.py
│   ├── i9n/
│   │   ├── test_auth_flows.py
│   │   ├── test_authorization_code_flow.py
│   │   ├── test_authorization_response_types.py
│   │   ├── test_crud_api.py
│   │   ├── test_device_code_flow.py
│   │   ├── test_full_workflow.py
│   │   ├── test_long_lived_worker_flow.py
│   │   ├── test_oidc_endpoints.py
│   │   ├── test_rfc7662.py
│   │   ├── test_rfc8414_metadata.py
│   │   ├── test_rfc8628.py
│   │   ├── test_rfc8693_token_exchange_endpoint.py
│   │   ├── test_service_key_creation.py
│   │   ├── test_service_key_introspection_flow.py
│   │   └── test_token_exchange_flow.py
│   └── unit/
│       ├── test_adapters.py
│       ├── test_auth_code_exchange_pkce.py
│       ├── test_authorize_id_token_hashes.py
│       ├── test_authorize_response_modes.py
│       ├── test_backends.py
│       ├── test_bulk_schema_fields.py
│       ├── test_crypto.py
│       ├── test_deps_imports.py
│       ├── test_engine_initialization.py
│       ├── test_security.deps.py
│       ├── test_jwks_rotation.py
│       ├── test_jwtoken.py
│       ├── test_models.py
│       ├── test_oidc_authorize_scope_nonce.py
│       ├── test_oidc_id_token.py
│       ├── test_oidc_id_token_encryption.py
│       ├── test_openapi_examples.py
│       ├── test_openapi_well_known_endpoints.py
│       ├── test_openid_configuration.py
│       ├── test_openid_userinfo_endpoint.py
│       ├── test_remote_adapter.py
│       ├── test_rfc6749_auth_flow_endpoints.py
│       ├── test_rfc6749_token_endpoint.py
│       ├── test_rfc6749_validators.py
│       ├── test_rfc6750_bearer_token.py
│       ├── test_rfc7009_token_revocation.py
│       ├── test_rfc7515_jws.py
│       ├── test_rfc7516_jwe.py
│       ├── test_rfc7517_jwk.py
│       ├── test_rfc7518_jwa.py
│       ├── test_rfc7519_jwt.py
│       ├── test_rfc7520_examples.py
│       ├── test_rfc7521_assertion_framework.py
│       ├── test_rfc7523_jwt_profile.py
│       ├── test_rfc7591_client_registration_endpoint.py
│       ├── test_rfc7591_dynamic_client_registration.py
│       ├── test_rfc7592_client_management_endpoint.py
│       ├── test_rfc7592_client_registration_management.py
│       ├── test_rfc7636_pkce.py
│       ├── test_rfc7638_jwk_thumbprint.py
│       ├── test_rfc7662_token_introspection.py
│       ├── test_rfc7662_unit.py
│       ├── test_rfc7800_proof_of_possession.py
│       ├── test_rfc7952_security_event_token.py
│       ├── test_rfc8037_eddsa.py
│       ├── test_rfc8176_amr.py
│       ├── test_rfc8252_native_app_redirects.py
│       ├── test_rfc8291_webpush_encryption.py
│       ├── test_rfc8414_authorization_server_metadata.py
│       ├── test_rfc8523_jwt_client_auth.py
│       ├── test_rfc8628_device_authorization.py
│       ├── test_rfc8693_token_exchange.py
│       ├── test_rfc8705_compliance.py
│       ├── test_rfc8707_resource_indicators.py
│       ├── test_rfc8725_jwt_best_practices.py
│       ├── test_rfc8812_webauthn_algorithms.py
│       ├── test_rfc8932_dns_privacy.py
│       ├── test_rfc8932_enhanced_metadata.py
│       ├── test_rfc9068_jwt_profile.py
│       ├── test_rfc9101_jwt_secured_authorization_request.py
│       ├── test_rfc9126_pushed_authorization_requests.py
│       ├── test_rfc9207_issuer_identification.py
│       ├── test_rfc9396_authorization_details.py
│       ├── test_rfc9449_dpop.py
│       ├── test_runtime_cfg.py
│       ├── test_user_register_schema.py
│       └── test_well_known_endpoints_behavior.py
└── tigrbl_auth/
    ├── __init__.py
    ├── adapters/
    │   ├── __init__.py
    │   ├── auth_context.py
    │   ├── local_adapter.py
    │   └── remote_adapter.py
    ├── app.py
    ├── backends.py
    ├── crypto.py
    ├── db.py
    ├── errors.py
    ├── security.deps.py
    ├── jwtoken.py
    ├── oidc_discovery.py
    ├── oidc_id_token.py
    ├── oidc_userinfo.py
    ├── orm/
    │   ├── __init__.py
    │   ├── api_key.py
    │   ├── auth_code.py
    │   ├── auth_session.py
    │   ├── client.py
    │   ├── device_code.py
    │   ├── pushed_authorization_request.py
    │   ├── revoked_token.py
    │   ├── service.py
    │   ├── service_key.py
    │   ├── tenant.py
    │   └── user.py
    ├── principal_ctx.py
    ├── rfc/
    │   ├── __init__.py
    │   ├── rfc6749.py
    │   ├── rfc6749_token.py
    │   ├── rfc6750.py
    │   ├── rfc7009.py
    │   ├── rfc7515.py
    │   ├── rfc7516.py
    │   ├── rfc7517.py
    │   ├── rfc7518.py
    │   ├── rfc7519.py
    │   ├── rfc7520.py
    │   ├── rfc7521.py
    │   ├── rfc7523.py
    │   ├── rfc7591.py
    │   ├── rfc7592.py
    │   ├── rfc7636_pkce.py
    │   ├── rfc7638.py
    │   ├── rfc7662.py
    │   ├── rfc7662_introspection.py
    │   ├── rfc7800.py
    │   ├── rfc7952.py
    │   ├── rfc8037.py
    │   ├── rfc8176.py
    │   ├── rfc8252.py
    │   ├── rfc8291.py
    │   ├── rfc8414.py
    │   ├── rfc8414_metadata.py
    │   ├── rfc8523.py
    │   ├── rfc8628.py
    │   ├── rfc8693.py
    │   ├── rfc8705.py
    │   ├── rfc8707.py
    │   ├── rfc8725.py
    │   ├── rfc8812.py
    │   ├── rfc8932.py
    │   ├── rfc9068.py
    │   ├── rfc9101.py
    │   ├── rfc9126.py
    │   ├── rfc9207.py
    │   ├── rfc9396.py
    │   └── rfc9449_dpop.py
    ├── routers/
    │   ├── __init__.py
    │   ├── auth_flows.py
    │   ├── authz/
    │   │   ├── __init__.py
    │   │   └── oidc.py
    │   ├── schemas.py
    │   ├── shared.py
    │   └── surface.py
    ├── runtime_cfg.py
    ├── typing.py
    └── vendor/
        ├── __init__.py
        ├── fastapi.py
        ├── pydantic.py
        ├── sqlalchemy.py
        └── tigrbl.py
```

---

## 2. What is correct about the current tree

The current tree already has the right **raw ingredients**:

- a Tigrbl app assembly root in `app.py`,
- a Tigrbl router aggregation root in `routers/surface.py`,
- ORM-backed resources in `orm/`,
- standards-focused implementations and tests,
- RFC/OIDC/OpenAPI-adjacent coverage already present,
- both REST-style and JSON-RPC-oriented surface composition,
- unit and integration test layers.

That means the package is **structurally salvageable**.

---

## 3. What is incorrect or unsustainable about the current tree

### 3.1 Runtime and compliance are mixed together

The package has runtime behavior, standards claims, and test evidence all implied indirectly by a flat `rfc/` directory. That is workable for prototyping, but not for certifiable claims.

### 3.2 RFC number is being used as the primary package architecture

That is the wrong long-term boundary. Runtime code should be organized by:

- protocol surface,
- resource model,
- operational responsibility,
- security boundary,
- published API contract.

RFC numbers should instead organize:

- conformance tests,
- evidence bundles,
- target manifests,
- release claims,
- certification reports.

### 3.3 Tigrbl vendor shims are overused

`vendor/` currently re-exports Tigrbl, FastAPI, Pydantic, and SQLAlchemy symbols. That makes upgrade boundaries murkier and blurs ownership.

### 3.4 No governance plane exists

There is no first-class:

- `docs/adr/`,
- `compliance/`,
- `specs/`,
- `gates/`,
- `migrations/`,
- evidence retention policy.

### 3.5 Tests are broad but not bounded by claim type

The package has many tests, but there is no clean split among:

- unit behavior,
- integration behavior,
- conformance behavior,
- negative testing,
- interop testing,
- evidence-producing certification runs.

---

## 4. Correct sustainable project tree

This is the target tree that keeps the package Tigrbl-native **and** makes it certifiable.

### Repository placement

```text
pkgs/standards/tigrbl_auth/
```

### Sustainable bounded tree

```text
pkgs/standards/tigrbl_auth/
├── pyproject.toml
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── Makefile
├── docs/
│   ├── adr/
│   │   ├── 0001-package-boundary.md
│   │   ├── 0002-runtime-vs-compliance.md
│   │   ├── 0003-token-signing-policy.md
│   │   ├── 0004-session-and-logout-policy.md
│   │   ├── 0005-release-gate-policy.md
│   │   ├── 0006-openapi-openrpc-boundary.md
│   │   ├── 0007-evidence-and-attestation-policy.md
│   │   └── 0008-independent-peer-claim-policy.md
│   ├── architecture/
│   ├── standards/
│   ├── compliance/
│   └── runbooks/
├── compliance/
│   ├── targets/
│   │   ├── standards-matrix.yaml
│   │   ├── target-set.yaml
│   │   ├── certification-tiers.yaml
│   │   └── implementation-s.yaml
│   ├── mappings/
│   │   ├── feature-to-target.yaml
│   │   ├── target-to-endpoint.yaml
│   │   ├── target-to-test.yaml
│   │   ├── target-to-evidence.yaml
│   │   └── target-to-adr.yaml
│   ├── claims/
│   │   ├── self-asserted/
│   │   ├── certified/
│   │   └── peer-reviewed/
│   ├── evidence/
│   │   ├── fixtures/
│   │   ├── captures/
│   │   ├── interoperability/
│   │   ├── negative/
│   │   └── reports/
│   └── gates/
│       ├── foundation.yaml
│       ├── interoperable.yaml
│       ├── production.yaml
│       ├── hardening.yaml
│       └── independent-peer.yaml
├── specs/
│   ├── openapi/
│   │   ├── public.openapi.yaml
│   │   ├── admin.openapi.yaml
│   │   └── resource.openapi.yaml
│   ├── openrpc/
│   │   ├── admin.openrpc.json
│   │   └── internal.openrpc.json
│   └── jsonschema/
├── scripts/
│   ├── build_openapi.py
│   ├── build_openrpc.py
│   ├── verify_claims.py
│   ├── verify_gates.py
│   ├── collect_evidence.py
│   └── render_matrix.py
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── conformance/
│   │   ├── oauth2/
│   │   ├── oidc/
│   │   ├── jose/
│   │   ├── openapi/
│   │   └── openrpc/
│   ├── interop/
│   ├── negative/
│   ├── security/
│   ├── e2e/
│   └── fixtures/
└── tigrbl_auth/
    ├── __init__.py
    ├── plugin.py
    ├── gateway.py
    ├── version.py
    ├── api/
    │   ├── __init__.py
    │   ├── app.py
    │   ├── surface.py
    │   ├── rest/
    │   │   ├── __init__.py
    │   │   ├── authn.py
    │   │   ├── oauth2.py
    │   │   ├── oidc.py
    │   │   ├── metadata.py
    │   │   └── userinfo.py
    │   └── rpc/
    │       ├── __init__.py
    │       ├── admin.py
    │       ├── sessions.py
    │       └── diagnostics.py
    ├── tables/
    │   ├── __init__.py
    │   ├── tenant.py
    │   ├── user.py
    │   ├── client.py
    │   ├── auth_session.py
    │   ├── auth_code.py
    │   ├── device_code.py
    │   ├── api_key.py
    │   ├── service.py
    │   ├── service_key.py
    │   ├── revoked_token.py
    │   └── pushed_authorization_request.py
    ├── ops/
    │   ├── __init__.py
    │   ├── authenticate.py
    │   ├── authorize.py
    │   ├── exchange_token.py
    │   ├── introspect.py
    │   ├── revoke.py
    │   ├── register_client.py
    │   ├── register_user.py
    │   ├── publish_metadata.py
    │   └── logout.py
    ├── services/
    │   ├── __init__.py
    │   ├── token_service.py
    │   ├── session_service.py
    │   ├── discovery_service.py
    │   ├── userinfo_service.py
    │   └── registration_service.py
    ├── standards/
    │   ├── __init__.py
    │   ├── oauth2/
    │   │   ├── authorize.py
    │   │   ├── token.py
    │   │   ├── revocation.py
    │   │   ├── introspection.py
    │   │   ├── registration.py
    │   │   ├── device.py
    │   │   ├── exchange.py
    │   │   ├── metadata.py
    │   │   ├── jar.py
    │   │   ├── par.py
    │   │   ├── rar.py
    │   │   ├── issuer.py
    │   │   ├── mtls.py
    │   │   └── dpop.py
    │   ├── oidc/
    │   │   ├── discovery.py
    │   │   ├── id_token.py
    │   │   ├── userinfo.py
    │   │   ├── session.py
    │   │   └── logout.py
    │   ├── jose/
    │   │   ├── jwk.py
    │   │   ├── jws.py
    │   │   ├── jwe.py
    │   │   ├── jwt.py
    │   │   ├── thumbprint.py
    │   │   └── best_practices.py
    │   └── http/
    │       ├── well_known.py
    │       ├── tls.py
    │       └── cookies.py
    ├── adapters/
    │   ├── __init__.py
    │   ├── auth_context.py
    │   ├── local.py
    │   ├── remote.py
    │   └── key_material.py
    ├── security/
    │   ├── __init__.py
    │   ├── csrf.py
    │   ├── nonce.py
    │   ├── replay.py
    │   ├── redirect_uri.py
    │   └── audience.py
    ├── config/
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── features.py
    │   └── constants.py
    ├── db/
    │   ├── __init__.py
    │   ├── engine.py
    │   ├── session.py
    │   └── bootstrap.py
    ├── migrations/
    │   ├── env.py
    │   └── versions/
    └── cli/
        ├── __init__.py
        ├── verify.py
        ├── gates.py
        ├── evidence.py
        └── specs.py
```

---

## 5. Boundary rules for the sustainable tree

### Runtime plane

Lives under `tigrbl_auth/` and contains only executable package behavior.

### Standards plane

Lives under `tigrbl_auth/standards/` and contains reusable standards logic grouped by protocol family, not flat RFC number.

### Spec plane

Lives under `specs/` and contains generated/published OpenAPI, OpenRPC, and JSON Schema artifacts.

### Compliance plane

Lives under `compliance/` and contains claims, mappings, evidence, reports, and gate manifests.

### Governance plane

Lives under `docs/adr/` and release gate manifests. Nothing enters Tier 3 or Tier 4 claim posture without entries here.

---

## 6. Migration from current tree to sustainable tree

### 6.1 Package placement

```text
current:  tigrbl_auth/
target:   pkgs/standards/tigrbl_auth/
```

### 6.2 Direct move map

| Current | Target | Action |
|---|---|---|
| `tigrbl_auth/app.py` | `tigrbl_auth/api/app.py` | move and slim to composition root only |
| `tigrbl_auth/routers/surface.py` | `tigrbl_auth/api/surface.py` | move |
| `tigrbl_auth/routers/auth_flows.py` | `tigrbl_auth/api/rest/authn.py` and `tigrbl_auth/ops/authenticate.py` | split transport from operation logic |
| `tigrbl_auth/routers/authz/oidc.py` | `tigrbl_auth/api/rest/oidc.py` and `tigrbl_auth/ops/authorize.py` | split transport from operation logic |
| `tigrbl_auth/orm/*` | `tigrbl_auth/tables/*` | rename to Tigrbl table boundary |
| `tigrbl_auth/db.py` | `tigrbl_auth/db/{engine,session,bootstrap}.py` | split |
| `tigrbl_auth/runtime_cfg.py` | `tigrbl_auth/config/settings.py` | move |
| `tigrbl_auth/backends.py` | `tigrbl_auth/ops/authenticate.py` + `tigrbl_auth/adapters/*` | split |
| `tigrbl_auth/crypto.py` | `tigrbl_auth/standards/jose/*` | split by JOSE responsibility |
| `tigrbl_auth/jwtoken.py` | `tigrbl_auth/standards/jose/jwt.py` | move |
| `tigrbl_auth/oidc_discovery.py` | `tigrbl_auth/standards/oidc/discovery.py` | move |
| `tigrbl_auth/oidc_id_token.py` | `tigrbl_auth/standards/oidc/id_token.py` | move |
| `tigrbl_auth/oidc_userinfo.py` | `tigrbl_auth/standards/oidc/userinfo.py` | move |
| `tigrbl_auth/rfc/*` | `tigrbl_auth/standards/{oauth2,oidc,jose,http}/*` | regroup by protocol family |
| `tigrbl_auth/errors.py` | `tigrbl_auth/api/rest/errors.py` and/or `tigrbl_auth/standards/common/errors.py` | split by concern |
| `tigrbl_auth/security.deps.py` | `tigrbl_auth/api/rest/dependencies.py` | move |
| `tigrbl_auth/vendor/*` | remove | replace with direct imports |
| `tests/integration/*` | `tests/integration/*` | rename |
| `tests/unit/test_rfc*.py` | `tests/conformance/**` and `tests/unit/**` | split pure unit from claim tests |
| ad hoc OpenAPI checks | `specs/openapi/*` + `tests/conformance/openapi/*` | materialize published contract |
| no ADRs | `docs/adr/*` | add |
| no compliance manifests | `compliance/**/*` | add |
| no migrations | `tigrbl_auth/migrations/*` | add |

---

## 7. Ordered migration plan

### Device-code request item — Freeze claims

- declare the target standards set,
- remove or quarantine non-core RFCs that are not part of the certifiable auth-server boundary,
- define which claims are Tier 2, Tier 3, and Tier 4.

### Device-code polling item — Install governance

- create `docs/adr/`,
- create `compliance/targets/`,
- create `compliance/mappings/`,
- create `compliance/gates/`.

### Item 3 — Reshape runtime package

- rename `orm` to `tables`,
- move `routers` to `api`,
- split transport handlers from operational logic into `ops/`,
- split protocol logic into `standards/`.

### Item 4 — Remove `vendor/`

- convert to direct imports,
- keep compatibility shims only if temporary and clearly deprecated.

### Item 5 — Materialize contracts

- generate and check in OpenAPI artifacts,
- generate and check in OpenRPC artifacts,
- gate diffs in CI.

### Item 6 — Reshape tests

- keep pure unit tests in `tests/unit/`,
- move standards compliance tests to `tests/conformance/`,
- move wire-level and third-party checks to `tests/interop/`,
- move exploit-style and invalid-input coverage to `tests/negative/`.

### Item 7 — Install evidence and release gates

- create evidence bundle generation,
- create release attestation manifest,
- block Tier 3 claims without preserved artifacts,
- block Tier 4 claims without independent peer evidence.

---

## 8. Release gates the new tree must support

### Foundation gate

- target tree exists,
- ADR system exists,
- standards target manifests exist,
- runtime and compliance boundaries are separate.

### Interoperable gate

- OAuth2/OIDC baseline claims mapped to tests and endpoints,
- OpenAPI contract published,
- `.well-known` and JWKS publication stable.

### Production gate

- token revocation and introspection evidence retained,
- browser session and logout behavior documented,
- schema migrations in place,
- conformance suite green.

### Hardening gate

- DPoP and/or mTLS verified where claimed,
- PAR/JAR/RAR gates enforced where claimed,
- negative testing and replay defense evidence retained,
- key rotation exercised.

### Independent peer claim gate

- external interop evidence retained,
- third-party or peer-reviewed report linked,
- claim package is reproducible.

---

## 9. Bottom line

The current package tree is **correct enough to migrate**, but **not correct enough to certify**.

The correct long-term project tree is one that separates:

1. **runtime code**,
2. **standards logic**,
3. **published contracts**,
4. **compliance evidence**,
5. **architectural governance**.

That is the sustainable boundary for a certifiably compliant `tigrbl_auth` package.
