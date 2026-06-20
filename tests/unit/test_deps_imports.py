from __future__ import annotations

from swarmauri_core.key_providers import KeyAlg
from swarmauri_tokens_jwt import JWTTokenService


def test_provider_packages_expose_tokens_and_key_types() -> None:
    assert JWTTokenService is not None
    assert KeyAlg is not None
