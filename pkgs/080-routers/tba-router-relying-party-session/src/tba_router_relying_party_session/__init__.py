ROUTES = ("/v1/rp/login", "/v1/rp/callback", "/v1/rp/session", "/v1/rp/refresh", "/v1/rp/step-up", "/v1/rp/logout", "/health")
SECURE_COOKIE = {"httponly": True, "secure": True, "samesite": "lax"}
MUTATION_ROUTES = frozenset({"/v1/rp/refresh", "/v1/rp/step-up", "/v1/rp/logout"})

def require_csrf(path: str, cookie_token: str | None, header_token: str | None) -> None:
    if path in MUTATION_ROUTES and (not cookie_token or cookie_token != header_token):
        raise PermissionError("CSRF validation failed")

__all__ = ["MUTATION_ROUTES", "ROUTES", "SECURE_COOKIE", "require_csrf"]
