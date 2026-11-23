from tba_provider_certificate_evidence import (
    load_crls,
    load_logs,
    verify_chain,
    verify_transparency,
)


def verify_certificate_evidence(
    *, at, ct_public_keys_pem, intermediates, leaf, local_crls_by_url, roots
):
    """Supply caller-owned integration inputs; this definition does not execute a deployment."""
    chain = verify_chain(leaf, intermediates, roots, at)
    crls = load_crls(chain, local_crls_by_url.get, at)
    verify_chain(leaf, chain[1:-1], chain[-1:], at, crls)
    verify_transparency(chain[0], chain[1], load_logs(ct_public_keys_pem), at)
