> [!WARNING]
> Non-authoritative active document.
> Use this as a future-state app note, not as certification or release truth.

# `tigrbl-auth-service-admin-surface`

## Purpose

`tigrbl-auth-service-admin-surface` is the non-human access console. It exists for service owners and workload operators who need to manage machine principals and machine trust posture.

## Primary role

- onboard machine principals
- issue API keys or client credentials
- inspect token and introspection posture
- manage workload and service trust relationships

## Suggested deployment

| Dimension | Value |
|---|---|
| Kind | edge app |
| Suggested origin | `https://service-auth.example.com` |
| Suggested mount | `/` |
| Deployment pattern | service-operator SPA in front of token and machine-control surfaces |

## Backend surfaces consumed

- `/token`
- `/introspect`
- JWKS endpoints
- machine/service auth surfaces
- future workload identity methods

## Owned views

| View family | Role |
|---|---|
| Service dashboard | machine-access entrypoint |
| Machine principals | onboard and manage service identities |
| Credential operations | issue and rotate API keys or client credentials |
| Trust posture | workload federation and verification setup |
| Token inspection | inspect auth behavior and introspection responses |

## Talks to / boundaries

| Counterparty | Relationship |
|---|---|
| `tigrbl-auth-idp` | consumes token, introspection, JWKS, and machine-control surfaces |
| downstream services | configures how service-to-service access is established |

It should not own human-user UX or platform tenant lifecycle.

## Repo basis

- token plane
- auth backends
- API-key and service-key capability
- introspection support

## Main split rule

Keep non-human identity administration separate from tenant human administration.
