"""Client table alias and executable runtime specification."""

from tigrbl_identity_storage.tables import Client

from ..derive import deriveRuntimeTableSpec
from ..make import makeRuntimeOperation
from ..ops.clients import (
    disable_client,
    enable_client,
    lookup_client,
    replace_client_secret_hash,
)


ClientTable = Client
ClientRuntimeSpec = deriveRuntimeTableSpec(
    ClientTable,
    operations=(
        makeRuntimeOperation(
            alias="lookup_client",
            handler=lookup_client,
            tx_scope="read_only",
            persist="skip",
        ),
        makeRuntimeOperation(alias="enable", handler=enable_client, arity="member"),
        makeRuntimeOperation(alias="disable", handler=disable_client, arity="member"),
        makeRuntimeOperation(
            alias="rotate_secret_hash",
            handler=replace_client_secret_hash,
            arity="member",
        ),
    ),
)


__all__ = ["ClientRuntimeSpec", "ClientTable"]
