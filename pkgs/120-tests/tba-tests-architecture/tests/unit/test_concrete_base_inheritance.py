from __future__ import annotations


def test_all_concrete_implementations_inherit_05_bases() -> None:
    from inspect import isclass

    import tba_concrete_authorization_policy_attributes_mapping as attributes
    import tba_concrete_authorization_policy_combiner_default as combining
    import tba_concrete_authorization_policy_evaluators_default as evaluators
    import tba_concrete_authorization_policy_obligations as obligations
    import tba_concrete_authorization_policy_rules as rules
    import tigrbl_identity_credentials_concrete as credentials
    import tigrbl_identity_identities_concrete as identities
    import tba_concrete_authorization_scope_set_matcher as scopes
    import tba_provider_claims_local as claims
    import tba_concrete_pairwise_subject_identifier as pairwise_subjects
    import tba_concrete_public_subject_identifier as public_subjects
    from tba_bases_authorization_policy import (
        AdviceHandlerBase,
        AttributeResolverBase,
        AttributeSelectorBase,
        ConditionEvaluatorBase,
        ObligationHandlerBase,
        PolicyCombinerBase,
        PolicyRuleBase,
        RuleEvaluatorBase,
    )
    from tba_bases_identity_model import CredentialBase, IdentityBase
    from tba_bases_authorization_policy import ScopeMatcherBase
    from tba_bases_identity_claims import ClaimsProviderBase
    from tba_bases_digital_credential import CredentialFormatBase
    from tba_bases_identity_model import SubjectIdentifierStrategyBase

    groups = {
        IdentityBase: [getattr(identities, name) for name in identities.__all__],
        CredentialBase: [
            getattr(credentials, name)
            for name in credentials.__all__
            if name not in {"Mdoc", "SdJwtVc"} and isclass(getattr(credentials, name))
        ],
        CredentialFormatBase: [credentials.Mdoc, credentials.SdJwtVc],
        PolicyRuleBase: [getattr(rules, name) for name in rules.__all__],
        AttributeResolverBase: [attributes.MappingAttributeResolver],
        AttributeSelectorBase: [attributes.MappingAttributeSelector],
        PolicyCombinerBase: [combining.DefaultPolicyCombiner],
        ConditionEvaluatorBase: [evaluators.DefaultConditionEvaluator],
        RuleEvaluatorBase: [evaluators.DefaultRuleEvaluator],
        ObligationHandlerBase: [
            obligations.NoopObligationHandler,
            obligations.CollectingObligationHandler,
        ],
        AdviceHandlerBase: [
            obligations.NoopAdviceHandler,
            obligations.CollectingAdviceHandler,
        ],
        ScopeMatcherBase: [scopes.ScopeSetMatcher],
        ClaimsProviderBase: [claims.LocalClaimsProvider],
        SubjectIdentifierStrategyBase: [
            public_subjects.PublicSubjectIdentifierStrategy,
            pairwise_subjects.PairwiseSubjectIdentifierStrategy,
        ],
    }
    for base, implementations in groups.items():
        for implementation in implementations:
            assert issubclass(implementation, base), implementation.__name__
