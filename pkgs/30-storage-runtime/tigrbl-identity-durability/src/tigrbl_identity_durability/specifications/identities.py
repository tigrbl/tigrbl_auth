"""User identity table alias and executable runtime specification."""

from tigrbl_identity_storage.tables import User

from tigrbl_table_durability import deriveRuntimeTableSpec
from tigrbl_table_durability import makeRuntimeOperation
from tigrbl_identity_durability.operations.identities import (
    lookup_identity_by_identifier,
    replace_password_hash,
    set_identity_enabled,
)


UserTable = User
UserRuntimeSpec = deriveRuntimeTableSpec(
    UserTable,
    operations=(
        makeRuntimeOperation(
            alias="lookup_by_identifier",
            handler=lookup_identity_by_identifier,
            tx_scope="read_only",
            persist="skip",
        ),
        makeRuntimeOperation(
            alias="replace_password_hash",
            handler=replace_password_hash,
            arity="member",
        ),
        makeRuntimeOperation(
            alias="set_enabled",
            handler=set_identity_enabled,
            arity="member",
        ),
    ),
)


__all__ = ["UserRuntimeSpec", "UserTable"]
