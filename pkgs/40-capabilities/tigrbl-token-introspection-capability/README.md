# tigrbl-token-introspection-capability

This layer-40 package exposes one composable operation:
`token.introspection:introspect_token`.

The capability accepts a typed `TokenIntrospectionRequest`, delegates durable
lookup to an injected callable, and returns `TokenIntrospectionResult`. The
injected callable may be synchronous or asynchronous and must return either a
typed result or a mapping containing `active` plus normalized token claims.

Readiness requires the `introspect_token` target to be bound at construction.
The capability does not parse HTTP, authenticate an OAuth client, choose RFC
7662 errors, open a database/session, verify token cryptography, or publish a
route. OAuth maps this capability into its versioned protocol at layer 50 and a
layer-80 API owns the carrier binding.
