"""Derived executable specifications grouped by durable table family."""

from .attestation import *
from .authorization import *
from .credentials import *
from .oidc import *
from .presentations import *
from .replay import *
from .security_events import *
from .workloads import *

DURABLE_RUNTIME_TABLE_SPECS = (
    AttributePolicyRuntimeSpec,
    RoleRuntimeSpec,
    TenantMembershipRuntimeSpec,
    DelegatedAdminScopeRuntimeSpec,
    BackchannelLogoutReplayRuntimeSpec,
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
)

__all__ = [
    *[name for name in globals() if name.endswith(("RuntimeSpec", "Table"))],
    "DURABLE_RUNTIME_TABLE_SPECS",
]
