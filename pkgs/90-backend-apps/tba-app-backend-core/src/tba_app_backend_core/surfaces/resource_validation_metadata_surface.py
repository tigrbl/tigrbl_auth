"""Runtime composition for resource-validation metadata carriers."""

from tigrbl import TigrblApp
from tba_router_resource_validation_metadata import (
    build_resource_validation_metadata_router,
    include_resource_validation_metadata as include_metadata_carrier,
)
from tba_runtime_identity.deployment import deployment_from_app
from tba_runtime_identity.settings import settings

from tba_server_identity.resource_validation_metadata_runtime import (
    capability_metadata,
    verifier_contract_metadata,
)


router = build_resource_validation_metadata_router(
    capability_metadata=capability_metadata,
    verifier_contract_metadata=verifier_contract_metadata,
)
api = router


def include_resource_validation_metadata(app: TigrblApp) -> None:
    deployment = deployment_from_app(app, settings)
    include_metadata_carrier(
        app,
        router,
        enabled=deployment.product_surface == "resource-validation-app",
    )


__all__ = ["api", "include_resource_validation_metadata", "router"]
