<!-- NON_AUTHORITATIVE_HISTORICAL -->

> [!WARNING]
> Historical checkpoint / planning note — non-authoritative for the current release.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` for current release truth.

> [!WARNING] Historical / non-authoritative document. This file is retained for provenance or implementation context only. Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports for current release truth.

> **Historical / non-authoritative** — This document is retained for planning or provenance only.
> Do **not** use it to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# public-route checkpoint — Baseline Interoperable Auth Server

This checkpoint promotes the baseline OAuth2 / OIDC / JOSE release path into
`standards/*`, finalizes `/authorize`, `/token`, JWKS, OIDC discovery, and
Authorization Server metadata in the target tree, and generates the first real
OpenAPI public contract.

Completed in this checkpoint:
- baseline OAuth2 modules promoted into `tigrbl_auth/standards/oauth2/*`
- baseline OIDC modules promoted into `tigrbl_auth/standards/oidc/*`
- baseline JOSE modules promoted into `tigrbl_auth/standards/jose/*`
- finalized release-path `/authorize`, `/token`, `/userinfo`, discovery, JWKS,
  and authorization-server metadata surfaces under the target tree
- enforced PKCE, redirect URI, state / nonce / issuer baseline behavior in the
  release-path authorize and token flows
- generated `specs/openapi/tigrbl_auth.public.openapi.json`
- initialized `tests/conformance/baseline/` with migrated baseline tests

Honest status:
- baseline implementation work is now present in the target tree
- OpenRPC, Tier 3 evidence, advanced protocol profiles, and independent peer
  validation remain incomplete
