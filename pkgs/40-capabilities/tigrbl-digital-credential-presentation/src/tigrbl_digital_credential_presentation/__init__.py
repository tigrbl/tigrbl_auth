"""Composable presentation verification over consent/replay durability."""

from __future__ import annotations

import inspect
from collections.abc import Callable

from tigrbl_capability import Capability
from tigrbl_identity_contracts.capabilities import (
    CapabilityDefinition,
    CapabilityOperation,
)
from tigrbl_identity_contracts.digital_credentials import (
    PresentationRequest,
    PresentationResult,
    PresentationVerifierPort,
)

ReplayConsumer = Callable[[str, str], object]
ConsentChecker = Callable[[str, PresentationRequest], object]
TransactionRecorder = Callable[[str, PresentationRequest], object]
ResultRecorder = Callable[[str, PresentationRequest, PresentationResult], object]


async def _resolve(value):
    return await value if inspect.isawaitable(value) else value


class DigitalCredentialPresentationCapability(Capability):
    def __init__(
        self,
        verifier: PresentationVerifierPort,
        replay_consumer: ReplayConsumer,
        consent_checker: ConsentChecker,
        transaction_recorder: TransactionRecorder,
        result_recorder: ResultRecorder,
    ):
        self._verifier = verifier
        self._replay = replay_consumer
        self._consent = consent_checker
        self._transaction_recorder = transaction_recorder
        self._result_recorder = result_recorder
        super().__init__(
            CapabilityDefinition(
                capability_id="digital-credential.presentation",
                version="1.0",
            ),
            operations={
                "check_consent": CapabilityOperation(
                    target=self.check_consent,
                    delegated=True,
                ),
                "reserve_replay": CapabilityOperation(
                    target=self.reserve_replay,
                    delegated=True,
                ),
                "verify_presentation": CapabilityOperation(
                    target=self.verify_presentation,
                    delegated=True,
                ),
                "record_transaction": CapabilityOperation(
                    target=self.record_transaction,
                    delegated=True,
                ),
                "record_result": CapabilityOperation(
                    target=self.record_result,
                    delegated=True,
                ),
                "present": CapabilityOperation(target=self.present, delegated=True),
            },
        )

    async def check_consent(
        self,
        holder: str,
        request: PresentationRequest,
    ) -> bool:
        return bool(await _resolve(self._consent(holder, request)))

    async def reserve_replay(self, audience: str, replay_value: str) -> bool:
        return bool(await _resolve(self._replay(audience, replay_value)))

    async def verify_presentation(
        self,
        encoded_presentation: str | bytes,
        request: PresentationRequest,
    ) -> PresentationResult:
        return await _resolve(self._verifier.verify(encoded_presentation, request))

    async def record_transaction(
        self,
        holder: str,
        request: PresentationRequest,
    ) -> object:
        return await _resolve(self._transaction_recorder(holder, request))

    async def record_result(
        self,
        holder: str,
        request: PresentationRequest,
        result: PresentationResult,
    ) -> object:
        return await _resolve(self._result_recorder(holder, request, result))

    async def present(
        self,
        holder: str,
        encoded_presentation: str | bytes,
        request: PresentationRequest,
    ) -> PresentationResult:
        await self.record_transaction(holder, request)
        if not await self.check_consent(holder, request):
            result = PresentationResult(
                False,
                errors=("holder consent is absent",),
            )
        elif not await self.reserve_replay(
            request.binding.audience,
            request.binding.replay_value,
        ):
            result = PresentationResult(
                False,
                errors=("presentation replay detected",),
            )
        else:
            result = await self.verify_presentation(encoded_presentation, request)
        await self.record_result(holder, request, result)
        return result


__all__ = [
    "ConsentChecker",
    "DigitalCredentialPresentationCapability",
    "ReplayConsumer",
    "ResultRecorder",
    "TransactionRecorder",
]
