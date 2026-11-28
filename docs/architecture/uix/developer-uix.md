> [!WARNING]
> Non-authoritative active document.
> Use this as a future-state UIX note, not as certification or release truth.

# `developer-uix`

## Purpose

`developer-uix` is the tenant integration UIX for app owners and delegated developers.

## Persona

- tenant app developer
- delegated app owner

## Suggested mount

| Dimension | Value |
|---|---|
| Origin | `https://developer-auth.example.com` |
| Mount | `/` |
| UIX kind | developer or integration SPA |

## Owned pages and views

- developer dashboard
- app catalog
- create OIDC app
- app detail
- redirect URI management
- grant and auth method config
- client secret rotation
- JWKS metadata management
- discovery reference
- integration examples

## Core workflows

- register apps
- update client metadata
- rotate secrets
- review discovery metadata
- prepare app integration settings

## Backend lane

Consumes `/register`, `/register/{client_id}`, tenant discovery docs, and `/rpc` client-control methods.

## Exclusions

- no platform tenant lifecycle
- no general end-user profile UX
