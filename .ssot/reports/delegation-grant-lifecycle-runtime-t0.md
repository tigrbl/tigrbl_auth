# DelegationGrant Lifecycle Runtime T0 Evidence

This evidence records the implemented runtime surfaces for the DelegationGrant lifecycle plan.

Runtime coverage:
- Canonical storage tables are defined in `pkgs/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/delegation_grant.py`.
- Compatibility facades re-export the canonical storage classes through `tigrbl_auth.tables` and `tigrbl_auth.orm`.
- Migration revision `0011_delegation_grant_lifecycle_tables` creates and drops the five DelegationGrant lifecycle tables.
- Policy exports expose the lifecycle service through `tigrbl_identity_policy` and `tigrbl_auth.services.formal_authorization`.
- OAuth token exchange can persist delegation grant linkage metadata without owning grant lifecycle truth.

Verification commands:
- `uv run pytest tests/unit/test_delegation_grant_lifecycle_contract.py tests/unit/test_storage_canonical_facades.py`
- `uv run pytest tests/integration/test_migration_upgrade_downgrade_safety.py`
