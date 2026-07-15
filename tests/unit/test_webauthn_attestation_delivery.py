from __future__ import annotations

import hashlib
from datetime import datetime, timedelta, timezone

import cbor2
import pytest
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.x509.oid import NameOID

from tigrbl_attestation_packed_provider import verify_packed_attestation
from tigrbl_attestation_tpm_provider import verify_tpm_attestation
from tigrbl_attestation_u2f_provider import verify_u2f_attestation
from tigrbl_fido_metadata_service_provider import FidoMetadataServiceProvider


def _key_material():
    private = ec.generate_private_key(ec.SECP256R1())
    numbers = private.public_key().public_numbers()
    cose = cbor2.dumps(
        {
            1: 2,
            3: -7,
            -1: 1,
            -2: numbers.x.to_bytes(32, "big"),
            -3: numbers.y.to_bytes(32, "big"),
        },
        canonical=True,
    )
    return private, cose, numbers


def _certificate(private, *, packed_profile: bool = False) -> bytes:
    now = datetime.now(timezone.utc)
    attributes = [
        x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Example"),
        x509.NameAttribute(NameOID.COMMON_NAME, "Authenticator"),
    ]
    if packed_profile:
        attributes.append(
            x509.NameAttribute(
                NameOID.ORGANIZATIONAL_UNIT_NAME, "Authenticator Attestation"
            )
        )
    name = x509.Name(attributes)
    certificate = (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .public_key(private.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - timedelta(minutes=1))
        .not_valid_after(now + timedelta(days=1))
        .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
        .sign(private, hashes.SHA256())
    )
    return certificate.public_bytes(serialization.Encoding.DER)


def test_packed_self_and_basic_attestation_verify():
    credential_private, cose, _ = _key_material()
    auth, client_hash = b"authenticator-data", b"c" * 32
    self_signature = credential_private.sign(
        auth + client_hash, ec.ECDSA(hashes.SHA256())
    )
    result = verify_packed_attestation(
        statement={"alg": -7, "sig": self_signature},
        authenticator_data=auth,
        client_data_hash=client_hash,
        credential_public_key=cose,
    )
    assert result.attestation_type.value == "self"

    attestation_private, _, _ = _key_material()
    signature = attestation_private.sign(auth + client_hash, ec.ECDSA(hashes.SHA256()))
    result = verify_packed_attestation(
        statement={
            "alg": -7,
            "sig": signature,
            "x5c": [_certificate(attestation_private, packed_profile=True)],
        },
        authenticator_data=auth,
        client_data_hash=client_hash,
        credential_public_key=cose,
        trust_path_validator=lambda chain: len(chain) == 1,
    )
    assert result.trusted


def test_u2f_attestation_binds_rp_client_credential_and_key():
    _, cose, numbers = _key_material()
    attestation_private, _, _ = _key_material()
    rp_hash, client_hash, credential_id = b"r" * 32, b"c" * 32, b"credential"
    signed = (
        b"\x00"
        + rp_hash
        + client_hash
        + credential_id
        + b"\x04"
        + numbers.x.to_bytes(32, "big")
        + numbers.y.to_bytes(32, "big")
    )
    signature = attestation_private.sign(signed, ec.ECDSA(hashes.SHA256()))
    result = verify_u2f_attestation(
        statement={"sig": signature, "x5c": [_certificate(attestation_private)]},
        rp_id_hash=rp_hash,
        client_data_hash=client_hash,
        credential_id=credential_id,
        credential_public_key=cose,
        trust_path_validator=lambda _: True,
    )
    assert result.trusted


def test_tpm_attestation_binds_cert_info_and_public_area():
    _, cose, numbers = _key_material()
    aik_private, _, _ = _key_material()
    pub_area = (
        (0x0023).to_bytes(2, "big")
        + (0x000B).to_bytes(2, "big")
        + b"\x00" * 4
        + b"\x00\x00"
        + (0x0010).to_bytes(2, "big")
        + (0x0010).to_bytes(2, "big")
        + (0x0003).to_bytes(2, "big")
        + (0x0010).to_bytes(2, "big")
        + (32).to_bytes(2, "big")
        + numbers.x.to_bytes(32, "big")
        + (32).to_bytes(2, "big")
        + numbers.y.to_bytes(32, "big")
    )
    auth, client_hash = b"auth", b"c" * 32
    extra = hashlib.sha256(auth + client_hash).digest()
    name = (0x000B).to_bytes(2, "big") + hashlib.sha256(pub_area).digest()
    cert_info = (
        (0xFF544347).to_bytes(4, "big")
        + (0x8017).to_bytes(2, "big")
        + b"\x00\x00"
        + len(extra).to_bytes(2, "big")
        + extra
        + b"\x00" * 25
        + len(name).to_bytes(2, "big")
        + name
        + b"\x00\x00"
    )
    signature = aik_private.sign(cert_info, ec.ECDSA(hashes.SHA256()))
    result = verify_tpm_attestation(
        statement={
            "ver": "2.0",
            "alg": -7,
            "sig": signature,
            "certInfo": cert_info,
            "pubArea": pub_area,
            "x5c": [_certificate(aik_private)],
        },
        authenticator_data=auth,
        client_data_hash=client_hash,
        credential_public_key=cose,
        trust_path_validator=lambda _: True,
    )
    assert result.trusted


@pytest.mark.asyncio
async def test_metadata_provider_rejects_rollback_and_resolves_status():
    claims = {
        "no": 2,
        "nextUpdate": (
            datetime.now(timezone.utc).date() + timedelta(days=1)
        ).isoformat(),
        "entries": [
            {
                "aaguid": "00000000-0000-0000-0000-000000000001",
                "statusReports": [{"status": "FIDO_CERTIFIED"}],
                "metadataStatement": {"description": "Test"},
            }
        ],
    }
    provider = FidoMetadataServiceProvider(
        fetch_blob=lambda: "signed", verify_signed_blob=lambda _: claims
    )
    result = await provider.resolve(bytes.fromhex("00" * 15 + "01"))
    assert result.found and result.status == "FIDO_CERTIFIED"
    claims["no"] = 1
    with pytest.raises(ValueError, match="rollback"):
        await provider.refresh()
