from tigrbl_auth_protocol_oidc.standards.openid4vc import (
    HaipPolicy,
    parse_credential_offer,
    parse_presentation_request,
)


def test_offer_and_presentation_request() -> None:
    offer = parse_credential_offer(
        {
            "credential_issuer": "https://issuer.example",
            "credential_configuration_ids": ["pid"],
            "grants": {},
        }
    )
    request = parse_presentation_request(
        {
            "client_id": "x509_san_dns:verifier.example",
            "nonce": "n",
            "response_type": "vp_token",
            "dcql_query": {"credentials": []},
        }
    )
    assert offer.credential_configuration_ids == ("pid",)
    assert request.nonce == "n"
    assert HaipPolicy().accepts_format("mso_mdoc")
