"""Workload table aliases and executable runtime specifications."""

from tigrbl_identity_storage.tables import SpiffeTrustBundle, SvidRecord

from tigrbl_table_durability import deriveRuntimeTableSpec
from tigrbl_table_durability import makeRuntimeOperation
from tigrbl_workload_identity_durability.operations.workloads import (
    activate_spiffe_trust_bundle,
    record_svid,
    record_workload_credential,
)

SvidRecordTable = SvidRecord
SpiffeTrustBundleTable = SpiffeTrustBundle

SvidRecordRuntimeSpec = deriveRuntimeTableSpec(
    SvidRecordTable,
    operations=(
        makeRuntimeOperation(alias="record_workload_credential", handler=record_workload_credential),
        makeRuntimeOperation(alias="record_svid", handler=record_svid),
    ),
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
