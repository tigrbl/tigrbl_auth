"""Token-record table alias and executable runtime specification."""

from tigrbl_identity_storage.tables import TokenRecord

from ..derive import deriveRuntimeTableSpec
from ..make import makeRuntimeOperation
from ..ops.tokens import (
    introspect_token_record,
    mark_refresh_token_rotated,
    persist_issued_token,
    revoke_refresh_token_family,
)

TokenRecordTable = TokenRecord
TokenRecordRuntimeSpec = deriveRuntimeTableSpec(
    TokenRecordTable,
    operations=(
        makeRuntimeOperation(alias="persist_issued", handler=persist_issued_token),
        makeRuntimeOperation(alias="mark_rotated", handler=mark_refresh_token_rotated),
        makeRuntimeOperation(alias="revoke_family", handler=revoke_refresh_token_family),
        makeRuntimeOperation(alias="introspect", handler=introspect_token_record),
    ),
)

__all__ = ["TokenRecordRuntimeSpec", "TokenRecordTable"]
