> [!WARNING]
> Non-authoritative active document.
> Use this as a future-state UIX note, not as certification or release truth.

# `tenant-admin-uix`

## Purpose

`tenant-admin-uix` is the tenant-scoped administrative UIX for one tenant at a time.

## Persona

- tenant administrator

## Suggested mount

| Dimension | Value |
|---|---|
| Origin | `https://tenant-auth-admin.example.com` |
| Mount | `/` |
| UIX kind | tenant-scoped operator SPA |

## Owned pages and views

- login
- forgot password
- reset password
- change password
- tenant dashboard
- identity list
- principal detail
- create principal
- credential issuance
- signing keys
- JWKS publication
- tenant config or policy

## Core workflows

- create principals
- issue or rotate credentials
- manage tenant admins
- rotate signing keys
- inspect tenant discovery posture

## Backend lane

Consumes `/admin/auth/*`, `/admin/identities`, `/rpc`, and tenant discovery or JWKS parity surfaces.

## Exclusions

- no cross-tenant tenant creation
- no platform-wide authority assignment
