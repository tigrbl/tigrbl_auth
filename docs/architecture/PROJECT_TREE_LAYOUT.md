> [!WARNING] Non-authoritative active document. For current release and certification truth, use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports.

<!-- NON_AUTHORITATIVE_HISTORICAL -->
> [!WARNING]
> Historical / non-authoritative checkpoint document.
> Do **not** use this file to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

> [!WARNING] Historical / non-authoritative document. This file is retained for provenance or implementation context only. Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports for current release truth.

> **Historical / non-authoritative** — This document is retained for planning or provenance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# Project Tree Layout

The repository is normalized around a Tigrbl-native, certification-native package tree.

```text
docs/{adr,architecture,standards,compliance,runbooks}
compliance/{targets,mappings,claims,evidence,gates,waivers}
specs/{openapi,openrpc,jsonschema}
scripts/
tests/{unit,integration,conformance,interop,negative,security,e2e,perf,examples}
tba_auth/{plugin,gateway,api,tables,ops,services,standards,security,config,adapters,schemas,migrations,cli}
```

Legacy paths remain in the repository only as `legacy_transition` artifacts until they are fully replaced.
