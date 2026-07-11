"""Base classes for JOSE providers."""

from abc import ABC
from typing import Any, Iterable, Mapping

from tigrbl_identity_contracts.jose import (
    JoseKeySetPort,
    JwePolicyPort,
    JwtCoderPort,
    KeyRotationAdministrationPort,
    KeyRotationPolicyPort,
)


class JwtCoderBase(JwtCoderPort, ABC):
    def sign(self, **kwargs: Any) -> str:
        raise NotImplementedError

    def verify(self, token: str, **kwargs: Any) -> Mapping[str, Any]:
        raise NotImplementedError

    def decode(self, token: str, **kwargs: Any) -> Mapping[str, Any]:
        raise NotImplementedError


class JoseKeySetBase(JoseKeySetPort, ABC):
    @property
    def keys(self) -> Mapping[str, Any]:
        raise NotImplementedError

    def add(self, key: Any) -> Any:
        raise NotImplementedError

    def rotate(self, **kwargs: Any) -> Any:
        raise NotImplementedError


class JwePolicyBase(JwePolicyPort, ABC):
    def as_header(self, *, typ: str | None = None, cty: str | None = None) -> Mapping[str, str]:
        raise NotImplementedError


class KeyRotationPolicyBase(KeyRotationPolicyPort, ABC):
    @property
    def versions(self) -> Mapping[tuple[str, str], Any]:
        raise NotImplementedError

    def create_policy_version(self, policy_id: str, version_id: str, **kwargs: Any) -> Any:
        raise NotImplementedError

    def approve_policy_version(self, policy_id: str, version_id: str, *, actor: str) -> Any:
        raise NotImplementedError

    def publish_policy_version(self, policy_id: str, version_id: str, *, actor: str) -> Any:
        raise NotImplementedError

    def effective_policy(self, **scope: str) -> Any | None:
        raise NotImplementedError


class KeyRotationAdministrationBase(KeyRotationAdministrationPort, ABC):
    @property
    def audit_records(self) -> Iterable[Any]:
        raise NotImplementedError

    def view_effective_policy(self, **scope: str) -> Any:
        raise NotImplementedError

    def execute_rotation(self, **kwargs: Any) -> Any:
        raise NotImplementedError


__all__ = [
    "JoseKeySetBase",
    "JwePolicyBase",
    "JwtCoderBase",
    "KeyRotationAdministrationBase",
    "KeyRotationPolicyBase",
]
