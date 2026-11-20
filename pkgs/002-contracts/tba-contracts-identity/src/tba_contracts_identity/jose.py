"""Provider-neutral contracts for JOSE services."""

from __future__ import annotations

from typing import Any, Iterable, Mapping, Protocol, runtime_checkable


@runtime_checkable
class JwtCoderPort(Protocol):
    def sign(self, **kwargs: Any) -> str: ...
    def verify(self, token: str, **kwargs: Any) -> Mapping[str, Any]: ...
    def decode(self, token: str, **kwargs: Any) -> Mapping[str, Any]: ...


@runtime_checkable
class JoseKeySetPort(Protocol):
    @property
    def keys(self) -> Mapping[str, Any]: ...
    def add(self, key: Any) -> Any: ...
    def rotate(self, **kwargs: Any) -> Any: ...


@runtime_checkable
class JwePolicyPort(Protocol):
    def as_header(self, *, typ: str | None = None, cty: str | None = None) -> Mapping[str, str]: ...


@runtime_checkable
class KeyRotationPolicyPort(Protocol):
    @property
    def versions(self) -> Mapping[tuple[str, str], Any]: ...
    def create_policy_version(self, policy_id: str, version_id: str, **kwargs: Any) -> Any: ...
    def approve_policy_version(self, policy_id: str, version_id: str, *, actor: str) -> Any: ...
    def publish_policy_version(self, policy_id: str, version_id: str, *, actor: str) -> Any: ...
    def effective_policy(self, **scope: str) -> Any | None: ...


@runtime_checkable
class KeyRotationAdministrationPort(Protocol):
    @property
    def audit_records(self) -> Iterable[Any]: ...
    def view_effective_policy(self, **scope: str) -> Any: ...
    def execute_rotation(self, **kwargs: Any) -> Any: ...


__all__ = [
    "JoseKeySetPort",
    "JwePolicyPort",
    "JwtCoderPort",
    "KeyRotationAdministrationPort",
    "KeyRotationPolicyPort",
]
