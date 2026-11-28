from tba_protocol_dmarc import discover_policy


def inspect_dmarc(*, dns):
    """Supply caller-owned integration inputs; this definition does not execute a deployment."""
    result = discover_policy(dns, "mail.example.com")
    print(result.status.value, result.policy_source, result.effective_policy)
