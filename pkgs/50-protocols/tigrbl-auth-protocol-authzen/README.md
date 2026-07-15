# tigrbl-auth-protocol-authzen

Layer-50 owner for OpenID AuthZEN Authorization API 1.0 and its superseded
draft/Implementer’s Draft history.

The package owns version selection, feature gates, lossless configuration
migrations, AuthZEN entity/message schemas, protocol errors, and the explicit
mapping from wire operations to `policy.evaluation` and
`artifact.processing` capabilities.

It intentionally declares an empty protocol claim class set: AuthZEN exchanges
policy entities and decisions rather than a registered token claim set. Signed
PDP metadata uses the separately owned JWT artifact processing capability.

## Non-goals

This package does not implement policy decisions, own policy data, construct
providers, authenticate API callers, open sessions, or mount HTTP routes.
