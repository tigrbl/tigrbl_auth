from collections.abc import Callable

from tigrbl_digital_credential_bases import PresentationVerifierBase
from tigrbl_identity_contracts.digital_credentials import (
    PresentationRequest,
    PresentationResult,
)

PresentationHandler = Callable[[bytes | str, PresentationRequest], PresentationResult]


class DispatchingPresentationVerifier(PresentationVerifierBase):
    def __init__(self):
        self._handlers: dict[str, PresentationHandler] = {}

    def register(self, format_identifier: str, handler: PresentationHandler) -> None:
        if not format_identifier or format_identifier in self._handlers:
            raise ValueError("presentation format must be non-empty and unique")
        self._handlers[format_identifier] = handler

    def verify(
        self, presentation: bytes | str, request: PresentationRequest, /
    ) -> PresentationResult:
        available = [
            format_ for format_ in request.accepted_formats if format_ in self._handlers
        ]
        if not available:
            return PresentationResult(
                False, errors=("no accepted presentation format is supported",)
            )
        results = [
            self._handlers[format_](presentation, request) for format_ in available
        ]
        valid = [result for result in results if result.valid]
        if len(valid) == 1:
            return valid[0]
        if len(valid) > 1:
            return PresentationResult(
                False, errors=("presentation matched multiple format handlers",)
            )
        return PresentationResult(
            False, errors=tuple(error for result in results for error in result.errors)
        )


__all__ = ["DispatchingPresentationVerifier", "PresentationHandler"]
