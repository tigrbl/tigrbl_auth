import json

import cbor2
import pytest

from tigrbl_cose_concrete import decode_cose_message
from tigrbl_cwt_concrete import CwtClaimsSet
from tigrbl_cwt_svid_extension_credential_concrete import CwtSvidExtensionCredential
from tigrbl_did_document_concrete import DidDocument
from tigrbl_identity_core.base64url import base64url_encode
from tigrbl_jwt_concrete import decode_jwt_unverified
from tigrbl_jwt_svid_credential_concrete import JwtSvidCredential
from tigrbl_oidc_id_token_concrete import OidcIdToken
from tigrbl_vc_cose_credential_concrete import VcCoseCredential
from tigrbl_vc_jose_credential_concrete import VcJoseCredential
from tigrbl_wit_concrete import WorkloadIdentityToken
from tigrbl_wit_svid_credential_concrete import WitSvidCredential
from tigrbl_wpt_concrete import WorkloadProofToken
from tigrbl_x509_svid_credential_concrete import X509SvidCredential


def _jwt(claims, *, typ="JWT"):
    header=base64url_encode(json.dumps({"alg":"ES256","typ":typ},separators=(",",":")).encode())
    payload=base64url_encode(json.dumps(claims,separators=(",",":")).encode())
    signature=base64url_encode(b"structural-signature")
    return decode_jwt_unverified(f"{header}.{payload}.{signature}")


def test_oidc_id_token_is_a_standalone_token_object() -> None:
    token=OidcIdToken(_jwt({"iss":"https://issuer.example","sub":"user","aud":"client","exp":20,"iat":10},typ="JWT"))
    assert token.claims["aud"] == "client"
    with pytest.raises(ValueError, match="required claims"):
        OidcIdToken(_jwt({"sub":"user"}))


def test_did_document_is_an_identity_document_not_a_credential() -> None:
    document=DidDocument("did:example:123",{"id":"did:example:123","verificationMethod":[]})
    assert document.subject == "did:example:123"
    assert document.content["id"] == "did:example:123"
    assert not hasattr(document,"format_identifier")


def test_vc_jose_and_vc_cose_are_separate_credential_formats() -> None:
    jwt=_jwt({"vc":{"type":["VerifiableCredential"]}})
    jose=VcJoseCredential(jwt.jws,{"vc":{"type":["VerifiableCredential"]}})
    encoded=cbor2.dumps(cbor2.CBORTag(18,[b"",{},b"credential",b"signature"]))
    cose=VcCoseCredential(decode_cose_message(encoded),{1:"issuer",2:"subject"})
    assert jose.format_identifier == "vc-jose"
    assert cose.format_identifier == "vc-cose"


def test_wit_wit_svid_and_wpt_remain_distinct_objects() -> None:
    spiffe_id="spiffe://example.org/workload"
    wit=WorkloadIdentityToken(_jwt({"sub":spiffe_id,"cnf":{"jwk":{"kty":"EC"}},"exp":20},typ="wit+jwt"))
    wit_svid=WitSvidCredential(wit,spiffe_id)
    wpt=WorkloadProofToken(_jwt({"aud":"https://service.example","exp":20,"jti":"proof-1","wth":"A"*43},typ="wpt+jwt"))
    assert wit_svid.token is wit
    assert wpt.claims["wth"] == "A"*43


def test_each_svid_format_has_a_standalone_credential_class() -> None:
    spiffe_id="spiffe://example.org/workload"
    x509=X509SvidCredential(spiffe_id,(b"leaf-certificate",),key_reference="key:1")
    jwt=JwtSvidCredential(_jwt({"sub":spiffe_id,"aud":["service"],"exp":20}),spiffe_id,("service",))
    claims=CwtClaimsSet({2:spiffe_id,4:20,8:{5:b"thumbprint"}})
    cwt=CwtSvidExtensionCredential(claims.encode(),claims,spiffe_id,{5:b"thumbprint"})
    assert x509.format_identifier == "x509-svid"
    assert jwt.format_identifier == "jwt-svid"
    assert cwt.format_identifier == "cwt-svid-extension"


def test_cwt_svid_is_explicitly_an_extension_not_an_official_svid_alias() -> None:
    assert CwtSvidExtensionCredential.format_identifier.endswith("-extension")
    assert "extension" in CwtSvidExtensionCredential.__name__.lower()