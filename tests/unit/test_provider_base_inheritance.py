from __future__ import annotations

import importlib


PROVIDER_BASES = {
    "tba_provider_authenticator_api_key_local.ApiKeyLocalAuthenticator": "tba_bases_identity_authenticator.AuthenticatorBase",
    "tba_provider_authenticator_client_secret_local.ClientSecretLocalAuthenticator": "tba_bases_identity_authenticator.AuthenticatorBase",
    "tba_provider_authenticator_dpop_proof.DpopProofAuthenticator": "tba_bases_identity_authenticator.AuthenticatorBase",
    "tba_provider_authenticator_federated_oidc.FederatedOidcAuthenticator": "tba_bases_identity_authenticator.AuthenticatorBase",
    "tba_provider_authenticator_mtls_client_cert.MtlsClientCertAuthenticator": "tba_bases_identity_authenticator.AuthenticatorBase",
    "tba_provider_authenticator_otp_local.OtpLocalAuthenticator": "tba_bases_identity_authenticator.ChallengeAuthenticatorBase",
    "tba_provider_authenticator_password_local.PasswordLocalAuthenticator": "tba_bases_identity_authenticator.AuthenticatorBase",
    "tba_provider_authenticator_recovery_code_local.RecoveryCodeLocalAuthenticator": "tba_bases_identity_authenticator.AuthenticatorBase",
    "tba_provider_authenticator_remote_introspection.RemoteIntrospectionAuthenticator": "tba_bases_identity_authenticator.AuthenticatorBase",
    "tba_provider_authenticator_service_key_local.ServiceKeyLocalAuthenticator": "tba_bases_identity_authenticator.AuthenticatorBase",
    "tba_provider_authenticator_session_local.SessionLocalAuthenticator": "tba_bases_identity_authenticator.AuthenticatorBase",
    "tba_provider_authorization_resource_server_verifier.ResourceServerVerifier": "tba_bases_resource_server.ResourceServerVerifierBase",
    "tba_concrete_authorization_provenance.DeterministicProvenanceArtifactBuilder": "tba_bases_security_provenance.ProvenanceArtifactBuilderBase",
    "tba_provider_identity_jose.JWTCoder": "tba_bases_jose.JwtCoderBase",
    "tba_provider_identity_jose.JoseKeySet": "tba_bases_jose.JoseKeySetBase",
    "tba_provider_identity_jose.JWEPolicy": "tba_bases_jose.JwePolicyBase",
    "tba_provider_identity_jose.KeyRotationPolicyGovernance": "tba_bases_jose.KeyRotationPolicyBase",
    "tba_provider_identity_jose.KeyRotationAdministration": "tba_bases_jose.KeyRotationAdministrationBase",
    "tba_concrete_acr_evaluator_basic.BasicAcrEvaluator": "tba_bases_authentication_context.AcrEvaluatorBase",
    "tba_concrete_amr_evaluator_basic.BasicAmrEvaluator": "tba_bases_authentication_context.AmrEvaluatorBase",
    "tba_concrete_mtls_confirmation_binding.MtlsBindingValidator": "tba_bases_security_trust_domain.CertificateServiceDomainBase",
    "tba_provider_claims_local.LocalSecurityClaimsProvider": "tba_bases_identity_claims.ClaimsProviderBase",
    "tba_concrete_dpop_confirmation_binding.DpopCnfBindingValidator": "tba_bases_security_trust_domain.ConfirmationBindingValidatorBase",
    "tba_concrete_mtls_confirmation_binding.MtlsCnfBindingValidator": "tba_bases_security_trust_domain.ConfirmationBindingValidatorBase",
    "tba_concrete_dpop_confirmation_binding.DpopBindingValidator": "tba_bases_security_trust_domain.ProofOfPossessionDomainBase",
    "tba_concrete_pkce.PkceProofProvider": "tba_bases_security_trust_domain.ProofOfPossessionDomainBase",
    "tba_provider_security_signing_pqc.PQCSigningProvider": "tba_bases_security_trust_domain.SigningProviderBase",
    "tba_concrete_pairwise_subject_identifier.PairwiseSubjectIdentifierStrategy": "tba_bases_identity_model.SubjectIdentifierStrategyBase",
    "tba_provider_token_introspection.IntrospectionClient": "tba_bases_security_trust_domain.TokenIntrospectionClientBase",
    "tba_provider_security_token_jwks_cache.JWKSCache": "tba_bases_security_trust_domain.VerificationKeyCacheBase",
}


def _load(qualified_name: str) -> type:
    module_name, name = qualified_name.rsplit(".", 1)
    return getattr(importlib.import_module(module_name), name)


def test_exceptional_and_authenticator_providers_inherit_05_bases() -> None:
    for provider_name, base_name in PROVIDER_BASES.items():
        assert issubclass(_load(provider_name), _load(base_name)), provider_name
