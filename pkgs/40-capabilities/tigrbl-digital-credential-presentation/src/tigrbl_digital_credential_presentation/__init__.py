from collections.abc import Callable

from tigrbl_capability import Capability
from tigrbl_identity_contracts.capabilities import CapabilityMetadata
from tigrbl_identity_contracts.digital_credentials import (
    PresentationRequest,
    PresentationResult,
    PresentationVerifierPort,
)

ReplayConsumer = Callable[[str, str], bool]
ConsentChecker = Callable[[str, PresentationRequest], bool]


class DigitalCredentialPresentationCapability(Capability):
    def __init__(
        self,
        verifier: PresentationVerifierPort,
        replay_consumer: ReplayConsumer,
        consent_checker: ConsentChecker,
    ):
        super().__init__(
            CapabilityMetadata(
                capability_id="digital-credential.presentation",
                version="1.0",
                operations=("present",),
                guarantees=("consent-before-verification", "replay-check-before-verification"),
                dependencies=(type(verifier).__name__,),
            )
        )
        self._verifier = verifier
        self._replay = replay_consumer
        self._consent = consent_checker
        self.bind("present", self.present, delegated=True)

    def present(
        self,
        holder: str,
        encoded_presentation: str | bytes,
        request: PresentationRequest,
    ) -> PresentationResult:
        if not self._consent(holder, request):
            return PresentationResult(False, errors=("holder consent is absent",))
        binding = request.binding
        replay_key = binding.replay_value
        if not self._replay(binding.audience, replay_key):
            return PresentationResult(False, errors=("presentation replay detected",))
        return self._verifier.verify(encoded_presentation, request)


__all__ = [
    "ConsentChecker",
    "DigitalCredentialPresentationCapability",
    "ReplayConsumer",
]
