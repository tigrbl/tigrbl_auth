"""Consent table alias and executable runtime specification."""

from tigrbl_identity_storage.tables import Consent

from ..derive import deriveRuntimeTableSpec
from ..make import makeRuntimeOperation
from ..ops.consents import (
    list_consents_for_user,
    revoke_consent_for_user,
    revoke_consents_for_client,
)

ConsentTable = Consent
ConsentRuntimeSpec = deriveRuntimeTableSpec(
    ConsentTable,
    operations=(
        makeRuntimeOperation(
            alias="list_for_user",
            handler=list_consents_for_user,
        ),
        makeRuntimeOperation(
            alias="revoke_for_user",
            handler=revoke_consent_for_user,
            arity="member",
        ),
        makeRuntimeOperation(
            alias="revoke_for_client",
            handler=revoke_consents_for_client,
        ),
    ),
)

__all__ = ["ConsentRuntimeSpec", "ConsentTable"]
