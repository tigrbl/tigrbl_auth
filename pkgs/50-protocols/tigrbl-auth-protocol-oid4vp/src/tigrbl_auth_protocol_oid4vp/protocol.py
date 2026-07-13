from collections.abc import Mapping

from tigrbl_digital_credential_presentation import (
    DigitalCredentialPresentationCapability,
)
from tigrbl_identity_contracts.digital_credentials import (
    PresentationRequest,
    TransactionBinding,
)


class Oid4vpProtocol:
    version = "1.0"

    def __init__(self, capability: DigitalCredentialPresentationCapability):
        self._capability = capability

    def verify(
        self,
        holder: str,
        vp_token: str | bytes,
        authorization_request: Mapping[str, object],
    ):
        client_id, nonce = (
            authorization_request.get("client_id"),
            authorization_request.get("nonce"),
        )
        formats = authorization_request.get("accepted_formats")
        if not isinstance(client_id, str) or not isinstance(nonce, str) or not nonce:
            raise ValueError("OID4VP request requires client_id and nonce")
        if (
            not isinstance(formats, list)
            or not formats
            or not all(isinstance(item, str) for item in formats)
        ):
            raise ValueError("OID4VP request requires accepted_formats")
        transaction_id = authorization_request.get("state")
        request = PresentationRequest(
            tuple(formats),
            TransactionBinding(
                nonce,
                client_id,
                transaction_id if isinstance(transaction_id, str) else None,
            ),
        )
        return self._capability.present(holder, vp_token, request)


__all__ = ["Oid4vpProtocol"]
