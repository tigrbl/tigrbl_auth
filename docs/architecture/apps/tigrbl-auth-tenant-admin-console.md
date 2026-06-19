> [!WARNING]
> Non-authoritative active document.
> Use this as a future-state app note, not as certification or release truth.

# `tigrbl-auth-tenant-admin-console`

## Purpose

`tigrbl-auth-tenant-admin-console` is the tenant-scoped operator console. It gives one tenant administrative control over its own principals, credentials, and signing posture.

## Primary role

- manage tenant principals
- issue or manage credentials
- manage tenant signing keys and JWKS publication
- inspect tenant-local auth posture and config

## Suggested deployment

| Dimension | Value |
|---|---|
| Kind | edge app |
| Suggested origin | `https://tenant-auth-admin.example.com` |
| Suggested mount | `/` |
| Deployment pattern | tenant-scoped SPA in front of the IDP admin lane |

## Backend surfaces consumed

- `/admin/auth/*`
- `/admin/identities`
- `/rpc`
- tenant discovery and tenant JWKS endpoints for parity/reference

## Owned views

| View family | Role |
|---|---|
| Tenant dashboard | tenant-local status and navigation |
| Identity administration | create and manage principals |
| Credential workflows | issue and rotate tenant credentials |
| Signing keys | manage signing material and JWKS output |
| Tenant config | tenant-local policy and namespace posture |

## Talks to / boundaries

| Counterparty | Relationship |
|---|---|
| `tigrbl-auth-idp` | consumes admin REST, RPC, and tenant discovery/JWKS surfaces |
| `tigrbl-auth-platform-admin-console` | receives tenant bootstrap from platform-level operators |
| `tigrbl-auth-developer-portal` | may delegate tenant application integration to app owners |

It should not own cross-tenant creation or platform superuser authority assignment.

## Repo basis

- tenant-relevant portions of current `pkgs/90-apps/admin-uix`
- identity and tenant JWKS components

## Main split rule

This app is one-tenant-at-a-time administration, not deployment-wide control.
