> [!WARNING]
> Non-authoritative active document.
> Use this as a future-state UIX note, not as certification or release truth.

# `public-uix`

## Purpose

`public-uix` is the public end-user experience for tenant human users.

## Persona

- tenant human user

## Suggested mount

| Dimension | Value |
|---|---|
| Origin | `https://login.example.com` |
| Mount | `/` |
| UIX kind | public SPA |

## Owned pages and views

- `#/login`
- `#/register`
- `#/callback`
- `#/profile`
- `#/forgot-password`
- `#/reset-password`
- `#/verify-email`
- `#/terms`
- `#/consent`

## Core workflows

- login
- registration
- consent
- logout
- password recovery
- email verification
- profile access

## Backend lane

Consumes only the public auth lane and tenant discovery documents.

## Exclusions

- no tenant admin
- no platform admin
- no client-management console
