# OAuth and GNAP protocol boundary

| Package | Owns | Supported import |
| --- | --- | --- |
| `tba-protocol-oauth` | OAuth authorization, token exchanges, dynamic client registration, and OAuth extension processing | `tba_protocol_oauth` |
| `tba-protocol-gnap` | GNAP grant requests, interaction and continuation, and GNAP-specific wire processing | `tba_protocol_gnap` |

Each protocol package is independently distributable. Its base distribution and
extras exclude the other protocol and its legacy package names. Both packages
may depend on neutral identity contracts and reusable capabilities. Runtime
packages that serve both protocols declare both dependencies explicitly and own
the composition. A runtime's dependency on both packages belongs at that runtime
boundary, outside either protocol package.

Use each protocol's native request and response types at the wire boundary.
Adapters that map data between protocols belong in an explicit integration
layer. GNAP callers moving off the removed `tba_protocol_oauth.standards.gnap`
shim should install `tba-protocol-gnap` and import from `tba_protocol_gnap`.

The SSOT boundary is `bnd:oauth-gnap-protocol-independence`. Its regression
checks Python imports, manifest dependencies and extras, and the transitive
workspace lock graph in both directions. Built-wheel checks should install one
protocol into a clean environment and prove its peer is absent.

[OAuth 2.0 (RFC 6749)](https://www.rfc-editor.org/rfc/rfc6749.html) ·
[GNAP (RFC 9635)](https://www.rfc-editor.org/rfc/rfc9635.html)
