"""Packed attestation verification from WebAuthn section 8.2."""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence

import cbor2
from cryptography import x509
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, ed25519, padding, rsa
from cryptography.x509.oid import NameOID
from tigrbl_identity_contracts.public_key_authentication import (
    AttestationTrustResult,
    AttestationType,
    AuthenticatorAttestation,
)
from tigrbl_public_key_authentication_bases import AttestationStatementVerifierBase
from tigrbl_security_cose import resolve_cose_algorithm, verify_detached_signature


def _hash(name: str | None):
    return {"sha256": hashes.SHA256, "sha384": hashes.SHA384, "sha512": hashes.SHA512}[
        name
    ]()


def _verify_certificate_signature(
    certificate: x509.Certificate, algorithm: int, message: bytes, signature: bytes
) -> bool:
    spec = resolve_cose_algorithm(algorithm)
    key = certificate.public_key()
    try:
        if isinstance(key, ec.EllipticCurvePublicKey):
            key.verify(signature, message, ec.ECDSA(_hash(spec.hash_name)))
        elif isinstance(key, rsa.RSAPublicKey):
            scheme = (
                padding.PSS(
                    mgf=padding.MGF1(_hash(spec.hash_name)),
                    salt_length=padding.PSS.DIGEST_LENGTH,
                )
                if spec.name.startswith("PS")
                else padding.PKCS1v15()
            )
            key.verify(signature, message, scheme, _hash(spec.hash_name))
        elif isinstance(key, ed25519.Ed25519PublicKey) and spec.name == "EdDSA":
            key.verify(signature, message)
        else:
            raise ValueError(
                "attestation certificate key does not match the COSE algorithm"
            )
    except InvalidSignature:
        return False
    return True


def _validate_leaf_profile(certificate: x509.Certificate) -> None:
    if certificate.version is not x509.Version.v3:
        raise ValueError("packed attestation certificate must be X.509 v3")
    for oid in (NameOID.COUNTRY_NAME, NameOID.ORGANIZATION_NAME, NameOID.COMMON_NAME):
        if not certificate.subject.get_attributes_for_oid(oid):
            raise ValueError("packed attestation certificate subject is incomplete")
    units = certificate.subject.get_attributes_for_oid(NameOID.ORGANIZATIONAL_UNIT_NAME)
    if not any(item.value == "Authenticator Attestation" for item in units):
        raise ValueError("packed attestation certificate OU is invalid")
    try:
        if certificate.extensions.get_extension_for_class(
            x509.BasicConstraints
        ).value.ca:
            raise ValueError("packed attestation leaf certificate cannot be a CA")
    except x509.ExtensionNotFound:
        pass


def verify_packed_attestation(
    *,
    statement: Mapping[str, object],
    authenticator_data: bytes,
    client_data_hash: bytes,
    credential_public_key: bytes,
    trust_path_validator: Callable[[Sequence[bytes]], bool] | None = None,
) -> AttestationTrustResult:
    algorithm = statement.get("alg")
    signature = statement.get("sig")
    if not isinstance(algorithm, int) or not isinstance(signature, bytes):
        raise ValueError("packed attestation requires alg and sig")
    signed = authenticator_data + client_data_hash
    chain = statement.get("x5c")
    if chain is None:
        if not verify_detached_signature(
            public_key=credential_public_key,
            algorithm=algorithm,
            message=signed,
            signature=signature,
        ):
            raise ValueError("packed self-attestation signature is invalid")
        return AttestationTrustResult(
            False, AttestationType.SELF, reason="self attestation has no trust path"
        )
    if (
        not isinstance(chain, (list, tuple))
        or not chain
        or not all(isinstance(item, bytes) for item in chain)
    ):
        raise ValueError("packed x5c must be a non-empty certificate sequence")
    leaf = x509.load_der_x509_certificate(chain[0])
    _validate_leaf_profile(leaf)
    if not _verify_certificate_signature(leaf, algorithm, signed, signature):
        raise ValueError("packed attestation signature is invalid")
    trusted = bool(trust_path_validator and trust_path_validator(tuple(chain)))
    return AttestationTrustResult(
        trusted,
        AttestationType.BASIC,
        tuple(chain),
        None if trusted else "certificate path not trusted",
    )


class PackedAttestationVerifier(AttestationStatementVerifierBase):
    def __init__(
        self, trust_path_validator: Callable[[Sequence[bytes]], bool] | None = None
    ) -> None:
        self._trust_path_validator = trust_path_validator

    def verify(
        self, attestation: AuthenticatorAttestation, /
    ) -> AttestationTrustResult:
        statement = cbor2.loads(attestation.statement)
        if (
            not isinstance(statement, Mapping)
            or attestation.credential_public_key is None
        ):
            raise ValueError(
                "packed attestation is missing statement or credential key"
            )
        return verify_packed_attestation(
            statement=statement,
            authenticator_data=attestation.authenticator_data,
            client_data_hash=attestation.client_data_hash,
            credential_public_key=attestation.credential_public_key,
            trust_path_validator=self._trust_path_validator,
        )


__all__ = ["PackedAttestationVerifier", "verify_packed_attestation"]
