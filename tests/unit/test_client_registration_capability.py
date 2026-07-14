from __future__ import annotations

from datetime import datetime, timezone

import pytest

from tigrbl_auth_protocol_oauth.capability_requirements import (
    CAPABILITY_REQUIREMENTS,
)
from tigrbl_auth_protocol_oauth.standards.client_registration_management import (
    ClientRegistrationManagementDisabledError,
    RFC7592ClientRegistrationManagementService,
)
from tigrbl_auth_protocol_oauth.standards.dynamic_client_registration import (
    DynamicClientRegistrationDisabledError,
    RFC7591DynamicClientRegistrationService,
)
from tigrbl_client_registration_capability import ClientRegistrationCapability
from tigrbl_identity_contracts.oauth import (
    ClientRegistrationCreateRequest,
    ClientRegistrationRecord,
    ClientRegistrationUpdateRequest,
)


def _record(*, disabled: bool = False) -> ClientRegistrationRecord:
    return ClientRegistrationRecord(
        client_id="00000000-0000-0000-0000-000000000301",
        tenant_id="00000000-0000-0000-0000-000000000201",
        registration_id="00000000-0000-0000-0000-000000000401",
        redirect_uris=("https://client.example/cb",),
        grant_types=("authorization_code",),
        response_types=("code",),
        metadata={"token_endpoint_auth_method": "private_key_jwt"},
        registration_client_uri="https://issuer.example/register/client",
        disabled_at=datetime.now(timezone.utc) if disabled else None,
        client_active=not disabled,
    )


def _create_request() -> ClientRegistrationCreateRequest:
    return ClientRegistrationCreateRequest(
        client_id="00000000-0000-0000-0000-000000000301",
        tenant_id="00000000-0000-0000-0000-000000000201",
        client_secret_hash="hashed-secret",
        redirect_uris=("https://client.example/cb",),
        metadata={"token_endpoint_auth_method": "private_key_jwt"},
    )


def _update_request() -> ClientRegistrationUpdateRequest:
    return ClientRegistrationUpdateRequest(
        client_id="00000000-0000-0000-0000-000000000301",
        redirect_uris=("https://client.example/new",),
        grant_types=("authorization_code",),
        response_types=("code",),
        metadata={"client_name": "Changed"},
        updated_fields=("client_name", "redirect_uris"),
    )


@pytest.mark.asyncio
async def test_capability_delegates_full_registration_lifecycle_and_audit() -> None:
    audit_events: list[dict[str, object]] = []

    async def create(_request):
        return _record()

    async def get(_client_id):
        return _record()

    async def update(_request):
        return _record()

    async def disable(_client_id):
        return _record(disabled=True)

    capability = ClientRegistrationCapability(
        create,
        get,
        update,
        disable,
        lambda event: audit_events.append(dict(event)),
    )
    assert capability.capability_report()["bound_operations"] == (
        "disable_registration",
        "get_registration",
        "record_audit_event",
        "register_client",
        "update_registration",
    )

    created = await capability.call("register_client", _create_request())
    fetched = await capability.call("get_registration", created.value.client_id)
    changed = await capability.call("update_registration", _update_request())
    disabled = await capability.call("disable_registration", changed.value.client_id)

    assert fetched.value.client_id == created.value.client_id
    assert disabled.value.disabled_at is not None
    assert [event["event_type"] for event in audit_events] == [
        "client.registration.created",
        "client.registration.updated",
        "client.registration.deleted",
    ]


def test_capability_rejects_missing_required_lifecycle_operation() -> None:
    with pytest.raises(NotImplementedError, match="get_registration"):
        ClientRegistrationCapability(lambda request: _record(), None, None, None)


@pytest.mark.asyncio
async def test_rfc_services_map_to_capability_and_honor_feature_state() -> None:
    capability = ClientRegistrationCapability(
        lambda request: _record(),
        lambda client_id: _record(),
        lambda request: _record(),
        lambda client_id: _record(disabled=True),
    )
    registration = RFC7591DynamicClientRegistrationService(capability)
    management = RFC7592ClientRegistrationManagementService(capability)

    assert (await registration.register(_create_request())).client_id
    assert (await management.get(_record().client_id)).client_id
    assert (await management.update(_update_request())).client_id
    assert (await management.delete(_record().client_id)).disabled_at is not None

    with pytest.raises(DynamicClientRegistrationDisabledError):
        await RFC7591DynamicClientRegistrationService(
            capability, enabled=False
        ).register(_create_request())
    with pytest.raises(ClientRegistrationManagementDisabledError):
        await RFC7592ClientRegistrationManagementService(
            capability, enabled=False
        ).get(_record().client_id)


def test_rfc_7591_and_7592_requirements_map_every_wire_operation() -> None:
    requirements = {
        (item.revision, item.operation)
        for item in CAPABILITY_REQUIREMENTS
        if item.capability_id == "client.registration"
    }
    assert requirements == {
        ("RFC7591", "register_client"),
        ("RFC7592", "get_registration"),
        ("RFC7592", "update_registration"),
        ("RFC7592", "disable_registration"),
    }
