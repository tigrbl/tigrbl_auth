from __future__ import annotations

from tigrbl_auth.api.rest.schemas import RevocationOut
from tigrbl_auth.framework import TigrblRouter
from tigrbl_auth.ops.revoke import revoke_request

api = TigrblRouter()
router = api


@api.route("/revoke", methods=["POST"], response_model=RevocationOut)
async def revoke(request):
    return await revoke_request(request=request)
