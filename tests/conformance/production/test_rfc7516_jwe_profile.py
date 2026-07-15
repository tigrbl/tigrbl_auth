from __future__ import annotations

import asyncio
from secrets import token_bytes

from tigrbl_identity_jose.standards.rfc7516 import (
    SUPPORTED_JWE_ALG_VALUES,
    SUPPORTED_JWE_ENC_VALUES,
    decrypt_jwe,
    encrypt_jwe,
    jwe_policy_metadata,
)


def test_rfc7516_compact_jwe_profile_round_trip_and_metadata() -> None:
    key = {"kty": "oct", "k": token_bytes(32)}
    token = asyncio.run(encrypt_jwe("sensitive", key, typ="JWT"))
    assert token.count(".") == 4
    assert asyncio.run(decrypt_jwe(token, key)) == "sensitive"

    metadata = jwe_policy_metadata()
    assert metadata["id_token_encryption_alg_values_supported"] == list(
        SUPPORTED_JWE_ALG_VALUES
    )
    assert metadata["id_token_encryption_enc_values_supported"] == list(
        SUPPORTED_JWE_ENC_VALUES
    )
