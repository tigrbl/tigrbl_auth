from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from tigrbl_authenticator_client_secret_local import ClientSecretLocalAuthenticator
from tigrbl_authenticator_password_local import PasswordLocalAuthenticator
from tigrbl_principal_authentication import (
    ApiKeyAuthenticationCapability,
    ClientSecretAuthenticationCapability,
    PasswordAuthenticationCapability,
)
from tigrbl_secret_hashing_bcrypt_provider import BcryptSecretHasher


@pytest.mark.asyncio
async def test_password_capability_composes_lookup_and_provider() -> None:
    hasher = BcryptSecretHasher(rounds=4)
    record = {
        "id": "user-1",
        "is_active": True,
        "password_hash": hasher.hash_secret("correct").encoded,
    }

    async def lookup(_context):
        return record

    capability = PasswordAuthenticationCapability(
        lookup,
        PasswordLocalAuthenticator(secret_verifier=hasher),
    )
    accepted = await capability.call(
        "authenticate_password",
        identifier="alice",
        password="correct",
        db=object(),
    )
    rejected = await capability.authenticate_password(
        identifier="alice",
        password="wrong",
        db=object(),
    )

    assert accepted.value.authenticated is True
    assert accepted.value.record is record
    assert accepted.delegated is True
    assert rejected.authenticated is False
    assert rejected.record is None


@pytest.mark.asyncio
async def test_client_secret_capability_supports_lookup_and_loaded_record() -> None:
    hasher = BcryptSecretHasher(rounds=4)
    record = {
        "id": "client-1",
        "is_active": True,
        "client_secret_hash": hasher.hash_secret("correct").encoded,
    }

    async def lookup(_context):
        return record

    capability = ClientSecretAuthenticationCapability(
        lookup,
        ClientSecretLocalAuthenticator(secret_verifier=hasher),
    )

    accepted = await capability.authenticate_client_secret(
        client_id="client-1",
        client_secret="correct",
        db=object(),
    )
    rejected = capability.verify_client_record(record, "wrong")

    assert accepted.authenticated is True
    assert accepted.record is record
    assert rejected.authenticated is False


def test_token_and_introspection_callers_use_capability_not_model_method() -> None:
    from tigrbl_identity_storage_runtime import introspection, token_request

    hasher = BcryptSecretHasher()
    record = {
        "id": "client-1",
        "is_active": True,
        "client_secret_hash": hasher.hash_secret("correct").encoded,
    }
    assert token_request.client_secret_authentication.verify_client_record(
        record,
        "correct",
    ).authenticated
    assert introspection.client_secret_authentication.verify_client_record(
        record,
        "wrong",
    ).authenticated is False


def _api_key_capability(api_keys, service_keys, touched):
    async def find_api_keys(_db, digest):
        return [row for row in api_keys if row["digest"] == digest]

    async def find_service_keys(_db, digest):
        return [row for row in service_keys if row["digest"] == digest]

    async def resolve_user(_db, record):
        return record.get("user")

    async def mark_used(_db, record):
        touched.append(record)

    return ApiKeyAuthenticationCapability(
        digest_key=lambda value: f"digest:{value}",
        find_api_keys=find_api_keys,
        find_service_keys=find_service_keys,
        resolve_user=resolve_user,
        mark_used=mark_used,
    )


@pytest.mark.asyncio
async def test_api_key_capability_authenticates_user_and_records_evidence() -> None:
    user = {"id": "user-1", "is_active": True}
    credential = {
        "id": "api-key-1",
        "digest": "digest:correct",
        "user": user,
        "status": "active",
    }
    touched = []
    capability = _api_key_capability([credential], [], touched)

    result = await capability.call(
        "authenticate_api_key",
        api_key="correct",
        db=object(),
    )

    assert result.value.authenticated is True
    assert result.value.record is user
    assert result.value.credential_record is credential
    assert result.value.principal_kind == "user"
    assert result.value.evidence.subject_id == "user-1"
    assert result.value.evidence.credential_id == "api-key-1"
    assert touched == [credential]


@pytest.mark.asyncio
async def test_api_key_capability_authenticates_service_identity() -> None:
    service = {"id": "service-1", "is_active": True}
    credential = {
        "id": "service-key-1",
        "digest": "digest:correct",
        "service_identity": service,
        "status": "active",
    }
    touched = []
    capability = _api_key_capability([], [credential], touched)

    result = await capability.authenticate_api_key(
        api_key="correct",
        db=object(),
    )

    assert result.authenticated is True
    assert result.record is service
    assert result.principal_kind == "service_identity"
    assert touched == [credential]


@pytest.mark.asyncio
async def test_api_key_capability_rejects_expired_or_inactive_records() -> None:
    expired = {
        "id": "api-key-expired",
        "digest": "digest:correct",
        "user": {"id": "user-1", "is_active": True},
        "valid_to": datetime.now(timezone.utc) - timedelta(seconds=1),
    }
    inactive = {
        "id": "api-key-inactive",
        "digest": "digest:inactive",
        "user": {"id": "user-2", "is_active": False},
    }
    touched = []
    capability = _api_key_capability([expired, inactive], [], touched)

    expired_result = await capability.authenticate_api_key(
        api_key="correct",
        db=object(),
    )
    inactive_result = await capability.authenticate_api_key(
        api_key="inactive",
        db=object(),
    )

    assert expired_result.authenticated is False
    assert inactive_result.authenticated is False
    assert touched == []


def test_server_api_key_authentication_uses_capability_composition() -> None:
    from tigrbl_identity_server.security import api_key_authentication

    assert isinstance(
        api_key_authentication.api_key_authentication,
        ApiKeyAuthenticationCapability,
    )

    for module_name in ("auth.py", "security_deps.py", "../rest/shared.py"):
        path = (
            __import__("pathlib").Path(__file__).resolve().parents[2]
            / "pkgs"
            / "60-runtime"
            / "tigrbl-identity-server"
            / "src"
            / "tigrbl_identity_server"
            / "security"
            / module_name
        )
        assert "tigrbl_authn_credentials.backends" not in path.read_text(
            encoding="utf-8"
        )

    token_runtime = (
        __import__("pathlib").Path(__file__).resolve().parents[2]
        / "pkgs"
        / "30-storage-runtime"
        / "tigrbl-identity-storage-runtime"
        / "src"
        / "tigrbl_identity_storage_runtime"
        / "token_runtime.py"
    ).read_text(encoding="utf-8")
    assert "_pwd_backend" not in token_runtime
