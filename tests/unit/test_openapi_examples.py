import pytest_asyncio

import asyncio

from tigrbl_identity_server.surfaces import AdminRouter, PublicRouter

ORM_MODELS = [
    "Tenant",
    "User",
    "Client",
    "CredentialApiKey",
    "ServiceIdentity",
    "CredentialServiceKey",
    "AuthSession",
    "AuthCode",
    "PushedAuthorizationRequest",
]


@pytest_asyncio.fixture()
async def openapi_spec() -> dict:
    """Initialize the admin router once and return its OpenAPI spec."""
    init = PublicRouter.initialize()
    if asyncio.iscoroutine(init):
        await init
    init = AdminRouter.initialize()
    if asyncio.iscoroutine(init):
        await init
    return AdminRouter.openapi()


def test_request_response_examples_presence(openapi_spec: dict) -> None:
    """Ensure clear responses expose example bodies for every ORM."""
    checked = 0
    for model in ORM_MODELS:
        schema_name = f"{model}ClearResponse"
        schema = openapi_spec["components"]["schemas"].get(schema_name)
        if schema is None:
            continue
        checked += 1
        assert schema.get("examples"), f"{schema_name} lacks examples"
    assert checked > 0


def test_openapi_contains_all_schemas(openapi_spec: dict) -> None:
    """Verify OpenAPI documents request/response schemas for each ORM."""
    schema_names = set(openapi_spec["components"]["schemas"].keys())
    for model in ORM_MODELS:
        expected = {
            f"{model}{suffix}"
            for suffix in (
                "CreateRequest",
                "CreateResponse",
                "DeleteRequest",
                "DeleteResponse",
                "ReplaceRequest",
                "ReplaceResponse",
            )
        }
        assert expected.issubset(schema_names), f"schemas missing for {model}"


def test_all_models_registered_on_api_and_tables() -> None:
    """Ensure Tigrbl tracks all ORM models in schemas and tables."""
    expected = set(ORM_MODELS)
    assert expected.issubset(set(AdminRouter.tables.keys()))
    assert expected.issubset(vars(AdminRouter.schemas).keys())
