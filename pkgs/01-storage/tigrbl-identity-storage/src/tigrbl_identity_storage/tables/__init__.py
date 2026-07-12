"""Persistence models and engine exports for the Tigrbl-native package tree."""

from tigrbl import bind

from tigrbl_identity_storage.framework import RestOltpTable

from .realm import AdminRealmOut, AdminRealmProvisionIn, AdminRealmUpdateIn, Realm
from .tenant import AdminTenantOut, AdminTenantProvisionIn, AdminTenantUpdateIn, Tenant
from .user import (
    AdminIdentityOut,
    AdminIdentityProvisionIn,
    AdminIdentityUpdateIn,
    AdminPasswordChangeIn,
    AdminPasswordResetCompleteIn,
    AdminPasswordResetRequestIn,
    AdminSessionOut,
    CredsIn as AdminCredsIn,
    MyAccountMutationOut,
    MyAccountPasswordChangeIn,
    MyAccountProfileOut,
    MyAccountProfileUpdateIn,
    User,
)
from .client import Client, _CLIENT_ID_RE
from .client_registration import (
    ClientRegistration,
    DynamicClientRegistrationIn,
    DynamicClientRegistrationManagementIn,
    DynamicClientRegistrationOut,
)
from .authorization_server import AuthorizationServer
from .principal import Principal
from .service_identity import ServiceIdentity
from .machine_identity import MachineIdentity
from .workload_identity import WorkloadIdentity
from .credential_api_key import CredentialApiKey
from .credential_service_key import CredentialServiceKey
from .credential import Credential
from .credential_audit_event import CredentialAuditEvent
from .credential_client_secret import CredentialClientSecret
from .credential_dpop_key import CredentialDpopKey
from .credential_mfa_factor import CredentialMfaFactor
from .credential_mtls_certificate import CredentialMtlsCertificate
from .credential_password import CredentialPassword
from .credential_recovery_code import CredentialRecoveryCode
from .credential_webauthn_passkey import CredentialWebAuthnPasskey
from .crypto_key import CryptoKey
from .crypto_key_version import CryptoKeyVersion
from .principal_key_binding import PrincipalKeyBinding
from .key_envelope import KeyEnvelope
from .key_attestation_evidence import KeyAttestationEvidence
from .credential_ecosystem_registry import CredentialConfiguration,CredentialIssuer,WalletAttestation,WalletInstance,WalletKeyBinding,WalletRegistration
from .credential_issuance_state import CredentialDeferredTransaction,CredentialIssuanceTransaction,CredentialNotification,CredentialOffer,CredentialStatusEntry,CredentialStatusList,CredentialStatusPublication
from .presentation_state import PresentationConsent,PresentationReplay,PresentationTransaction,VerifierRegistration
from .attestation_state import AttestationAppraisalPolicy,AttestationEndorsement,AttestationEvidence,AttestationReferenceManifest,AttestationReferenceValue,AttestationResult
from .auth_session import AuthSession, CredsIn, MyAccountSessionOut, TokenPair as LoginTokenPair
from .auth_code import AuthCode
from .device_code import DeviceAuthorizationIn, DeviceAuthorizationOut, DeviceCode
from .revoked_token import RevocationIn, RevocationOut, RevokedToken
from .token_record import (
    AuthorizationCodeGrantForm,
    IntrospectOut,
    PasswordGrantForm,
    RefreshIn,
    TokenPair,
    TokenRecord,
)
from .delegation_grant import (
    DelegationGrant,
    DelegationGrantEdge,
    DelegationGrantProof,
    DelegationGrantRecord,
    DelegationGrantScope,
    DelegationGrantTokenLink,
)
from .pushed_authorization_request import (
    PushedAuthorizationRequest,
    PushedAuthorizationRequestIn,
    PushedAuthorizationResponse,
)
from .consent import Consent
from .audit_event import AuditEvent
from .logout_state import LogoutIn, LogoutOut, LogoutState
from .backchannel_logout_replay import BackchannelLogoutReplay
from .authentication_challenge import AuthenticationChallenge
from .key_rotation_event import KeyRotationEvent
from .key_rotation_policy import KeyRotationPolicy
from .tenant_membership import TenantMembership
from .subject_alias import SubjectAlias
from .role import Role
from .attribute_policy import AttributePolicy
from .policy_condition import PolicyCondition
from .policy import Policy
from .policy_version import PolicyVersion
from .policy_set import PolicySet
from .policy_set_member import PolicySetMember
from .policy_target import PolicyTarget
from .delegated_admin_scope import DelegatedAdminScope
from .entitlement import Entitlement
from .entitlement_assignment import EntitlementAssignment
from .access_review_campaign import AccessReviewCampaign
from .access_review_item import AccessReviewItem
from .access_review_decision import AccessReviewDecision
from .residency_zone import ResidencyZone
from .tenant_residency import TenantResidency
from .sdk_package import SDKPackageRecord
from .plugin_descriptor import PluginDescriptorRecord
from .plugin_lifecycle_event import PluginLifecycleEventRecord
from .scim_schema import ScimSchemaRecord
from .scim_user import ScimUserRecord
from .scim_group import ScimGroupRecord
from .scim_patch_event import ScimPatchEvent
from .release_capability_record import ReleaseCapabilityRecord
from .release_authorization_state import ReleaseAuthorizationState
from .runtime_qualification import RuntimeQualificationRecord
from .release_security_posture import ReleaseSecurityPosture
from .release_posture import ReleasePosture
from .release_attestation_event import ReleaseAttestationEvent
from .control_correctness_report import ControlCorrectnessReport
from .authz_verification_report import AuthzVerificationReport
from .resource_server_contract import ResourceServerContract
from .provider_artifact import ProviderArtifact
from .identity_provider import IdentityProvider
from .federation import Federation
from .federated_session import FederatedSession
from .authorization_invariant import AuthorizationInvariant
from .invariant_evaluation import InvariantEvaluation
from .invariant_violation import InvariantViolation
from .authority_derivation_graph import (
    AuthorityDerivationGraph,
    AuthorityDerivationGraphEdge,
    AuthorityDerivationGraphNode,
)
from .trust_federation_graph import (
    TrustFederationGraph,
    TrustFederationGraphEdge,
    TrustFederationGraphNode,
)
from .operator_metadata import OperatorMetadata
from .operator_record import OperatorRecord
from .operator_transaction import OperatorTransaction
from .operator_audit_event import OperatorAuditEvent
from .operator_activity import OperatorActivity
from .engine import ENGINE, dsn, get_db
from ._schema_ctx import set_schema


_TABLE_MODELS = (
    Realm,
    Tenant,
    User,
    Client,
    ClientRegistration,
    AuthorizationServer,
    Principal,
    ServiceIdentity,
    MachineIdentity,
    WorkloadIdentity,
    CredentialApiKey,
    CredentialServiceKey,
    Credential,
    CredentialAuditEvent,
    CredentialClientSecret,
    CredentialDpopKey,
    CredentialMfaFactor,
    CredentialMtlsCertificate,
    CredentialPassword,
    CredentialRecoveryCode,
    CredentialWebAuthnPasskey,
    CryptoKey,
    CryptoKeyVersion,
    PrincipalKeyBinding,
    KeyEnvelope,
    KeyAttestationEvidence,
    CredentialIssuer,
    CredentialConfiguration,
    WalletRegistration,
    WalletInstance,
    WalletAttestation,
    WalletKeyBinding,
    CredentialOffer,
    CredentialIssuanceTransaction,
    CredentialDeferredTransaction,
    CredentialNotification,
    CredentialStatusList,
    CredentialStatusEntry,
    CredentialStatusPublication,
    VerifierRegistration,
    PresentationTransaction,
    PresentationConsent,
    PresentationReplay,
    AttestationEvidence,
    AttestationResult,
    AttestationReferenceManifest,
    AttestationReferenceValue,
    AttestationEndorsement,
    AttestationAppraisalPolicy,
    AuthSession,
    AuthCode,
    DeviceCode,
    RevokedToken,
    TokenRecord,
    DelegationGrant,
    DelegationGrantScope,
    DelegationGrantProof,
    DelegationGrantEdge,
    DelegationGrantTokenLink,
    PushedAuthorizationRequest,
    Consent,
    AuditEvent,
    LogoutState,
    BackchannelLogoutReplay,
    AuthenticationChallenge,
    KeyRotationEvent,
    KeyRotationPolicy,
    TenantMembership,
    SubjectAlias,
    Role,
    AttributePolicy,
    PolicyCondition,
    Policy,
    PolicyVersion,
    PolicySet,
    PolicySetMember,
    PolicyTarget,
    DelegatedAdminScope,
    Entitlement,
    EntitlementAssignment,
    AccessReviewCampaign,
    AccessReviewItem,
    AccessReviewDecision,
    ResidencyZone,
    TenantResidency,
    SDKPackageRecord,
    PluginDescriptorRecord,
    PluginLifecycleEventRecord,
    ScimSchemaRecord,
    ScimUserRecord,
    ScimGroupRecord,
    ScimPatchEvent,
    ReleaseCapabilityRecord,
    ReleaseAuthorizationState,
    RuntimeQualificationRecord,
    ReleaseSecurityPosture,
    ReleasePosture,
    ReleaseAttestationEvent,
    ControlCorrectnessReport,
    AuthzVerificationReport,
    ResourceServerContract,
    ProviderArtifact,
    IdentityProvider,
    Federation,
    FederatedSession,
    AuthorizationInvariant,
    InvariantEvaluation,
    InvariantViolation,
    AuthorityDerivationGraph,
    AuthorityDerivationGraphNode,
    AuthorityDerivationGraphEdge,
    TrustFederationGraph,
    TrustFederationGraphNode,
    TrustFederationGraphEdge,
    OperatorMetadata,
    OperatorRecord,
    OperatorTransaction,
    OperatorAuditEvent,
    OperatorActivity,
)
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
    set_schema(AuthSession, "list_account_sessions", out=list[MyAccountSessionOut])
    set_schema(AuthSession, "revoke_account_session", out=MyAccountMutationOut)

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

    set_schema(User, "admin_login", in_=AdminCredsIn, out=AdminSessionOut)
    set_schema(User, "admin_session", out=AdminSessionOut)
    set_schema(User, "admin_logout", out=AdminSessionOut)
    set_schema(User, "admin_forgot_password", in_=AdminPasswordResetRequestIn, out=AdminSessionOut)
    set_schema(User, "admin_reset_password", in_=AdminPasswordResetCompleteIn, out=AdminSessionOut)
    set_schema(User, "admin_change_password", in_=AdminPasswordChangeIn, out=AdminSessionOut)
    set_schema(User, "admin_create_identity", in_=AdminIdentityProvisionIn, out=AdminIdentityOut)
    set_schema(User, "admin_update_identity", in_=AdminIdentityUpdateIn, out=AdminIdentityOut)
    set_schema(User, "admin_delete_identity", out=AdminIdentityOut)
    set_schema(User, "get_account_profile", out=MyAccountProfileOut)
    set_schema(User, "update_account_profile", in_=MyAccountProfileUpdateIn, out=MyAccountProfileOut)
    set_schema(User, "change_account_password", in_=MyAccountPasswordChangeIn, out=MyAccountMutationOut)

    set_schema(Tenant, "admin_create_tenant", in_=AdminTenantProvisionIn, out=AdminTenantOut)
    set_schema(Tenant, "admin_update_tenant", in_=AdminTenantUpdateIn, out=AdminTenantOut)
    set_schema(Tenant, "admin_delete_tenant", out=AdminTenantOut)
    set_schema(Realm, "admin_create_realm", in_=AdminRealmProvisionIn, out=AdminRealmOut)
    set_schema(Realm, "admin_update_realm", in_=AdminRealmUpdateIn, out=AdminRealmOut)
    set_schema(Realm, "admin_delete_realm", out=AdminRealmOut)


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
