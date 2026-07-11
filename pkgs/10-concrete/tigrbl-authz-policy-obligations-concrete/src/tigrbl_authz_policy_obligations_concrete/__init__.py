"""No-op and collecting obligation/advice handlers."""

from __future__ import annotations

from tigrbl_authz_policy_bases import AdviceHandlerBase, ObligationHandlerBase
from tigrbl_identity_contracts.policy import Advice, Obligation, PolicyDecision


class NoopObligationHandler(ObligationHandlerBase):
    async def handle_obligation(self, obligation: Obligation, decision: PolicyDecision, /) -> None:
        return None


class NoopAdviceHandler(AdviceHandlerBase):
    async def handle_advice(self, advice: Advice, decision: PolicyDecision, /) -> None:
        return None


class CollectingObligationHandler(ObligationHandlerBase):
    def __init__(self) -> None:
        self.items: list[tuple[Obligation, PolicyDecision]] = []

    async def handle_obligation(self, obligation: Obligation, decision: PolicyDecision, /) -> None:
        self.items.append((obligation, decision))


class CollectingAdviceHandler(AdviceHandlerBase):
    def __init__(self) -> None:
        self.items: list[tuple[Advice, PolicyDecision]] = []

    async def handle_advice(self, advice: Advice, decision: PolicyDecision, /) -> None:
        self.items.append((advice, decision))


__all__ = [
    "CollectingAdviceHandler",
    "CollectingObligationHandler",
    "NoopAdviceHandler",
    "NoopObligationHandler",
]
