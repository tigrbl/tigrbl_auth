"""Composable policy-administration capability."""

from collections.abc import Callable
from typing import Any

from tigrbl_capability import Capability
from tigrbl_identity_contracts.capabilities import (
    CapabilityDefinition,
    CapabilityOperation,
)


class PolicyAdministrationCapability(Capability):
    def __init__(
        self,
        administer: Callable[..., Any],
        *,
        simulate: Callable[..., Any] | None = None,
    ) -> None:
        self._administer = administer
        self._simulate = simulate
        super().__init__(
            CapabilityDefinition("policy.administration", "1.0"),
            operations={
                "administer": CapabilityOperation(
                    target=self.administer, delegated=True
                ),
                "simulate": CapabilityOperation(
                    target=self.simulate if simulate is not None else None,
                    required=False,
                    delegated=True,
                ),
            },
        )

    def administer(self, *args: Any, **kwargs: Any) -> Any:
        return self._administer(*args, **kwargs)

    def simulate(self, *args: Any, **kwargs: Any) -> Any:
        if self._simulate is None:
            raise NotImplementedError("policy simulation operation is not bound")
        return self._simulate(*args, **kwargs)


__all__ = ["PolicyAdministrationCapability"]
