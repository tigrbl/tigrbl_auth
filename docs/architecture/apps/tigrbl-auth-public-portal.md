> [!WARNING]
> Non-authoritative active document.
> Use this as a future-state app note, not as certification or release truth.

# `tigrbl-auth-public-portal`

## Purpose

`tigrbl-auth-public-portal` is the browser-facing entrypoint for tenant human users. It owns the public authentication experience and nothing in the admin plane.

## Primary role

- login
- registration
- consent
- callback completion
- recovery and verification
- authenticated profile entry

## Suggested deployment

| Dimension | Value |
|---|---|
| Kind | edge app |
| Suggested origin | `https://login.example.com` |
| Suggested mount | `/` |
| Deployment pattern | public SPA in front of the IDP public lane |

## Backend surfaces consumed

- `/authorize`
- `/token`
- `/userinfo`
- `/logout`
- `/register`
- tenant discovery and JWKS metadata
- recovery and verification endpoints

## Owned views

| View family | Role |
|---|---|
| Login | authenticate human users |
| Register | onboard end users |
| Consent | authorize application access |
| Callback | complete OIDC flow |
| Recovery | forgot/reset password and verification |
| Profile | authenticated self-view |

## Talks to / boundaries

| Counterparty | Relationship |
|---|---|
| `tigrbl-auth-idp` | consumes public auth and discovery lanes |
| tenant applications | receives browser redirects into auth flows |

It should not consume `/admin/*` or `/rpc`.

## Repo basis

- current `apps/public-uix`
- current public route allowlist and hash-route pages

## Main split rule

Keep this app strictly public and end-user facing. Do not collapse tenant admin or developer workflows into it.
