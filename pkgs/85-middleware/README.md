# Middleware adapters

Layer 85 contains middleware that wraps applications and enforces request-level
behavior. It sits above clients (75) and routers (80), below application
composition (90).

The current ASGI policy enforcement adapter depends on an injected decision
function and declares the policy decision client as a dependency. The layer
allows primitives, contracts, clients, and middleware. Concrete router and
backend application dependencies are forbidden. Backend applications may
compose clients, routers, and middleware.
