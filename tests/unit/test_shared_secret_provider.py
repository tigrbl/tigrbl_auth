from __future__ import annotations

import pytest

from tigrbl_authenticator_client_secret_local import ClientSecretLocalAuthenticator
from tigrbl_authenticator_password_local import PasswordLocalAuthenticator
from tigrbl_identity_contracts.shared_secrets import SecretHash
from tigrbl_secret_hashing_bcrypt_provider import BcryptSecretHasher


def test_bcrypt_provider_hashes_verifies_and_detects_rehash() -> None:
    legacy = BcryptSecretHasher(rounds=4)
    current = BcryptSecretHasher(rounds=5)
    encoded = legacy.hash_secret("correct horse battery staple")

    assert isinstance(encoded, SecretHash)
    assert current.verify_secret("wrong", encoded).verified is False
    result = current.verify_secret("correct horse battery staple", encoded)
    assert result.verified is True
    assert result.needs_rehash is True


def test_bcrypt_provider_rejects_empty_long_and_malformed_inputs() -> None:
    provider = BcryptSecretHasher(rounds=4)

    with pytest.raises(ValueError, match="required"):
        provider.hash_secret("")
    with pytest.raises(ValueError, match="72-byte"):
        provider.hash_secret("x" * 73)
    assert provider.verify_secret("presented", b"not-a-bcrypt-hash").verified is False
    assert provider.verify_secret("presented", None).verified is False


def test_local_authenticators_delegate_to_secret_provider() -> None:
    provider = BcryptSecretHasher(rounds=4)
    encoded = provider.hash_secret("shared-secret")
    password = PasswordLocalAuthenticator(secret_verifier=provider)
    client = ClientSecretLocalAuthenticator(secret_verifier=provider)

    assert password.verify_secret("shared-secret", encoded)
    assert client.verify_secret("shared-secret", encoded.encoded)
    assert not password.verify_secret("wrong", encoded)
