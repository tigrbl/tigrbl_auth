<!-- NON_AUTHORITATIVE_HISTORICAL -->
> [!WARNING]
> Historical / non-authoritative checkpoint document.
> Do **not** use this file to determine the current certification state, executable surface, or release readiness.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and `CERTIFICATION_STATUS.md` instead.

# Certification Boundary

This document declares the authoritative certification boundary for the current `tba_auth` checkpoint.

## Authority

- Canonical scope manifest: `compliance/targets/certification_scope.yaml`
- Repository tier: `3`
- Fully certifiable now: `False`
- Fully RFC compliant now: `False`

## Scope buckets

### baseline-certifiable-now

- Count: `12`
- Meaning: Baseline certification candidate set. This is a scope bucket, not a Tier 3 or Tier 4 promotion.

### production-completion-required

- Count: `14`
- Meaning: In-scope production RFC/OIDC targets that still require route, persistence, runtime, or evidence completion.

### hardening-completion-required

- Count: `13`
- Meaning: In-scope hardening RFC/OIDC targets that still require runtime enforcement, public surface completion, or evidence completion.

### runtime-completion-required

- Count: `4`
- Meaning: In-scope ASGI application and runner-profile targets required before the package can truthfully claim a fully featured runtime boundary.

### operator-completion-required

- Count: `5`
- Meaning: In-scope CLI/operator/release targets required before the package can truthfully claim a fully featured package boundary.

## Why this file exists

The repository uses this artifact to keep targets, claims, active routes, contracts, tests, and evidence planning aligned in one authoritative scope document so discrepancies are explicit and reviewable.

## Current truthful status

- The baseline candidate set is materially stronger than the production and hardening candidate sets.
- Production and hardening targets remain in scope, and most are now implementation-backed, but several remain evidence-incomplete, profile-bounded, or not yet independently validated.
- Extension and alignment-only work remains deferred or quarantined from the default certification claim boundary.

## Most common discrepancies

- `active-without-effective-claim:baseline`: `2` targets
- `active-without-effective-claim:production`: `2` targets
- `surface-drift`: `2` targets

## Required boundary outputs present in this checkpoint

- `compliance/targets/certification_scope.yaml`
- `docs/compliance/CERTIFICATION_BOUNDARY.md`
- `docs/compliance/TARGET_REALITY_MATRIX.md`

## Still not completed in this checkpoint

- full Tier 3 evidence promotion across production and hardening targets
- broader interop breadth for sender-constrained and assertion-based profiles
- Tier 4 independent peer validation

