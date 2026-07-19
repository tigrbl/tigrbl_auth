import json

import cbor2
import pytest

from tigrbl_cose_concrete import CoseMessageKind, decode_cose_message
from tigrbl_cwt_concrete import CwtClaimsSet, decode_cwt_claims
from tigrbl_identity_core.base64url import base64url_encode
from tigrbl_jwe_concrete import parse_jwe_compact
from tigrbl_jws_concrete import parse_jws_compact
from tigrbl_jwt_concrete import decode_jwt_unverified


def _json_segment(value: object) -> str:
    return base64url_encode(json.dumps(value, separators=(",", ":")).encode())


def test_jws_compact_exposes_exact_signing_input() -> None:
    protected = _json_segment({"alg": "ES256", "typ": "JWT"})
    payload = base64url_encode(b'{"sub":"workload"}')
    signature = base64url_encode(b"signature")
    jws = parse_jws_compact(f"{protected}.{payload}.{signature}")

    assert jws.protected_headers["alg"] == "ES256"
    assert jws.payload == b'{"sub":"workload"}'
    assert jws.signing_input() == f"{protected}.{payload}".encode()


def test_jws_supports_detached_and_unencoded_payloads() -> None:
    protected = _json_segment({"alg": "ES256", "b64": False, "crit": ["b64"]})
    signature = base64url_encode(b"signature")
    jws = parse_jws_compact(f"{protected}..{signature}")

    assert jws.detached is True
    assert jws.signing_input(b"message") == protected.encode() + b".message"


def test_jwe_compact_preserves_direct_encryption_empty_key_segment() -> None:
    protected = _json_segment({"alg": "dir", "enc": "A256GCM"})
    value = ".".join(
        (
            protected,
            "",
            base64url_encode(b"123456789012"),
            base64url_encode(b"ciphertext"),
            base64url_encode(b"authentication-tag"),
        )
    )
    jwe = parse_jwe_compact(value)

    assert jwe.encrypted_key == b""
    assert jwe.protected_headers == {"alg": "dir", "enc": "A256GCM"}
    assert jwe.additional_authenticated_data == protected.encode()


def test_jwt_decoder_is_explicitly_unverified() -> None:
    protected = _json_segment({"alg": "ES256", "typ": "JWT"})
    claims = _json_segment({"iss": "https://issuer.example", "sub": "subject"})
    token = f"{protected}.{claims}.{base64url_encode(b'signature')}"

    jwt = decode_jwt_unverified(token)

    assert jwt.claims["sub"] == "subject"
    assert jwt.integrity_verified is False


@pytest.mark.parametrize(
    ("tag", "kind", "value"),
    [
        (98, CoseMessageKind.SIGN, [b"", {}, b"payload", []]),
        (18, CoseMessageKind.SIGN1, [cbor2.dumps({1: -7}), {}, b"payload", b"sig"]),
        (96, CoseMessageKind.ENCRYPT, [b"", {}, b"ciphertext", []]),
        (16, CoseMessageKind.ENCRYPT0, [b"", {}, b"ciphertext"]),
        (97, CoseMessageKind.MAC, [b"", {}, b"payload", b"tag", []]),
        (17, CoseMessageKind.MAC0, [b"", {}, b"payload", b"tag"]),
    ],
)
def test_cose_message_decoder_distinguishes_all_rfc9052_structures(
    tag,
    kind,
    value,
) -> None:
    message = decode_cose_message(cbor2.dumps(cbor2.CBORTag(tag, value)))

    assert message.kind is kind
    assert message.tagged is True


def test_untagged_cose_requires_explicit_expected_kind() -> None:
    encoded = cbor2.dumps([b"", {}, b"payload", b"signature"])
    with pytest.raises(ValueError, match="expected kind"):
        decode_cose_message(encoded)

    message = decode_cose_message(encoded, expected_kind=CoseMessageKind.SIGN1)
    assert message.kind is CoseMessageKind.SIGN1


def test_cwt_claims_preserve_integer_labels_and_encode_canonically() -> None:
    claims = CwtClaimsSet({1: "issuer", 2: "subject", 8: {5: b"thumbprint"}})
    encoded = claims.encode()
    decoded = decode_cwt_claims(encoded)

    assert decoded.get_registered("iss") == "issuer"
    assert decoded.get_registered("cnf") == {5: b"thumbprint"}
    assert decoded.encode() == encoded


def test_structural_decoders_reject_ambiguous_or_malformed_values() -> None:
    with pytest.raises(ValueError):
        parse_jws_compact("not.a.jws.with.extra")
    with pytest.raises(ValueError):
        parse_jwe_compact("not.a.jwe")
    with pytest.raises(ValueError):
        decode_cwt_claims(cbor2.dumps(["not", "a", "map"]))