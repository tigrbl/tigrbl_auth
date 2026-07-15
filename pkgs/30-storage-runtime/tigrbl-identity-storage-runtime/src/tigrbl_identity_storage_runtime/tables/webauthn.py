"""WebAuthn table aliases and executable durable specifications."""

from tigrbl_identity_storage.tables import (
    CredentialWebAuthnPasskey,
    WebAuthnAttestationRecord,
    WebAuthnCeremony,
    WebAuthnRelyingParty,
)

from ..derive import deriveRuntimeTableSpec
from ..make import makeRuntimeOperation
from ..ops.webauthn_ceremonies import (
    consume_ceremony,
    fail_ceremony,
    load_active_ceremony,
    reserve_authentication_ceremony,
    reserve_registration_ceremony,
)
from ..ops.webauthn_credentials import (
    find_discoverable_credentials,
    find_public_key_credential,
    insert_public_key_credential,
    list_principal_public_key_credentials,
    rename_public_key_credential,
    revoke_public_key_credential,
    update_assertion_state,
)
from ..ops.webauthn_relying_parties import resolve_relying_party_configuration

WebAuthnCeremonyTable = WebAuthnCeremony
WebAuthnRelyingPartyTable = WebAuthnRelyingParty
WebAuthnCredentialTable = CredentialWebAuthnPasskey
WebAuthnAttestationRecordTable = WebAuthnAttestationRecord

WebAuthnCeremonyRuntimeSpec = deriveRuntimeTableSpec(
    WebAuthnCeremonyTable,
    operations=tuple(
        makeRuntimeOperation(alias=name, handler=handler)
        for name, handler in (
            ("reserve_registration_ceremony", reserve_registration_ceremony),
            ("reserve_authentication_ceremony", reserve_authentication_ceremony),
            ("load_active_ceremony", load_active_ceremony),
            ("consume_ceremony", consume_ceremony),
            ("fail_ceremony", fail_ceremony),
        )
    ),
)
WebAuthnCredentialRuntimeSpec = deriveRuntimeTableSpec(
    WebAuthnCredentialTable,
    operations=tuple(
        makeRuntimeOperation(alias=name, handler=handler)
        for name, handler in (
            ("insert_public_key_credential", insert_public_key_credential),
            ("find_public_key_credential", find_public_key_credential),
            ("find_discoverable_credentials", find_discoverable_credentials),
            ("update_assertion_state", update_assertion_state),
            ("list_principal_public_key_credentials", list_principal_public_key_credentials),
            ("rename_public_key_credential", rename_public_key_credential),
            ("revoke_public_key_credential", revoke_public_key_credential),
        )
    ),
)
WebAuthnRelyingPartyRuntimeSpec = deriveRuntimeTableSpec(
    WebAuthnRelyingPartyTable,
    operations=(
        makeRuntimeOperation(
            alias="resolve_relying_party_configuration",
            handler=resolve_relying_party_configuration,
            tx_scope="read",
            persist="skip",
        ),
    ),
)
WebAuthnAttestationRecordRuntimeSpec = deriveRuntimeTableSpec(WebAuthnAttestationRecordTable)

__all__ = [name for name in globals() if name.endswith(("RuntimeSpec", "Table"))]
