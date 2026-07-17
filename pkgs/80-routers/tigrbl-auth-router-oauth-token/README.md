# tigrbl-auth-router-oauth-token

This layer-80 package owns the OAuth token endpoint HTTP carrier: the POST
route, request/database dependency injection, and the protocol response model.

It receives the layer-60 token-request processor by injection. It does not
authenticate clients, evaluate grants, issue tokens, open storage sessions, or
own token lifecycle state.
