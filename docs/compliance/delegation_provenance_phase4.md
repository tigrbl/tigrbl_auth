# Delegation Provenance Phase 4

## Scope

- `feat:delegation-graph-and-token-exchange-provenance`
- `clm:delegation-graph-and-token-exchange-provenance`

## Runtime delivery

- Added deterministic delegation-lineage artifact construction in `tigrbl_auth/services/authorization_provenance.py`.
- Runtime RFC 8693 issuance in `tigrbl_auth/standards/oauth2/token_exchange.py` now:
  - derives a delegation provenance artifact from subject token, actor token, effective audience/resource, and sender-constraint mode
  - persists the artifact with the issued access-token record
  - emits lineage identifiers into durable audit events
- Operator token-exchange persistence in `tigrbl_auth/services/operator_service.py` now records the same lineage artifact in the operator-plane token record.

## Verification

Executed with a repo-local uv cache:

```powershell
$env:UV_CACHE_DIR='E:\swarmauri_github\tigrbl_auth\.tmp\uv-cache'
uv run pytest tests\unit\test_authorization_provenance.py tests\unit\test_hardening_cluster_a.py tests\integration\test_persistence_lifecycle_durability.py tests\integration\test_auth_flows.py tests\negative\test_resource_exchange_abuse.py -k "provenance or lineage or token_exchange or refresh_token or exchange"
```

Observed result:

- `10 passed, 27 deselected`

## Covered assertions

- delegation lineage is deterministic for identical inputs
- delegation lineage changes when actor provenance changes
- runtime token exchange persists delegation provenance into durable token state
- runtime token exchange emits delegation lineage identifiers into audit details
- operator token exchange persists lineage into operator token records
