"""Typed validation registry for WebAuthn extension inputs and outputs."""

from __future__ import annotations

from collections.abc import Callable, Mapping

ExtensionValidator = Callable[[object], object]


def validate_appid(value: object) -> str:
    if not isinstance(value, str) or not value.startswith("https://"):
        raise ValueError("appid must be an HTTPS URL")
    return value


def validate_cred_props(value: object) -> bool:
    if not isinstance(value, bool):
        raise ValueError("credProps.rk must be boolean")
    return value


def validate_credential_protection(value: object) -> int:
    if not isinstance(value, int) or value not in {1, 2, 3}:
        raise ValueError("credentialProtectionPolicy is invalid")
    return value


def validate_large_blob(value: object) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise ValueError("largeBlob extension value must be an object")
    if "supported" in value and not isinstance(value["supported"], bool):
        raise ValueError("largeBlob.supported must be boolean")
    return value


def validate_payment(value: object) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise ValueError("payment extension value must be an object")
    return value


class ExtensionRegistry:
    def __init__(self) -> None:
        self._validators: dict[str, ExtensionValidator] = {
            "appid": validate_appid,
            "credProps": validate_cred_props,
            "credentialProtectionPolicy": validate_credential_protection,
            "largeBlob": validate_large_blob,
            "payment": validate_payment,
        }

    def validate(
        self, values: Mapping[str, object], *, allowed: frozenset[str]
    ) -> dict[str, object]:
        unknown = set(values).difference(allowed)
        if unknown:
            raise ValueError(f"WebAuthn extensions are not enabled: {sorted(unknown)}")
        return {name: self._validators[name](value) for name, value in values.items()}


__all__ = [
    "ExtensionRegistry",
    "validate_appid",
    "validate_cred_props",
    "validate_credential_protection",
    "validate_large_blob",
    "validate_payment",
]
