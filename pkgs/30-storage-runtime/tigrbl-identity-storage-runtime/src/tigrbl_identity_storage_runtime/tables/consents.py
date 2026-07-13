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
            response_model=Consent.schemas.list.out,
        ),
        makeRuntimeOperation(
            alias="revoke_for_user",
            handler=revoke_consent_for_user,
            arity="member",
            response_model=Consent.schemas.update.out,
        ),
        makeRuntimeOperation(
            alias="revoke_for_client",
            handler=revoke_consents_for_client,
            response_model=Consent.schemas.update.out,
        ),
    ),
)

__all__ = ["ConsentRuntimeSpec", "ConsentTable"]
