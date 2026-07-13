# Package Layer Ownership

The numbered package directories declare semantic ownership. They are not
release phases and a package does not need to exist in every layer.

## Canonical responsibilities

| Layer | Responsibility | Must not own |
| --- | --- | --- |
| `00-primitives` | dependency-light values and deterministic utilities | domain implementations or integrations |
| `01-storage` | storage schemas and persistence primitives | application workflows |
| `02-contracts` | protocols, ports, enums, and transport-neutral contract values | concrete implementations |
| `05-bases` | reusable abstract bases and mixins implementing contract structure | deployable provider behavior |
| `10-concrete` | first concrete domain implementations | external integrations or application workflows |
| `20-providers` | concrete providers, algorithms, adapters, factories, and integrations | multi-provider application workflows |
| `30-storage-runtime` | composed repositories, persistence services, and storage-backed runtimes | protocol or product composition |
| `40-capabilities` | complete multi-component application use cases | single implementations, integrations, persistence, protocols, or app construction |
| `50-protocols` | OAuth, OIDC, credential, attestation, and event protocol behavior | process construction |
| `60-runtime` | dependency injection, process construction, runners, and runtime lifecycle | product API policy |
| `70-facade` | compatibility and ergonomic suite entry point | canonical lower-layer behavior |
| `80-apis` | product-specific API applications and surface composition | lower-layer implementation truth |

## Layer 40 decision rule

Layer 40 is optional and deliberately sparse. A package belongs there only if
removing it would eliminate a complete use case that coordinates multiple
layer-20 providers and/or layer-30 storage runtimes.

A layer-40 package may:

- express workflows using layer-02 contract values and ports;
- coordinate concrete layer-10 values, layer-20 providers, and layer-30 runtimes;
- enforce ordering, consent, replay, transaction, compensation, audit, and
  fail-closed workflow rules;
- return a complete application outcome.

A layer-40 package may not:

- inherit from or implement a type owned below layer 10;
- import layer-00 primitive internals or layer-01 storage implementations;
- inherit from layer-05 bases;
- own a single provider, algorithm, adapter, factory, or integration;
- access database tables or sessions directly;
- construct providers or processes;
- implement protocol transport or API routing.

Provider construction and external integration belong to layer 20. Composed
storage behavior belongs to layer 30. Whole-process dependency injection and
application construction belong to layer 60.

## Registered capabilities

The authoritative registry is `CAPABILITY_PURPOSES` in
`scripts/validate_layer_boundaries.py`. The current layer-40 packages are:

| Package | Complete use case |
| --- | --- |
| `tigrbl-attestation-appraisal` | coordinate evidence appraisal and result recording |
| `tigrbl-digital-credential-issuance` | coordinate configuration, wallet trust, offers, and issuance |
| `tigrbl-digital-credential-presentation` | coordinate consent, replay defense, and verification |
| `tigrbl-identity-admin-control-plane` | coordinate administrative resource lifecycle use cases |
| `tigrbl-security-events` | coordinate event transmission, receipt, and recording |
| `tigrbl-workload-identity` | coordinate workload credential retrieval and identity verification |

Adding a layer-40 package requires adding its multi-component use-case purpose
to the registry. The boundary validator rejects unregistered packages and stale
registrations.

## Continuous enforcement

Run:

```shell
python scripts/validate_layer_boundaries.py
pytest -q tests/unit/test_layer_40_capability_boundary.py
```

The validator checks live package metadata and Python ASTs. It rejects:

- prohibited layer-40 manifest dependencies;
- prohibited imports, including type-checking and function-local imports;
- direct inheritance from layers 00, 01, 02, or 05;
- unregistered layer-40 packages;
- stale capability registrations.

The general package-layer tests continue to verify that every package resides
in exactly one declared filesystem layer and that frontend workspaces remain
outside the Python dependency graph.
