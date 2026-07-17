# Package Dependency Layering Migration

The detailed numbered-layer ownership policy and the deliberately sparse
layer-40 capability definition are maintained in
[`PACKAGE_LAYER_OWNERSHIP.md`](PACKAGE_LAYER_OWNERSHIP.md).

This plan makes the package rename work enforceable. The target graph is directional:

1. Foundational packages own identity, authn, authz, protocol, storage, runtime, server, contracts, and testkit behavior.
2. `tigrbl-auth` is a compatibility facade and composed product front door over those packages.
3. `tigrbl-auth-router-*` backend products consume the facade for ergonomic app assembly.
4. Frontend UIX workspaces consume HTTP, OpenAPI, OpenRPC, OIDC discovery, and UIX packages. They do not import Python internals.

## Target Layers

| Layer | Packages | Allowed direction |
| --- | --- | --- |
| Foundation | `tigrbl-identity-*`, `tigrbl-authn-*`, `tigrbl-authz-*`, `tigrbl-auth-protocol-*` | May depend sideways/downward only through owned package contracts. Must not import `tigrbl_auth`. |
| Facade | `tigrbl-auth` | May import foundational packages and preserve compatibility paths. Must not become canonical truth for identity, authn, authz, protocol, storage, or policy. |
| Downstream backend | `tigrbl-auth-router-*` | May import `tigrbl_auth` and product-local code. Should not reach around the facade into storage or lower internals unless a product contract requires it. |
| Downstream frontend | `pkgs/105-ui/*-uix`, `pkgs/105-ui/rp`, `pkgs/100-uix-core/uix-core` | May consume API contracts, discovery metadata, generated clients, and browser-safe UIX packages. Must not import Python `tigrbl_auth` modules. |

## Staged Enforcement

### T0: Inventory

Classify every Python package under `pkgs/` into exactly one of foundation, facade, or downstream backend. Classify each frontend workspace separately. This prevents ambiguous ownership during the migration.

### T1: Drift Guard

Allow current foundational imports of `tigrbl_auth` only when named in the migration exception ledger in `tests/unit/test_package_dependency_layering.py`. New foundational packages, including the new authn/authz/protocol package names, cannot import the facade. Any new upward import fails the boundary test.

Current T1 exception packages:

- `tigrbl-identity-admin`
- `tigrbl-identity-cli`
- `tigrbl-identity-contracts`
- `tigrbl-authn-credentials`
- `tigrbl-identity-jose`
- `tigrbl-auth-protocol-oauth`
- `tigrbl-auth-protocol-oidc`
- `tigrbl-authz-policy`
- `tigrbl-authz-resource-server`
- `tigrbl-auth-protocol-rp`
- `tigrbl-identity-runtime`
- `tigrbl-identity-server`
- `tigrbl-identity-storage`

### T2: Zero Exceptions

Remove the exception ledger by moving facade-owned imports down into the owning foundational packages or by replacing them with lower-layer contracts. At T2, no foundational package imports `tigrbl_auth`; only `tigrbl-auth` and `tigrbl-auth-router-*` packages do.

Status: complete for direct Python imports. The exception ledger in `tests/unit/test_package_dependency_layering.py` is empty, and foundational packages now import the canonical split package roots directly.

## SSOT Entity Changes

Update existing governance anchors:

- ADR `adr:1096`: package-suite split now includes the dependency-layering rule.
- ADR `adr:1104`: facade ergonomics are constrained by a hard no-upward-import boundary.
- SPEC `spc:1099`: package boundary specification includes the foundation -> facade -> backend/frontend graph.
- SPEC `spc:1113`: staged migration plan includes T0 inventory, T1 drift guard, and T2 zero-exception enforcement.

Add feature, claims, tests, and evidence:

- Feature `feat:package-dependency-layering-guard`
- Claim `clm:package-dependency-layering-guard-t0`
- Claim `clm:package-dependency-layering-guard-t1`
- Claim `clm:package-dependency-layering-guard-t2`
- Test `tst:package-dependency-layering-guard-t0-t1`
- Test `tst:package-dependency-layering-guard-t2`
- Evidence `evd:package-dependency-layering-guard-t0-t1-pytest`
- Evidence `evd:package-dependency-layering-guard-t2-pytest`

## Runtime Migration Work

T2 moved or rehomed these facade-owned surfaces:

- framework and typing helpers into dependency-light foundation packages;
- API contract helpers into contracts or server;
- settings and deployment helpers into runtime;
- token and key helpers into credentials or JOSE;
- OAuth/OIDC standards helpers into protocol packages;
- table, migration, and persistence helpers into storage;
- policy, admin-gate, and release posture helpers into authz policy.
