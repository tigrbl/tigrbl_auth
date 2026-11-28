import base64
import hashlib

import pytest

from tba_contracts_identity.shared_secrets import SecretHashingPort, SecretVerificationPort
from tba_provider_secret_hashing_pbkdf2 import Pbkdf2SecretHasher


PASSWORD = "Legacy café password"


def legacy_record(password: str, rounds: int, salt: bytes) -> str:
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, rounds)
    salt_text = base64.urlsafe_b64encode(salt).decode()
    digest_text = base64.urlsafe_b64encode(digest).decode()
    return f"pbkdf2_sha256${rounds}${salt_text}${digest_text}"


def test_legacy_wire_format_matches_both_consumer_generators():
    hasher = Pbkdf2SecretHasher()
    salt = bytes(range(16))
    encoded = legacy_record(PASSWORD, 310_000, salt)
    assert hasher.hash_secret(PASSWORD, salt=salt).encoded == encoded
    assert hasher.verify_secret(PASSWORD, encoded).verified
    assert hasher.verify_secret(PASSWORD.encode(), encoded.encode()).verified
    assert not hasher.verify_secret("different password", encoded).verified


def test_verified_records_request_upgrade_without_downgrading():
    hasher = Pbkdf2SecretHasher(rounds=200)
    lower = legacy_record(PASSWORD, 100, b"legacy salt")
    higher = legacy_record(PASSWORD, 300, b"current salt")
    assert hasher.verify_secret(PASSWORD, lower).needs_rehash
    assert not hasher.verify_secret("different password", lower).needs_rehash
    assert not hasher.verify_secret(PASSWORD, higher).needs_rehash
    assert isinstance(hasher, SecretHashingPort)
    assert isinstance(hasher, SecretVerificationPort)


@pytest.mark.parametrize("encoded", [None, "", "bcrypt$1", b"\xff", "pbkdf2_sha256$0$a$$"])
def test_malformed_records_fail_verification(encoded):
    assert not Pbkdf2SecretHasher().verify_secret(PASSWORD, encoded).verified
