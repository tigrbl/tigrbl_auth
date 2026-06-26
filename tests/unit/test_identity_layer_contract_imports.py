from __future__ import annotations

import importlib


def test_authorization_server_table_and_schema_exports() -> None:
    storage_tables = importlib.import_module("tigrbl_identity_storage.tables")
    storage_schemas = importlib.import_module("tigrbl_identity_storage.schemas")
    contract_schemas = importlib.import_module("tigrbl_identity_contracts.schemas")

    assert storage_tables.AuthorizationServer.__name__ == "AuthorizationServer"
    assert storage_tables.TABLE_MODEL_BY_NAME["AuthorizationServer"] is (
        storage_tables.AuthorizationServer
    )

    schema_names = (
        "AuthorizationServerCreateRequest",
        "AuthorizationServerReadResponse",
        "AuthorizationServerUpdateRequest",
    )
    for name in schema_names:
        assert getattr(contract_schemas, name) is getattr(storage_schemas, name)


def test_policy_repository_table_contract_and_runtime_exports() -> None:
    storage_tables = importlib.import_module("tigrbl_identity_storage.tables")
    storage_schemas = importlib.import_module("tigrbl_identity_storage.schemas")
    contract_schemas = importlib.import_module("tigrbl_identity_contracts.schemas")
    policy_contracts = importlib.import_module("tigrbl_identity_contracts.policy")
    runtime = importlib.import_module("tigrbl_identity_storage_runtime.policy_repository")

    for table_name in (
        "Policy",
        "PolicyVersion",
        "PolicySet",
        "PolicySetMember",
        "PolicyTarget",
    ):
        assert getattr(storage_tables, table_name).__name__ == table_name
        assert storage_tables.TABLE_MODEL_BY_NAME[table_name] is getattr(storage_tables, table_name)

    schema_names = (
        "PolicyCreateRequest",
        "PolicyReadResponse",
        "PolicyUpdateRequest",
        "PolicyVersionCreateRequest",
        "PolicySetCreateRequest",
        "PolicySetMemberCreateRequest",
        "PolicyTargetCreateRequest",
    )
    for name in schema_names:
        assert getattr(contract_schemas, name) is getattr(storage_schemas, name)

    for name in (
        "PolicyAdministrationPointPort",
        "PolicyRetrievalPointPort",
        "PolicySetRepositoryPort",
        "TargetMatcherPort",
    ):
        assert hasattr(policy_contracts, name)

    assert hasattr(runtime, "StoragePolicyRepository")


def test_oauth_contracts_use_storage_schema_lineage() -> None:
    oauth = importlib.import_module("tigrbl_identity_contracts.oauth")
    schemas = importlib.import_module("tigrbl_identity_contracts.schemas")

    assert oauth.ConsentCreateRequest is schemas.ConsentCreateRequest
    assert oauth.RefreshIn is schemas.RefreshIn
    assert oauth.RevocationIn is schemas.RevocationIn
    assert oauth.AuthorizationServerReadResponse is schemas.AuthorizationServerReadResponse

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

    importlib.import_module("tigrbl_oauth_scope_matcher")
    importlib.import_module("tigrbl_oidc_claims_concrete")
    importlib.import_module("tigrbl_oidc_subject_strategy")
    importlib.import_module("tigrbl_security_auth_context_acr_basic")
    importlib.import_module("tigrbl_security_auth_context_amr_basic")
    importlib.import_module("tigrbl_security_claims_provider_local")
    importlib.import_module("tigrbl_security_oidc_federation_provider")
    importlib.import_module("tigrbl_security_subject_pairwise_provider")
    importlib.import_module("tigrbl_security_webfinger_provider")
