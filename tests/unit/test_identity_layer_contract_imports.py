from __future__ import annotations

import importlib


def test_authorization_server_table_and_schema_exports() -> None:
    storage_tables = importlib.import_module("tigrbl_identity_storage.tables")
    oauth = importlib.import_module("tigrbl_identity_contracts.oauth")

    assert storage_tables.AuthorizationServer.__name__ == "AuthorizationServer"
    assert storage_tables.TABLE_MODEL_BY_NAME["AuthorizationServer"] is (
        storage_tables.AuthorizationServer
    )

    assert oauth.AuthorizationServerConfiguration.__module__.startswith(
        "tigrbl_identity_contracts"
    )
    assert oauth.AuthorizationServerPatch.__module__.startswith(
        "tigrbl_identity_contracts"
    )


def test_policy_table_contract_exports() -> None:
    storage_tables = importlib.import_module("tigrbl_identity_storage.tables")
    policy_contracts = importlib.import_module("tigrbl_identity_contracts.policy")

    for table_name in (
        "Policy",
        "PolicyVersion",
        "PolicySet",
        "PolicySetMember",
        "PolicyTarget",
    ):
        assert getattr(storage_tables, table_name).__name__ == table_name
        assert storage_tables.TABLE_MODEL_BY_NAME[table_name] is getattr(storage_tables, table_name)

    for name in (
        "PolicyAdministrationPointPort",
        "PolicyRetrievalPointPort",
        "PolicySetRepositoryPort",
        "TargetMatcherPort",
    ):
        assert hasattr(policy_contracts, name)


def test_oauth_contracts_own_protocol_neutral_semantic_records() -> None:
    oauth = importlib.import_module("tigrbl_identity_contracts.oauth")

    for name in (
        "AuthorizationServerConfiguration",
        "ConsentGrantRequest",
        "ConsentRecord",
        "IssuedTokenSet",
        "RefreshTokenRequest",
        "TokenRevocationRequest",
        "TokenRevocationResult",
    ):
        value = getattr(oauth, name)
        assert value.__module__.startswith("tigrbl_identity_contracts")

    for legacy_name in ("ConsentGrant", "ConsentDecision", "ConsentRevocation"):
        assert not hasattr(oauth, legacy_name)


def test_oidc_contract_surfaces_import_cleanly() -> None:
    oidc = importlib.import_module("tigrbl_identity_contracts.oidc")

    for name in (
        "ClaimsProviderPort",
        "DiscoveryPublisherPort",
        "FrontChannelLogoutPort",
        "IdTokenIssuerPort",
        "OpenIDProviderPort",
        "RelyingPartyPort",
        "RpInitiatedLogoutPort",
        "SessionServicePort",
        "SubjectIdentifierStrategyPort",
        "UserInfoProviderPort",
        "WebFingerResolverPort",
    ):
        assert hasattr(oidc, name)


def test_security_trust_contracts_bases_and_implementations_import_cleanly() -> None:
    trust_contracts = importlib.import_module("tigrbl_security_trust_contracts")
    trust_bases = importlib.import_module("tigrbl_security_trust_domain_bases")

    for name in ("IAcrEvaluator", "IAmrEvaluator", "IPkceVerifier"):
        assert hasattr(trust_contracts, name)
    for name in (
        "AcrEvaluatorBase",
        "AmrEvaluatorBase",
        "ClaimsProviderBase",
        "OidcFederationProviderBase",
        "PkceVerifierBase",
        "SubjectIdentifierStrategyBase",
        "WebFingerResolverBase",
    ):
        assert hasattr(trust_bases, name)

    importlib.import_module("tigrbl_authorization_scope_set_matcher_concrete")
    importlib.import_module("tigrbl_identity_assurance_concrete")
    importlib.import_module("tigrbl_pairwise_subject_identifier_concrete")
    importlib.import_module("tigrbl_security_auth_context_acr_basic")
    importlib.import_module("tigrbl_security_auth_context_amr_basic")
    importlib.import_module("tigrbl_security_claims_provider_local")
    importlib.import_module("tigrbl_security_oidc_federation_provider")
    importlib.import_module("tigrbl_security_subject_pairwise_provider")
    importlib.import_module("tigrbl_security_webfinger_provider")
