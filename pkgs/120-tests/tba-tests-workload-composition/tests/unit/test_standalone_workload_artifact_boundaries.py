import json
from tba_primitives_identity.base64url import base64url_encode
from tba_concrete_jwt import decode_jwt_unverified
from tba_concrete_wit import WorkloadIdentityToken
from tba_concrete_wit_svid_credential import WitSvidCredential
from tba_concrete_wpt import WorkloadProofToken


def _jwt(claims, *, typ="JWT"):
    header = base64url_encode(
        json.dumps({"alg": "ES256", "typ": typ}, separators=(",", ":")).encode()
    )
    payload = base64url_encode(json.dumps(claims, separators=(",", ":")).encode())
    signature = base64url_encode(b"structural-signature")
    return decode_jwt_unverified(f"{header}.{payload}.{signature}")


def test_wit_wit_svid_and_wpt_remain_distinct_objects() -> None:
    spiffe_id = "spiffe://example.org/workload"
    wit = WorkloadIdentityToken(
        _jwt(
            {"sub": spiffe_id, "cnf": {"jwk": {"kty": "EC"}}, "exp": 20}, typ="wit+jwt"
        )
    )
    wit_svid = WitSvidCredential(wit, spiffe_id)
    wpt = WorkloadProofToken(
        _jwt(
            {
                "aud": "https://service.example",
                "exp": 20,
                "jti": "proof-1",
                "wth": "A" * 43,
            },
            typ="wpt+jwt",
        )
    )
    assert wit_svid.token is wit
    assert wpt.claims["wth"] == "A" * 43
