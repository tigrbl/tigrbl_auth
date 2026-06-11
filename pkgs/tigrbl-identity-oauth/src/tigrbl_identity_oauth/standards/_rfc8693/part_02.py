@api.route("/token/exchange", methods=["POST"])
async def token_exchange_endpoint(
    request: Request,
    dpop: str | None = Header(None, alias="DPoP"),
):
    """RFC 8693 token exchange endpoint."""

    if not runtime_cfg.settings.enable_rfc8693:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "token exchange disabled")

    jkt: str | None = None
    dpop_header = _header_value(dpop)
    if dpop_header:
        try:
            jkt = verify_proof(dpop_header, request.method, str(request.url))
        except ValueError as exc:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, str(exc)) from exc

    raw_body = request.body.decode("utf-8") if getattr(request, "body", b"") else ""
    form_data = parse_qs(raw_body, keep_blank_values=True)

    def _one(name: str, *, required: bool = False) -> str | None:
        values = form_data.get(name) or []
        value = values[0] if values else None
        if required and not value:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, f"missing {name}")
        return value

    token_request = validate_token_exchange_request(
        grant_type=_one("grant_type", required=True),
        subject_token=_one("subject_token", required=True),
        subject_token_type=_one("subject_token_type", required=True),
        actor_token=_one("actor_token"),
        actor_token_type=_one("actor_token_type"),
        audience=_one("audience"),
        scope=_one("scope"),
    )
    response = exchange_token(token_request, issuer="token-exchange", jkt=jkt)
    return response.to_dict()


def makeImpersonationToken(
    subject_token: str,
    actor_token: str,
    *,
    audience: Optional[str] = None,
    scope: Optional[str] = None,
) -> TokenExchangeResponse:
    """Create an impersonation token per RFC 8693 Section 2.1.

    Args:
        subject_token: Token of the user being impersonated
        actor_token: Token of the user performing impersonation
        audience: Target audience for the token
        scope: Requested scope

    Returns:
        TokenExchangeResponse with impersonation token
    """
    if not runtime_cfg.settings.enable_rfc8693:
        raise RuntimeError("RFC 8693 support disabled")

    request = TokenExchangeRequest(
        grant_type=TOKEN_EXCHANGE_GRANT_TYPE,
        subject_token=subject_token,
        subject_token_type=TokenType.ACCESS_TOKEN.value,
        actor_token=actor_token,
        actor_token_type=TokenType.ACCESS_TOKEN.value,
        audience=audience,
        scope=scope,
    )

    request.validate()
    return exchange_token(request, issuer="impersonation-service")


def makeDelegationToken(
    subject_token: str,
    *,
    audience: Optional[str] = None,
    scope: Optional[str] = None,
) -> TokenExchangeResponse:
    """Create a delegation token per RFC 8693 Section 2.2.

    Args:
        subject_token: Token to be delegated
        audience: Target audience for the token
        scope: Requested scope (typically narrower than original)

    Returns:
        TokenExchangeResponse with delegation token
    """
    if not runtime_cfg.settings.enable_rfc8693:
        raise RuntimeError("RFC 8693 support disabled")

    request = TokenExchangeRequest(
        grant_type=TOKEN_EXCHANGE_GRANT_TYPE,
        subject_token=subject_token,
        subject_token_type=TokenType.ACCESS_TOKEN.value,
        audience=audience,
        scope=scope,
    )

    request.validate()
    return exchange_token(request, issuer="delegation-service")


def create_impersonation_token(
    subject_token: str,
    actor_token: str,
    *,
    audience: Optional[str] = None,
    scope: Optional[str] = None,
) -> TokenExchangeResponse:
    warnings.warn(
        "create_impersonation_token is deprecated, use makeImpersonationToken",
        DeprecationWarning,
        stacklevel=2,
    )
    return makeImpersonationToken(
        subject_token,
        actor_token,
        audience=audience,
        scope=scope,
    )


def create_delegation_token(
    subject_token: str,
    *,
    audience: Optional[str] = None,
    scope: Optional[str] = None,
) -> TokenExchangeResponse:
    warnings.warn(
        "create_delegation_token is deprecated, use makeDelegationToken",
        DeprecationWarning,
        stacklevel=2,
    )
    return makeDelegationToken(
        subject_token,
        audience=audience,
        scope=scope,
    )


__all__ = [
    "TokenExchangeRequest",
    "TokenExchangeResponse",
    "TokenType",
    "validate_token_exchange_request",
    "validate_subject_token",
    "exchange_token",
    "makeImpersonationToken",
    "makeDelegationToken",
    "create_impersonation_token",
    "create_delegation_token",
    "TOKEN_EXCHANGE_GRANT_TYPE",
    "RFC8693_SPEC_URL",
    "include_rfc8693",
    "api",
    "router",
]
