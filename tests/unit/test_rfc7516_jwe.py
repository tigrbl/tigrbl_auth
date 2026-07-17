"""Dependency-light tests for RFC 7516 compact JWE support."""

from __future__ import annotations

import asyncio
from secrets import token_bytes

import pytest

from tigrbl_identity_jose.standards.rfc7516 import (
    JWEPolicyError,
    decrypt_jwe,
    encrypt_jwe,
)


@pytest.mark.unit
def test_encrypt_and_decrypt_jwe_round_trip() -> None:
    key = {"kty": "oct", "k": token_bytes(32)}
    token = asyncio.run(encrypt_jwe("sensitive", key))
    assert asyncio.run(decrypt_jwe(token, key)) == "sensitive"


@pytest.mark.unit
def test_rejects_invalid_direct_encryption_key_length() -> None:
    key = {"kty": "oct", "k": token_bytes(16)}
    with pytest.raises(JWEPolicyError):
        asyncio.run(encrypt_jwe("sensitive", key))


@pytest.mark.unit
def test_rejects_unsupported_header_alg() -> None:
    key = {"kty": "oct", "k": token_bytes(32)}
    with pytest.raises(JWEPolicyError):
        asyncio.run(encrypt_jwe("sensitive", key, alg="RSA-OAEP"))


@pytest.mark.unit
def test_rejects_invalid_compact_jwe_serialization() -> None:
    key = {"kty": "oct", "k": token_bytes(32)}
    with pytest.raises(JWEPolicyError):
        asyncio.run(decrypt_jwe("not-a-valid-jwe", key))


@pytest.mark.unit
def test_rejects_mismatched_key_material() -> None:
    key = {"kty": "oct", "k": token_bytes(32)}
    wrong_key = {"kty": "oct", "k": token_bytes(32)}
    token = asyncio.run(encrypt_jwe("sensitive", key))
    with pytest.raises(JWEPolicyError):
        asyncio.run(decrypt_jwe(token, wrong_key))
