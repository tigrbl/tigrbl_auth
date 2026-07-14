# tigrbl-token-issuance-capability

This layer-40 package coordinates two required delegated operations:
`issue_token_pair` and `redeem_refresh_token`. It reports readiness from those
bindings and can delegate lifecycle audit recording through an optional third
operation.

It does not parse OAuth requests, authenticate clients, select grants, sign
tokens, open storage sessions, or choose token profiles. Layer 50 maps protocol
operations; layer 60 injects signing and request-scoped durable composition;
layer 80 owns HTTP.
