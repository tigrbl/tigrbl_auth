"""Authentication-session table alias and executable runtime specification."""

from tigrbl_identity_storage.tables import AuthSession

from tigrbl_table_durability import deriveRuntimeTableSpec
from tigrbl_table_durability import makeRuntimeOperation
from tigrbl_session_durability.operations.sessions import (
    bind_session_client,
    get_active_session,
    rotate_session_cookie_secret,
    terminate_session,
    touch_session,
)

AuthSessionTable = AuthSession
AuthSessionRuntimeSpec = deriveRuntimeTableSpec(
    AuthSessionTable,
    operations=(
        makeRuntimeOperation(
            alias="terminate",
            handler=terminate_session,
            arity="member",
        ),
        makeRuntimeOperation(
            alias="touch",
            handler=touch_session,
            arity="member",
        ),
        makeRuntimeOperation(
            alias="get_active",
            handler=get_active_session,
            arity="member",
        ),
        makeRuntimeOperation(
            alias="rotate_cookie_secret",
            handler=rotate_session_cookie_secret,
            arity="member",
        ),
        makeRuntimeOperation(
            alias="bind_client",
            handler=bind_session_client,
            arity="member",
        ),
    ),
)

__all__ = ["AuthSessionRuntimeSpec", "AuthSessionTable"]
