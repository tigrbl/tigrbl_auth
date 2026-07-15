# tigrbl-policy-evaluation-capability

Layer-40 protocol-neutral composition for policy evaluation, batch evaluation,
entity search, and effective policy-service description.

## Injected dependencies

A policy evaluation callable is required. Entity search and service-description
callables are optional. The targets are supplied by layer-10/20 implementations
or layer-60 composition; this package does not construct an evaluator.

## Operations and readiness

`evaluate` is required. `evaluate_many` is available as an order-preserving
composition of `evaluate`. `search_entities` and `describe` are optional and
are reported unavailable when their targets are not bound. Readiness follows
the required evaluation target.

## Protocol consumers

The layer-50 AuthZEN package maps Authorization API 1.0 evaluation, batch,
search, and PDP-metadata requirements to these operations. XACML adapters may
consume the same normalized capability through their own versioned mappings.

## Non-goals

This package does not parse AuthZEN or XACML messages, choose HTTP paths,
authenticate callers, own policy state, open sessions, or implement a policy
decision algorithm.
