import asyncio

from tba_middleware_policy_enforcement_asgi import PolicyEnforcementMiddleware


async def protected(scope, receive, send):
    raise AssertionError("a denied request reached the app")


messages = []


async def send(message):
    messages.append(message)


async def receive():
    raise AssertionError("a denied request read the body")


middleware = PolicyEnforcementMiddleware(protected, lambda scope: {"allowed": False})
asyncio.run(middleware({"type": "http"}, receive, send))
assert messages[0]["status"] == 403
assert messages[1]["body"] == b"Forbidden"
