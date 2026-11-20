import pytest
from tba_profile_credential_vc_jose_cose import select_format, validate_jose_vc


def test_vc_profile_rejects_legacy_nested_vc_claim() -> None:
    with pytest.raises(ValueError, match="legacy vc and vp"):
        validate_jose_vc(
            {"alg": "EdDSA", "typ": "vc+jwt"},
            {"vc": {"type": ["VerifiableCredential"]}},
        )


def test_vc_profile_does_not_advertise_unimplemented_presentations() -> None:
    with pytest.raises(ValueError, match="unsupported VC-JOSE-COSE media type"):
        select_format("application/vp+jwt")
