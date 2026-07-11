from __future__ import annotations


def _explicitly_inherits(base: type, contract: type) -> bool:
    return contract in base.__mro__[1:]


def test_authenticator_bases_explicitly_inherit_contracts() -> None:
    from tigrbl_identity_authenticator_bases import AuthenticatorBase, ChallengeAuthenticatorBase
    from tigrbl_identity_contracts.authenticators import IAuthenticator, IChallengeAuthenticator

    assert _explicitly_inherits(AuthenticatorBase, IAuthenticator)
    assert _explicitly_inherits(ChallengeAuthenticatorBase, IChallengeAuthenticator)


def test_security_bases_explicitly_inherit_contracts() -> None:
    import tigrbl_security_trust_contracts as contracts
    import tigrbl_security_trust_domain_bases as bases

    expected = {
        "CapabilityProviderBase": "ICapabilityProvider",
        "ArtifactCodecBase": "IArtifactCodec",
        "ArtifactIssuerBase": "IArtifactIssuer",
        "ArtifactVerifierBase": "IArtifactVerifier",
        "ArtifactOpenerBase": "IArtifactOpener",
        "RecipientSetEditorBase": "IRecipientSetEditor",
        "SigningProviderBase": "ISigningProvider",
        "PkceVerifierBase": "IPkceVerifier",
        "AcrEvaluatorBase": "IAcrEvaluator",
        "AmrEvaluatorBase": "IAmrEvaluator",
        "KeyResolverBase": "IKeyResolver",
        "KeyLifecycleProviderBase": "IKeyLifecycleProvider",
        "EncryptionProviderBase": "IEncryptionProvider",
        "KeyWrappingProviderBase": "IKeyWrappingProvider",
        "KeyEncapsulationProviderBase": "IKeyEncapsulationProvider",
        "AttestationProviderBase": "IAttestationProvider",
        "PublicKeyExporterBase": "IPublicKeyExporter",
        "CipherPolicyDomainBase": "ICipherPolicy",
        "ConfirmationBindingValidatorBase": "IConfirmationBindingValidator",
        "SenderConstraintValidatorBase": "ISenderConstraintValidator",
        "VerificationKeyResolverBase": "IVerificationKeyResolver",
        "VerificationKeyCacheBase": "IVerificationKeyCache",
        "TokenIntrospectionClientBase": "ITokenIntrospectionClient",
    }
    for base_name, contract_name in expected.items():
        assert _explicitly_inherits(
            getattr(bases, base_name), getattr(contracts, contract_name)
        ), base_name


def test_domain_bases_explicitly_inherit_identity_contracts() -> None:
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
    from tigrbl_identity_contracts import Credential, Identity
    from tigrbl_identity_contracts.policy import (
        AdviceHandlerPort,
        AttributeResolverPort,
        AttributeSelectorPort,
        ConditionEvaluatorPort,
        ObligationHandlerPort,
        PolicyCombinerPort,
        PolicyRule,
        RuleEvaluatorPort,
    )
    from tigrbl_identity_model_bases import CredentialBase, IdentityBase
    from tigrbl_oauth_bases import ScopeMatcherBase
    from tigrbl_identity_contracts.oauth import ScopeMatcherPort

    pairs = (
        (IdentityBase, Identity),
        (CredentialBase, Credential),
        (PolicyRuleBase, PolicyRule),
        (AttributeResolverBase, AttributeResolverPort),
        (AttributeSelectorBase, AttributeSelectorPort),
        (PolicyCombinerBase, PolicyCombinerPort),
        (ConditionEvaluatorBase, ConditionEvaluatorPort),
        (RuleEvaluatorBase, RuleEvaluatorPort),
        (ObligationHandlerBase, ObligationHandlerPort),
        (AdviceHandlerBase, AdviceHandlerPort),
        (ScopeMatcherBase, ScopeMatcherPort),
    )
    for base, contract in pairs:
        assert _explicitly_inherits(base, contract), base.__name__
