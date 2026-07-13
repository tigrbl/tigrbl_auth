from collections.abc import Mapping

from tigrbl_digital_credential_issuance import DigitalCredentialIssuanceCapability
from tigrbl_identity_contracts.digital_credentials import (
    CredentialFormat,
    CredentialIssuanceRequest,
)


class Oid4vciProtocol:
    version = "1.0"

    def __init__(self, capability: DigitalCredentialIssuanceCapability):
        self._capability = capability

    def credential(
        self,
        payload: Mapping[str, object],
        *,
        wallet_attestation: str | bytes | None = None,
    ):
        configuration_id = payload.get("credential_configuration_id")
        format_identifier = payload.get("format")
        if not isinstance(configuration_id, str) or not isinstance(
            format_identifier, str
        ):
            raise ValueError(
                "credential request requires credential_configuration_id and format"
            )
        proofs = payload.get("proofs")
        request = CredentialIssuanceRequest(
            configuration_id,
            CredentialFormat(format_identifier),
            proof=str(proofs) if proofs is not None else None,
        )
        return self._capability.issue(request, wallet_attestation=wallet_attestation)


__all__ = ["Oid4vciProtocol"]
