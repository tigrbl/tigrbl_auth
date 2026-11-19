"""Composable advanced-authentication capability."""

from collections.abc import Callable
from typing import Any

from tigrbl_capability import Capability
from tigrbl_identity_contracts.capabilities import (
    CapabilityDefinition,
    CapabilityOperation,
)


class AdvancedAuthenticationCapability(Capability):
    def __init__(
        self,
        begin: Callable[..., Any],
        *,
        complete: Callable[..., Any] | None = None,
    ) -> None:
        self._begin = begin
        self._complete = complete
        super().__init__(
            CapabilityDefinition("authentication.advanced", "1.0"),
            operations={
                "begin": CapabilityOperation(target=self.begin, delegated=True),
                "complete": CapabilityOperation(
                    target=self.complete if complete is not None else None,
                    required=False,
                    delegated=True,
                ),
            },
        )

    def begin(self, *args: Any, **kwargs: Any) -> Any:
        return self._begin(*args, **kwargs)

    def complete(self, *args: Any, **kwargs: Any) -> Any:
        if self._complete is None:
            raise NotImplementedError("advanced authentication completion is not bound")
        return self._complete(*args, **kwargs)


__all__ = ["AdvancedAuthenticationCapability"]
