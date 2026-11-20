from tba_provider_security_cose import CoseSign1Provider


def test_cose_provider_refuses_to_claim_signing_or_verification_without_backends():
    provider = CoseSign1Provider()
    try:
        provider.sign1(b"payload", {1: -7})
    except RuntimeError:
        pass
    else:
        raise AssertionError("COSE signing succeeded without a backend")
