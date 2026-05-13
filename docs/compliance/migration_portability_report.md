# Migration Portability Report

- passed: `True`
- python_version: `3.12`
- supported_backends: `sqlite, postgres`
- validated_backends: `sqlite, postgres`
- pytest_exit_code: `0`
- expected_head_revision: `0009_admin_identity_bootstrap_and_password_recovery`
- downgrade_target_revision: `0008_refresh_token_family_state`
- revision_inventory_count: `9`

## sqlite

- available: `True`
- passed: `True`
- upgrade_passed: `True`
- downgrade_passed: `True`
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

- available: `True`
- passed: `True`
- upgrade_passed: `True`
- downgrade_passed: `True`
- reapply_passed: `True`
- downgraded_revision: `0008_refresh_token_family_state`
- head_revision_after_upgrade: `0009_admin_identity_bootstrap_and_password_recovery`
- head_revision_after_downgrade: `0008_refresh_token_family_state`
- head_revision_after_reapply: `0009_admin_identity_bootstrap_and_password_recovery`
- artifacts:
  - `downgrade`: `dist\migration-portability\postgres\downgrade.json`
  - `reapply`: `dist\migration-portability\postgres\reapply.json`
  - `upgrade`: `dist\migration-portability\postgres\upgrade.json`
