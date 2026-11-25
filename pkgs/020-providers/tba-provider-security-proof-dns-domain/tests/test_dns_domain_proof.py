import httpx
import pytest

from tba_provider_security_proof_dns_domain import DnsDomainOwnershipVerifier, DomainProofUnavailable


@pytest.mark.parametrize(("txt_owner", "target", "expected"), [
    ("_proof.login.example.net.", "edge.example.org.", True),
    ("_proof.other.example.net.", "edge.example.org.", False),
    ("_proof.login.example.net.", "other.example.org.", False),
])
def test_proof_requires_exact_owner_and_target(txt_owner, target, expected):
    def query(request):
        if request.url.params["type"] == "TXT":
            answer = {"name": txt_owner, "type": 16, "data": '"challenge"'}
        else:
            answer = {"name": "login.example.net.", "type": 5, "data": target}
        return httpx.Response(200, json={"Status": 0, "Answer": [answer]})

    verifier = DnsDomainOwnershipVerifier("https://dns.example.org/query", transport=httpx.MockTransport(query))
    assert verifier.verify(hostname="login.example.net", record_name="_proof.login.example.net",
                           proof="challenge", cname_target="edge.example.org") is expected


def test_resolver_failure_fails_closed():
    verifier = DnsDomainOwnershipVerifier("https://dns.example.org/query",
                                          transport=httpx.MockTransport(lambda request: httpx.Response(503)))
    with pytest.raises(DomainProofUnavailable):
        verifier.verify(hostname="login.example.net", record_name="_proof.login.example.net",
                        proof="challenge", cname_target="edge.example.org")
