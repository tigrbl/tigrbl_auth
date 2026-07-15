"""WebAuthn Level 2 authentication ceremony processing."""

from __future__ import annotations

import hashlib
import secrets
from dataclasses import dataclass

from tigrbl_identity_contracts.public_key_authentication import (
    AuthenticatorProvenanceEvidence,
    CredentialBackupEvidence,
    CredentialLifecycleStatus,
    PublicKeyAuthenticationEvidence,
    PublicKeyCredentialSource,
    UserPresenceEvidence,
    UserVerificationEvidence,
    VerifiedPublicKeyAssertion,
    VerifierBindingEvidence,
)
from tigrbl_security_cose import verify_detached_signature

from ..codecs import decode_authenticator_data, parse_client_data
from ..errors import AuthenticationVerificationError
from ..schemas import (
    PublicKeyCredential,
    PublicKeyCredentialDescriptor,
    PublicKeyCredentialRequestOptions,
)


@dataclass(frozen=True, slots=True)
class AuthenticationExpectation:
    ceremony_id: str
    rp_id: str
    origin: str
    challenge: bytes
    credential: PublicKeyCredentialSource
    user_verification: str = "preferred"


def build_request_options(
    *,
    rp_id: str,
    allowed_credentials: tuple[PublicKeyCredentialSource, ...] = (),
    user_verification: str = "preferred",
    timeout_ms: int = 300_000,
    challenge: bytes | None = None,
) -> PublicKeyCredentialRequestOptions:
    return PublicKeyCredentialRequestOptions(
        challenge=challenge or secrets.token_bytes(32),
        timeout=timeout_ms,
        rp_id=rp_id,
        allow_credentials=tuple(
            PublicKeyCredentialDescriptor(
                id=item.external_id, transports=item.transports
            )
            for item in allowed_credentials
        ),
        user_verification=user_verification,
    )


def verify_authentication_response(
    credential: PublicKeyCredential,
    *,
    expected: AuthenticationExpectation,
) -> VerifiedPublicKeyAssertion:
    try:
        source = expected.credential
        if source.status is not CredentialLifecycleStatus.ACTIVE:
            raise AuthenticationVerificationError("credential is not active")
        if source.binding.rp_id != expected.rp_id:
            raise AuthenticationVerificationError(
                "credential is not bound to the relying party"
            )
        if credential.type != "public-key" or not secrets.compare_digest(
            credential.raw_id, source.external_id
        ):
            raise AuthenticationVerificationError(
                "asserted credential identifier does not match"
            )
        response = credential.response
        if not hasattr(response, "signature"):
            raise AuthenticationVerificationError(
                "authentication requires an assertion response"
            )
        client = parse_client_data(
            response.client_data_json,
            expected_type="webauthn.get",
            expected_challenge=expected.challenge,
            expected_origin=expected.origin,
        )
        if client.value.cross_origin:
            raise AuthenticationVerificationError(
                "cross-origin authentication is not enabled"
            )
        auth = decode_authenticator_data(response.authenticator_data)
        if not auth.matches_rp_id_hash(
            hashlib.sha256(expected.rp_id.encode("utf-8")).digest()
        ):
            raise AuthenticationVerificationError(
                "relying-party identifier hash does not match"
            )
        if not auth.user_present:
            raise AuthenticationVerificationError(
                "authenticator did not report user presence"
            )
        if expected.user_verification == "required" and not auth.user_verified:
            raise AuthenticationVerificationError(
                "authenticator did not report user verification"
            )
        if response.user_handle is not None and source.binding.user_handle is not None:
            if not secrets.compare_digest(
                response.user_handle, source.binding.user_handle
            ):
                raise AuthenticationVerificationError(
                    "asserted user handle does not match"
                )
        if not verify_detached_signature(
            public_key=source.public_key,
            algorithm=source.algorithm,
            message=response.authenticator_data + client.digest,
            signature=response.signature,
        ):
            raise AuthenticationVerificationError("assertion signature is invalid")
        if (
            source.sign_count
            and auth.sign_count
            and auth.sign_count <= source.sign_count
        ):
            raise AuthenticationVerificationError(
                "authenticator counter did not advance"
            )
        principal_id = source.binding.principal_id
        if principal_id is None:
            raise AuthenticationVerificationError(
                "credential has no resolved principal binding"
            )
        evidence = PublicKeyAuthenticationEvidence(
            credential_id=source.credential_id,
            user_presence=UserPresenceEvidence(True),
            user_verification=UserVerificationEvidence(auth.user_verified),
            verifier_binding=VerifierBindingEvidence(
                expected.rp_id, expected.origin, True
            ),
            backup=CredentialBackupEvidence(
                eligible=bool(auth.flags & 0x08),
                backed_up=bool(auth.flags & 0x10),
            ),
            provenance=AuthenticatorProvenanceEvidence(),
        )
        return VerifiedPublicKeyAssertion(
            ceremony_id=expected.ceremony_id,
            credential_id=source.credential_id,
            principal_id=principal_id,
            sign_count=auth.sign_count,
            evidence=evidence,
        )
    except AuthenticationVerificationError:
        raise
    except Exception as exc:
        raise AuthenticationVerificationError(str(exc)) from exc


__all__ = [
    "AuthenticationExpectation",
    "build_request_options",
    "verify_authentication_response",
]
