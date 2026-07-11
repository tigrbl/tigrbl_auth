from __future__ import annotations


def test_all_concrete_implementations_inherit_05_bases() -> None:
    import tigrbl_authz_policy_attributes_mapping as attributes
    import tigrbl_authz_policy_combiner_default as combining
    import tigrbl_authz_policy_evaluators_default as evaluators
    import tigrbl_authz_policy_obligations_concrete as obligations
    import tigrbl_authz_policy_rules_concrete as rules
    import tigrbl_identity_credentials_concrete as credentials
    import tigrbl_identity_identities_concrete as identities
    import tigrbl_oauth_scope_matcher as oauth
    import tigrbl_oidc_claims_concrete as claims
    import tigrbl_oidc_subject_strategy as subjects
    from tigrbl_authz_policy_bases import (
        AdviceHandlerBase,
        AttributeResolverBase,
        AttributeSelectorBase,
        ConditionEvaluatorBase,
        ObligationHandlerBase,
        PolicyCombinerBase,
        PolicyRuleBase,
        RuleEvaluatorBase,
    )
    from tigrbl_identity_model_bases import CredentialBase, IdentityBase
    from tigrbl_oauth_bases import ScopeMatcherBase
    from tigrbl_oidc_bases import ClaimsProviderBase, SubjectIdentifierStrategyBase

    groups = {
        IdentityBase: [getattr(identities, name) for name in identities.__all__],
        CredentialBase: [getattr(credentials, name) for name in credentials.__all__],
        PolicyRuleBase: [getattr(rules, name) for name in rules.__all__],
        AttributeResolverBase: [attributes.MappingAttributeResolver],
        AttributeSelectorBase: [attributes.MappingAttributeSelector],
        PolicyCombinerBase: [combining.DefaultPolicyCombiner],
        ConditionEvaluatorBase: [evaluators.DefaultConditionEvaluator],
        RuleEvaluatorBase: [evaluators.DefaultRuleEvaluator],
        ObligationHandlerBase: [obligations.NoopObligationHandler, obligations.CollectingObligationHandler],
        AdviceHandlerBase: [obligations.NoopAdviceHandler, obligations.CollectingAdviceHandler],
        ScopeMatcherBase: [oauth.DefaultScopeMatcher],
        ClaimsProviderBase: [claims.LocalClaimsProvider],
        SubjectIdentifierStrategyBase: [subjects.PublicSubjectStrategy, subjects.PairwiseSubjectStrategy],
    }
    for base, implementations in groups.items():
        for implementation in implementations:
            assert issubclass(implementation, base), implementation.__name__
