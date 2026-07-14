from tigrbl_auth_protocol_oauth.reusable_components import ScopeSetMatcher
from tigrbl_auth_protocol_oidc.reusable_components import (
    EapAcrValue,
    LocalClaimsProvider,
    PairwiseSubjectIdentifierStrategy,
    PublicSubjectIdentifierStrategy,
    parse_verified_claims,
)
from tigrbl_authorization_scope_set_matcher_concrete import ScopeSetMatcher as NeutralScopeSetMatcher
from tigrbl_pairwise_subject_identifier_concrete import PairwiseSubjectIdentifierStrategy as NeutralPairwiseStrategy


def test_protocol_packages_compose_protocol_neutral_concretes() -> None:
    assert (
        ScopeSetMatcher.__module__ == "tigrbl_authorization_scope_set_matcher_concrete"
    )
    assert LocalClaimsProvider.__module__ == "tigrbl_security_claims_provider_local"
    assert (
        PublicSubjectIdentifierStrategy.__module__
        == "tigrbl_public_subject_identifier_concrete"
    )
    assert (
        PairwiseSubjectIdentifierStrategy.__module__
        == "tigrbl_pairwise_subject_identifier_concrete"
    )
    assert parse_verified_claims.__module__ == "tigrbl_identity_assurance_concrete"


def test_protocol_composition_uses_neutral_owners_directly() -> None:
    assert NeutralScopeSetMatcher is ScopeSetMatcher
    assert NeutralPairwiseStrategy is PairwiseSubjectIdentifierStrategy
    assert EapAcrValue.__module__ == "tigrbl_identity_contracts.oidc.eap_acr"
