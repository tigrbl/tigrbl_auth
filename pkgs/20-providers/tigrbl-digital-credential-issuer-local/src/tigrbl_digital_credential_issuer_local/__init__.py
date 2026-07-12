from collections.abc import Callable

from tigrbl_digital_credential_bases import CredentialIssuerBase
from tigrbl_identity_contracts.digital_credentials import (
    CredentialConfiguration,
    CredentialIssuanceRequest,
    CredentialIssuanceResult,
)

IssuanceHandler = Callable[[CredentialIssuanceRequest], CredentialIssuanceResult]


class LocalDigitalCredentialIssuer(CredentialIssuerBase):
    def __init__(self):
        self._configurations: dict[str, CredentialConfiguration] = {}
        self._handlers: dict[str, IssuanceHandler] = {}

    def register(
        self, configuration: CredentialConfiguration, handler: IssuanceHandler
    ) -> None:
        if configuration.identifier in self._configurations:
            raise ValueError(
                f"duplicate credential configuration: {configuration.identifier}"
            )
        self._configurations[configuration.identifier] = configuration
        self._handlers[configuration.identifier] = handler

    def issue(self, request: CredentialIssuanceRequest, /) -> CredentialIssuanceResult:
        configuration = self._configurations.get(request.configuration_id)
        if configuration is None:
            raise LookupError(request.configuration_id)
        if request.format not in configuration.supported_formats:
            raise ValueError(
                "requested credential format is not supported by configuration"
            )
        result = self._handlers[request.configuration_id](request)
        if result.credential is None and result.transaction_id is None:
            raise ValueError(
                "issuance must return a credential or deferred transaction"
            )
        if result.credential is not None and result.credential.format != request.format:
            raise ValueError("issuer returned a credential in an unrequested format")
        return result

    @property
    def configurations(self) -> tuple[CredentialConfiguration, ...]:
        return tuple(self._configurations.values())


__all__ = ["IssuanceHandler", "LocalDigitalCredentialIssuer"]
