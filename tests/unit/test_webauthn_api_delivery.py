import pytest

from tigrbl_auth_router_webauthn import (
    PublicKeyCredentialIn,
    decode_base64url,
    encode_base64url,
    parse_public_key_credential,
    to_json_value,
)
from tigrbl_auth_protocol_webauthn import build_request_options


def test_base64url_transport_is_unpadded_and_strict():
    assert encode_base64url(b"credential\x00") == "Y3JlZGVudGlhbAA"
    assert decode_base64url("Y3JlZGVudGlhbAA") == b"credential\x00"
    with pytest.raises(ValueError):
        decode_base64url("not+base64url")


def test_request_options_use_web_api_json_names():
    value = to_json_value(
        build_request_options(rp_id="login.example", challenge=b"a" * 32)
    )
    assert value["rpId"] == "login.example"
    assert value["challenge"] == encode_base64url(b"a" * 32)
    assert "rp_id" not in value


def test_assertion_carrier_parses_to_protocol_schema():
    value = PublicKeyCredentialIn.model_validate(
        {
            "id": "credential",
            "rawId": encode_base64url(b"credential"),
            "type": "public-key",
            "response": {
                "client_data_json": encode_base64url(b"{}"),
                "authenticator_data": encode_base64url(b"a" * 37),
                "signature": encode_base64url(b"signature"),
            },
        }
    )
    parsed = parse_public_key_credential(value)
    assert parsed.raw_id == b"credential"
    assert parsed.response.signature == b"signature"
