# IAM, CIAM, PAM, And Adjacent Identity Categories Focus

Research date: 2026-05-28

Scope: this note frames IAM, CIAM, PAM, IGA, workforce identity, customer identity, developer identity, service/workload identity, and adjacent identity-security categories for `tigrbl_auth`.

The key point: IAM, CIAM, and PAM are product categories, not single protocols. OAuth, OIDC, SCIM, MFA, RBAC, IdP federation, M2M, and admin APIs are component capabilities that can be assembled into those product categories.

## Category Vocabulary

| Category | Meaning | Typical users | Typical capabilities |
| --- | --- | --- | --- |
| IAM | Broad identity and access management for users, apps, services, policies, credentials, and protected resources. | Enterprise admins, platform operators, developers, employees, services. | SSO, MFA, users, groups, roles, apps, APIs, lifecycle, policy, audit, federation. |
| Workforce IAM | IAM focused on employees, contractors, workforce apps, directories, SSO, lifecycle, and enterprise controls. | Employees, IT admins, security teams. | SSO, directory sync, device/risk policy, lifecycle management, app assignments, admin roles. |
| CIAM | Customer identity and access management for external users, customers, partners, B2B/B2C apps, hosted login, self-service, scale, branding, and consent. | Customers, partners, tenant users, tenant admins, app developers. | Hosted login, registration, profile, consent, MFA, social/enterprise IdPs, organizations, branding, APIs. |
| PAM | Privileged access management for high-risk human, service, and infrastructure access. | Privileged admins, operators, SREs, infrastructure owners. | JIT elevation, approvals, session brokering, credential vaulting, infrastructure access, recording, break-glass, access reviews. |
| IGA | Identity governance and administration for access lifecycle, reviews, approvals, entitlements, SoD, and compliance. | Governance teams, auditors, managers, app owners. | Access requests, reviews, certifications, entitlement catalog, approval workflows, lifecycle. |
| NHI / workload identity | Non-human identity for services, workloads, CI/CD, API clients, machines, devices, and agents. | Service owners, platform engineers, workload operators. | Service principals, workload federation, client credentials, service keys, API keys, rotation, validation, audit. |
| Developer identity platform | Identity product surface for app developers integrating auth into apps and APIs. | Tenant developers, customer developers, integration owners. | App/client registration, redirect URIs, client secrets/JWKS, SDKs, docs, test clients, scopes. |

## Current `tigrbl_auth` Fit

| Category | Current fit | Evidence | Interpretation |
| --- | --- | --- | --- |
| CIAM | Strongest fit. Public API/UIX, tenant branding intent, hosted login, registration/recovery, consent, OAuth/OIDC, RP packages, developer API, organizations/tenants, and external-user journeys point here. | [Surface Packaging](architecture/SURFACE_SEPARATED_PRODUCT_PACKAGING.md), [Role User Journeys](architecture/ROLE_USER_JOURNEYS_AND_STORIES.md), [Public API spec](../.ssot/specs/SPEC-1166-public-app-contract.yaml), [Public UIX spec](../.ssot/specs/SPEC-1167-public-uix-composition-contract.yaml) | `tigrbl_auth` can credibly be framed as a CIAM-oriented identity provider platform in target architecture, with current implementation still maturing feature by feature. |
| IAM | Partial but broad. The suite has tenants, principals, credentials, policy, admin surfaces, JOSE, OAuth/OIDC, storage, runtime, operator, resource-server, and RP packages. | [Product Provenance Lineage](architecture/product-provenance-lineage.md), [Policy boundary](../.ssot/adr/ADR-1099-policy-is-an-explicit-package-boundary.yaml) | Use "identity platform" or "IAM suite" carefully; core IAM pieces exist, but not every workforce/enterprise IAM capability is productized. |
| Workforce IAM | Underframed/partial. Tenant-admin and platform-admin cover administration, but there is no full workforce directory/lifecycle/device posture/app catalog product yet. | [Platform-admin ADR](../.ssot/adr/ADR-1078-platform-admin-cross-tenant-authority.yaml), [Tenant-admin ADR](../.ssot/adr/ADR-1079-tenant-admin-tenant-scoped-self-service-authority.yaml) | Could support workforce-style tenants later, but current product language should not imply Okta Workforce Cloud parity. |
| PAM | Mostly gap. Admin authority, break-glass intent, service/workload identity, audit, and policy primitives exist, but no privileged session brokering, credential vaulting, JIT elevation, infrastructure connectors, or recording. | [Role User Journeys](architecture/ROLE_USER_JOURNEYS_AND_STORIES.md), [Authorization Models Focus](authorization-models-focus.md), [M2M Focus](m2m-workload-identity-focus.md) | Do not market as PAM. Treat PAM as a future privileged-access product lane if needed. |
| IGA | Early governance signals only. SSOT, audit, policy, delegation, lifecycle, and product tiers exist conceptually, but access reviews/certifications/approval workflows are not mature runtime products. | [Authorization Models Focus](authorization-models-focus.md), [ADR-1086](../.ssot/adr/ADR-1086-management-api-product-with-deployable-surface-slices.yaml) | Useful future adjacency, not current product claim. |
| NHI / workload identity | Strong planned lane. Service-admin, M2M, service keys/API keys, workload principals, resource validation, and client credentials align well. | [M2M Focus](m2m-workload-identity-focus.md), [M2M Vendor Matrix](m2m-vendor-coverage-matrix.md), [Service-admin ADR](../.ssot/adr/ADR-1081-service-admin-machine-workload-identity-administration.yaml) | This is a real product angle and should be paired with CIAM rather than hidden under generic IAM. |
| Developer identity platform | Strong planned lane. Developer API/UIX, RP packages, client registration, SDK examples, and public issuer integration all point here. | [Surface Packaging](architecture/SURFACE_SEPARATED_PRODUCT_PACKAGING.md), [Developer API ADR](../.ssot/adr/ADR-1080-developer-app-app-oauth-client-self-service.yaml) | This is one of the clearest surfaces: tenant developers integrate apps and APIs with the issuer. |

## Competitor Product Shape

| Vendor | IAM / workforce identity | CIAM / customer identity | PAM / privileged access | Adjacent notes |
| --- | --- | --- | --- | --- |
| Auth0 / Okta CIC | Auth0 is more customer/developer identity than workforce IAM. Auth0 Management API manages tenants, apps, connections, users, organizations. See [Auth0 APIs](https://dev.auth0.com/docs/api). | Strong CIAM: Authentication API, Universal Login, Organizations, My Account, My Organization, Management API. See [Auth0 Organizations](https://auth0.com/docs/organizations), [Auth0 My Organization API](https://auth0.com/docs/manage-users/my-organization-api). | Not the main Auth0 product. Okta portfolio handles PAM through Okta Privileged Access. | Auth0 FGA adds fine-grained authorization as a separate product surface. |
| Okta WIC / CIC | Strong workforce IAM through Okta Workforce Identity Cloud: SSO, Universal Directory, lifecycle, MFA, policies, admin roles, app access. See [Okta docs](https://help.okta.com/en-us/Content/index.htm). | Strong CIAM through Okta Customer Identity Cloud / Auth0. | Strong PAM product through Okta Privileged Access: infrastructure access, privileged access governance, credential vaulting, compliance reporting. See [Okta Privileged Access](https://help.okta.com/oie/en-us/content/topics/privileged-access/pam-overview.htm). | Okta also frames workload identity/NHI under Privileged Access. See [Okta workloads](https://help.okta.com/oie/en-us/content/topics/privileged-access/pam-workloads.htm). |
| Keycloak | Strong open-source IAM/IdP server: realms, users, groups, roles, clients, admin console/API, SSO, federation, Authorization Services. See [Keycloak Server Administration Guide](https://www.keycloak.org/docs/latest/server_admin/). | Can be used for CIAM, but CIAM product polish, customer self-service, tenant org UX, marketing consent, and managed operations depend on implementer. | Not a PAM product by default. Privileged admin roles exist, but no full PAM vault/session/JIT product. | Strong self-hosted IAM substrate, weaker packaged product segmentation. |
| FusionAuth | IAM-adjacent app identity platform, but public framing is CIAM. | Strong CIAM: login, registration, MFA, IdPs, tenants, applications, APIs, roles, groups. See [FusionAuth docs](https://fusionauth.io/docs), [FusionAuth get started](https://fusionauth.io/docs/get-started/). | Not a full PAM product by default. | Strong developer-oriented CIAM with self-host/cloud deployment choices. |
| Amazon | AWS IAM and IAM Identity Center cover workforce/cloud IAM; Cognito covers app/customer identity; Verified Permissions covers app authorization. See [Cognito IAM guide](https://docs.aws.amazon.com/cognito/latest/developerguide/security-iam.html), [AWS IAM federation](https://docs.aws.amazon.com/en_en/IAM/latest/UserGuide/id_roles_providers.html). | Cognito is AWS's CIAM/app identity product. See [AWS customer identity management guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture-identity-management/customer-identity-management.html). | AWS has IAM, IAM Identity Center, temporary credentials, and partner/PAM ecosystem rather than Cognito-as-PAM. | The AWS pattern is split products: Cognito for customer/app users, IAM/Identity Center for cloud/workforce access, Verified Permissions for app authorization. |
| Microsoft Entra | Strong workforce IAM through Entra ID, Conditional Access, app registrations, enterprise apps, groups, roles, device/risk integrations. | CIAM through Microsoft Entra External ID. See [Entra External ID](https://learn.microsoft.com/en-us/entra/external-id/). | Privileged access through Entra Privileged Identity Management and governance. See [PIM deployment plan](https://github.com/MicrosoftDocs/entra-docs/blob/main/docs/id-governance/privileged-identity-management/pim-deployment-plan.md). | Useful reference for separating workforce IAM, external identity/CIAM, governance, and PIM. |

## Product Category Mapping

| `tigrbl_auth` surface | IAM | CIAM | PAM | IGA | NHI/workload | Developer platform |
| --- | --- | --- | --- | --- | --- | --- |
| `tigrbl-auth-backend-app-public` | Partial | Strong | No | No | Token issuance only | Strong |
| `@tigrbl-auth/public-uix` | Partial | Strong | No | No | No | Strong for app login testing |
| `tigrbl-auth-backend-app-platform-admin` | Strong platform control | Partial | Privileged admin basis only | Partial | Partial | No |
| `tigrbl-auth-backend-app-tenant-admin` | Strong tenant control | Strong for tenant-owned customer/user admin | Privileged admin basis only | Partial | Partial | Partial |
| `tigrbl-auth-backend-app-developer` | Partial | Strong for app integration | No | No | M2M client setup partial | Strong |
| `tigrbl-auth-backend-app-service-admin` | Strong for NHI | Partial | PAM-adjacent but not PAM | Partial | Strong | Partial |
| `tigrbl-auth-backend-app-resource-validation` | Strong for API IAM | Strong for protected APIs | No | No | Strong | Strong |
| `tigrbl-authz-policy` | Strong foundation | Strong foundation | Foundation only | Foundation only | Strong foundation | Strong foundation |
| `tigrbl-identity-operator` | Strong operator tooling | Partial | PAM-adjacent only | Partial | Partial | No |

## What `tigrbl_auth` Should Claim

| Claim | Recommendation | Reason |
| --- | --- | --- |
| "CIAM platform" | Good target claim, but qualify current maturity. | Public login, tenant apps, external users, developer integration, hosted UI, RP packages, organizations/tenants, and API auth align with CIAM. |
| "Identity provider / authorization server" | Good current/target claim. | OAuth/OIDC issuer behavior is core to the suite. |
| "IAM suite" | Acceptable as broad architecture wording, but avoid implying full workforce IAM parity. | The suite has IAM foundations but not complete workforce lifecycle, directory sync, device posture, or app catalog. |
| "Management API" | Good product framing for platform-admin, tenant-admin, developer, and service-admin slices. | ADR-1086 already aligns with competitor management API patterns. |
| "M2M / workload identity" | Good target product lane. | Service-admin, client credentials, service keys, API keys, resource validation, and workload plans align strongly. |
| "PAM" | Do not claim yet. | Missing JIT elevation, approvals, session brokering, vaulting, infrastructure connectors, recording, and access reviews. |
| "IGA" | Do not claim yet. | Missing access request/review/certification and entitlement lifecycle product. |
| "Zero Trust identity platform" | Use only as future positioning, not current proof. | Requires consistent policy, continuous evaluation, device/risk, workload trust, and enforcement. |

## PAM Gap Breakdown

| PAM capability | Current `tigrbl_auth` state | Needed before claiming PAM |
| --- | --- | --- |
| Privileged account inventory | Admin/service principals exist conceptually. | Canonical privileged account/resource model and ownership. |
| JIT elevation | Underframed. | Request/approval workflow, time-bound elevation, automatic expiry. |
| Credential vaulting | Not present. | Vault integration or built-in secure secret custody, checkout, rotation, one-time reveal. |
| Session brokering | Not present. | SSH/RDP/database/Kubernetes/SaaS session proxy or broker integrations. |
| Session recording | Not present. | Recording, tamper-proof storage, replay, redaction, retention. |
| Break-glass | Mentioned in journeys, not productized. | Emergency access workflow, approval exceptions, post-use review, audit. |
| Access reviews | Underframed. | Review campaigns, certifier workflow, evidence and revocation. |
| Infrastructure connectors | Not present. | Connectors for servers, databases, Kubernetes, cloud accounts, SaaS admin planes. |
| Privileged workload identity | Planned through M2M/workload identity. | Federated workload trust, just-in-time service credentials, policy and audit. |

## Recommended Product Framing

| Product | Description | Current maturity |
| --- | --- | --- |
| Tigrbl Auth CIAM | Customer/tenant-facing identity provider with hosted login, registration, recovery, consent, OAuth/OIDC, app integration, and tenant/developer admin. | Best strategic framing; implementation still maturing by capability. |
| Tigrbl Auth Management API | One management product with platform, tenant, developer, and service/workload resource groups exposed as deployable frontdoor slices. | Strong architectural direction; ADR-1086 draft should mature. |
| Tigrbl Auth Developer Platform | App/client registration, RP SDKs, resource-server validation, examples, discovery, JWKS, token integration. | Strong direction. |
| Tigrbl Auth Workload Identity | Service principals, API keys, service keys, client credentials, resource validation, workload federation. | Strong planned lane; needs productized grants/rotation/audit. |
| Tigrbl Auth Workforce IAM | Employee/contractor identity, app assignments, lifecycle, tenant admin, policy. | Possible future packaging, but underframed today. |
| Tigrbl Auth PAM | JIT privileged access and infrastructure/admin-session controls. | Future adjacency only; do not claim now. |
| Tigrbl Auth IGA | Access requests, reviews, certifications, entitlement governance. | Future adjacency only; do not claim now. |

## Recommended Next Steps

| Priority | Work | Why |
| --- | --- | --- |
| P0 | Mature ADR-1086 from draft if agreed: Management API is one product with deployable surface slices. | Aligns product language with competitors without undoing package/frontdoor separation. |
| P0 | State the primary product as CIAM + Management API + Developer Platform + Workload Identity. | Accurate to current architecture and stronger than generic IAM. |
| P0 | Add specs for tenant/org lifecycle, app/client lifecycle, service/workload lifecycle, and policy lifecycle under that product model. | Converts category language into implementable contracts. |
| P1 | Add explicit "not PAM / not IGA yet" status notes in architecture docs. | Prevents overclaiming. |
| P1 | Define privileged admin/break-glass as a narrow security feature before broad PAM. | Provides useful privileged-control value without pretending to be a PAM suite. |
| P1 | Define access review and entitlement inventory as an IGA-adjacent future slice. | Gives governance a path without blocking CIAM/M2M maturity. |
| P2 | Revisit workforce IAM packaging after tenant-admin, policy, lifecycle, federation, SCIM, and MFA are mature. | Workforce IAM needs broader lifecycle and directory semantics than current public issuer work. |

## Key Takeaway

`tigrbl_auth` is best framed as:

```text
CIAM-oriented identity provider + management API + developer integration platform
+ workload identity lane
```

It has IAM foundations, but PAM and IGA should remain future adjacent categories until specific runtime surfaces, tests, and governance contracts exist.

## Bibliography

- Auth0: [Auth0 APIs](https://dev.auth0.com/docs/api)
- Auth0: [Organizations](https://auth0.com/docs/organizations)
- Auth0: [My Organization API](https://auth0.com/docs/manage-users/my-organization-api)
- Okta: [Okta Documentation](https://help.okta.com/en-us/Content/index.htm)
- Okta: [Okta Privileged Access](https://help.okta.com/oie/en-us/content/topics/privileged-access/pam-overview.htm)
- Okta: [Okta Privileged Access workloads](https://help.okta.com/oie/en-us/content/topics/privileged-access/pam-workloads.htm)
- Keycloak: [Server Administration Guide](https://www.keycloak.org/docs/latest/server_admin/)
- FusionAuth: [Documentation](https://fusionauth.io/docs)
- FusionAuth: [Get Started](https://fusionauth.io/docs/get-started/)
- FusionAuth: [Enterprise CIAM](https://fusionauth.io/platform/enterprise)
- Amazon Cognito: [Identity and access management for Amazon Cognito](https://docs.aws.amazon.com/cognito/latest/developerguide/security-iam.html)
- AWS IAM: [Identity providers and federation into AWS](https://docs.aws.amazon.com/en_en/IAM/latest/UserGuide/id_roles_providers.html)
- AWS Prescriptive Guidance: [Customer identity management](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture-identity-management/customer-identity-management.html)
- Microsoft Entra: [External ID](https://learn.microsoft.com/en-us/entra/external-id/)
- Microsoft Entra: [Privileged Identity Management deployment plan](https://github.com/MicrosoftDocs/entra-docs/blob/main/docs/id-governance/privileged-identity-management/pim-deployment-plan.md)
