from __future__ import annotations

from tigrbl_identity_contracts.rest import RevocationOut
from tigrbl_identity_server.framework import TigrblRouter
from tigrbl_identity_oauth.ops.revoke import revoke_request

api = TigrblRouter()
router = api


@api.route("/revoke", methods=["POST"], response_model=RevocationOut)
async def revoke(request):
    return await revoke_request(request=request)
