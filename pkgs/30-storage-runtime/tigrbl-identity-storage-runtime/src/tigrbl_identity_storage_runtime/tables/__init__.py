"""Derived executable specifications grouped by durable table family."""

from .attestation import *
from .credentials import *
from .presentations import *
from .replay import *
from .security_events import *
from .workloads import *

DURABLE_RUNTIME_TABLE_SPECS = (
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
