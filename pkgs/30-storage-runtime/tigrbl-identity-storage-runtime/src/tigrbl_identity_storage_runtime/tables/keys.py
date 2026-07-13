"""Crypto-key aliases and executable persistence specifications."""

from tigrbl_identity_storage.tables import CryptoKey, CryptoKeyVersion

from ..derive import deriveRuntimeTableSpec
from ..hooks.keys import CRYPTO_KEY_RUNTIME_HOOKS


CryptoKeyTable = CryptoKey
CryptoKeyVersionTable = CryptoKeyVersion

CryptoKeyRuntimeSpec = deriveRuntimeTableSpec(
    CryptoKeyTable,
    hooks=CRYPTO_KEY_RUNTIME_HOOKS,
)
CryptoKeyVersionRuntimeSpec = deriveRuntimeTableSpec(CryptoKeyVersionTable)


__all__ = [
    "CryptoKeyRuntimeSpec",
    "CryptoKeyTable",
    "CryptoKeyVersionRuntimeSpec",
    "CryptoKeyVersionTable",
]
