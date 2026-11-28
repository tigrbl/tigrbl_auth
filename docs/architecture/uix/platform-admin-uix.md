> [!WARNING]
> Non-authoritative active document.
> Use this as a future-state UIX note, not as certification or release truth.

# `platform-admin-uix`

## Purpose

`platform-admin-uix` is the superuser control-plane UIX for the entire deployment.

## Persona

- platform superuser

## Suggested mount

| Dimension | Value |
|---|---|
| Origin | `https://platform-auth-admin.example.com` |
| Mount | `/` |
| UIX kind | privileged operator SPA |

## Owned pages and views

- login
- forgot password
- reset password
- change password
- platform dashboard
- tenant list
- create tenant
- tenant detail
- assign tenant admin
- platform identity administration
- audit or health overview

## Core workflows

- create tenant
- delete tenant
- assign tenant admins
- inspect cross-tenant state
- manage deployment-wide privileged identities

## Backend lane

Consumes `/admin/auth/*`, `/admin/tenants`, `/admin/identities`, and `/rpc`.

## Exclusions

- no tenant end-user auth
- no tenant-local day-to-day admin
- no developer self-service portal responsibilities
