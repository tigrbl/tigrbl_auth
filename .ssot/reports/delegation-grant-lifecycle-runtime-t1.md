# DelegationGrant Lifecycle Runtime T1 Evidence

This evidence records executable behavioral coverage for T1 DelegationGrant lifecycle claims.

Behavioral coverage:
- Grant creation, activation, inspection, listing, replacement, revocation, expiry, evaluation, audit capture, and token linkage are exercised by `tests/unit/test_delegation_grant_lifecycle_contract.py`.
- Scope normalization is deterministic and validates required tenant/action inputs.
- Cross-tenant attenuation denial is covered through policy proof evaluation.
- Revocation collapses descendant grants and blocks token linkage for inactive grants.
- Management projections are restricted to admin/developer/service management surfaces.
- OAuth token exchange only consumes a supplied `delegation_grant_id` and emits token/provenance linkage metadata; grant lifecycle ownership remains in policy/storage.

Verification commands:
- `uv run pytest tests/unit/test_delegation_grant_lifecycle_contract.py`
- `uv run pytest tests/integration/test_migration_upgrade_downgrade_safety.py`
