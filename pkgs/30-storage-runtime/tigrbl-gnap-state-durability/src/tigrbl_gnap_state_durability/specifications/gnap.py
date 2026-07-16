"""GNAP durable-state aliases and executable runtime specifications."""

from tigrbl_identity_storage.tables import (
    GnapClientInstance,
    GnapContinuation,
    GnapGrant,
    GnapInteraction,
)

from tigrbl_table_durability import deriveRuntimeTableSpec
from tigrbl_table_durability import makeRuntimeOperation
from tigrbl_gnap_state_durability.operations.gnap import (
    complete_gnap_interaction,
    create_gnap_grant,
    read_gnap_continuation,
    read_gnap_grant,
    record_gnap_client_instance,
    record_gnap_continuation,
    record_gnap_interaction,
    rotate_gnap_continuation,
    update_gnap_grant,
)

GnapClientInstanceTable = GnapClientInstance
GnapClientInstanceRuntimeSpec = deriveRuntimeTableSpec(
    GnapClientInstanceTable,
    operations=(
        makeRuntimeOperation(
            alias="record_client_instance", handler=record_gnap_client_instance
        ),
    ),
)

GnapGrantTable = GnapGrant
GnapGrantRuntimeSpec = deriveRuntimeTableSpec(
    GnapGrantTable,
    operations=(
        makeRuntimeOperation(alias="create_grant", handler=create_gnap_grant),
        makeRuntimeOperation(
            alias="read_grant",
            handler=read_gnap_grant,
            tx_scope="read_only",
            persist="skip",
        ),
        makeRuntimeOperation(alias="update_grant", handler=update_gnap_grant),
    ),
)

GnapContinuationTable = GnapContinuation
GnapContinuationRuntimeSpec = deriveRuntimeTableSpec(
    GnapContinuationTable,
    operations=(
        makeRuntimeOperation(
            alias="record_continuation", handler=record_gnap_continuation
        ),
        makeRuntimeOperation(
            alias="read_continuation",
            handler=read_gnap_continuation,
            tx_scope="read_only",
            persist="skip",
        ),
        makeRuntimeOperation(
            alias="rotate_continuation", handler=rotate_gnap_continuation
        ),
    ),
)

GnapInteractionTable = GnapInteraction
GnapInteractionRuntimeSpec = deriveRuntimeTableSpec(
    GnapInteractionTable,
    operations=(
        makeRuntimeOperation(
            alias="record_interaction", handler=record_gnap_interaction
        ),
        makeRuntimeOperation(
            alias="complete_interaction", handler=complete_gnap_interaction
        ),
    ),
)

__all__ = [
    "GnapClientInstanceRuntimeSpec",
    "GnapClientInstanceTable",
    "GnapContinuationRuntimeSpec",
    "GnapContinuationTable",
    "GnapGrantRuntimeSpec",
    "GnapGrantTable",
    "GnapInteractionRuntimeSpec",
    "GnapInteractionTable",
]
