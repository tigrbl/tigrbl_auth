import json
import cbor2
from tba_concrete_cose import decode_cose_message
from tba_primitives_identity.base64url import base64url_encode
from tba_concrete_jwt import decode_jwt_unverified
from tba_concrete_vc_cose_credential import VcCoseCredential
from tba_concrete_vc_jose_credential import VcJoseCredential


def _jwt(claims, *, typ="JWT"):
    header = base64url_encode(
        json.dumps({"alg": "ES256", "typ": typ}, separators=(",", ":")).encode()
    )
    payload = base64url_encode(json.dumps(claims, separators=(",", ":")).encode())
    signature = base64url_encode(b"structural-signature")
    return decode_jwt_unverified(f"{header}.{payload}.{signature}")


def test_vc_jose_and_vc_cose_are_separate_credential_formats() -> None:
    jwt = _jwt({"vc": {"type": ["VerifiableCredential"]}})
    jose = VcJoseCredential(jwt.jws, {"vc": {"type": ["VerifiableCredential"]}})
    encoded = cbor2.dumps(cbor2.CBORTag(18, [b"", {}, b"credential", b"signature"]))
    cose = VcCoseCredential(decode_cose_message(encoded), {1: "issuer", 2: "subject"})
    assert jose.format_identifier == "vc-jose"
    assert cose.format_identifier == "vc-cose"
