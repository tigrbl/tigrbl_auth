# tigrbl-auth-plugin

Standalone `TigrblAuthPlugin` package for the Tigrbl auth package suite.

- Package: `tigrbl-auth-plugin`
- Import root: `tigrbl_auth_plugin`
- Owns `TigrblAuthPlugin` and the `install()` convenience function.
- Installs Tigrbl auth runtime surfaces into an existing `TigrblApp`.
- `tigrbl_identity_server.plugin` and `tigrbl_auth.plugin` are compatibility wrappers.

## Adoption Option

`TigrblAuthPlugin` is one adoption option for downstream applications that already own a `TigrblApp` and want to mount the identity provider surfaces into that app. Other adoption options remain valid: build a complete provider app through `tigrbl-identity-server`, build a gateway through `tigrbl-identity-server`, or run those app factories through `tigrbl-identity-runtime`.

```python
from tigrbl_auth_plugin import TigrblAuthPlugin

plugin = TigrblAuthPlugin(settings=settings)
plugin.install(app)
```
