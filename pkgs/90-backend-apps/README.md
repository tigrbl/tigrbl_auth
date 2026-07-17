# Layer 90: Backend Apps

This layer owns deployable backend applications. Distribution names use
`tigrbl-auth-backend-app-*` and Python import roots use
`tigrbl_auth_backend_app_*`.

Each package closes over one product surface: its mounted layer-80 routers,
app-local routers, tables, operations, local and global hooks, policy,
middleware, configuration, startup, and shutdown behavior. Apps may depend on
routers; routers may never depend on apps.

The existing `105-ui` directory is a sibling presentation layer. Backend apps
and browser applications share a composition tier but remain separate package
families and dependency graphs.
