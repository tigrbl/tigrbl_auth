"""A remote verifier with explicit caller policy and shared atomic replay storage."""

from collections.abc import Awaitable, Callable
from time import time

from tigrbl import Request, TigrblApp
from tba_contracts_replay import ReplayCheckPort
from tba_profile_workload_proof_wimse_wpt import WptProofVerifier
from tba_router_wpt_verification import build_wpt_verification_router

from .settings import WptVerifierSettings


def build_app(
    settings: WptVerifierSettings,
    *,
    replay_store: ReplayCheckPort,
    authenticate: Callable[[Request], Awaitable[str | None]],
    authorize_verification: Callable[[str], Awaitable[bool]],
    clock: Callable[[], float] = time,
) -> TigrblApp:
    verifier = WptProofVerifier(
        trust_by_domain=settings.trust_by_domain, replay_store=replay_store, clock=clock
    )
    app = TigrblApp()
    app.include_router(
        build_wpt_verification_router(
            verifier=verifier,
            audience=settings.audience,
            authenticate=authenticate,
            authorize_verification=authorize_verification,
            required_token_headers=settings.required_token_headers,
        )
    )
    return app
