from tba_provider_security_proof_dns_domain import DnsDomainOwnershipVerifier


def verify_claim(verifier: DnsDomainOwnershipVerifier, proof: str) -> bool:
    return verifier.verify(
        hostname="login.customer.example",
        record_name="_privpw.login.customer.example",
        proof=proof,
        cname_target="edge.provider.example",
    )
