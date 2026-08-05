"""Compatibility projection of independently owned storage components."""
# ruff: noqa: F401,F403

from tigrbl_identity_storage_core.framework import RestOltpTable
from tigrbl_identity_storage_foundation.tables import Realm, Tenant, User, Principal, SubjectAlias, ServiceIdentity, MachineIdentity
from tigrbl_identity_storage_authentication.tables import Credential, CredentialApiKey, CredentialServiceKey, CredentialAuditEvent, CredentialClientSecret, CredentialDpopKey, CredentialMfaFactor, CredentialMtlsCertificate, CredentialPassword, CredentialRecoveryCode, AuthenticationChallenge
from tigrbl_identity_storage_oauth.tables import Client, ClientRegistration, AuthorizationServer, AuthSession, AuthCode, DeviceCode, RevokedToken, PushedAuthorizationRequest
from tigrbl_identity_storage_oidc.tables import LogoutState, BackchannelLogoutReplay
from tigrbl_identity_storage_token.tables import TokenRecord, ProtectedArtifactReference, PossessionProofReplay
from tigrbl_identity_storage_consent.tables import Consent
from tigrbl_identity_storage_delegation.tables import DelegationGrant, DelegationGrantScope, DelegationGrantProof, DelegationGrantEdge, DelegationGrantTokenLink
from tigrbl_identity_storage_key_material.tables import CryptoKey, CryptoKeyVersion, PrincipalKeyBinding, KeyEnvelope, KeyAttestationEvidence, KeyRotationEvent, KeyRotationPolicy
from tigrbl_identity_storage_authorization_policy.tables import TenantMembership, Role, AttributePolicy, PolicyCondition, Policy, PolicyVersion, PolicySet, PolicySetMember, PolicyTarget, DelegatedAdminScope, AuthorizationInvariant, InvariantEvaluation, InvariantViolation
from tigrbl_identity_storage_access_governance.tables import Entitlement, EntitlementAssignment, AccessReviewCampaign, AccessReviewItem, AccessReviewDecision
from tigrbl_identity_storage_residency.tables import ResidencyZone, TenantResidency
from tigrbl_identity_storage_audit.tables import AuditEvent
from tigrbl_identity_storage_federation.tables import ProviderArtifact, IdentityProvider, Federation, FederatedSession
from tigrbl_identity_storage_digital_credential.tables import CredentialIssuer, CredentialConfiguration, WalletRegistration, WalletInstance, WalletAttestation, WalletKeyBinding, CredentialOffer, CredentialIssuanceTransaction, CredentialDeferredTransaction, CredentialNotification, CredentialStatusList, CredentialStatusEntry, CredentialStatusPublication
from tigrbl_identity_storage_presentation.tables import VerifierRegistration, PresentationTransaction, PresentationConsent, PresentationReplay
from tigrbl_identity_storage_attestation.tables import AttestationEvidence, AttestationResult, AttestationReferenceManifest, AttestationReferenceValue, AttestationEndorsement, AttestationAppraisalPolicy
from tigrbl_identity_storage_workload_identity.tables import WorkloadIdentity, SvidRecord, SpiffeTrustBundle, TrustDomainFederation, WorkloadReferenceBinding, WorkloadCredentialEntitlement
from tigrbl_identity_storage_security_event.tables import SecurityEvent, SecurityEventSubscription, SecurityEventDelivery, SecurityEventReplay
from tigrbl_identity_storage_replay_protection.tables import ReplayReservation, DpopReplay, DpopNonce
from tigrbl_identity_storage_did.tables import DidDocument, DidDocumentVersion, DidVerificationMethod, DidService, DidResolutionCache
from tigrbl_identity_storage_gnap.tables import GnapGrant, GnapContinuation, GnapClientInstance, GnapInteraction
from tigrbl_identity_storage_certificate.tables import CertificateRecord, TrustAnchor, CertificateStatusSnapshot
from tigrbl_identity_storage_claims.tables import ClaimDefinition, ClaimSourceBinding, ClaimReleasePolicy, ClaimProvenanceRecord, ClaimSnapshot
from tigrbl_identity_storage_webauthn.tables import CredentialWebAuthnPasskey, WebAuthnAttestationRecord, WebAuthnCeremony, WebAuthnRelyingParty
from tigrbl_identity_storage_authority_graph.tables import AuthorityDerivationGraph, AuthorityDerivationGraphNode, AuthorityDerivationGraphEdge
from tigrbl_identity_storage_trust_federation_graph.tables import TrustFederationGraph, TrustFederationGraphNode, TrustFederationGraphEdge
from tigrbl_identity_storage_scim.tables import ScimSchemaRecord, ScimUserRecord, ScimGroupRecord, ScimPatchEvent
from tigrbl_identity_storage_release_governance.tables import SDKPackageRecord, PluginDescriptorRecord, PluginLifecycleEventRecord, ReleaseCapabilityRecord, ReleaseAuthorizationState, RuntimeQualificationRecord, ReleaseSecurityPosture, ReleasePosture, ReleaseAttestationEvent, ControlCorrectnessReport, AuthzVerificationReport, ResourceServerContract
from tigrbl_identity_storage_operator.tables import OperatorMetadata, OperatorRecord, OperatorTransaction, OperatorAuditEvent, OperatorActivity
from tigrbl_identity_storage_oauth.tables.client import _CLIENT_ID_RE
from tigrbl_identity_storage_delegation.tables.delegation_grant import DelegationGrantRecord

_TABLE_MODELS = (
    Realm,
    Tenant,
    User,
    Principal,
    SubjectAlias,
    ServiceIdentity,
    MachineIdentity,
    Credential,
    CredentialApiKey,
    CredentialServiceKey,
    CredentialAuditEvent,
    CredentialClientSecret,
    CredentialDpopKey,
    CredentialMfaFactor,
    CredentialMtlsCertificate,
    CredentialPassword,
    CredentialRecoveryCode,
    AuthenticationChallenge,
    Client,
    ClientRegistration,
    AuthorizationServer,
    AuthSession,
    AuthCode,
    DeviceCode,
    RevokedToken,
    PushedAuthorizationRequest,
    LogoutState,
    BackchannelLogoutReplay,
    TokenRecord,
    ProtectedArtifactReference,
    PossessionProofReplay,
    Consent,
    DelegationGrant,
    DelegationGrantScope,
    DelegationGrantProof,
    DelegationGrantEdge,
    DelegationGrantTokenLink,
    CryptoKey,
    CryptoKeyVersion,
    PrincipalKeyBinding,
    KeyEnvelope,
    KeyAttestationEvidence,
    KeyRotationEvent,
    KeyRotationPolicy,
    TenantMembership,
    Role,
    AttributePolicy,
    PolicyCondition,
    Policy,
    PolicyVersion,
    PolicySet,
    PolicySetMember,
    PolicyTarget,
    DelegatedAdminScope,
    AuthorizationInvariant,
    InvariantEvaluation,
    InvariantViolation,
    Entitlement,
    EntitlementAssignment,
    AccessReviewCampaign,
    AccessReviewItem,
    AccessReviewDecision,
    ResidencyZone,
    TenantResidency,
    AuditEvent,
    ProviderArtifact,
    IdentityProvider,
    Federation,
    FederatedSession,
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
    WorkloadIdentity,
    SvidRecord,
    SpiffeTrustBundle,
    TrustDomainFederation,
    WorkloadReferenceBinding,
    WorkloadCredentialEntitlement,
    SecurityEvent,
    SecurityEventSubscription,
    SecurityEventDelivery,
    SecurityEventReplay,
    ReplayReservation,
    DpopReplay,
    DpopNonce,
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
    CredentialWebAuthnPasskey,
    WebAuthnAttestationRecord,
    WebAuthnCeremony,
    WebAuthnRelyingParty,
    AuthorityDerivationGraph,
    AuthorityDerivationGraphNode,
    AuthorityDerivationGraphEdge,
    TrustFederationGraph,
    TrustFederationGraphNode,
    TrustFederationGraphEdge,
    ScimSchemaRecord,
    ScimUserRecord,
    ScimGroupRecord,
    ScimPatchEvent,
    SDKPackageRecord,
    PluginDescriptorRecord,
    PluginLifecycleEventRecord,
    ReleaseCapabilityRecord,
    ReleaseAuthorizationState,
    RuntimeQualificationRecord,
    ReleaseSecurityPosture,
    ReleasePosture,
    ReleaseAttestationEvent,
    ControlCorrectnessReport,
    AuthzVerificationReport,
    ResourceServerContract,
    OperatorMetadata,
    OperatorRecord,
    OperatorTransaction,
    OperatorAuditEvent,
    OperatorActivity,
)
