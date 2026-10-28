"""Tigrbl route binding for WebAuthn semantic operations."""

from __future__ import annotations

import inspect
from collections.abc import Callable

from tigrbl import Request, TigrblApp, TigrblRouter

from .schemas import (
    AuthenticationOptionsIn,
    PublicKeyCredentialIn,
    RegistrationOptionsIn,
    RenameCredentialIn,
)
from .serialization import parse_public_key_credential, to_json_value


async def _call(target: Callable[..., object], **kwargs: object) -> object:
    value = target(**kwargs)
    return await value if inspect.isawaitable(value) else value


def build_webauthn_router(
    *,
    begin_public_key_registration: Callable[..., object],
    complete_public_key_registration: Callable[..., object],
    begin_public_key_authentication: Callable[..., object],
    complete_public_key_authentication: Callable[..., object],
    list_public_key_credentials: Callable[..., object] | None = None,
    rename_public_key_credential: Callable[..., object] | None = None,
    revoke_public_key_credential: Callable[..., object] | None = None,
) -> TigrblRouter:
    router = TigrblRouter()

    @router.route("/webauthn/registration/options", methods=["POST"])
    async def registration_options(
        request: Request, body: RegistrationOptionsIn | None = None
    ):
        body = body or RegistrationOptionsIn.model_validate(await request.json() or {})
        result = await _call(
            begin_public_key_registration,
            request=request,
            user_name=body.user_name,
            display_name=body.display_name,
        )
        return to_json_value(result)

    @router.route("/webauthn/registration/complete", methods=["POST"])
    async def registration_complete(
        request: Request, body: PublicKeyCredentialIn | None = None
    ):
        body = body or PublicKeyCredentialIn.model_validate(await request.json() or {})
        result = await _call(
            complete_public_key_registration,
            request=request,
            credential=parse_public_key_credential(body),
        )
        return to_json_value(result)

    @router.route("/webauthn/authentication/options", methods=["POST"])
    async def authentication_options(
        request: Request, body: AuthenticationOptionsIn | None = None
    ):
        body = body or AuthenticationOptionsIn.model_validate(
            await request.json() or {}
        )
        result = await _call(
            begin_public_key_authentication,
            request=request,
            user_name=body.user_name,
            conditional=body.conditional,
        )
        return to_json_value(result)

    @router.route("/webauthn/authentication/complete", methods=["POST"])
    async def authentication_complete(
        request: Request, body: PublicKeyCredentialIn | None = None
    ):
        body = body or PublicKeyCredentialIn.model_validate(await request.json() or {})
        result = await _call(
            complete_public_key_authentication,
            request=request,
            credential=parse_public_key_credential(body),
        )
        return to_json_value(result)

    if list_public_key_credentials is not None:

        @router.route("/webauthn/credentials", methods=["GET"])
        async def credential_list(request: Request):
            return to_json_value(
                await _call(list_public_key_credentials, request=request)
            )

    if rename_public_key_credential is not None:

        @router.route("/webauthn/credentials/{credential_id}", methods=["PATCH"])
        async def credential_rename(
            request: Request, credential_id: str, body: RenameCredentialIn | None = None
        ):
            body = body or RenameCredentialIn.model_validate(await request.json() or {})
            return to_json_value(
                await _call(
                    rename_public_key_credential,
                    request=request,
                    credential_id=credential_id,
                    display_name=body.display_name,
                )
            )

    if revoke_public_key_credential is not None:

        @router.route("/webauthn/credentials/{credential_id}", methods=["DELETE"])
        async def credential_revoke(request: Request, credential_id: str):
            return to_json_value(
                await _call(
                    revoke_public_key_credential,
                    request=request,
                    credential_id=credential_id,
                )
            )

    return router


def include_webauthn_endpoints(
    app: TigrblApp, router: TigrblRouter, *, enabled: bool = True
) -> None:
    if enabled:
        app.include_router(router)


__all__ = ["build_webauthn_router", "include_webauthn_endpoints"]
