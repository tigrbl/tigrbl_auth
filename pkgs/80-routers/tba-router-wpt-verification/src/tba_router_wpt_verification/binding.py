"""Delegate WIT/WPT authentication for one deployment-configured recipient."""

from collections.abc import Awaitable, Callable

from tigrbl import JSONResponse, Request, TigrblRouter
from tba_concrete_jwt import decode_jwt_unverified
from tba_profile_workload_proof_wimse_wpt import (
    WptProofVerifier,
    normalize_wpt_audience,
)

from .schemas import WptVerificationRequest, WptVerificationResponse


def build_wpt_verification_router(
    *,
    verifier: WptProofVerifier,
    audience: str,
    authenticate: Callable[[Request], Awaitable[str | None]],
    authorize_verification: Callable[[str], Awaitable[bool]],
    bound_token_headers: tuple[str, ...] = (),
) -> TigrblRouter:
    """Authenticate the delegating service before consuming any proof replay state.

    The caller must forward the original request's WIT, WPT and token headers,
    including duplicates. It uses the returned identity for that request once;
    this is not a non-consuming token-inspection endpoint.
    """
    recipient = normalize_wpt_audience(audience)
    required = tuple(name.lower() for name in bound_token_headers)
    if any(name in {"authorization", "workload-identity-token"} for name in required):
        raise ValueError("credential headers cannot be additional token bindings")
    router = TigrblRouter()

    def reject(status: int, detail: str):
        return JSONResponse(
            {"detail": detail},
            status_code=status,
            headers={"Cache-Control": "no-store"},
        )

    @router.route(
        "/wpt/verify", methods=["POST"], response_model=WptVerificationResponse
    )
    async def verify(request: Request):
        principal = await authenticate(request)
        if not principal:
            return reject(401, "verification caller authentication required")
        if await authorize_verification(principal) is not True:
            return reject(403, "verification caller is not authorized")
        try:
            body = WptVerificationRequest.model_validate(await request.json())
            if any(
                header.name.lower() in {"authorization", "workload-identity-token"}
                for header in body.token_headers
            ):
                raise ValueError("credential header in token headers")
        except (ValueError, TypeError):
            return reject(400, "invalid proof verification request")
        headers = [
            ("Workload-Identity-Token", body.workload_identity_token),
            ("Authorization", f"WPT {body.workload_proof_token}"),
            *((header.name, header.value) for header in body.token_headers),
        ]
        try:
            wit = verifier.authenticate_request(
                headers, audience=recipient, bound_token_headers=required
            )
        except (ValueError, TypeError, KeyError, UnicodeError):
            return reject(401, "workload proof verification failed")
        # authenticate_request has verified this proof and reserved its replay
        # identifier. Decoding the same token here does not verify it a second time.
        claims = decode_jwt_unverified(body.workload_proof_token).claims
        payload = WptVerificationResponse(
            valid=True,
            subject=wit.claims["sub"],
            audience=recipient,
            proof_id=claims["jti"],
            expires_at=claims["exp"],
        )
        return JSONResponse(payload.model_dump(), headers={"Cache-Control": "no-store"})

    return router
