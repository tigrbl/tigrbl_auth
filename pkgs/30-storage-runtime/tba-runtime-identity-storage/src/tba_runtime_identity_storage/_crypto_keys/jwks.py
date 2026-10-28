"""JWKS formatting for storage-backed public crypto key material."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

_JWK_SECRET_FIELDS = {"d", "p", "q", "dp", "dq", "qi"}


def _row_value(row: Any, key: str, default: Any = None) -> Any:
    if isinstance(row, Mapping):
        return row.get(key, default)
    return getattr(row, key, default)


def _public_jwk(row: Any) -> dict[str, Any] | None:
    material = _row_value(row, "public_material")
    if not isinstance(material, Mapping):
        return None
    fmt = str(_row_value(row, "public_material_format", "jwk") or "jwk")
    if fmt not in {"jwk", "jwks"}:
        return None
    return {str(key): value for key, value in material.items() if str(key) not in _JWK_SECRET_FIELDS}


def jwks_from_crypto_keys(rows: Iterable[Any]) -> dict[str, list[dict[str, Any]]]:
    keys = [jwk for row in rows if (jwk := _public_jwk(row)) is not None]
    return {"keys": keys}


__all__ = ["jwks_from_crypto_keys"]
