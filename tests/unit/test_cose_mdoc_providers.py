import pickle
from hashlib import sha256

from tigrbl_identity_contracts.digital_credentials import (
    CredentialFormat,
    CredentialIssuanceRequest,
    CredentialVerificationRequest,
)
from tigrbl_mdoc_issuer_provider import MdocIssuerProvider
from tigrbl_mdoc_verifier_provider import MdocVerifierProvider
from tigrbl_security_cose import CoseSign1Provider


def _encode(value):
    return pickle.dumps(dict(value), protocol=4)


def _decode(value):
    return pickle.loads(value)


def _cose():
    return CoseSign1Provider(
        signer=lambda payload, headers, aad: b"COSE" + payload,
        verifier=lambda encoded, aad, profile: (
            encoded.startswith(b"COSE") and profile == "mdoc-issuer"
        ),
    )


def _request():
    item = {
        "digestID": 0,
        "random": b"random",
        "elementIdentifier": "family_name",
        "elementValue": "Doe",
    }
    mso = {
        "version": "1.0",
        "digestAlgorithm": "SHA-256",
        "valueDigests": {"org.iso.18013.5.1": {0: sha256(_encode(item)).digest()}},
        "deviceKeyInfo": {"deviceKey": {"kty": 2}},
        "docType": "org.iso.18013.5.1.mDL",
        "validityInfo": {
            "signed": "2026-01-01T00:00:00Z",
            "validFrom": "2026-01-01T00:00:00Z",
            "validUntil": "2027-01-01T00:00:00Z",
        },
    }
    return CredentialIssuanceRequest(
        "mdl",
        CredentialFormat("mso_mdoc", "application/mdl"),
        subject="did:example:alice",
        attributes={
            "mdoc": {
                "docType": "org.iso.18013.5.1.mDL",
                "issuerSigned": {
                    "nameSpaces": {"org.iso.18013.5.1": [item]},
                },
            },
            "mobile_security_object": mso,
        },
    )


def test_cose_provider_refuses_to_claim_signing_or_verification_without_backends():
    provider = CoseSign1Provider()
    try:
        provider.sign1(b"payload", {1: -7})
    except RuntimeError:
        pass
    else:
        raise AssertionError("COSE signing succeeded without a backend")


def test_mdoc_issuer_and_verifier_compose_cbor_cose_and_digest_validation():
    issuance = MdocIssuerProvider(_cose(), _encode, -7).issue(_request())
    assert issuance.credential is not None
    verifier = MdocVerifierProvider(
        _cose(),
        _encode,
        _decode,
        lambda encoded: encoded.removeprefix(b"COSE"),
    )
    result = verifier.verify(
        CredentialVerificationRequest(
            issuance.credential,
            CredentialFormat("mso_mdoc", "application/mdl"),
        )
    )
    assert result.valid
    assert result.claims["org.iso.18013.5.1"]["family_name"] == "Doe"


def test_mdoc_verifier_rejects_tampered_issuer_signed_item():
    issuance = MdocIssuerProvider(_cose(), _encode, -7).issue(_request())
    raw = _decode(issuance.credential.payload)
    raw["issuerSigned"]["nameSpaces"]["org.iso.18013.5.1"][0]["elementValue"] = (
        "Mallory"
    )
    tampered = type(issuance.credential)(
        issuance.credential.format,
        _encode(raw),
        subject=issuance.credential.subject,
    )
    verifier = MdocVerifierProvider(
        _cose(), _encode, _decode, lambda encoded: encoded.removeprefix(b"COSE")
    )
    result = verifier.verify(CredentialVerificationRequest(tampered, tampered.format))
    assert not result.valid and "digest mismatch" in result.errors[0]
