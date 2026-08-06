from __future__ import annotations

from tigrbl_identity_jose.framework import KeyAlg, JWTTokenService


def test_provider_packages_expose_tokens_and_key_types() -> None:
    assert JWTTokenService is not None
    assert KeyAlg is not None
