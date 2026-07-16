"""WebAuthn Level 2 registration ceremony processing."""

from __future__ import annotations

import base64
import hashlib
import secrets
from dataclasses import dataclass

from tigrbl_identity_contracts.public_key_authentication import (
    AttestationTrustResult,
    AttestationType,
    CredentialBinding,
    PublicKeyCredentialSource,
    VerifiedCredentialRegistration,
)
from tigrbl_cose_concrete import decode_cose_key
from tigrbl_cose_cryptography_provider import verify_detached_signature

from ..codecs import decode_attestation_object, parse_client_data
from ..attestation import AttestationVerificationInput, AttestationVerifierRegistry
from ..errors import RegistrationVerificationError
from ..schemas import (
    AuthenticatorSelectionCriteria,
    PublicKeyCredential,
    PublicKeyCredentialCreationOptions,
    PublicKeyCredentialDescriptor,
    PublicKeyCredentialParameters,
    PublicKeyCredentialRpEntity,
    PublicKeyCredentialUserEntity,
)


def _identifier(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode("ascii")


@dataclass(frozen=True, slots=True)
class RegistrationExpectation:
    ceremony_id: str
    tenant_id: str
    principal_id: str
    rp_id: str
    origin: str
    challenge: bytes
    user_handle: bytes
    allowed_algorithms: tuple[int, ...] = (-7, -257)
    user_verification: str = "preferred"
    attestation_verifiers: AttestationVerifierRegistry | None = None


def build_creation_options(
    *,
    rp_id: str,
    rp_name: str,
    user_handle: bytes,
    user_name: str,
    user_display_name: str,
    algorithms: tuple[int, ...] = (-7, -257),
    excluded_credential_ids: tuple[bytes, ...] = (),
    user_verification: str = "preferred",
    resident_key: str = "preferred",
    attestation: str = "none",
    timeout_ms: int = 300_000,
    challenge: bytes | None = None,
) -> PublicKeyCredentialCreationOptions:
    if not algorithms:
        raise ValueError("at least one credential algorithm is required")
    return PublicKeyCredentialCreationOptions(
        challenge=challenge or secrets.token_bytes(32),
        rp=PublicKeyCredentialRpEntity(id=rp_id, name=rp_name),
        user=PublicKeyCredentialUserEntity(
            id=user_handle, name=user_name, display_name=user_display_name
        ),
        pub_key_cred_params=tuple(
            PublicKeyCredentialParameters(alg=value) for value in algorithms
        ),
        timeout=timeout_ms,
        exclude_credentials=tuple(
            PublicKeyCredentialDescriptor(id=value) for value in excluded_credential_ids
        ),
        authenticator_selection=AuthenticatorSelectionCriteria(
            resident_key=resident_key,
            require_resident_key=resident_key == "required",
            user_verification=user_verification,
        ),
        attestation=attestation,
    )


def verify_registration_response(
    credential: PublicKeyCredential,
    *,
    expected: RegistrationExpectation,
) -> VerifiedCredentialRegistration:
    try:
        if credential.type != "public-key" or credential.raw_id == b"":
            raise RegistrationVerificationError(
                "registration credential type or identifier is invalid"
            )
        response = credential.response
        if not hasattr(response, "attestation_object"):
            raise RegistrationVerificationError(
                "registration requires an attestation response"
            )
        client = parse_client_data(
            response.client_data_json,
            expected_type="webauthn.create",
            expected_challenge=expected.challenge,
            expected_origin=expected.origin,
        )
        if client.value.cross_origin:
            raise RegistrationVerificationError(
                "cross-origin registration is not enabled"
            )
        attestation = decode_attestation_object(response.attestation_object)
        auth = attestation.authenticator_data
        if not auth.matches_rp_id_hash(
            hashlib.sha256(expected.rp_id.encode("utf-8")).digest()
        ):
            raise RegistrationVerificationError(
                "relying-party identifier hash does not match"
            )
        if not auth.user_present:
            raise RegistrationVerificationError(
                "authenticator did not report user presence"
            )
        if expected.user_verification == "required" and not auth.user_verified:
            raise RegistrationVerificationError(
                "authenticator did not report user verification"
            )
        data = auth.attested_credential_data
        if data is None:
            raise RegistrationVerificationError(
                "registration omitted attested credential data"
            )
        if not secrets.compare_digest(data.credential_id, credential.raw_id):
            raise RegistrationVerificationError(
                "credential identifier does not match authenticator data"
            )
        cose_key = decode_cose_key(data.credential_public_key)
        algorithm = cose_key.get(3)
        if (
            not isinstance(algorithm, int)
            or algorithm not in expected.allowed_algorithms
        ):
            raise RegistrationVerificationError("credential algorithm is not allowed")
        if attestation.format == "none":
            if attestation.statement:
                raise RegistrationVerificationError(
                    "none attestation must have an empty statement"
                )
            trust = AttestationTrustResult(
                False, AttestationType.NONE, reason="attestation not requested"
            )
        elif attestation.format == "packed" and "x5c" not in attestation.statement:
            statement_algorithm = attestation.statement.get("alg")
            signature = attestation.statement.get("sig")
            if statement_algorithm != algorithm or not isinstance(signature, bytes):
                raise RegistrationVerificationError(
                    "packed self-attestation statement is invalid"
                )
            if not verify_detached_signature(
                public_key=data.credential_public_key,
                algorithm=algorithm,
                message=auth.raw + client.digest,
                signature=signature,
            ):
                raise RegistrationVerificationError(
                    "packed self-attestation signature is invalid"
                )
            trust = AttestationTrustResult(
                False, AttestationType.SELF, reason="self attestation"
            )
        else:
            if expected.attestation_verifiers is None:
                raise RegistrationVerificationError(
                    f"attestation format requires a configured provider: {attestation.format}"
                )
            trust = expected.attestation_verifiers.verify(
                AttestationVerificationInput(
                    format=attestation.format,
                    statement=attestation.statement,
                    authenticator_data=auth.raw,
                    client_data_hash=client.digest,
                    rp_id_hash=auth.rp_id_hash,
                    credential_id=data.credential_id,
                    credential_public_key=data.credential_public_key,
                    aaguid=data.aaguid,
                )
            )
        source = PublicKeyCredentialSource(
            credential_id=_identifier(credential.raw_id),
            external_id=credential.raw_id,
            public_key=data.credential_public_key,
            algorithm=algorithm,
            binding=CredentialBinding(
                tenant_id=expected.tenant_id,
                rp_id=expected.rp_id,
                principal_id=expected.principal_id,
                user_handle=expected.user_handle,
            ),
            sign_count=auth.sign_count,
            transports=tuple(response.transports),
            discoverable=False,
            backup_eligible=bool(auth.flags & 0x08),
            backup_state=bool(auth.flags & 0x10),
        )
        return VerifiedCredentialRegistration(expected.ceremony_id, source, trust)
    except RegistrationVerificationError:
        raise
    except Exception as exc:
        raise RegistrationVerificationError(str(exc)) from exc


__all__ = [
    "RegistrationExpectation",
    "build_creation_options",
    "verify_registration_response",
]
