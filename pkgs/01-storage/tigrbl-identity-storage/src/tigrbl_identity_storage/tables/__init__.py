'Persistence models and engine exports for the Tigrbl-native package tree.'

from tigrbl import bind

from ._registry import *  # noqa: F401,F403
from ._registry import _CLIENT_ID_RE, _TABLE_MODELS

TABLE_MODELS = _TABLE_MODELS
TABLE_MODEL_BY_NAME = {model.__name__: model for model in TABLE_MODELS}
TABLE_MODEL_BY_TABLENAME = {model.__tablename__: model for model in TABLE_MODELS}


def _ensure_runtime_bindings() -> None:
    """Materialize model handlers/schemas through Tigrbl's public bind API."""

    for model in _TABLE_MODELS:
        handlers = getattr(model, "handlers", None)
        if getattr(handlers, "read", None) is None:
            bind(model)


def _attach_custom_op_schemas() -> None:
    set_schema(TokenRecord, "token", in_=None, out=TokenPair)
    set_schema(TokenRecord, "authorization_code_grant", in_=AuthorizationCodeGrantForm, out=TokenPair)
    set_schema(TokenRecord, "password_grant", in_=PasswordGrantForm, out=TokenPair)
    set_schema(TokenRecord, "refresh", in_=RefreshIn, out=TokenPair)
    set_schema(TokenRecord, "introspect", out=IntrospectOut)

    set_schema(ClientRegistration, "register", in_=DynamicClientRegistrationIn, out=DynamicClientRegistrationOut)
    set_schema(ClientRegistration, "register_get", out=DynamicClientRegistrationOut)
    set_schema(
        ClientRegistration,
        "register_put",
        in_=DynamicClientRegistrationManagementIn,
        out=DynamicClientRegistrationOut,
    )
    set_schema(ClientRegistration, "register_delete", out=dict)

    set_schema(DeviceCode, "device_authorization", in_=DeviceAuthorizationIn, out=DeviceAuthorizationOut)
    set_schema(PushedAuthorizationRequest, "par", in_=PushedAuthorizationRequestIn, out=PushedAuthorizationResponse)
    set_schema(RevokedToken, "revoke", in_=RevocationIn, out=RevocationOut)
    set_schema(LogoutState, "logout", in_=LogoutIn, out=LogoutOut)



_ensure_runtime_bindings()
_attach_custom_op_schemas()

__all__ = [
    "RestOltpTable",
    "ENGINE",
    "dsn",
    "get_db",
    "TABLE_MODELS",
    "TABLE_MODEL_BY_NAME",
    "TABLE_MODEL_BY_TABLENAME",
    "Tenant",
    "Realm",
    "User",
    "Client",
    "_CLIENT_ID_RE",
    "ClientRegistration",
    "AuthorizationServer",
    "Principal",
    "ServiceIdentity",
    "MachineIdentity",
    "WorkloadIdentity",
    "CredentialApiKey",
    "CredentialServiceKey",
    "Credential",
    "CredentialAuditEvent",
    "CredentialClientSecret",
    "CredentialDpopKey",
    "CredentialMfaFactor",
    "CredentialMtlsCertificate",
    "CredentialPassword",
    "CredentialRecoveryCode",
    "CredentialWebAuthnPasskey",
    "CryptoKey",
    "CryptoKeyVersion",
    "PrincipalKeyBinding",
    "KeyEnvelope",
    "KeyAttestationEvidence",
    "CredentialIssuer",
    "CredentialConfiguration",
    "WalletRegistration",
    "WalletInstance",
    "WalletAttestation",
    "WalletKeyBinding",
    "CredentialOffer",
    "CredentialIssuanceTransaction",
    "CredentialDeferredTransaction",
    "CredentialNotification",
    "CredentialStatusList",
    "CredentialStatusEntry",
    "CredentialStatusPublication",
    "VerifierRegistration",
    "PresentationTransaction",
    "PresentationConsent",
    "PresentationReplay",
    "AttestationEvidence",
    "AttestationResult",
    "AttestationReferenceManifest",
    "AttestationReferenceValue",
    "AttestationEndorsement",
    "AttestationAppraisalPolicy",
    "SvidRecord",
    "SpiffeTrustBundle",
    "TrustDomainFederation",
    "SecurityEvent",
    "SecurityEventSubscription",
    "SecurityEventDelivery",
    "SecurityEventReplay",
    "ReplayReservation",
    "DidDocument",
    "DidDocumentVersion",
    "DidVerificationMethod",
    "DidService",
    "DidResolutionCache",
    "GnapGrant",
    "GnapContinuation",
    "GnapClientInstance",
    "GnapInteraction",
    "CertificateRecord",
    "TrustAnchor",
    "CertificateStatusSnapshot",
    "ClaimDefinition",
    "ClaimSourceBinding",
    "ClaimReleasePolicy",
    "ClaimProvenanceRecord",
    "ClaimSnapshot",
    "AuthSession",
    "AuthCode",
    "DeviceCode",
    "RevokedToken",
    "TokenRecord",
    "DelegationGrantEdge",
    "DelegationGrantProof",
    "DelegationGrant",
    "DelegationGrantRecord",
    "DelegationGrantScope",
    "DelegationGrantTokenLink",
    "PushedAuthorizationRequest",
    "Consent",
    "AuditEvent",
    "LogoutState",
    "BackchannelLogoutReplay",
    "AuthenticationChallenge",
    "DpopReplay",
    "DpopNonce",
    "KeyRotationEvent",
    "KeyRotationPolicy",
    "TenantMembership",
    "SubjectAlias",
    "Role",
    "AttributePolicy",
    "PolicyCondition",
    "Policy",
    "PolicyVersion",
    "PolicySet",
    "PolicySetMember",
    "PolicyTarget",
    "DelegatedAdminScope",
    "Entitlement",
    "EntitlementAssignment",
    "AccessReviewCampaign",
    "AccessReviewItem",
    "AccessReviewDecision",
    "ResidencyZone",
    "TenantResidency",
    "SDKPackageRecord",
    "PluginDescriptorRecord",
    "PluginLifecycleEventRecord",
    "ScimSchemaRecord",
    "ScimUserRecord",
    "ScimGroupRecord",
    "ScimPatchEvent",
    "ReleaseCapabilityRecord",
    "ReleaseAuthorizationState",
    "RuntimeQualificationRecord",
    "ReleaseSecurityPosture",
    "ReleasePosture",
    "ReleaseAttestationEvent",
    "ControlCorrectnessReport",
    "AuthzVerificationReport",
    "ResourceServerContract",
    "ProviderArtifact",
    "IdentityProvider",
    "Federation",
    "FederatedSession",
    "AuthorizationInvariant",
    "InvariantEvaluation",
    "InvariantViolation",
    "AuthorityDerivationGraph",
    "AuthorityDerivationGraphNode",
    "AuthorityDerivationGraphEdge",
    "TrustFederationGraph",
    "TrustFederationGraphNode",
    "TrustFederationGraphEdge",
    "OperatorMetadata",
    "OperatorRecord",
    "OperatorTransaction",
    "OperatorAuditEvent",
    "OperatorActivity",
]
__all__ = list(dict.fromkeys(__all__))
