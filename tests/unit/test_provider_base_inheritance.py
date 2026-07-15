from __future__ import annotations

import importlib


PROVIDER_BASES = {
    "tigrbl_authenticator_api_key_local.ApiKeyLocalAuthenticator": "tigrbl_identity_authenticator_bases.AuthenticatorBase",
    "tigrbl_authenticator_client_secret_local.ClientSecretLocalAuthenticator": "tigrbl_identity_authenticator_bases.AuthenticatorBase",
    "tigrbl_authenticator_dpop_proof.DpopProofAuthenticator": "tigrbl_identity_authenticator_bases.AuthenticatorBase",
    "tigrbl_authenticator_federated_oidc.FederatedOidcAuthenticator": "tigrbl_identity_authenticator_bases.AuthenticatorBase",
    "tigrbl_authenticator_mtls_client_cert.MtlsClientCertAuthenticator": "tigrbl_identity_authenticator_bases.AuthenticatorBase",
    "tigrbl_authenticator_otp_local.OtpLocalAuthenticator": "tigrbl_identity_authenticator_bases.ChallengeAuthenticatorBase",
    "tigrbl_authenticator_password_local.PasswordLocalAuthenticator": "tigrbl_identity_authenticator_bases.AuthenticatorBase",
    "tigrbl_authenticator_recovery_code_local.RecoveryCodeLocalAuthenticator": "tigrbl_identity_authenticator_bases.AuthenticatorBase",
    "tigrbl_authenticator_remote_introspection.RemoteIntrospectionAuthenticator": "tigrbl_identity_authenticator_bases.AuthenticatorBase",
    "tigrbl_authenticator_service_key_local.ServiceKeyLocalAuthenticator": "tigrbl_identity_authenticator_bases.AuthenticatorBase",
    "tigrbl_authenticator_session_local.SessionLocalAuthenticator": "tigrbl_identity_authenticator_bases.AuthenticatorBase",
    "tigrbl_authz_resource_server_verifier.ResourceServerVerifier": "tigrbl_resource_server_bases.ResourceServerVerifierBase",
    "tigrbl_security_authorization_provenance_builder.DeterministicProvenanceArtifactBuilder": "tigrbl_security_provenance_bases.ProvenanceArtifactBuilderBase",
    "tigrbl_identity_jose.JWTCoder": "tigrbl_jose_bases.JwtCoderBase",
    "tigrbl_identity_jose.JoseKeySet": "tigrbl_jose_bases.JoseKeySetBase",
    "tigrbl_identity_jose.JWEPolicy": "tigrbl_jose_bases.JwePolicyBase",
    "tigrbl_identity_jose.KeyRotationPolicyGovernance": "tigrbl_jose_bases.KeyRotationPolicyBase",
    "tigrbl_identity_jose.KeyRotationAdministration": "tigrbl_jose_bases.KeyRotationAdministrationBase",
    "tigrbl_security_auth_context_acr_basic.BasicAcrEvaluator": "tigrbl_security_trust_domain_bases.AcrEvaluatorBase",
    "tigrbl_security_auth_context_amr_basic.BasicAmrEvaluator": "tigrbl_security_trust_domain_bases.AmrEvaluatorBase",
    "tigrbl_security_certificate_mtls.MtlsBindingValidator": "tigrbl_security_trust_domain_bases.CertificateServiceDomainBase",
    "tigrbl_security_claims_provider_local.LocalSecurityClaimsProvider": "tigrbl_identity_claims_bases.ClaimsProviderBase",
    "tigrbl_security_dpop_cnf_binding_validator.DpopCnfBindingValidator": "tigrbl_security_trust_domain_bases.ConfirmationBindingValidatorBase",
    "tigrbl_security_mtls_cnf_binding_validator.MtlsCnfBindingValidator": "tigrbl_security_trust_domain_bases.ConfirmationBindingValidatorBase",
    "tigrbl_security_oidc_federation_provider.StaticOidcFederationProvider": "tigrbl_security_trust_domain_bases.OidcFederationProviderBase",
    "tigrbl_security_proof_dpop.DpopBindingValidator": "tigrbl_security_trust_domain_bases.ProofOfPossessionDomainBase",
    "tigrbl_security_proof_pkce.PkceProofProvider": "tigrbl_security_trust_domain_bases.ProofOfPossessionDomainBase",
    "tigrbl_security_sender_constraint_validator.SenderConstraintValidator": "tigrbl_security_trust_domain_bases.SenderConstraintValidatorBase",
    "tigrbl_security_signing_pqc.PQCSigningProvider": "tigrbl_security_trust_domain_bases.SigningProviderBase",
    "tigrbl_security_subject_pairwise_provider.PairwiseSubjectProvider": "tigrbl_security_trust_domain_bases.SubjectIdentifierStrategyBase",
    "tigrbl_security_token_introspection_client.IntrospectionClient": "tigrbl_security_trust_domain_bases.TokenIntrospectionClientBase",
    "tigrbl_security_token_jwks_cache.JWKSCache": "tigrbl_security_trust_domain_bases.VerificationKeyCacheBase",
    "tigrbl_security_webfinger_provider.WebFingerProvider": "tigrbl_security_trust_domain_bases.WebFingerResolverBase",
}


def _load(qualified_name: str) -> type:
    module_name, name = qualified_name.rsplit(".", 1)
    return getattr(importlib.import_module(module_name), name)


def test_exceptional_and_authenticator_providers_inherit_05_bases() -> None:
    for provider_name, base_name in PROVIDER_BASES.items():
        assert issubclass(_load(provider_name), _load(base_name)), provider_name
