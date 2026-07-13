import pytest

from tigrbl_claim_subject_concrete import SubjectClaim
from tigrbl_identity_claims_bases import ClaimSetComposerBase
from tigrbl_identity_contracts.claims import Claim, ClaimDisclosure, ClaimProvenance
from tigrbl_identity_core import (
    ClaimDisclosureMode,
    ClaimIdentifier,
    ClaimNameKind,
    ClaimSourceKind,
    ClaimType,
    ClaimValueType,
)
from tigrbl_identity_storage.tables.claim_state import (
    ClaimDefinition,
    ClaimProvenanceRecord,
    ClaimReleasePolicy,
    ClaimSnapshot,
    ClaimSourceBinding,
)


class Composer(ClaimSetComposerBase):
    pass


def test_claim_identifier_supports_json_cwt_and_mdoc_forms():
    assert ClaimIdentifier("sub", ClaimNameKind.REGISTERED).label == "sub"
    assert ClaimIdentifier(2, ClaimNameKind.INTEGER_LABEL).label == 2
    assert (
        ClaimIdentifier(
            "family_name",
            ClaimNameKind.NAMESPACED,
            "org.iso.18013.5.1",
        ).namespace
        == "org.iso.18013.5.1"
    )
    with pytest.raises(ValueError):
        ClaimIdentifier("2", ClaimNameKind.INTEGER_LABEL)
    with pytest.raises(ValueError):
        ClaimIdentifier("family_name", ClaimNameKind.NAMESPACED)


def test_claim_carries_provenance_and_disclosure_without_protocol_ownership():
    claim = Claim(
        "family_name",
        "Doe",
        ClaimType.IDENTITY,
        ClaimValueType.STRING,
        provenance=ClaimProvenance(ClaimSourceKind.CREDENTIAL, source_id="cred-1"),
        disclosure=ClaimDisclosure(ClaimDisclosureMode.CONSENTED, purpose="age check"),
    )
    assert claim.identifier.label == "family_name"
    assert claim.provenance.source_id == "cred-1"
    assert claim.disclosure.mode is ClaimDisclosureMode.CONSENTED


def test_claim_set_base_requires_version_and_rejects_duplicates():
    composer = Composer()
    subject = SubjectClaim("alice")
    assert composer.compose((subject,), protocol="jwt", version="RFC7519").claims == (
        subject,
    )
    with pytest.raises(ValueError):
        composer.compose((subject,), protocol="jwt", version="")
    with pytest.raises(ValueError):
        composer.compose((subject, SubjectClaim("bob")), protocol="jwt", version="RFC7519")


def test_storage_owns_private_claim_configuration_not_standard_semantics():
    assert {model.__tablename__ for model in (
        ClaimDefinition,
        ClaimSourceBinding,
        ClaimReleasePolicy,
        ClaimProvenanceRecord,
        ClaimSnapshot,
    )} == {
        "claim_definitions",
        "claim_source_bindings",
        "claim_release_policies",
        "claim_provenance_records",
        "claim_snapshots",
    }
    assert not hasattr(ClaimSnapshot, "value")
    assert hasattr(ClaimSnapshot, "protected_artifact_locator")
