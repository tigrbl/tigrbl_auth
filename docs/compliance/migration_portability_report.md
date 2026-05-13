# Migration Portability Report

- passed: `False`
- python_version: `3.12`
- supported_backends: `sqlite, postgres`
- validated_backends: `sqlite`
- pytest_exit_code: `1`
- expected_head_revision: `0009_admin_identity_bootstrap_and_password_recovery`
- downgrade_target_revision: `0008_refresh_token_family_state`
- revision_inventory_count: `9`

## sqlite

- available: `True`
- passed: `False`
- upgrade_passed: `True`
- downgrade_passed: `False`
- reapply_passed: `True`
- downgraded_revision: `0008_refresh_token_family_state`
- head_revision_after_upgrade: `0009_admin_identity_bootstrap_and_password_recovery`
- head_revision_after_downgrade: `0008_refresh_token_family_state`
- head_revision_after_reapply: `0009_admin_identity_bootstrap_and_password_recovery`
- artifacts:
  - `downgrade`: `dist\migration-portability\sqlite\downgrade.json`
  - `reapply`: `dist\migration-portability\sqlite\reapply.json`
  - `upgrade`: `dist\migration-portability\sqlite\upgrade.json`

## postgres

- available: `False`
- passed: `False`
- upgrade_passed: `False`
- downgrade_passed: `False`
- reapply_passed: `False`
- downgraded_revision: `None`
- head_revision_after_upgrade: `None`
- head_revision_after_downgrade: `None`
- head_revision_after_reapply: `None`
- failure: `POSTGRES_URL not set in the current environment.`

## open_gaps

- sqlite backend did not pass upgrade → downgrade → reapply validation.
- postgres backend was not available in the current environment.
- The migration portability pytest lane did not pass.
