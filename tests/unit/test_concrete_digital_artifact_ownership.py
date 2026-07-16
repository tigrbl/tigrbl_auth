from tigrbl_attestation_bases import AttestationEvidenceBase
from tigrbl_digital_credential_bases import CredentialFormatBase, PresentationFormatBase
from tigrbl_eat_evidence_concrete import EatEvidence
from tigrbl_mdoc_credential_concrete import MdocCredential
from tigrbl_sd_jwt_concrete import SdJwtSerialization
from tigrbl_sd_jwt_vc_credential_concrete import SdJwtVcCredential
from tigrbl_verifiable_credential_concrete import VerifiableCredential
from tigrbl_verifiable_presentation_concrete import VerifiablePresentation


def test_standalone_digital_artifacts_inherit_canonical_bases() -> None:
    assert issubclass(MdocCredential, CredentialFormatBase)
    assert issubclass(SdJwtVcCredential, CredentialFormatBase)
    assert issubclass(VerifiableCredential, CredentialFormatBase)
    assert issubclass(VerifiablePresentation, PresentationFormatBase)
    assert issubclass(EatEvidence, AttestationEvidenceBase)


def test_sd_jwt_vc_credential_is_protocol_revision_neutral() -> None:
    credential = SdJwtVcCredential(
        SdJwtSerialization("a.b.c", ("disclosure",)),
        {"typ": "dc+sd-jwt"},
        {"iss": "https://issuer.example"},
    )
    assert credential.format_identifier == "dc+sd-jwt"
    assert credential.disclosures == ("disclosure",)


def test_eat_evidence_requires_profile_and_claims() -> None:
    evidence = EatEvidence.from_claims(
        "https://profile.example/eat", {"ueid": "device"}, "a.b.c"
    )
    assert evidence.profile == "https://profile.example/eat"
    assert evidence.claims["ueid"] == "device"
