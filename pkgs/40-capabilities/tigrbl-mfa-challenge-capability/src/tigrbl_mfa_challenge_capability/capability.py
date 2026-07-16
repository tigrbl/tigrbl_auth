"""Multi-factor challenge ceremony capability."""

from collections.abc import Callable
from typing import Any

from tigrbl_capability import Capability
from tigrbl_identity_contracts.capabilities import CapabilityDefinition, CapabilityOperation


class MfaChallengeCapability(Capability):
    def __init__(self, begin_challenge: Callable[..., Any], *, complete_challenge: Callable[..., Any]) -> None:
        self._begin_challenge = begin_challenge
        self._complete_challenge = complete_challenge
        super().__init__(
            CapabilityDefinition("authentication.mfa-challenge", "1.0"),
            operations={
                "begin_mfa_challenge": CapabilityOperation(target=self.begin_mfa_challenge, delegated=True),
                "complete_mfa_challenge": CapabilityOperation(target=self.complete_mfa_challenge, delegated=True),
            },
        )

    def begin_mfa_challenge(self, *args: Any, **kwargs: Any) -> Any:
        return self._begin_challenge(*args, **kwargs)

    def complete_mfa_challenge(self, *args: Any, **kwargs: Any) -> Any:
        return self._complete_challenge(*args, **kwargs)


__all__ = ["MfaChallengeCapability"]
