import base64
import json

from tigrbl_identity_credentials_concrete import parse_mdoc, parse_sd_jwt_vc, validate_verifiable_credential


def _b64(value: dict) -> str:
    return base64.urlsafe_b64encode(json.dumps(value).encode()).decode().rstrip("=")


def test_sd_jwt_vc_structure() -> None:
    value = f'{_b64({"typ": "dc+sd-jwt", "alg": "ES256"})}.{_b64({"iss": "https://i", "vct": "Example"})}.sig~disc~'
    parsed = parse_sd_jwt_vc(value)
    assert parsed.claims["vct"] == "Example"
    assert parsed.disclosures == ("disc",)


def test_mdoc_structure() -> None:
    parsed = parse_mdoc({"docType": "org.iso.18013.5.1.mDL", "issuerSigned": {"nameSpaces": {}, "issuerAuth": b"cose"}})
    assert parsed.doc_type.endswith("mDL")


def test_vcdm_structure() -> None:
    validate_verifiable_credential({"@context": ["https://www.w3.org/ns/credentials/v2"], "type": ["VerifiableCredential"], "issuer": "did:example:i", "credentialSubject": {"id": "did:example:s"}})
