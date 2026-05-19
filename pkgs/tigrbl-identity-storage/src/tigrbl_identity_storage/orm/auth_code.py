"""Legacy import facade for canonical table module ``tigrbl_auth.tables.auth_code``."""

from tigrbl_auth.api.rest.shared import _jwt
from tigrbl_auth.rfc.rfc7636_pkce import verify_code_challenge
from tigrbl_auth.standards.oidc.id_token import mint_id_token
from tigrbl_auth.tables.auth_code import AuthCode


async def _exchange(ctx: dict, auth_code: AuthCode):
    payload = dict(ctx.get("payload") or {})
    if auth_code.code_challenge and not verify_code_challenge(
        payload.get("code_verifier", ""),
        auth_code.code_challenge,
    ):
        raise ValueError("invalid code_verifier")
    access, refresh = await _jwt.async_sign_pair(
        sub=str(auth_code.user_id),
        tid=str(auth_code.tenant_id),
    )
    id_token = await mint_id_token(
        sub=str(auth_code.user_id),
        aud=str(auth_code.client_id),
        nonce=str(auth_code.nonce or ""),
        issuer="https://authn.example.com",
    )
    delete_core = getattr(AuthCode.handlers.delete, "core", None)
    if callable(delete_core):
        await delete_core(auth_code)
    return {"access_token": access, "refresh_token": refresh, "id_token": id_token}


if not hasattr(AuthCode, "exchange"):
    setattr(AuthCode, "exchange", staticmethod(_exchange))

__all__ = ["AuthCode", "_jwt", "mint_id_token"]
