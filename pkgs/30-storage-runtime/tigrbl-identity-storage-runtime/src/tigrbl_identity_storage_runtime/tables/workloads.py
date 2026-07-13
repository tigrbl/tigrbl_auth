"""Workload table aliases and executable runtime specifications."""

from tigrbl_identity_storage.tables import SpiffeTrustBundle, SvidRecord

from ..derive import deriveRuntimeTableSpec
from ..make import makeRuntimeOperation
from ..ops.workloads import activate_spiffe_trust_bundle, record_svid

SvidRecordTable = SvidRecord
SpiffeTrustBundleTable = SpiffeTrustBundle

SvidRecordRuntimeSpec = deriveRuntimeTableSpec(
    SvidRecordTable,
    operations=(makeRuntimeOperation(alias="record_svid", handler=record_svid),),
)
SpiffeTrustBundleRuntimeSpec = deriveRuntimeTableSpec(
    SpiffeTrustBundleTable,
    operations=(
        makeRuntimeOperation(
            alias="activate_trust_bundle",
            handler=activate_spiffe_trust_bundle,
        ),
    ),
)

__all__ = [
    "SpiffeTrustBundleRuntimeSpec",
    "SpiffeTrustBundleTable",
    "SvidRecordRuntimeSpec",
    "SvidRecordTable",
]
