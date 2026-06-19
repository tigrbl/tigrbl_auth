> [!WARNING]
> Non-authoritative active document.
> Use this as a future-state app note, not as certification or release truth.

# `tigrbl-auth-platform-admin-console`

## Purpose

`tigrbl-auth-platform-admin-console` is the deployment-wide control-plane console for superusers. It owns cross-tenant operations and platform authority assignment.

## Primary role

- create and delete tenants
- assign tenant admins
- inspect cross-tenant state
- manage platform-level identities and authority

## Suggested deployment

| Dimension | Value |
|---|---|
| Kind | edge app |
| Suggested origin | `https://platform-auth-admin.example.com` |
| Suggested mount | `/` |
| Deployment pattern | privileged SPA in front of the IDP admin lane |

## Backend surfaces consumed

- `/admin/auth/*`
- `/admin/tenants`
- `/admin/identities`
- `/rpc`

## Owned views

| View family | Role |
|---|---|
| Platform dashboard | deployment-wide status and navigation |
| Tenant catalog | create, inspect, and retire tenants |
| Authority management | grant or review tenant-admin authority |
| Platform identity admin | cross-tenant privileged identity operations |

## Talks to / boundaries

| Counterparty | Relationship |
|---|---|
| `tigrbl-auth-idp` | consumes admin REST and RPC lanes |
| `tigrbl-auth-tenant-admin-console` | hands off tenant-local operations after tenant bootstrap |

It should not own tenant-local day-to-day admin or end-user auth.

## Repo basis

- platform-relevant portions of current `pkgs/90-ui/admin-uix`
- current tenant and identity management surfaces

## Main split rule

This app is for deployment authority, not tenant self-service.
