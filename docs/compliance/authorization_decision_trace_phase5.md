# Authorization Decision Trace Phase 5

## Scope

- `feat:authorization-decision-trace-reproducibility`
- `clm:authorization-decision-trace-reproducibility`

## Runtime delivery

- Added deterministic authorization decision-trace construction in `tigrbl_auth/services/authorization_provenance.py`.
- RFC 8693 issuance in `tigrbl_auth/standards/oauth2/token_exchange.py` now derives:
  - a stable `request_hash`
  - a stable `policy_hash`
  - a stable `derivation_hash`
  - a stable `decision_key`
- `tigrbl_auth/services/token_service.py` now preserves explicit authorization traces and delegation provenance in persisted token-record claims for issued token pairs.

## Verification

Executed with a repo-local uv cache:

```powershell
$env:UV_CACHE_DIR='E:\swarmauri_github\tigrbl_auth\.tmp\uv-cache'
uv run pytest tests\unit\test_authorization_provenance.py tests\unit\test_hardening_cluster_a.py tests\integration\test_persistence_lifecycle_durability.py -k "provenance or lineage or token_exchange"
uv run pytest tests\conformance\production\test_rfc7662_introspection.py tests\conformance\production\test_rfc9728_protected_resource_metadata.py -k "protected_resource or introspection"
```

Observed result:

- provenance slice: `8 passed, 12 deselected`
- verifier/introspection regression slice: `4 passed`

## Covered assertions

- authorization decision traces are deterministic for identical inputs
- persisted token records retain authorization traces alongside issued tokens
- runtime token exchange binds audit request identifiers to deterministic authorization request hashes
- verifier-contract and protected-resource metadata regressions remain green after the provenance changes
