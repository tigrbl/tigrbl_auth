# tigrbl-capability

Layer-10 neutral `Capability`. Authors provide a `CapabilityDefinition` and one
mapping of names to `CapabilityOperation` objects. Required operations must have
callable targets at construction. Optional operations may be present without a
target and are reported as unavailable. State is supplied as a fixed
`CapabilityState` or a live state provider.

The package has no implicit providers, persistence, policies, retries, timeouts,
namespaces, or environment-derived settings.
