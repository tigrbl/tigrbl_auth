# Provider end-session

Planned acceptance. Each tier requires a recorded run against the candidate revision.

Governed by spc:1237.

## T0

Table-test issuer, client, verified hint and session binding, current and recent sessions, confirmation, and byte-exact registered return matching.

## T1

Mount the actual router and runtime with durable adapter fixtures. Exercise GET and cross-site POST handoff, cancellation, idempotent completion, revocation failure and preservation of unrelated sessions.

## T2

From installed packages, use a synthetic provider and relying party with two browser scopes. Assert the exact return and state, preserve the other scope, and sign in as a different subject.
