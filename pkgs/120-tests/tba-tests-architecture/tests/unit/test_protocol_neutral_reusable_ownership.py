from tba_protocol_oauth.reusable_components import ScopeSetMatcher
from tba_protocol_oidc.reusable_components import (
    EapAcrValue,
    LocalClaimsProvider,
    PairwiseSubjectIdentifierStrategy,
    PublicSubjectIdentifierStrategy,
    parse_verified_claims,
)
from tba_concrete_authorization_scope_set_matcher import ScopeSetMatcher as NeutralScopeSetMatcher
from tba_concrete_pairwise_subject_identifier import PairwiseSubjectIdentifierStrategy as NeutralPairwiseStrategy


def test_protocol_packages_compose_protocol_neutral_concretes() -> None:
    assert (
        ScopeSetMatcher.__module__ == "tba_concrete_authorization_scope_set_matcher"
    )
    assert LocalClaimsProvider.__module__ == "tba_provider_claims_local"
    assert (
        PublicSubjectIdentifierStrategy.__module__
        == "tba_concrete_public_subject_identifier"
    )
    assert (
        PairwiseSubjectIdentifierStrategy.__module__
        == "tba_concrete_pairwise_subject_identifier"
    )
    assert parse_verified_claims.__module__ == "tba_concrete_identity_assurance"


def test_protocol_composition_uses_neutral_owners_directly() -> None:
    assert NeutralScopeSetMatcher is ScopeSetMatcher
    assert NeutralPairwiseStrategy is PairwiseSubjectIdentifierStrategy
    assert EapAcrValue.__module__ == "tba_contracts_identity.oidc.eap_acr"
