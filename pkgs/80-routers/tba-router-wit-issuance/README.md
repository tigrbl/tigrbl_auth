# tba-router-wit-issuance

Mount `build_wit_issuance_router(service=..., authenticate=...)` on a Tigrbl app.
`POST /wit/issue` accepts JSON with `confirmation_jwk` and returns
`workload_identity_token`. The async authenticator supplies a trusted enrollment
principal. Construct `WitTokenService` with a configured signer, identity
resolver, and confirmation-key authorizer. The authorizer must bind the
presented public key to that principal, for example through a registered key
or an authenticated enrollment proof.
