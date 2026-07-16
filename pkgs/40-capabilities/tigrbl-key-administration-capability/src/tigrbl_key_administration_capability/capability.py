"""Composable key-administration capability."""

from collections.abc import Callable
from typing import Any

from tigrbl_capability import Capability
from tigrbl_identity_contracts.capabilities import (
    CapabilityDefinition,
    CapabilityOperation,
)


class KeyAdministrationCapability(Capability):
    """Expose injected rotation and publication operations as one capability."""

    def __init__(
        self,
        rotate: Callable[..., Any],
        *,
        publish: Callable[..., Any] | None = None,
    ) -> None:
        self._rotate = rotate
        self._publish = publish
        super().__init__(
            CapabilityDefinition("key.administration", "1.0"),
            operations={
                "rotate": CapabilityOperation(target=self.rotate, delegated=True),
                "publish": CapabilityOperation(
                    target=self.publish if publish is not None else None,
                    required=False,
                    delegated=True,
                ),
            },
        )

    def rotate(self, *args: Any, **kwargs: Any) -> Any:
        return self._rotate(*args, **kwargs)

    def publish(self, *args: Any, **kwargs: Any) -> Any:
        if self._publish is None:
            raise NotImplementedError("key publication operation is not bound")
        return self._publish(*args, **kwargs)


__all__ = ["KeyAdministrationCapability"]
