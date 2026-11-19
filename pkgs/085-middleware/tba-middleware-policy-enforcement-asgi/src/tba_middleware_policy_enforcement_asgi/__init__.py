class PolicyEnforcementMiddleware:
    def __init__(self, app, decide):
        self.app, self.decide = app, decide
    async def __call__(self, scope, receive, send):
        if scope.get("type") == "http" and not self.decide(scope).get("allowed", False):
            await send({"type": "http.response.start", "status": 403, "headers": []})
            await send({"type": "http.response.body", "body": b"Forbidden"})
            return
        await self.app(scope, receive, send)

__all__ = ["PolicyEnforcementMiddleware"]
