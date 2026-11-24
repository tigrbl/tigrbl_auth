from tba_protocol_bimi import discover_assertion
from tba_protocol_dmarc import discover_policy


def inspect_bimi(*, dns):
    """Supply caller-owned integration inputs; this definition does not execute a deployment."""
    policy = discover_policy(dns, "mail.example.com")
    result = discover_assertion(
        dns, "mail.example.com", organizational_domain=policy.organizational_domain
    )
