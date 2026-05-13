from __future__ import annotations

import os
from pathlib import Path

import pytest

from tigrbl_auth.migrations import apply_all_async, column_names_async, downgrade_one_async, expected_table_names, verify_schema_async


pytestmark = [pytest.mark.integration, pytest.mark.asyncio]

REVISION_0007 = "0007_browser_session_cookie_and_auth_code_linkage"
REVISION_0008 = "0008_refresh_token_family_state"
REVISION_0006 = "0006_key_rotation_and_audit_tables"
SESSION_COLUMNS = {"session_state_salt", "cookie_secret_hash", "cookie_issued_at", "cookie_rotated_at"}
AUTH_CODE_COLUMNS = {"session_id"}
TOKEN_RECORD_COLUMNS = {"refresh_family_id", "refresh_parent_hash", "refresh_successor_hash", "used_at", "reuse_detected_at"}


def _backend_matrix(tmp_path: Path) -> list[tuple[str, str]]:
    cases = [("sqlite", f"sqlite+aiosqlite:///{tmp_path / 'tigrbl_auth_test.db'}")]
    postgres_url = os.environ.get("POSTGRES_URL")
    if postgres_url:
        cases.append(("postgres", postgres_url))
    return cases


async def _assert_upgrade_state() -> None:
    verification = await verify_schema_async()
    session_columns = set(await column_names_async("sessions"))
    auth_code_columns = set(await column_names_async("auth_codes"))
    token_record_columns = set(await column_names_async("token_records"))
    assert verification.passed is True
    assert SESSION_COLUMNS <= session_columns
    assert AUTH_CODE_COLUMNS <= auth_code_columns
    assert TOKEN_RECORD_COLUMNS <= token_record_columns
    assert set(expected_table_names()).issubset(set(verification.actual_tables))


async def _assert_downgrade_state() -> None:
    verification = await verify_schema_async()
    session_columns = set(await column_names_async("sessions"))
    auth_code_columns = set(await column_names_async("auth_codes"))
    token_record_columns = set(await column_names_async("token_records"))
    assert verification.passed is True
    assert SESSION_COLUMNS.isdisjoint(session_columns)
    assert AUTH_CODE_COLUMNS.isdisjoint(auth_code_columns)
    assert TOKEN_RECORD_COLUMNS.isdisjoint(token_record_columns)
    assert set(expected_table_names()).issubset(set(verification.actual_tables))


async def test_migration_chain_produces_expected_schema_on_sqlite_and_postgres(runtime_engine_factory, postgres_database_url, tmp_path):
    for backend, database_url in _backend_matrix(tmp_path):
        async with runtime_engine_factory(database_url):
            result = await apply_all_async()
            assert result.passed is True, backend
            await _assert_upgrade_state()


async def test_downgrade_then_reapply_is_schema_safe_on_sqlite_and_postgres(runtime_engine_factory, postgres_database_url, tmp_path):
    for backend, database_url in _backend_matrix(tmp_path):
        async with runtime_engine_factory(database_url):
            first = await apply_all_async()
            assert first.passed is True, backend
            await _assert_upgrade_state()

            downgraded_latest = await downgrade_one_async()
            assert downgraded_latest == REVISION_0008, backend

            downgraded = await downgrade_one_async()
            assert downgraded == REVISION_0007, backend

            downgraded_browser_session = await downgrade_one_async()
            assert downgraded_browser_session == REVISION_0006, backend
            await _assert_downgrade_state()

            reapplied = await apply_all_async()
            assert reapplied.passed is True, backend
            await _assert_upgrade_state()
            assert downgraded_latest in set(first.applied) | set(first.pending_before) | {downgraded_latest}
            assert downgraded in set(first.applied) | set(first.pending_before) | {downgraded}
            assert downgraded_browser_session in set(first.applied) | set(first.pending_before) | {downgraded_browser_session}
            assert downgraded in set(reapplied.applied) | set(reapplied.pending_before) | {downgraded}
