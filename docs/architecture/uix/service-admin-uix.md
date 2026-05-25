> [!WARNING]
> Non-authoritative active document.
> Use this as a future-state UIX note, not as certification or release truth.

# `service-admin-uix`

## Purpose

`service-admin-uix` is the operator UIX for machine identities and service-to-service access.

## Persona

- service owner
- workload operator
- platform integration operator

## Suggested mount

| Dimension | Value |
|---|---|
| Origin | `https://service-auth.example.com` |
| Mount | `/` |
| UIX kind | machine or workload operator SPA |

## Owned pages and views

- service dashboard
- machine principals
- API keys
- client credentials
- workload trust setup
- token inspection
- introspection test
- access posture
- secret rotation

## Core workflows

- onboard machine principals
- issue service credentials
- validate token behavior
- manage non-human trust relationships

## Backend lane

Consumes `/token`, `/introspect`, JWKS endpoints, and future machine/service control surfaces.

## Exclusions

- no human login UX
- no platform tenant creation
