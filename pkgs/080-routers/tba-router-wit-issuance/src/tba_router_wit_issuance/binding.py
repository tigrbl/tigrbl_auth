"""HTTP binding for native WIMSE WIT issuance."""

from collections.abc import Awaitable, Callable

from tigrbl import JSONResponse, Request, TigrblRouter
from tigrbl.runtime.status import HTTPException

from tba_runtime_identity.workload.wit_token_service import WitTokenService

from .schemas import WitIssueRequest, WitIssueResponse


def build_wit_issuance_router(
    *,
    service: WitTokenService,
    authenticate: Callable[[Request], Awaitable[str | None]],
) -> TigrblRouter:
    router = TigrblRouter()

    @router.route("/wit/issue", methods=["POST"], response_model=WitIssueResponse)
    async def issue(request: Request):
        principal = await authenticate(request)
        if not principal:
            raise HTTPException(401, "workload authentication required")
        try:
            body = WitIssueRequest.model_validate(await request.json())
            token = await service.issue(principal, body.confirmation_jwk)
            payload = WitIssueResponse(workload_identity_token=token)
        except PermissionError as exc:
            raise HTTPException(403, "workload issuance denied") from exc
        except ValueError as exc:
            raise HTTPException(400, "invalid workload credential request") from exc
        return JSONResponse(payload.model_dump(), headers={"Cache-Control": "no-store"})

    return router
