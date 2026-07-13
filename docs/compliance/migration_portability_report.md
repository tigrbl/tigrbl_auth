# Migration Portability Report

- passed: `True`
- python_version: `3.12`
- supported_backends: `sqlite, postgres`
- validated_backends: `sqlite, postgres`
- pytest_exit_code: `0`
- expected_head_revision: `0033_replay_reservations`
- downgrade_target_revision: `0032_claim_definition_and_provenance`
- revision_inventory_count: `33`

## sqlite

- available: `True`
- passed: `True`
- upgrade_passed: `True`
- downgrade_passed: `True`
- reapply_passed: `True`
- downgraded_revision: `0032_claim_definition_and_provenance`
- head_revision_after_upgrade: `0033_replay_reservations`
- head_revision_after_downgrade: `0032_claim_definition_and_provenance`
- head_revision_after_reapply: `0033_replay_reservations`
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
- downgraded_revision: `0032_claim_definition_and_provenance`
- head_revision_after_upgrade: `0033_replay_reservations`
- head_revision_after_downgrade: `0032_claim_definition_and_provenance`
- head_revision_after_reapply: `0033_replay_reservations`
- artifacts:
  - `downgrade`: `dist\migration-portability\postgres\downgrade.json`
  - `reapply`: `dist\migration-portability\postgres\reapply.json`
  - `upgrade`: `dist\migration-portability\postgres\upgrade.json`
