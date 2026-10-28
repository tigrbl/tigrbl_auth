# tigrbl-digital-credential-presentation

Layer-40 orchestration for holder consent, replay reservation, presentation
verification, and durable transaction/result recording.

## Injected dependencies

Required collaborators are a `PresentationVerifierPort`, consent checker,
replay reserver, transaction recorder, and result recorder. Each collaborator
may be synchronous or asynchronous.

## Operations and readiness

Operations are `check_consent`, `reserve_replay`, `verify_presentation`,
`record_transaction`, `record_result`, and the composed `present` operation.
All are required; construction fails if any target is missing. `present`
records every attempt and outcome, including consent and replay rejection.

## Protocol consumers

Layer-50 OID4VP maps presentation requests/responses to this capability. HAIP
configures its permitted credential formats, bindings, and trust rules.

## Non-goals

This package does not parse OID4VP/VP wire formats, select disclosure, retain
claims, choose trust anchors, open sessions, or expose routes.
