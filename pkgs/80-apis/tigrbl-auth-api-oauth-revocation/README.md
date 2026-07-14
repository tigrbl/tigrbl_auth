# tigrbl-auth-api-oauth-revocation

This layer-80 package owns RFC 7009 HTTP form parsing, required-token
validation, disabled-feature translation, route construction, and mounting.
It receives the layer-50 service by injection and does not own persistence,
audit recording, token semantics, or deployment composition.
