# tigrbl-principal-authentication

Layer-40 orchestration for record-backed password, client-secret, API-key, and
service-key authentication.

## Injected dependencies

Password/client capabilities receive durable lookup callables and layer-20
authenticators. API-key authentication receives user/service-key lookup,
principal resolution, and last-used mutation callables plus replaceable
layer-20 key authenticators.

## Operations and readiness

Operations are `authenticate_password`, `authenticate_client_secret`,
`verify_client_record`, and `authenticate_api_key`, split across three focused
capabilities. Each capability is ready when its constructor-required targets
are bound; required missing targets fail construction.

## Protocol consumers

Layer-50 OAuth and OIDC consume these capabilities for selected client and
end-user authentication methods. GNAP may consume the normalized principal
authentication result when configured.

## Non-goals

This package does not own credential tables, hashes, protocol method selection,
session creation, routes, or authentication policy.
