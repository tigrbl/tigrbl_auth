from collections.abc import Callable

from tigrbl_identity_contracts.digital_credentials import (
    PresentationRequest,
    PresentationResult,
)

PresentationHandler = Callable[[bytes | str, PresentationRequest], PresentationResult]


class DispatchingPresentationVerifier:
    """Dispatch presentation verification across registered format handlers."""

    def __init__(self) -> None:
        self._handlers: tuple[tuple[str, PresentationHandler], ...] = ()

    def register(self, format_identifier: str, handler: PresentationHandler) -> None:
        if not format_identifier or any(
            registered == format_identifier for registered, _handler in self._handlers
        ):
            raise ValueError("presentation format must be non-empty and unique")
        self._handlers += ((format_identifier, handler),)

    def verify(
        self, presentation: bytes | str, request: PresentationRequest, /
    ) -> PresentationResult:
        available = [
            (format_, handler)
            for format_ in request.accepted_formats
            for registered, handler in self._handlers
            if registered == format_
        ]
        if not available:
            return PresentationResult(
                False, errors=("no accepted presentation format is supported",)
            )
        results = [handler(presentation, request) for _format, handler in available]
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
