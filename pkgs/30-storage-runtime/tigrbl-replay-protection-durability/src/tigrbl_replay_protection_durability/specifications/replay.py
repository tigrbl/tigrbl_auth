"""Replay table alias and executable runtime specification."""

from tigrbl_identity_storage.tables import ReplayReservation

from tigrbl_table_durability import deriveRuntimeTableSpec
from tigrbl_table_durability import makeRuntimeOperation
from tigrbl_replay_protection_durability.operations.replay import check_and_reserve

ReplayReservationTable = ReplayReservation
ReplayReservationRuntimeSpec = deriveRuntimeTableSpec(
    ReplayReservationTable,
    operations=(
        makeRuntimeOperation(
            alias="check_and_reserve",
            handler=check_and_reserve,
        ),
    ),
)

__all__ = ["ReplayReservationRuntimeSpec", "ReplayReservationTable"]
