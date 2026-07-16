# tigrbl-attestation-appraisal

Layer-40 orchestration for verifying attestation evidence, resolving reference
material, appraising verified evidence, and recording appraisal results.

## Injected dependencies

Required: `EvidenceVerifierPort` and `AttestationAppraiserPort`. Optional:
`ReferenceMaterialProviderPort` and a durable result-recorder callable.

## Operations and readiness

Required operations are `verify_evidence` and `appraise`. Optional operations
are `resolve_reference_material` and `record_result`; the capability report
marks either unavailable when its collaborator is absent. Raw evidence is
never passed to the appraiser before successful verification.

## Protocol consumers

Layer-50 EAT, CoRIM, and HAIP packages consume these operations when their
selected profiles require evidence appraisal or reference material.

## Non-goals

This package does not parse EAT/CoRIM wire artifacts, choose trust anchors,
store evidence/results, open sessions, or expose transports.
