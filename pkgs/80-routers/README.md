# Layer 80: Routers

This layer owns reusable Tigrbl HTTP routers. Distribution names use
`tigrbl-auth-router-*` and Python import roots use `tigrbl_auth_router_*`.

A router package closes over the smallest independently mountable carrier
surface. It may expose one operation or table, or a cohesive combination of
operations, tables, schemas, serialization, error mapping, and router-local
hooks. It delegates semantic behavior to lower layers and does not construct a
deployable backend product.

Routers may be consumed by backend apps. Routers must never depend on or import
packages from `90-backend-apps`.
