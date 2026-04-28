> [!WARNING]
> Archived historical reference. This document is retained for audit history only and is **not** an authoritative current-state artifact.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` for the current source of truth.

# tigrbl_auth — 10 Usage Examples

These examples are split between:

- **Current-surface compatible examples**: grounded in the uploaded package's existing `surface_api`, discovery, token, introspection, device-flow, and token-exchange surfaces.
- **Target-tree examples**: aligned to the proposed Tigrbl-native tree with `plugin.py`, `api/`, `specs/`, `compliance/`, `gates/`, and `docs/adr/`.

---

## 1. Mount the auth package into a Tigrbl app

```python
from tigrbl.engine import engine
from tigrbl import TigrblApp
from tigrbl_auth.db import dsn
from tigrbl_auth.routers.surface import surface_api

app = TigrblApp(engine=engine(dsn))
surface_api.mount_jsonrpc(prefix="/rpc")
surface_api.attach_diagnostics(prefix="/system")
app.include_router(surface_api)
```

---

## 2. Run the app locally and inspect the REST docs

```bash
uvicorn tigrbl_auth.app:app --reload
open http://localhost:8000/docs
```

---

## 3. Read OIDC discovery metadata

```bash
curl http://localhost:8000/.well-known/openid-configuration | jq
```

Typical use:
- verify `issuer`
- verify `jwks_uri`
- verify `authorization_endpoint`, `token_endpoint`, and supported scopes

---

## 4. Read the JWKS document for token validation

```bash
curl http://localhost:8000/.well-known/jwks.json | jq
```

Typical use:
- hand the JWK set to a resource server
- validate `kid` rotation behavior
- verify signing keys published by the issuer

---

## 5. Use PKCE helpers for an authorization-code client

```python
from tigrbl_auth import create_code_verifier, create_code_challenge

verifier = create_code_verifier()
challenge = create_code_challenge(verifier)

print({
    "code_verifier": verifier,
    "code_challenge": challenge,
    "code_challenge_method": "S256",
})
```

Typical use:
- SPA
- native app
- confidential client using hardened auth-code flow

---

## 6. Introspect an access token or API key

```bash
curl -X POST http://localhost:8000/introspect \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'token=YOUR_ACCESS_TOKEN'
```

Typical use:
- API gateway asks whether token is active
- resource server checks validity and claims
- compliance tests verify RFC 7662 behavior

---

## 7. Run the device-code flow

```bash
# Device-code request item: request a device code
curl -X POST http://localhost:8000/device_codes/device_authorization \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'client_id=test-client&scope=openid'

# Device-code polling item: poll the token endpoint after approval
curl -X POST http://localhost:8000/token \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=urn:ietf:params:oauth:grant-type:device_code&device_code=DEVICE_CODE&client_id=test-client'
```

Typical use:
- CLI login
- TV/device activation
- headless fleet onboarding

---

## 8. Exchange a subject token for a narrower audience token

```bash
curl -X POST http://localhost:8000/token/exchange \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=urn:ietf:params:oauth:grant-type:token-exchange' \
  -d 'subject_token=SUBJECT_TOKEN' \
  -d 'subject_token_type=urn:ietf:params:oauth:token-type:access_token' \
  -d 'audience=https://api.example.com' \
  -d 'scope=read'
```

Typical use:
- service-to-service delegation
- audience reduction
- tenant-scoped downstream calls

---

## 9. Target-tree install pattern using the proposed plugin layout

```python
from tigrbl import TigrblApp
from tigrbl.engine import engine
from tigrbl_auth.plugin import install
from tigrbl_auth.config.settings import Settings

settings = Settings.from_env()
app = TigrblApp(engine=engine(settings.database_dsn))
install(app, settings=settings)
```

Target behavior:
- installs REST routes from `tigrbl_auth/api/rest/`
- installs JSON-RPC methods from `tigrbl_auth/api/rpc/`
- registers tables from `tigrbl_auth/tables/`
- loads standards features from `tigrbl_auth/standards/`

---

## 10. Enforce ADRs and release gates before cutting a release

```bash
# verify required ADRs exist for the claimed features
python scripts/verify_claims.py \
  --targets compliance/targets/standards-matrix.yaml \
  --adr-map compliance/mappings/target-to-adr.yaml

# run the release gate for a production claim
python scripts/run_release_gates.py \
  --gate gates/release/production-readiness-production.yaml \
  --claims compliance/targets/release-claims.yaml \
  --evidence compliance/evidence/
```

Target behavior:
- blocks release if required ADRs are missing
- blocks release if OpenAPI/OpenRPC artifacts are stale
- blocks release if evidence for Tier 3/Tier 4 claims is incomplete
- produces an auditable certification bundle

---

## Notes

- Examples **1–8** are grounded in the current package surface and tests.
- Examples **9–10** are **target-state** examples for the proposed tree and governance model.
- For a certifiable package, runtime usage alone is not enough; ADR, evidence, and release-gate workflows must be part of normal package operation.
