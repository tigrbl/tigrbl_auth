"""Derived executable specifications grouped by durable table family."""

from .attestation import *
from .audit import *
from .authorization import *
from .clients import *
from .consents import *
from .credentials import *
from .delegation import *
from .dpop import *
from .gnap import *
from .oidc import *
from .oauth import *
from .identities import *
from .keys import *
from .presentations import *
from .replay import *
from .security_events import *
from .sessions import *
from .tokens import *
from .workloads import *

DURABLE_RUNTIME_TABLE_SPECS = (
    AttributePolicyRuntimeSpec,
    AuditEventRuntimeSpec,
    RoleRuntimeSpec,
    TenantMembershipRuntimeSpec,
    DelegatedAdminScopeRuntimeSpec,
    BackchannelLogoutReplayRuntimeSpec,
    AuthSessionRuntimeSpec,
    ConsentRuntimeSpec,
    LogoutStateRuntimeSpec,
    TokenRecordRuntimeSpec,
    AuthCodeRuntimeSpec,
    ClientRegistrationRuntimeSpec,
    RevokedTokenRuntimeSpec,
    ClientRuntimeSpec,
    UserRuntimeSpec,
    DelegationGrantRuntimeSpec,
    DelegationGrantEdgeRuntimeSpec,
    DelegationGrantProofRuntimeSpec,
    DelegationGrantTokenLinkRuntimeSpec,
    DeviceCodeRuntimeSpec,
    PushedAuthorizationRequestRuntimeSpec,
    CryptoKeyRuntimeSpec,
    CryptoKeyVersionRuntimeSpec,
    CredentialOfferRuntimeSpec,
    CredentialIssuanceTransactionRuntimeSpec,
    CredentialStatusEntryRuntimeSpec,
    PresentationTransactionRuntimeSpec,
    PresentationConsentRuntimeSpec,
    PresentationReplayRuntimeSpec,
    AttestationEvidenceRuntimeSpec,
    AttestationResultRuntimeSpec,
    AttestationReferenceManifestRuntimeSpec,
    SecurityEventRuntimeSpec,
    SecurityEventDeliveryRuntimeSpec,
    SecurityEventReplayRuntimeSpec,
    SvidRecordRuntimeSpec,
    SpiffeTrustBundleRuntimeSpec,
    ReplayReservationRuntimeSpec,
    DpopReplayRuntimeSpec,
    DpopNonceRuntimeSpec,
    GnapClientInstanceRuntimeSpec,
    GnapGrantRuntimeSpec,
    GnapContinuationRuntimeSpec,
    GnapInteractionRuntimeSpec,
)

__all__ = [
    *[name for name in globals() if name.endswith(("RuntimeSpec", "Table"))],
    "DURABLE_RUNTIME_TABLE_SPECS",
]
