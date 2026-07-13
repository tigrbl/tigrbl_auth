"""OIDC durable-state aliases and executable runtime specifications."""

from tigrbl_identity_storage.tables import BackchannelLogoutReplay

from ..derive import deriveRuntimeTableSpec
from ..make import makeRuntimeOperation
from ..ops.oidc_replay import register_backchannel_logout_replay

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

__all__ = [
    "BackchannelLogoutReplayRuntimeSpec",
    "BackchannelLogoutReplayTable",
]
