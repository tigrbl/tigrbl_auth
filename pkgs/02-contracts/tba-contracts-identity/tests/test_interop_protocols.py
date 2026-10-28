from tba_protocol_oauth.standards.gnap import parse_gnap_request
from tba_protocol_oidc.standards.set_delivery import SetPollRequest, SetPushRequest
from tba_contracts_identity.decentralized import Did
from tba_contracts_identity.policy_interop import XacmlDecision, xacml_to_authzen


def test_did_and_policy_adaptation() -> None:
    assert str(Did.parse("did:web:example.com")) == "did:web:example.com"
    assert xacml_to_authzen(XacmlDecision("Permit")).decision


def test_gnap_and_set_delivery_structures() -> None:
    request = parse_gnap_request({"access_token": {"access": ["read"]}, "client": "instance-id"})
    assert request.access_token[0]["access"] == ["read"]
    assert SetPushRequest("a.b.c").form() == {"SET": "a.b.c"}
    assert SetPollRequest(max_events=10).max_events == 10
