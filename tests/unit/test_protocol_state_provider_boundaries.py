from __future__ import annotations

from pathlib import Path

import pytest

from tigrbl_auth_protocol_oauth.standards.dpop import (
    configure_state_providers,
    issue_nonce,
)
from tigrbl_auth_protocol_rp import RPConfiguration, RelyingParty
from tigrbl_replay_memory_provider import (
    MemoryReplayCheckProvider,
    MemoryRPSessionProvider,
    MemoryRPStateProvider,
    MemorySingleUseNonceProvider,
)


ROOT = Path(__file__).resolve().parents[2]


def test_layer_50_contains_no_implicit_store_implementations() -> None:
    source = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (ROOT / "pkgs" / "50-protocols").rglob("*.py")
    )
    for forbidden in (
        "class StateNonceStore",
        "class TokenStore",
        "class DPoPReplayStore",
        "class DPoPNonceStore",
        "DEFAULT_REPLAY_STORE",
        "DEFAULT_NONCE_STORE",
    ):
        assert forbidden not in source


def test_layer_50_does_not_import_runtime_settings() -> None:
    source = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (ROOT / "pkgs" / "50-protocols").rglob("*.py")
    )
    assert "tigrbl_identity_runtime.settings" not in source
    assert "from tigrbl_identity_runtime import settings" not in source


def test_layer_20_does_not_own_sql_sessions_or_transactions() -> None:
    source = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (ROOT / "pkgs" / "20-providers").rglob("*.py")
    )
    for forbidden in (
        "storage_session",
        "create_engine",
        "AsyncSession",
        "HybridSession",
        "import sqlalchemy",
        "from sqlalchemy",
    ):
        assert forbidden not in source


def test_layer_50_does_not_own_database_or_environment_key_loading() -> None:
    source = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (ROOT / "pkgs" / "50-protocols").rglob("*.py")
    )
    for forbidden in (
        "tigrbl_identity_storage.tables",
        "storage_session",
        "from sqlalchemy",
        "import sqlalchemy",
        "key_management",
        "FileKeyProvider",
        "_DEFAULT_KEY_PATH",
    ):
        assert forbidden not in source


def test_layer_40_consumes_normalized_contracts_not_protocol_modules() -> None:
    source = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (ROOT / "pkgs" / "40-capabilities").rglob("*.py")
    )
    assert "tigrbl_auth_protocol_" not in source
    assert ".nonce" not in source
    assert ".jti" not in source
    assert "Header(" not in source


def test_rp_requires_explicit_state_and_session_providers() -> None:
    config = RPConfiguration(
        issuer="https://issuer.example",
        client_id="client",
        redirect_uri="https://client.example/callback",
    )
    with pytest.raises(TypeError):
        RelyingParty(config)  # type: ignore[call-arg]

    rp = RelyingParty(
        config,
        state_store=MemoryRPStateProvider(),
        session_store=MemoryRPSessionProvider(),
    )
    assert rp.build_authorization_url("https://issuer.example/authorize")[1].state


def test_dpop_state_is_explicitly_provider_configured() -> None:
    configure_state_providers(
        replay=MemoryReplayCheckProvider(), nonce=MemorySingleUseNonceProvider()
    )
    assert issue_nonce()
