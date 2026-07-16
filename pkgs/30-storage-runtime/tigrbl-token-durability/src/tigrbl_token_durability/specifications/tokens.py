"""Token-record table alias and executable runtime specification."""

from tigrbl_identity_storage.tables import TokenRecord

from tigrbl_table_durability import deriveRuntimeTableSpec
from tigrbl_table_durability import makeRuntimeOperation
from tigrbl_token_durability.operations.tokens import (
    introspect_token_record,
    mark_refresh_token_rotated,
    persist_issued_token,
    read_token_record,
    revoke_refresh_token_family,
)

TokenRecordTable = TokenRecord
TokenRecordRuntimeSpec = deriveRuntimeTableSpec(
    TokenRecordTable,
    operations=(
        makeRuntimeOperation(alias="persist_issued", handler=persist_issued_token),
        makeRuntimeOperation(
            alias="get_by_hash",
            handler=read_token_record,
            tx_scope="read_only",
            persist="skip",
        ),
        makeRuntimeOperation(alias="mark_rotated", handler=mark_refresh_token_rotated),
        makeRuntimeOperation(
            alias="revoke_family", handler=revoke_refresh_token_family
        ),
        makeRuntimeOperation(alias="introspect", handler=introspect_token_record),
    ),
)

__all__ = ["TokenRecordRuntimeSpec", "TokenRecordTable"]
