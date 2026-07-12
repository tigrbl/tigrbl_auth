import base64
import json

import pytest
from tigrbl_jose_concrete import (
    add_cnf_claim,
    jwk_thumbprint,
    parse_compact_jose,
    validate_amr_claim,
    verify_proof_of_possession,
)
from tigrbl_sd_jwt_concrete import (
    Disclosure,
    decode_disclosure,
    disclosure_digest,
    encode_disclosure,
    parse_key_binding_claims,
    parse_sd_jwt_serialization,
    reconstruct_claims,
)


def _segment(value: object) -> str:
    return base64.urlsafe_b64encode(json.dumps(value).encode()).rstrip(b"=").decode()


def test_jwk_thumbprint_matches_rfc_7638_example():
    jwk = {
        "kty": "RSA",
        "n": "0vx7agoebGcQSuuPiLJXZptN9nndrQmbXEps2ai5M",
        "e": "AQAB",
        "alg": "RS256",
        "kid": "ignored",
    }
    assert jwk_thumbprint(jwk) == jwk_thumbprint(
        {"kty": "RSA", "n": jwk["n"], "e": "AQAB"}
    )


def test_confirmation_and_amr_are_provider_free():
    jwk = {"kty": "OKP", "crv": "Ed25519", "x": "11qYAYdk9J"}
    payload = add_cnf_claim({"sub": "alice"}, jwk)
    assert verify_proof_of_possession(payload, jwk)
    assert validate_amr_claim(("hwk", "pop"))
    assert not validate_amr_claim(("unknown",))


def test_compact_jose_parser_distinguishes_jws_and_jwe():
    header = _segment({"alg": "none"})
    assert parse_compact_jose(f"{header}.payload.signature").segment_count == 3
    assert parse_compact_jose(f"{header}.key.iv.ciphertext.tag").segment_count == 5


def test_sd_jwt_disclosure_round_trip_digest_and_reconstruction():
    encoded = encode_disclosure(Disclosure("salt", "given_name", "Alice"))
    digest = disclosure_digest(encoded)
    assert decode_disclosure(encoded).claim_name == "given_name"
    assert reconstruct_claims({"_sd_alg": "sha-256", "_sd": [digest]}, (encoded,)) == {
        "given_name": "Alice"
    }


def test_sd_jwt_serialization_and_key_binding_are_structural_not_trust_decisions():
    serialization = parse_sd_jwt_serialization("a.b.c~disclosure~d.e.f~")
    assert serialization.key_binding_jwt == "d.e.f"
    claims = parse_key_binding_claims(
        {"aud": "https://verifier", "nonce": "n", "iat": 1, "sd_hash": "hash"}
    )
    assert claims.nonce == "n"
    with pytest.raises(ValueError):
        parse_key_binding_claims({"aud": "https://verifier"})


def test_reconstruction_rejects_unreferenced_disclosure():
    encoded = encode_disclosure(Disclosure("salt", "name", "Alice"))
    with pytest.raises(ValueError, match="unreferenced"):
        reconstruct_claims({"_sd": []}, (encoded,))
