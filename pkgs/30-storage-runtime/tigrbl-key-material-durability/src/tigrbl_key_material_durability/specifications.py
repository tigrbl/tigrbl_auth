"""Crypto-key aliases and executable persistence specifications."""

from tigrbl_identity_storage.tables import CryptoKey, CryptoKeyVersion

from tigrbl_table_durability import deriveRuntimeTableSpec
from tigrbl_key_material_durability.hooks import CRYPTO_KEY_RUNTIME_HOOKS


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
