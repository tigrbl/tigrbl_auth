import json
from tba_concrete_cwt import CwtClaimsSet
from tba_concrete_cwt_svid_extension_credential import CwtSvidExtensionCredential
from tba_primitives_identity.base64url import base64url_encode
from tba_concrete_jwt import decode_jwt_unverified
from tba_concrete_jwt_svid_credential import JwtSvidCredential
from tba_concrete_x509_svid_credential import X509SvidCredential


def _jwt(claims, *, typ="JWT"):
    header = base64url_encode(
        json.dumps({"alg": "ES256", "typ": typ}, separators=(",", ":")).encode()
    )
    payload = base64url_encode(json.dumps(claims, separators=(",", ":")).encode())
    signature = base64url_encode(b"structural-signature")
    return decode_jwt_unverified(f"{header}.{payload}.{signature}")


def test_each_svid_format_has_a_standalone_credential_class() -> None:
    spiffe_id = "spiffe://example.org/workload"
    x509 = X509SvidCredential(spiffe_id, (b"leaf-certificate",), key_reference="key:1")
    jwt = JwtSvidCredential(
        _jwt({"sub": spiffe_id, "aud": ["service"], "exp": 20}), spiffe_id, ("service",)
    )
    claims = CwtClaimsSet({2: spiffe_id, 4: 20, 8: {5: b"thumbprint"}})
    cwt = CwtSvidExtensionCredential(
        claims.encode(), claims, spiffe_id, {5: b"thumbprint"}
    )
    assert x509.format_identifier == "x509-svid"
    assert jwt.format_identifier == "jwt-svid"
    assert cwt.format_identifier == "cwt-svid-extension"


def test_cwt_svid_is_explicitly_an_extension_not_an_official_svid_alias() -> None:
    assert CwtSvidExtensionCredential.format_identifier.endswith("-extension")
    assert "extension" in CwtSvidExtensionCredential.__name__.lower()
