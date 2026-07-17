# tigrbl-auth-router-oauth-introspection

This layer-80 package owns the RFC 7662 HTTP carrier: POST form parsing,
required-token validation, transport-policy invocation, authenticated-caller
invocation, protocol-error translation, route construction, and mounting.

It receives the layer-50 `RFC7662IntrospectionService` and runtime-owned
collaborators by injection. It does not open storage sessions, look up clients,
verify client credentials, own token state, or implement token activity rules.
