> [!WARNING]
> Non-authoritative active document.
> Use this as a future-state app note, not as certification or release truth.

# `tigrbl-auth-idp`

## Purpose

`tigrbl-auth-idp` is the shared multi-tenant backend identity provider. It is the protocol and control-plane core that every other app and UIX composes around.

## Primary role

- issue and validate tokens
- serve discovery and JWKS documents
- expose tenant-scoped OIDC/OAuth surfaces
- expose platform and tenant administration surfaces

## Suggested deployment

| Dimension | Value |
|---|---|
| Kind | backend app |
| Suggested origin | `https://id.example.com` |
| Suggested mount | `/` |
| Deployment pattern | shared regional or global identity plane |

## Owned path families

- `/authorize`
- `/token`
- `/userinfo`
- `/introspect`
- `/register`
- `/logout`
- `/.well-known/*`
- `/tenants/{tenant_slug}/.well-known/*`
- `/admin/*`
- `/rpc`

## Functional blocks

| Block | Role |
|---|---|
| Public auth lane | browser and app-facing OAuth/OIDC flows |
| Tenant discovery lane | per-tenant metadata and JWKS publication |
| Admin REST lane | operational CRUD for auth, tenants, and identities |
| Admin RPC lane | richer control-plane methods for keys, clients, and directories |

## Talks to / used by

| Counterparty | Relationship |
|---|---|
| `tigrbl-auth-public-portal` | serves end-user auth flows |
| `tigrbl-auth-platform-admin-console` | serves deployment-wide administration |
| `tigrbl-auth-tenant-admin-console` | serves tenant-scoped administration |
| `tigrbl-auth-developer-portal` | serves client registration and metadata control |
| `tigrbl-auth-service-admin-surface` | serves machine access and introspection workflows |
| tenant applications and SDKs | protocol dependency |

## Repo basis

- current backend deployment in `tigrbl_auth`
- REST routers
- RPC methods
- discovery and JWKS services

## Main split rule

No bespoke operator or tenant UI should live inside this app. It should remain the shared protocol and control surface.
