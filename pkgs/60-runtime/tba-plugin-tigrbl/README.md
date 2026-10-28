# tba-plugin-tigrbl

Standalone `TbaPlugin` package for the TBA package suite.

- Package: `tba-plugin-tigrbl`
- Import root: `tba_plugin_tigrbl`
- Owns `TbaPlugin` and the `install()` convenience function.
- Installs TBA runtime surfaces into an existing `TigrblApp`.
- `tba_server_identity.plugin` and `tba_auth.plugin` are compatibility wrappers.

## Adoption Option

`TbaPlugin` is one adoption option for downstream applications that already own a `TigrblApp` and want to mount the identity provider surfaces into that app. Other adoption options remain valid: build a complete provider app through `tba-server-identity`, build a gateway through `tba-server-identity`, or run those app factories through `tba-runtime-identity`.

```python
from tba_plugin_tigrbl import TbaPlugin

plugin = TbaPlugin(settings=settings)
plugin.install(app)
```
