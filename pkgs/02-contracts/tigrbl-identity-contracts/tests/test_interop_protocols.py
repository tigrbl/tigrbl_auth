from tigrbl_auth_protocol_oauth.standards.gnap import parse_gnap_request
from tigrbl_auth_protocol_oidc.standards.set_delivery import SetPollRequest, SetPushRequest
from tigrbl_identity_contracts.decentralized import Did
from tigrbl_identity_contracts.policy_interop import XacmlDecision, xacml_to_authzen


def test_did_and_policy_adaptation() -> None:
    assert str(Did.parse("did:web:example.com")) == "did:web:example.com"
    assert xacml_to_authzen(XacmlDecision("Permit")).decision


def test_gnap_and_set_delivery_structures() -> None:
    request = parse_gnap_request({"access_token": {"access": ["read"]}, "client": "instance-id"})
    assert request.access_token[0]["access"] == ["read"]
    assert SetPushRequest("a.b.c").form() == {"SET": "a.b.c"}
    assert SetPollRequest(max_events=10).max_events == 10
