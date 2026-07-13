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
from .spiffe_state import SpiffeTrustBundle,SvidRecord,TrustDomainFederation
from .security_event_state import SecurityEvent,SecurityEventDelivery,SecurityEventReplay,SecurityEventSubscription
from .replay_reservation import ReplayReservation
from .did_gnap_state import DidDocument,DidDocumentVersion,DidResolutionCache,DidService,DidVerificationMethod,GnapClientInstance,GnapContinuation,GnapGrant,GnapInteraction
from .certificate_state import CertificateRecord,CertificateStatusSnapshot,TrustAnchor
from .claim_state import ClaimDefinition,ClaimProvenanceRecord,ClaimReleasePolicy,ClaimSnapshot,ClaimSourceBinding
from .auth_session import AuthSession, CredsIn, TokenPair as LoginTokenPair
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
    SvidRecord,
    SpiffeTrustBundle,
    TrustDomainFederation,
    SecurityEvent,
    SecurityEventSubscription,
    SecurityEventDelivery,
    SecurityEventReplay,
    ReplayReservation,
    DidDocument,
    DidDocumentVersion,
    DidVerificationMethod,
    DidService,
    DidResolutionCache,
    GnapGrant,
    GnapContinuation,
    GnapClientInstance,
    GnapInteraction,
    CertificateRecord,
    TrustAnchor,
    CertificateStatusSnapshot,
    ClaimDefinition,
    ClaimSourceBinding,
    ClaimReleasePolicy,
    ClaimProvenanceRecord,
    ClaimSnapshot,
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
