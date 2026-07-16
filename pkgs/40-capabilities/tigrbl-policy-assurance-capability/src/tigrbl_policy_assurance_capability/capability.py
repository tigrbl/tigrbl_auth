"""Composable policy-assurance capability."""

from collections.abc import Callable
from typing import Any

from tigrbl_capability import Capability
from tigrbl_identity_contracts.capabilities import (
    CapabilityDefinition,
    CapabilityOperation,
)


class PolicyAssuranceCapability(Capability):
    def __init__(
        self,
        evaluate: Callable[..., Any],
        *,
        report: Callable[..., Any] | None = None,
    ) -> None:
        self._evaluate = evaluate
        self._report = report
        super().__init__(
            CapabilityDefinition("policy.assurance", "1.0"),
            operations={
                "evaluate": CapabilityOperation(target=self.evaluate, delegated=True),
                "report": CapabilityOperation(
                    target=self.report if report is not None else None,
                    required=False,
                    delegated=True,
                ),
            },
        )

    def evaluate(self, *args: Any, **kwargs: Any) -> Any:
        return self._evaluate(*args, **kwargs)

    def report(self, *args: Any, **kwargs: Any) -> Any:
        if self._report is None:
            raise NotImplementedError("policy assurance report operation is not bound")
        return self._report(*args, **kwargs)


__all__ = ["PolicyAssuranceCapability"]
