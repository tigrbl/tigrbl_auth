"""HTTP binding for native WIMSE WIC issuance."""

from collections.abc import Awaitable, Callable

from tigrbl import JSONResponse, Request, TigrblRouter
from tigrbl.runtime.status import HTTPException

from tba_runtime_identity.workload.wic_service import WicIssuanceService

from .schemas import WicIssueRequest, WicIssueResponse


def build_wic_ca_router(
    *,
    service: WicIssuanceService,
    authenticate: Callable[[Request], Awaitable[str | None]],
) -> TigrblRouter:
    router = TigrblRouter()

    @router.route("/wic/issue", methods=["POST"], response_model=WicIssueResponse)
    async def issue(request: Request):
        principal = await authenticate(request)
        if not principal:
            raise HTTPException(401, "workload authentication required")
        try:
            body = WicIssueRequest.model_validate(await request.json())
            if not body.csr_pem.startswith("-----BEGIN "):
                raise ValueError("expected a PEM CSR")
            certificate = await service.issue(principal, body.csr_pem.encode("ascii"))
            payload = WicIssueResponse(certificate_pem=certificate.decode("ascii"))
        except PermissionError as exc:
            raise HTTPException(403, "workload issuance denied") from exc
        except ValueError as exc:
            raise HTTPException(400, "invalid workload credential request") from exc
        return JSONResponse(payload.model_dump(), headers={"Cache-Control": "no-store"})

    return router
