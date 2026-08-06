"""Replay table alias and executable runtime specification."""

from tigrbl_identity_storage.tables import ReplayReservation

from tigrbl import deriveTableSpec
from tigrbl import makeOp
from tigrbl_replay_protection_durability.operations.replay import check_and_reserve

ReplayReservationTable = ReplayReservation
ReplayReservationRuntimeSpec = deriveTableSpec(
    ReplayReservationTable,
    ops=(
        makeOp(
            extra={"owner_layer": "30-storage-runtime"},
            expose_routes=False,
            expose_rpc=False,
            expose_method=True,
            tx_scope="read_write",
            alias="check_and_reserve",
            handler=check_and_reserve,
        ),
    ),
)

__all__ = ["ReplayReservationRuntimeSpec", "ReplayReservationTable"]
