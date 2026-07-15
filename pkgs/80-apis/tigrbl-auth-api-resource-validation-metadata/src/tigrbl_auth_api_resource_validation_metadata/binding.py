"""HTTP carriers for resource-validation metadata projections."""

from collections.abc import Callable
from typing import Any

from tigrbl import Request, TigrblApp, TigrblRouter
from tigrbl_identity_contracts.resource_validation_metadata import (
    CAPABILITIES_METADATA_PATH,
    VERIFIER_CONTRACT_METADATA_PATH,
)


def build_resource_validation_metadata_router(
    *,
    capability_metadata: Callable[..., Any],
    verifier_contract_metadata: Callable[..., Any],
) -> TigrblRouter:
    router = TigrblRouter()

    @router.route(
        CAPABILITIES_METADATA_PATH,
        methods=["GET"],
        include_in_schema=True,
        tags=["metadata"],
    )
    async def capabilities(request: Request):
        return await capability_metadata(request)

    @router.route(
        VERIFIER_CONTRACT_METADATA_PATH,
        methods=["GET"],
        include_in_schema=True,
        tags=["metadata"],
    )
    async def verifier_contract(request: Request):
        return await verifier_contract_metadata(request)

    return router


def include_resource_validation_metadata(
    app: TigrblApp,
    router: TigrblRouter,
    *,
    enabled: bool,
) -> None:
    routes = getattr(getattr(app, "router", None), "routes", ())
    existing = {
        getattr(route, "path", None) or getattr(route, "path_template", None)
        for route in routes
    }
    if enabled and CAPABILITIES_METADATA_PATH not in existing:
        app.include_router(router)


__all__ = [
    "build_resource_validation_metadata_router",
    "include_resource_validation_metadata",
]
