from tigrbl_auth_protocol_oauth.reusable_components import ScopeSetMatcher
from tigrbl_auth_protocol_oidc.reusable_components import (
    LocalClaimsProvider,
    PairwiseSubjectIdentifierStrategy,
    PublicSubjectIdentifierStrategy,
    parse_verified_claims,
)
from tigrbl_oauth_scope_matcher import DefaultScopeMatcher
from tigrbl_oidc_claims_concrete import EapAcrValue
from tigrbl_oidc_subject_strategy import PairwiseSubjectStrategy


def test_protocol_packages_compose_protocol_neutral_concretes() -> None:
    assert ScopeSetMatcher.__module__ == "tigrbl_authorization_scope_set_matcher_concrete"
    assert LocalClaimsProvider.__module__ == "tigrbl_local_claims_provider_concrete"
    assert PublicSubjectIdentifierStrategy.__module__ == "tigrbl_public_subject_identifier_concrete"
    assert PairwiseSubjectIdentifierStrategy.__module__ == "tigrbl_pairwise_subject_identifier_concrete"
    assert parse_verified_claims.__module__ == "tigrbl_identity_assurance_concrete"


def test_old_domain_named_packages_are_compatibility_facades() -> None:
    assert DefaultScopeMatcher is ScopeSetMatcher
    assert PairwiseSubjectStrategy is PairwiseSubjectIdentifierStrategy
    assert EapAcrValue.__module__ == "tigrbl_eap_acr_concrete"
