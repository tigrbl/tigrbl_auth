import json
import pytest
from tigrbl_identity_core.base64url import base64url_encode
from tigrbl_jws_concrete import parse_jws_json, validate_unencoded_payload_headers
from tigrbl_jwe_concrete import parse_jwe_json
from tigrbl_jwt_concrete import validate_registered_claims
from tigrbl_cose_concrete import sig_structure
from tigrbl_cwt_concrete import CwtClaimsSet, decode_tagged_cwt, encode_tagged_cwt

def b64(value: bytes) -> str: return base64url_encode(value)
def test_jws_json_and_rfc7797() -> None:
    protected=b64(json.dumps({"alg":"ES256"}).encode())
    parsed=parse_jws_json({"payload":b64(b"p"),"protected":protected,"signature":b64(b"s")})
    assert parsed.payload == b"p"
    with pytest.raises(ValueError): validate_unencoded_payload_headers({"alg":"ES256","b64":False})
    validate_unencoded_payload_headers({"alg":"ES256","b64":False,"crit":["b64"]})
def test_jwe_json_headers_are_disjoint() -> None:
    protected=b64(json.dumps({"enc":"A256GCM"}).encode())
    parsed=parse_jwe_json({"protected":protected,"header":{"alg":"dir"},"encrypted_key":"","iv":b64(b"123456789012"),"ciphertext":b64(b"c"),"tag":b64(b"1234567890123456")})
    assert parsed.recipients[0].header["alg"] == "dir"
def test_jwt_cose_and_tagged_cwt() -> None:
    validate_registered_claims({"iss":"i","aud":["a"],"exp":20,"iat":1},issuer="i",audience="a",now=10)
    assert isinstance(sig_structure("Signature1",b"",b"",b"p"),bytes)
    claims=CwtClaimsSet({1:"i",4:20})
    assert decode_tagged_cwt(encode_tagged_cwt(claims)).get_registered("iss") == "i"