from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence

import cbor2
from cryptography import x509
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from tigrbl_identity_contracts.public_key_authentication import (
    AttestationTrustResult,
    AttestationType,
    AuthenticatorAttestation,
)
from tigrbl_public_key_authentication_bases import AttestationStatementVerifierBase
from tigrbl_security_cose import decode_cose_key


def verify_u2f_attestation(
    *,
    statement: Mapping[str, object],
    rp_id_hash: bytes,
    client_data_hash: bytes,
    credential_id: bytes,
    credential_public_key: bytes,
    trust_path_validator: Callable[[Sequence[bytes]], bool] | None = None,
) -> AttestationTrustResult:
    signature = statement.get("sig")
    chain = statement.get("x5c")
    if (
        not isinstance(signature, bytes)
        or not isinstance(chain, (list, tuple))
        or len(chain) != 1
        or not isinstance(chain[0], bytes)
    ):
        raise ValueError(
            "fido-u2f attestation requires sig and exactly one certificate"
        )
    key = decode_cose_key(credential_public_key)
    if key.get(1) != 2 or key.get(3) != -7 or key.get(-1) != 1:
        raise ValueError("fido-u2f credential key must be an ES256 P-256 key")
    x, y = key.get(-2), key.get(-3)
    if (
        not isinstance(x, bytes)
        or len(x) != 32
        or not isinstance(y, bytes)
        or len(y) != 32
    ):
        raise ValueError("fido-u2f credential key coordinates are invalid")
    verification_data = (
        b"\x00" + rp_id_hash + client_data_hash + credential_id + b"\x04" + x + y
    )
    certificate = x509.load_der_x509_certificate(chain[0])
    public_key = certificate.public_key()
    if not isinstance(public_key, ec.EllipticCurvePublicKey):
        raise ValueError("fido-u2f attestation certificate must contain an EC key")
    try:
        public_key.verify(signature, verification_data, ec.ECDSA(hashes.SHA256()))
    except InvalidSignature as exc:
        raise ValueError("fido-u2f attestation signature is invalid") from exc
    trusted = bool(trust_path_validator and trust_path_validator(tuple(chain)))
    return AttestationTrustResult(
        trusted,
        AttestationType.BASIC,
        tuple(chain),
        None if trusted else "certificate not trusted",
    )


class U2fAttestationVerifier(AttestationStatementVerifierBase):
    def __init__(
        self, trust_path_validator: Callable[[Sequence[bytes]], bool] | None = None
    ) -> None:
        self._trust_path_validator = trust_path_validator

    def verify(
        self, attestation: AuthenticatorAttestation, /
    ) -> AttestationTrustResult:
        statement = cbor2.loads(attestation.statement)
        if not isinstance(statement, Mapping) or any(
            value is None
            for value in (
                attestation.rp_id_hash,
                attestation.credential_id,
                attestation.credential_public_key,
            )
        ):
            raise ValueError("fido-u2f attestation is missing binding data")
        return verify_u2f_attestation(
            statement=statement,
            rp_id_hash=attestation.rp_id_hash,
            client_data_hash=attestation.client_data_hash,
            credential_id=attestation.credential_id,
            credential_public_key=attestation.credential_public_key,
            trust_path_validator=self._trust_path_validator,
        )


__all__ = ["U2fAttestationVerifier", "verify_u2f_attestation"]
