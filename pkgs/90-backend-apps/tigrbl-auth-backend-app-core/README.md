# tigrbl-auth-backend-app-core

Shared layer-90 composition for deployable Tigrbl Auth backend applications.

This package owns ASGI application construction, layer-80 router closure, HTTP
surface assembly, administrative gate wrapping, and product-surface selection.
Product backend-app packages supply a declared product contract and call the
shared build_product_app factory.

It does not own protocol semantics, capability implementations, durable table
behavior, runtime handlers, or storage. Those remain in layers 50, 40, 30, and
60 and are injected or imported downward.