from __future__ import annotations


def _explicitly_inherits(base: type, contract: type) -> bool:
    return contract in base.__mro__[1:]


def test_authenticator_bases_explicitly_inherit_contracts() -> None:
    from tba_bases_identity_authenticator import (
        AuthenticatorBase,
        ChallengeAuthenticatorBase,
    )
    from tba_contracts_identity.authenticators import (
        IAuthenticator,
        IChallengeAuthenticator,
    )

    assert _explicitly_inherits(AuthenticatorBase, IAuthenticator)
    assert _explicitly_inherits(ChallengeAuthenticatorBase, IChallengeAuthenticator)


def test_security_bases_explicitly_inherit_contracts() -> None:
    import tba_contracts_security_trust as contracts
    import tba_bases_security_trust_domain as bases

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
    from tba_contracts_identity import Credential, Identity
    from tba_contracts_identity.policy import (
        AdviceHandlerPort,
        AttributeResolverPort,
        AttributeSelectorPort,
        ConditionEvaluatorPort,
        ObligationHandlerPort,
        PolicyCombinerPort,
        PolicyRule,
        RuleEvaluatorPort,
    )
    from tba_bases_identity_model import CredentialBase, IdentityBase
    from tba_bases_authorization_policy import ScopeMatcherBase
    from tba_contracts_identity.oauth import ScopeMatcherPort

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
