# tigrbl-auth-router-oidc-userinfo

HTTP carrier binding for the OpenID Connect UserInfo endpoint.

This package owns the GET route and dependency materialization. Bearer-token
validation, subject lookup, claim selection, signing, deployment policy, and
durability are injected by runtime composition.
