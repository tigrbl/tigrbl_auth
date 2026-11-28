from tba_bases_attestation import AttestationEvidenceBase
from tba_bases_digital_credential import CredentialFormatBase, PresentationFormatBase
from tba_concrete_eat_evidence import EatEvidence
from tba_concrete_mdoc_credential import MdocCredential
from tba_concrete_sd_jwt import SdJwtSerialization
from tba_concrete_sd_jwt_vc_credential import SdJwtVcCredential
from tba_concrete_verifiable_credential import VerifiableCredential
from tba_concrete_verifiable_presentation import VerifiablePresentation


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
