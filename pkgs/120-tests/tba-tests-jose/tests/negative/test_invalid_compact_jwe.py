from __future__ import annotations

import asyncio

import pytest

from tba_provider_identity_jose.standards.rfc7516 import JWEPolicyError, decrypt_jwe


@pytest.mark.negative
def test_invalid_compact_jwe_is_rejected() -> None:
    with pytest.raises(JWEPolicyError):
        asyncio.run(decrypt_jwe("not-a-valid-jwe", {"kty": "oct", "k": b"0" * 32}))
