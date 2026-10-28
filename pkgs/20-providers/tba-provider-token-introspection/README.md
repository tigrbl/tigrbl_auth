# tba-provider-token-introspection

Layer-20 provider implementing `TokenIntrospectionClientBase`. It converts an
injected token-introspection transport's responses into typed introspection
results and access-token claims. The transport is supplied by the caller; this
package owns the provider adapter, not a general-purpose HTTP client.
