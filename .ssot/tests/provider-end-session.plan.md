# Provider end-session

Planned acceptance. Each tier requires a recorded run against the candidate revision.

Governed by spc:1237.

## T0

Verify hint and client binding, exact registered return matching, confirmation decisions, and eligible recent-session hints.

## T1

Extend the registered OIDC conformance test and mount the runtime through the logout router. Verify selected-session revocation and preservation of the other scope, cancellation, repeated logout, and storage failure.

## T2

Use a browser and a synthetic provider and relying party with two independent session scopes. Prove GET and cross-site POST logout, exact registered return including opaque state, preserved unrelated session, and sign-in as a different subject. Verify the package revision from isolated installed artifacts.
