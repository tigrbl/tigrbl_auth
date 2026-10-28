# DelegationGrant Lifecycle Runtime T0 Evidence

This evidence records the implemented runtime surfaces for the DelegationGrant lifecycle plan.

Runtime coverage:
- Canonical storage tables are defined in `pkgs/tba-storage-core/src/tba_storage_core/tables/delegation_grant.py`.
- Compatibility facades re-export the canonical storage classes through `tba_auth.tables` and `tba_auth.orm`.
- Migration revision `0011_delegation_grant_lifecycle_tables` creates and drops the five DelegationGrant lifecycle tables.
- Policy exports expose the lifecycle service through `tigrbl_identity_policy` and `tba_auth.services.formal_authorization`.
- OAuth token exchange can persist delegation grant linkage metadata without owning grant lifecycle truth.

Verification commands:
- `uv run pytest tests/unit/test_delegation_grant_lifecycle_contract.py tests/unit/test_storage_canonical_facades.py`
- `uv run pytest tests/integration/test_migration_upgrade_downgrade_safety.py`
