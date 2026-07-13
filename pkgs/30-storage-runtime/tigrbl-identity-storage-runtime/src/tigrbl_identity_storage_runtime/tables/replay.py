"""Replay table alias and executable runtime specification."""

from tigrbl_identity_storage.tables import ReplayReservation

from ..derive import deriveRuntimeTableSpec
from ..make import makeRuntimeOperation
from ..ops.replay import check_and_reserve

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
