# tigrbl-workload-identity

Layer-40 orchestration for retrieving and verifying SPIFFE workload
credentials and resolving trust bundles.

## Injected dependencies

Required collaborators are `SvidProviderPort` and `SvidVerifierPort`. A
`TrustBundleProviderPort` and refresh callable are optional.

## Operations and readiness

Required operations are `fetch_x509_svid`, `fetch_jwt_svid`, and `verify_svid`.
Optional `resolve_bundle` and `refresh` operations are reported unavailable
when unbound. Compatibility helpers compose fetch plus verify but are not
separate registered operations.

## Protocol consumers

No dedicated layer-50 SPIFFE/SVID package exists yet; runtime consumers use
this capability directly. A future versioned SPIFFE package must map its Workload
API/profile revisions to these operations. OAuth/OIDC may consume verified
workload identity without treating an SVID as an access token.

## Non-goals

This package does not own the Workload API transport, certificates/JWT parsing,
trust-bundle storage, certificate path policy, refresh scheduling, or routes.
