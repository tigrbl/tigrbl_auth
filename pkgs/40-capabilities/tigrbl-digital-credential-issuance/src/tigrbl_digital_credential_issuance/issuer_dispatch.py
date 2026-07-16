from collections.abc import Callable

from tigrbl_identity_contracts.digital_credentials import (
    CredentialConfiguration,
    CredentialIssuanceRequest,
    CredentialIssuanceResult,
)

IssuanceHandler = Callable[[CredentialIssuanceRequest], CredentialIssuanceResult]


class LocalDigitalCredentialIssuer:
    """Dispatch issuance to registered credential-format implementations."""

    def __init__(self) -> None:
        self._registrations: tuple[
            tuple[CredentialConfiguration, IssuanceHandler], ...
        ] = ()

    def register(
        self, configuration: CredentialConfiguration, handler: IssuanceHandler
    ) -> None:
        if any(
            registered.identifier == configuration.identifier
            for registered, _handler in self._registrations
        ):
            raise ValueError(
                f"duplicate credential configuration: {configuration.identifier}"
            )
        self._registrations += ((configuration, handler),)

    def issue(self, request: CredentialIssuanceRequest, /) -> CredentialIssuanceResult:
        registration = next(
            (
                (configuration, handler)
                for configuration, handler in self._registrations
                if configuration.identifier == request.configuration_id
            ),
            None,
        )
        if registration is None:
            raise LookupError(request.configuration_id)
        configuration, handler = registration
        if request.format not in configuration.supported_formats:
            raise ValueError(
                "requested credential format is not supported by configuration"
            )
        result = handler(request)
        if result.credential is None and result.transaction_id is None:
            raise ValueError(
                "issuance must return a credential or deferred transaction"
            )
        if result.credential is not None and result.credential.format != request.format:
            raise ValueError("issuer returned a credential in an unrequested format")
        return result

    @property
    def configurations(self) -> tuple[CredentialConfiguration, ...]:
        return tuple(configuration for configuration, _handler in self._registrations)


__all__ = ["IssuanceHandler", "LocalDigitalCredentialIssuer"]
