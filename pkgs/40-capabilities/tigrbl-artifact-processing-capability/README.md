# tigrbl-protocol-artifact-processing

Layer-40 protocol-neutral orchestration for encoded artifact processing through
an injected processor.

## Injected dependencies

A required `ArtifactProcessorPort` supplies deterministic decode, validate,
encode, and error-mapping behavior. Provider health/status attributes are read
only for effective reporting.

## Operations and readiness

Operations are `decode`, `validate`, `encode`, and `map_error`. Readiness is
derived from the complete bound required-operation set; health and status are
derived from the processor instead of being hard-coded.

## Protocol consumers

Any layer-50 protocol package may map a concrete artifact profile to these
operations. Its requirement rows must name the actual operation rather than a
generic catch-all validation claim.

## Non-goals

This package does not own wire schemas, revisions, keys, trust anchors,
persistence, HTTP, or deployment settings.
