from tigrbl_identity_contracts.workload_identity import SpiffeId, Svid, SvidFormat
from tigrbl_identity_credentials_concrete import parse_corim, parse_eat


def test_spiffe_id_and_svid_are_identity_and_credential_respectively() -> None:
    identity = SpiffeId.parse("spiffe://Example.org/ns/payments/sa/api")
    credential = Svid(identity, SvidFormat.JWT, "header.payload.signature")
    assert str(credential.spiffe_id) == "spiffe://example.org/ns/payments/sa/api"


def test_eat_and_corim_are_distinct_evidence_and_reference_material() -> None:
    evidence = parse_eat({265: "urn:example:eat", 10: b"nonce"})
    reference = parse_corim({"tag-identity": "tag-1", "comids": [{"measurements": []}]})
    assert evidence.profile == "urn:example:eat"
    assert reference.tag_identity == "tag-1"
