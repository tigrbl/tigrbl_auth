from __future__ import annotations

from pathlib import Path

import pytest

from tigrbl_account_self_service import AccountSelfServiceCapability
from tigrbl_identity_contracts.account_self_service import (
    AccountConsent,
    AccountMutation,
    AccountNotFoundError,
    AccountPrincipal,
    AccountProfile,
    AccountProfileUpdate,
    AccountSession,
)


ROOT = Path(__file__).resolve().parents[2]
PRINCIPAL = AccountPrincipal("identity", "tenant")
PROFILE = AccountProfile("identity", "tenant", "alice", "alice@example.test")
SESSION = AccountSession("session", "tenant", "identity", "alice")
CONSENT = AccountConsent("consent", "tenant", "identity", "client", "openid")


def _capability(*, session_result=SESSION, consent_result=CONSENT):
    return AccountSelfServiceCapability(
        profile_reader=lambda principal: PROFILE,
        profile_updater=lambda principal, spec: PROFILE,
        password_changer=lambda principal, current, new: AccountMutation(
            "changed", principal.identity_id
        ),
        session_lister=lambda principal: (SESSION,),
        session_revoker=lambda principal, identifier: (
            session_result and AccountMutation("revoked", identifier)
        ),
        consent_lister=lambda principal: (CONSENT,),
        consent_revoker=lambda principal, identifier: consent_result,
        authorized_app_revoker=lambda principal, identifier: (CONSENT,),
    )


def test_account_self_service_reports_one_effective_operation_definition() -> None:
    capability = _capability()

    assert capability.definition().capability_id == "account.self-service"
    assert tuple(sorted(capability.operations())) == (
        "change_password",
        "get_profile",
        "list_authorized_apps",
        "list_consents",
        "list_sessions",
        "revoke_authorized_app",
        "revoke_consent",
        "revoke_session",
        "update_profile",
    )
    report = capability.capability_report()
    assert report["bound_operations"] == tuple(sorted(capability.operations()))
    assert report["unavailable_optional_operations"] == ()


@pytest.mark.asyncio
async def test_account_self_service_delegates_typed_account_operations() -> None:
    capability = _capability()

    assert await capability.get_profile(PRINCIPAL) == PROFILE
    assert await capability.update_profile(PRINCIPAL, AccountProfileUpdate()) == PROFILE
    assert await capability.list_sessions(PRINCIPAL) == (SESSION,)
    assert await capability.list_consents(PRINCIPAL) == (CONSENT,)
    assert await capability.list_authorized_apps(PRINCIPAL) == (CONSENT,)


@pytest.mark.asyncio
async def test_account_self_service_normalizes_missing_owned_resources() -> None:
    with pytest.raises(AccountNotFoundError, match="session not found"):
        await _capability(session_result=None).revoke_session(PRINCIPAL, "missing")
    with pytest.raises(AccountNotFoundError, match="consent not found"):
        await _capability(consent_result=None).revoke_consent(PRINCIPAL, "missing")


def test_my_account_http_package_has_no_durable_or_hashing_implementation() -> None:
    package = ROOT / "pkgs" / "80-apis" / "tigrbl-auth-api-my-account"
    source = "\n".join(path.read_text() for path in (package / "src").rglob("*.py"))
    metadata = (package / "pyproject.toml").read_text()

    for forbidden in (
        "tigrbl_identity_storage",
        "BcryptSecretHasher",
        "read_table_record",
        "update_table_record",
        "list_table_records",
    ):
        assert forbidden not in source
    assert "tigrbl-identity-storage" not in metadata
    assert "tigrbl-secret-hashing" not in metadata
