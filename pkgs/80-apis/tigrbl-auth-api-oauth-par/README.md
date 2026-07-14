# tigrbl-auth-api-oauth-par

HTTP carrier binding for OAuth 2.0 Pushed Authorization Requests (RFC 9126).

This package owns request decoding, `/par` routing, HTTP error mapping, and
response serialization. It receives normalization, client authentication,
durability, and observation collaborators from runtime composition.
