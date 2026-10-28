"""Provider-bound public-key response materialization."""

from __future__ import annotations

from typing import Any


JWK_PRIVATE_PARAMETERS = frozenset({"d", "p", "q", "dp", "dq", "qi"})


def _public_jwk(material: Any) -> Any:
    if isinstance(material, dict):
        return {
            key: value
            for key, value in material.items()
            if key not in JWK_PRIVATE_PARAMETERS
        }
    return material


def materialize_public_key_record(payload: Any) -> Any:
    """Remove provider references and private JWK parameters from a response."""

    if isinstance(payload, dict):
        cleaned = dict(payload)
        cleaned.pop("provider_key_ref", None)
        cleaned["public_material"] = _public_jwk(cleaned.get("public_material"))
        return cleaned
    if hasattr(payload, "provider_key_ref"):
        try:
            setattr(payload, "provider_key_ref", None)
        except (AttributeError, TypeError):
            pass
    if hasattr(payload, "public_material"):
        try:
            setattr(payload, "public_material", _public_jwk(payload.public_material))
        except (AttributeError, TypeError):
            pass
    return payload


__all__ = ["JWK_PRIVATE_PARAMETERS", "materialize_public_key_record"]
