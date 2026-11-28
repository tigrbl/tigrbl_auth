"""Protocol-neutral injection boundary for deployment-selected settings."""

from __future__ import annotations

from threading import RLock
from typing import Any


class ProtocolSettingsOverlay:
    """Read deployment overrides first and complete defaults second."""

    def __init__(self, primary: object, fallback: object) -> None:
        object.__setattr__(self, "_primary", primary)
        object.__setattr__(self, "_fallback", fallback)

    def __getattr__(self, name: str) -> Any:
        primary = self._primary
        if hasattr(primary, name):
            return getattr(primary, name)
        return getattr(self._fallback, name)

    def __setattr__(self, name: str, value: Any) -> None:
        setattr(self._primary, name, value)


class ProtocolSettingsProxy:
    """Stable reference whose target is bound only by a composition layer."""

    def __init__(self) -> None:
        object.__setattr__(self, "_target", None)
        object.__setattr__(self, "_lock", RLock())

    def bind(self, target: object) -> None:
        if target is None:
            raise ValueError("protocol settings target is required")
        with self._lock:
            object.__setattr__(self, "_target", target)

    @property
    def configured(self) -> bool:
        return self._target is not None

    def __getattr__(self, name: str) -> Any:
        target = self._target
        if target is None:
            raise RuntimeError("protocol settings have not been bound by the runtime composition layer")
        return getattr(target, name)

    def __setattr__(self, name: str, value: Any) -> None:
        if name.startswith("_"):
            object.__setattr__(self, name, value)
            return
        target = self._target
        if target is None:
            raise RuntimeError("protocol settings have not been bound by the runtime composition layer")
        setattr(target, name, value)


protocol_settings = ProtocolSettingsProxy()


def bind_protocol_settings(target: object) -> None:
    protocol_settings.bind(target)


__all__ = [
    "ProtocolSettingsOverlay",
    "ProtocolSettingsProxy",
    "bind_protocol_settings",
    "protocol_settings",
]
