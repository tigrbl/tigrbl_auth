"""Compose the native WIT issuer with deployment-owned enrollment policy."""

from collections.abc import Awaitable, Callable, Mapping
from time import time

from tigrbl import Request, TigrblApp
from tba_provider_jose_cryptography.jws import ProtectedEnvelopeIssuerPort
from tba_router_wit_issuance import build_wit_issuance_router
from tba_runtime_identity.workload.enrollment import ResolveWorkloadIdentity
from tba_runtime_identity.workload.wit_token_service import (
    WitIssuerConfig,
    WitTokenService,
)


def build_app(
    settings: WitIssuerConfig,
    *,
    signer: ProtectedEnvelopeIssuerPort,
    authenticate: Callable[[Request], Awaitable[str | None]],
    resolve_identity: ResolveWorkloadIdentity,
    authorize_confirmation_key: Callable[[str, Mapping[str, object]], Awaitable[bool]],
    clock: Callable[[], float] = time,
) -> TigrblApp:
    service = WitTokenService(
        signer,
        settings,
        resolve_identity=resolve_identity,
        authorize_confirmation_key=authorize_confirmation_key,
        clock=clock,
    )
    app = TigrblApp()
    app.include_router(
        build_wit_issuance_router(service=service, authenticate=authenticate)
    )
    return app
