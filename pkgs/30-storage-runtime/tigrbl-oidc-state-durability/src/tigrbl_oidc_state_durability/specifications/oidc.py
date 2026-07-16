"""OIDC durable-state aliases and executable runtime specifications."""

from tigrbl_identity_storage.tables import BackchannelLogoutReplay, LogoutState

from tigrbl_table_durability import deriveRuntimeTableSpec
from tigrbl_table_durability import makeRuntimeOperation
from tigrbl_oidc_state_durability.operations.oidc_replay import (
    register_backchannel_logout_replay,
)
from tigrbl_oidc_state_durability.operations.oidc_logout import (
    ensure_logout_for_session,
    latest_logout_for_session,
    mark_logout_channel,
    update_logout_metadata,
)

BackchannelLogoutReplayTable = BackchannelLogoutReplay
BackchannelLogoutReplayRuntimeSpec = deriveRuntimeTableSpec(
    BackchannelLogoutReplayTable,
    operations=(
        makeRuntimeOperation(
            alias="register",
            handler=register_backchannel_logout_replay,
        ),
    ),
)

LogoutStateTable = LogoutState
LogoutStateRuntimeSpec = deriveRuntimeTableSpec(
    LogoutStateTable,
    operations=(
        makeRuntimeOperation(
            alias="latest_for_session",
            handler=latest_logout_for_session,
        ),
        makeRuntimeOperation(
            alias="update_metadata",
            handler=update_logout_metadata,
            arity="member",
        ),
        makeRuntimeOperation(
            alias="mark_channel",
            handler=mark_logout_channel,
            arity="member",
        ),
        makeRuntimeOperation(
            alias="ensure_for_session",
            handler=ensure_logout_for_session,
        ),
    ),
)

__all__ = [
    "BackchannelLogoutReplayRuntimeSpec",
    "BackchannelLogoutReplayTable",
    "LogoutStateRuntimeSpec",
    "LogoutStateTable",
]
