"""Composable access-governance capability."""

from collections.abc import Callable
from typing import Any

from tigrbl_capability import Capability
from tigrbl_identity_contracts.capabilities import (
    CapabilityDefinition,
    CapabilityOperation,
)


class AccessGovernanceCapability(Capability):
    def __init__(
        self,
        manage_entitlements: Callable[..., Any],
        *,
        run_access_review: Callable[..., Any] | None = None,
    ) -> None:
        self._manage_entitlements = manage_entitlements
        self._run_access_review = run_access_review
        super().__init__(
            CapabilityDefinition("access.governance", "1.0"),
            operations={
                "manage_entitlements": CapabilityOperation(
                    target=self.manage_entitlements,
                    delegated=True,
                ),
                "run_access_review": CapabilityOperation(
                    target=(
                        self.run_access_review
                        if run_access_review is not None
                        else None
                    ),
                    required=False,
                    delegated=True,
                ),
            },
        )

    def manage_entitlements(self, *args: Any, **kwargs: Any) -> Any:
        return self._manage_entitlements(*args, **kwargs)

    def run_access_review(self, *args: Any, **kwargs: Any) -> Any:
        if self._run_access_review is None:
            raise NotImplementedError("access review operation is not bound")
        return self._run_access_review(*args, **kwargs)


__all__ = ["AccessGovernanceCapability"]
