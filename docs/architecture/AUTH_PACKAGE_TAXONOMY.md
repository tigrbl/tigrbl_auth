# Auth Package Taxonomy

This taxonomy separates identity, authentication, authorization, protocol, and composed product ownership for the staged package migration.

## Prefix Rules

| Prefix | Scope | Must not own |
| --- | --- | --- |
| `tigrbl-identity-*` | Neutral identity records: subjects, tenants, realms, aliases, lifecycle, contracts, storage, administration, runtime support. | Credential proof, authorization policy decisions, OAuth/OIDC/RP wire behavior. |
| `tigrbl-authn-*` | Authentication lifecycle and proof of credential control. | Authorization policy engines, grants, permissions, or protocol wire ownership. |
| `tigrbl-authz-*` | Authority, policy, grants, permissions, scopes, resource-server enforcement, decisions, logs, and replay. | Credential verification, login flows, or protocol wire truth. |
| `tigrbl-auth-protocol-*` | OAuth, OIDC, and RP wire behavior, standards profiles, discovery, registration, PKCE, token exchange, PAR, and RAR. | Canonical identity records, credential truth, policy truth, or persistence ownership. |
| `tigrbl-auth*` | Composed products, front doors, APIs, CLI, and app/plugin assembly. | Canonical lower-level package truth that belongs to identity, authn, authz, or protocol packages. |

## Preferred Package Names

| Concern | Preferred package | Deprecated compatibility package |
| --- | --- | --- |
| Credential proof and lifecycle | `tigrbl-authn-credentials` | `tigrbl-identity-credentials` |
| Authorization policy and authority | `tigrbl-authz-policy` | `tigrbl-identity-policy` |
| Protected-resource enforcement | `tigrbl-authz-resource-server` | `tigrbl-identity-resource-server` |
| OAuth protocol behavior | `tigrbl-auth-protocol-oauth` | `tigrbl-identity-oauth` |
| OIDC provider protocol behavior | `tigrbl-auth-protocol-oidc` | `tigrbl-identity-oidc` |
| OIDC RP / OAuth client behavior | `tigrbl-auth-protocol-rp` | `tigrbl-identity-rp` |

## Stable Identity Packages

These packages remain under `tigrbl-identity-*` because their primary responsibility is neutral identity, shared contracts, or operational support rather than authn/authz behavior:

- `tigrbl-identity-core`
- `tigrbl-identity-contracts`
- `tigrbl-identity-principals`
- `tigrbl-identity-jose`
- `tigrbl-identity-storage`
- `tigrbl-identity-admin`
- `tigrbl-identity-server`
- `tigrbl-identity-runtime`
- `tigrbl-identity-operator`
- `tigrbl-identity-cli`
- `tigrbl-identity-testkit`

## Principal Narrowing

`tigrbl-identity-principals` owns subject, tenant, realm, alias, and lifecycle concepts. Authority roles and role-bearing membership semantics are authorization concepts. New code should import authority helpers from `tigrbl-authz-policy` or `tigrbl_identity_policy`; principal-side role helpers remain only as migration compatibility.

## Boundary Guards

Static tests enforce these rules for new work:

- identity packages do not import authn/authz behavior packages;
- authn packages do not import authz policy engines;
- authz packages do not import credential verifier or login surfaces;
- protocol packages do not own identity, credential, policy, or storage truth;
- deprecated `tigrbl-identity-*` package names stay importable during the migration window;
- foundational packages must not grow new imports of the `tigrbl_auth` facade. Current upward imports are tracked as T1 migration debt in `tests/unit/test_package_dependency_layering.py` and must be eliminated for T2.

The dependency layering migration is defined in `docs/architecture/PACKAGE_DEPENDENCY_LAYERING_MIGRATION.md`.
