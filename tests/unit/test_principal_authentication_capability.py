from __future__ import annotations

import pytest

from tigrbl_authenticator_client_secret_local import ClientSecretLocalAuthenticator
from tigrbl_authenticator_password_local import PasswordLocalAuthenticator
from tigrbl_principal_authentication import (
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
