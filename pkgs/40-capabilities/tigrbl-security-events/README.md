# tigrbl-security-events

Layer-40 orchestration for security-event transmission, receipt, durable
recording, subscription authorization, delivery history, and replay defense.

## Injected dependencies

Required collaborators are transmitter/receiver ports plus event recorder,
subscription resolver, delivery recorder, and replay reserver callables. All
may be synchronous or asynchronous; durable callables normally adapt layer 30.

## Operations and readiness

Operations are `record_event`, `resolve_subscription`, `record_delivery`,
`reserve_replay`, `transmit`, and `receive`. All are required. Transmission
checks the subscription and records delivery; receipt reserves replay state
before recording the event.

## Protocol consumers

The layer-50 SET package maps RFC 8417 event tokens and delivery semantics to
this capability. Shared-signals profiles may compose the same operations.

## Non-goals

This package does not encode/decode SETs, choose endpoints or transport,
resolve signing keys/trust, own tables, or expose HTTP.
