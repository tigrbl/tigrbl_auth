"""TPM attestation verification from WebAuthn section 8.3."""

from __future__ import annotations

import hashlib
from collections.abc import Callable, Mapping, Sequence

import cbor2
from cryptography import x509
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, padding, rsa
from tigrbl_identity_contracts.public_key_authentication import (
    AttestationTrustResult,
    AttestationType,
    AuthenticatorAttestation,
)
from tigrbl_public_key_authentication_bases import AttestationStatementVerifierBase
from tigrbl_security_cose import decode_cose_key, resolve_cose_algorithm

TPM_GENERATED_VALUE = 0xFF544347
TPM_ST_ATTEST_CERTIFY = 0x8017


class _Reader:
    def __init__(self, value: bytes):
        self.value, self.offset = value, 0

    def take(self, count: int) -> bytes:
        if count < 0 or self.offset + count > len(self.value):
            raise ValueError("TPM structure is truncated")
        result = self.value[self.offset : self.offset + count]
        self.offset += count
        return result

    def u16(self) -> int:
        return int.from_bytes(self.take(2), "big")

    def u32(self) -> int:
        return int.from_bytes(self.take(4), "big")

    def sized(self) -> bytes:
        return self.take(self.u16())


def _digest(name_alg: int, value: bytes) -> bytes:
    names = {0x000B: "sha256", 0x000C: "sha384", 0x000D: "sha512"}
    try:
        return hashlib.new(names[name_alg], value).digest()
    except KeyError as exc:
        raise ValueError(f"unsupported TPM name algorithm: {name_alg:#x}") from exc


def _cert_info_bindings(cert_info: bytes, signed: bytes, pub_area: bytes) -> None:
    reader = _Reader(cert_info)
    if reader.u32() != TPM_GENERATED_VALUE or reader.u16() != TPM_ST_ATTEST_CERTIFY:
        raise ValueError("TPM certInfo magic or type is invalid")
    reader.sized()  # qualifiedSigner
    extra_data = reader.sized()
    if extra_data not in {
        hashlib.sha256(signed).digest(),
        hashlib.sha384(signed).digest(),
        hashlib.sha512(signed).digest(),
    }:
        raise ValueError("TPM certInfo extraData does not bind the WebAuthn ceremony")
    reader.take(17 + 8)  # clockInfo and firmwareVersion
    name = reader.sized()
    reader.sized()  # qualifiedName
    if reader.offset != len(cert_info) or len(name) < 2:
        raise ValueError("TPM certInfo has invalid trailing data")
    name_alg = int.from_bytes(name[:2], "big")
    if name[2:] != _digest(name_alg, pub_area):
        raise ValueError("TPM certInfo name does not bind pubArea")


def _skip_sym(reader: _Reader) -> None:
    algorithm = reader.u16()
    if algorithm != 0x0010:
        reader.take(4)


def _skip_scheme(reader: _Reader) -> None:
    scheme = reader.u16()
    if scheme != 0x0010:
        reader.take(2)


def _public_area_matches(pub_area: bytes, encoded_cose_key: bytes) -> None:
    reader = _Reader(pub_area)
    key_type, name_alg = reader.u16(), reader.u16()
    reader.u32()
    reader.sized()
    cose = decode_cose_key(encoded_cose_key)
    if key_type == 0x0001:  # TPM_ALG_RSA
        _skip_sym(reader)
        _skip_scheme(reader)
        key_bits, exponent = reader.u16(), reader.u32()
        modulus = reader.sized()
        if cose.get(1) != 3 or modulus != cose.get(-1) or key_bits != len(modulus) * 8:
            raise ValueError("TPM RSA pubArea does not match the credential key")
        expected_exponent = int.from_bytes(cose.get(-2), "big")
        if (exponent or 65537) != expected_exponent:
            raise ValueError("TPM RSA exponent does not match the credential key")
    elif key_type == 0x0023:  # TPM_ALG_ECC
        _skip_sym(reader)
        _skip_scheme(reader)
        curve = reader.u16()
        _skip_scheme(reader)
        x, y = reader.sized(), reader.sized()
        curve_map = {0x0003: 1, 0x0004: 2, 0x0005: 3}
        if (
            cose.get(1) != 2
            or cose.get(-1) != curve_map.get(curve)
            or cose.get(-2) != x
            or cose.get(-3) != y
        ):
            raise ValueError("TPM ECC pubArea does not match the credential key")
    else:
        raise ValueError(f"unsupported TPM public key type: {key_type:#x}")
    if reader.offset != len(pub_area):
        raise ValueError("TPM pubArea has trailing data")
    _digest(name_alg, b"")


def _verify_signature(
    certificate: x509.Certificate, algorithm: int, message: bytes, signature: bytes
) -> None:
    spec, key = resolve_cose_algorithm(algorithm), certificate.public_key()
    digest = {
        "sha256": hashes.SHA256,
        "sha384": hashes.SHA384,
        "sha512": hashes.SHA512,
    }[spec.hash_name]()
    try:
        if isinstance(key, ec.EllipticCurvePublicKey):
            key.verify(signature, message, ec.ECDSA(digest))
        elif isinstance(key, rsa.RSAPublicKey):
            scheme = (
                padding.PSS(
                    mgf=padding.MGF1(digest), salt_length=padding.PSS.DIGEST_LENGTH
                )
                if spec.name.startswith("PS")
                else padding.PKCS1v15()
            )
            key.verify(signature, message, scheme, digest)
        else:
            raise ValueError("TPM attestation certificate key is unsupported")
    except InvalidSignature as exc:
        raise ValueError("TPM attestation signature is invalid") from exc


def verify_tpm_attestation(
    *,
    statement: Mapping[str, object],
    authenticator_data: bytes,
    client_data_hash: bytes,
    credential_public_key: bytes,
    trust_path_validator: Callable[[Sequence[bytes]], bool] | None = None,
) -> AttestationTrustResult:
    if statement.get("ver") != "2.0":
        raise ValueError("only TPM attestation version 2.0 is supported")
    algorithm, signature, cert_info, pub_area, chain = (
        statement.get(name) for name in ("alg", "sig", "certInfo", "pubArea", "x5c")
    )
    if not isinstance(algorithm, int) or not all(
        isinstance(item, bytes) for item in (signature, cert_info, pub_area)
    ):
        raise ValueError("TPM attestation statement fields are invalid")
    if (
        not isinstance(chain, (list, tuple))
        or not chain
        or not all(isinstance(item, bytes) for item in chain)
    ):
        raise ValueError("TPM attestation requires an x5c certificate path")
    signed = authenticator_data + client_data_hash
    _cert_info_bindings(cert_info, signed, pub_area)
    _public_area_matches(pub_area, credential_public_key)
    _verify_signature(
        x509.load_der_x509_certificate(chain[0]), algorithm, cert_info, signature
    )
    trusted = bool(trust_path_validator and trust_path_validator(tuple(chain)))
    return AttestationTrustResult(
        trusted,
        AttestationType.ATTCA,
        tuple(chain),
        None if trusted else "TPM attestation path not trusted",
    )


class TpmAttestationVerifier(AttestationStatementVerifierBase):
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
            raise ValueError("TPM attestation is missing statement or credential key")
        return verify_tpm_attestation(
            statement=statement,
            authenticator_data=attestation.authenticator_data,
            client_data_hash=attestation.client_data_hash,
            credential_public_key=attestation.credential_public_key,
            trust_path_validator=self._trust_path_validator,
        )


__all__ = ["TpmAttestationVerifier", "verify_tpm_attestation"]
