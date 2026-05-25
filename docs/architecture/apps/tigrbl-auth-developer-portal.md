> [!WARNING]
> Non-authoritative active document.
> Use this as a future-state app note, not as certification or release truth.

# `tigrbl-auth-developer-portal`

## Purpose

`tigrbl-auth-developer-portal` is the self-service integration surface for tenant app developers. It owns application registration and OIDC/OAuth client lifecycle.

## Primary role

- create OIDC applications
- manage redirect URIs and metadata
- rotate secrets or JWKS metadata
- expose discovery references and integration settings

## Suggested deployment

| Dimension | Value |
|---|---|
| Kind | edge app |
| Suggested origin | `https://developer-auth.example.com` |
| Suggested mount | `/` |
| Deployment pattern | developer-focused SPA in front of registration and client-control surfaces |

## Backend surfaces consumed

- `/register`
- `/register/{client_id}`
- `/rpc` client and client-registration methods
- tenant discovery documents

## Owned views

| View family | Role |
|---|---|
| Developer dashboard | integration entrypoint |
| App catalog | list owned or delegated applications |
| App registration | create clients and base metadata |
| Client settings | redirect URIs, auth methods, grants, scopes |
| Secret and JWKS operations | rotate credentials and signing references |
| Discovery reference | tenant metadata and integration guidance |

## Talks to / boundaries

| Counterparty | Relationship |
|---|---|
| `tigrbl-auth-idp` | consumes registration, discovery, and client control surfaces |
| `tigrbl-auth-tenant-admin-console` | may receive delegated authority from tenant admins |
| tenant applications | configures their federation posture |

It should not own deployment-wide admin or general human-user profile UX.

## Repo basis

- dormant `ClientManagement.tsx`
- dynamic client registration endpoints
- client registration RPC methods

## Main split rule

Treat app integration as its own product surface instead of hiding it inside a generic admin console.
