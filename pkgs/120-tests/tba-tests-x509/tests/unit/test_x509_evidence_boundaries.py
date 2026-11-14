import pytest

pytest.importorskip("asn1crypto")


from tba_codec_x509_logotype import decode_subject_logotype
from tba_provider_certificate_evidence import (
    PathValidationError,
    load_crls,
    verify_chain,
)

from tba_testkit_identity.mark_certificates import AT, LOGOTYPE, make_evidence


def test_logotype_codec_decodes_without_enforcing_bimi_logo_policy():
    leaf, *_ = make_evidence(corrupt_digest=True)
    logo = decode_subject_logotype(
        leaf.extensions.get_extension_for_oid(LOGOTYPE).value.value
    )
    assert logo is not None
    (image,) = logo.images
    assert image.media_type == "image/svg+xml"
    assert image.digests[0].digest == bytes(32)


def test_generic_evidence_verifier_exposes_revocation_without_bimi_policy():
    leaf, issuer, root, crls, _ = make_evidence(revoke_issuer=True, issuer_eku=False)
    chain = verify_chain(leaf, [issuer], [root], AT)
    assert chain == [leaf, issuer, root]
    evidence = load_crls(chain, crls.get, AT)
    with pytest.raises(PathValidationError) as error:
        verify_chain(leaf, [issuer], [root], AT, evidence)
    assert error.value.revoked
