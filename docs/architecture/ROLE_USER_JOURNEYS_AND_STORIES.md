> [!WARNING]
> Non-authoritative active document.
> Use this as a future-state product journey note, not as certification or release truth.
> For current executable and release truth, use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`, `CURRENT_STATE.md`, and the generated reference surfaces.

# Role User Journeys and Stories

This note captures proposed user journeys and user stories for the future-state `tigrbl_auth` platform roles.

Assumption: `direct customer` means a customer using Acme's identity platform directly, not a customer of one of Acme's tenants.

## 1. Platform owner

1. Journey: establish the identity platform.
   1. As a platform owner, I want to configure the global IDP, domains, compliance posture, and default tenant policies so that Acme can operate a trustworthy multi-tenant auth platform.
   2. As a platform owner, I want to define the tenancy model, authority boundaries, and product tiers so that every tenant is created under an intentional operating model.
   3. As a platform owner, I want visibility into all tenant, operator, and security boundaries so that I can prove the platform is governed.
2. Journey: delegate platform authority.
   1. As a platform owner, I want to appoint platform administrators and operators so that day-to-day work does not require owner access.
   2. As a platform owner, I want approval rules for privileged changes so that tenant-impacting actions have accountable review.
   3. As a platform owner, I want separation between business administration and runtime operations so that infrastructure operators cannot accidentally own tenant business authority.
3. Journey: steer platform lifecycle and risk.
   1. As a platform owner, I want to review adoption, incident, compliance, and tenant-risk reports so that I can decide where the platform needs investment.
   2. As a platform owner, I want to approve the rollout of new product surfaces such as `developer-uix` and `service-admin-uix` so that new authority paths are introduced deliberately.
   3. As a platform owner, I want certification and evidence summaries so that Acme can support enterprise and regulated customers.

## 2. Platform administrator

1. Journey: onboard tenants.
   1. As a platform administrator, I want to create tenant Beta from `platform-admin-uix` so that Beta receives its namespace, issuer, and admin boundary.
   2. As a platform administrator, I want to assign a tenant owner/admin so that Beta can self-manage without Acme handling every tenant action.
   3. As a platform administrator, I want to verify tenant discovery, JWKS, and default branding state so that the tenant starts from a usable baseline.
2. Journey: support tenant lifecycle.
   1. As a platform administrator, I want to inspect tenant status, admins, and configuration so that I can support tenant issues.
   2. As a platform administrator, I want to suspend, recover, or retire tenants so that platform risk can be controlled.
   3. As a platform administrator, I want to transfer tenant ownership safely so that organizational changes do not strand tenant administration.
3. Journey: manage tenant entitlements and templates.
   1. As a platform administrator, I want to assign tenant feature tiers so that Beta receives the correct platform capabilities.
   2. As a platform administrator, I want to apply tenant templates for login, registration, developer access, and service identity defaults so that onboarding is repeatable.
   3. As a platform administrator, I want to review tenant usage and entitlement drift so that tenants do not receive unapproved capabilities.

## 3. Platform operators

1. Journey: run the shared platform.
   1. As a platform operator, I want to deploy and monitor `tigrbl-auth-idp`, `public-uix`, and admin consoles so that authentication remains available.
   2. As a platform operator, I want to manage scaling, backups, and restore procedures so that the shared platform can survive expected failures.
   3. As a platform operator, I want runtime smoke checks for public, admin, discovery, JWKS, and token surfaces so that deployments are validated quickly.
2. Journey: maintain security posture.
   1. As a platform operator, I want to rotate platform infrastructure secrets and manage runtime configuration so that the service remains secure.
   2. As a platform operator, I want audit-safe break-glass access so that emergencies are handled without bypassing governance.
   3. As a platform operator, I want to patch dependencies and runtime images with change evidence so that the platform remains maintainable.
3. Journey: respond to incidents.
   1. As a platform operator, I want to triage outages across IDP, public UIX, admin UIX, token, and discovery surfaces so that incidents are localized quickly.
   2. As a platform operator, I want to isolate tenant-impacting configuration or key issues so that one tenant's incident does not become a platform-wide failure.
   3. As a platform operator, I want to produce post-incident evidence and recovery notes so that platform owners and affected tenants understand what happened.

## 4. Tenant owner

1. Journey: accept and configure tenancy.
   1. As a tenant owner, I want to claim Beta's tenant boundary so that I become accountable for its users, apps, keys, and policies.
   2. As a tenant owner, I want to configure tenant branding, issuer metadata, and login defaults so that Beta's users recognize the experience.
   3. As a tenant owner, I want to approve tenant baseline policy and registration defaults so that the namespace starts with the right security posture.
2. Journey: delegate tenant authority.
   1. As a tenant owner, I want to appoint tenant admins so that user and credential operations can be handled by the right people.
   2. As a tenant owner, I want to delegate developer and service-owner permissions so that app and machine access are controlled without overgranting.
   3. As a tenant owner, I want to review and revoke delegated permissions periodically so that stale authority does not accumulate.
3. Journey: govern tenant risk and lifecycle.
   1. As a tenant owner, I want to review tenant audit trails, app inventory, and service identities so that I understand who and what can act in my tenant.
   2. As a tenant owner, I want to approve sensitive key rotations, app trust changes, and service identity changes so that high-risk changes are intentional.
   3. As a tenant owner, I want tenant export, retention, and offboarding controls so that Beta can meet lifecycle and compliance obligations.

## 5. Tenant admin

1. Journey: manage tenant identities.
   1. As a tenant admin, I want to create, update, deactivate, and recover tenant users so that Beta can manage its workforce or members.
   2. As a tenant admin, I want to issue credentials and reset access so that users can regain access safely.
   3. As a tenant admin, I want to manage user status, required password changes, and role flags so that tenant access reflects current responsibilities.
2. Journey: manage tenant auth posture.
   1. As a tenant admin, I want to rotate tenant JWKS/signing keys so that Beta controls its signing lifecycle.
   2. As a tenant admin, I want to review tenant apps, service identities, and policy settings so that Beta's namespace stays secure.
   3. As a tenant admin, I want to verify tenant discovery and JWKS publication after changes so that relying parties receive correct metadata.
3. Journey: support tenant users and developers.
   1. As a tenant admin, I want to troubleshoot login, registration, recovery, consent, and logout problems so that users can keep working.
   2. As a tenant admin, I want to approve or reject developer app requests so that applications are registered under tenant policy.
   3. As a tenant admin, I want to grant service or workload access only to approved owners so that machine access stays accountable.

## 6. Tenant user

1. Journey: authenticate into tenant apps.
   1. As a tenant user, I want to log in through Beta's branded `public-uix` so that I can access tenant applications.
   2. As a tenant user, I want to consent to app access so that I understand what an app can use.
   3. As a tenant user, I want sessions and token refresh to behave predictably so that normal app use does not repeatedly interrupt me.
2. Journey: manage personal account access.
   1. As a tenant user, I want registration, forgot password, reset password, logout, and profile flows so that I can self-serve common account needs.
   2. As a tenant user, I want consistent tenant namespace routing so that I do not accidentally authenticate against the wrong tenant.
   3. As a tenant user, I want verification and recovery messages to clearly match my tenant so that I can trust account actions.
3. Journey: control personal authorization.
   1. As a tenant user, I want to see which applications I have authorized so that I understand where my account is being used.
   2. As a tenant user, I want to revoke or end app sessions where supported so that I can reduce unwanted access.
   3. As a tenant user, I want logout to end the intended tenant session so that shared devices and cross-app sessions are handled safely.

## 7. Tenant user developer

1. Journey: create tenant-owned applications.
   1. As a tenant developer, I want to use `developer-uix` to register an OIDC app so that my application can authenticate Beta users.
   2. As a tenant developer, I want to configure redirect URIs, grant types, client auth method, and metadata so that my app integrates correctly.
   3. As a tenant developer, I want to select public or confidential client posture so that my app's credential model matches its runtime.
2. Journey: operate app integration.
   1. As a tenant developer, I want to rotate client secrets or JWKS metadata so that app credentials can be maintained safely.
   2. As a tenant developer, I want discovery URLs and SDK examples so that I can implement login with `@tigrbl-auth/rp` or `tigrbl-identity-rp`.
   3. As a tenant developer, I want test and production client records so that I can validate integration before affecting users.
3. Journey: debug and evolve tenant apps.
   1. As a tenant developer, I want to inspect authorization, callback, token, and logout failures so that I can resolve integration issues.
   2. As a tenant developer, I want to update scopes and consent metadata so that users see accurate permission prompts.
   3. As a tenant developer, I want to decommission old clients safely so that stale redirect URIs and secrets stop working.

## 8. Tenant's customer

1. Journey: use a tenant-created app.
   1. As a tenant's customer, I want to register or log in through the tenant-branded public auth experience so that I can use the tenant's application.
   2. As a tenant's customer, I want forgot password, reset password, logout, and account verification so that I can self-manage access.
   3. As a tenant's customer, I want the login experience to make the tenant and app identity clear so that I trust where I am authenticating.
2. Journey: authorize application access.
   1. As a tenant's customer, I want to see consent prompts that name the tenant app so that I know what I am authorizing.
   2. As a tenant's customer, I want session and logout behavior to work across the app and identity provider so that access ends predictably.
   3. As a tenant's customer, I want consent to match the app's requested scopes so that I am not surprised by what the app can access.
3. Journey: manage customer account lifecycle.
   1. As a tenant's customer, I want to update my profile and contact data where allowed so that the tenant has current account information.
   2. As a tenant's customer, I want to recover access without contacting support for common issues so that app access remains self-service.
   3. As a tenant's customer, I want clear account closure or access-removal behavior so that I understand what happens when I leave the tenant app.

## 9. Tenant's customer developer

1. Journey: integrate with a tenant's developer ecosystem.
   1. As a tenant's customer developer, I want delegated access to a developer portal so that I can register an app against the tenant's federation.
   2. As a tenant's customer developer, I want app credentials, redirect URI management, and discovery metadata so that my integration can authenticate users.
   3. As a tenant's customer developer, I want delegated permissions scoped to only my customer organization or app so that I cannot affect unrelated tenant integrations.
2. Journey: consume tenant-protected APIs.
   1. As a tenant's customer developer, I want token, JWKS, and introspection guidance so that my app can call tenant APIs correctly.
   2. As a tenant's customer developer, I want sandbox/test clients so that I can validate integration before production approval.
   3. As a tenant's customer developer, I want resource and audience guidance so that access tokens are accepted by the right protected APIs.
3. Journey: operate third-party integration lifecycle.
   1. As a tenant's customer developer, I want to rotate credentials without tenant support tickets so that my integration can meet my security policy.
   2. As a tenant's customer developer, I want to see integration audit events relevant to my apps so that I can troubleshoot and prove usage.
   3. As a tenant's customer developer, I want to request approval for expanded scopes so that the tenant can govern risk before production use.

## 10. Direct customer owner / admin / developer / user

1. Journey: onboard as a direct Acme customer.
   1. As a direct customer owner, I want Acme to provision my organization as a first-class tenant so that I can manage my own identity boundary.
   2. As a direct customer admin, I want tenant-admin capabilities so that I can manage users, credentials, keys, and policy without Acme doing it for me.
   3. As a direct customer owner, I want to assign admins, developers, and service owners so that my organization can operate independently.
2. Journey: build and use direct customer apps.
   1. As a direct customer developer, I want `developer-uix` and RP SDKs so that I can register apps and implement login for my organization.
   2. As a direct customer user, I want `public-uix` login, registration, recovery, consent, logout, and profile flows so that I can use my organization's apps.
   3. As a direct customer developer, I want tenant discovery and SDK guidance so that my apps integrate without depending on Acme support.
3. Journey: operate direct customer security.
   1. As a direct customer admin, I want to rotate tenant keys and review app/service access so that my organization controls its own risk.
   2. As a direct customer owner, I want audit and compliance evidence for my tenant so that I can satisfy internal and external reviews.
   3. As a direct customer user, I want clear account recovery, consent, and logout behavior so that I can trust the direct customer identity experience.

---

## Story-Product Matrix

Product columns:

- `IDP`: `tigrbl-auth-idp`
- `Platform Admin`: `tigrbl-auth-platform-admin-console` / `platform-admin-uix`
- `Tenant Admin`: `tigrbl-auth-tenant-admin-console` / `tenant-admin-uix`
- `Public Portal`: `tigrbl-auth-public-portal` / `public-uix`
- `Developer Portal`: `tigrbl-auth-developer-portal` / `developer-uix`
- `Service Admin`: `tigrbl-auth-service-admin-surface` / `service-admin-uix`
- `SDK/API`: RP SDKs, resource-server helpers, protected API integration, or protocol-facing integration docs

Cell legend:

- ✅ Product is directly involved in the story.
- Blank cell means the product is not directly involved in that story.

| Role | Journey | Story | IDP | Platform Admin | Tenant Admin | Public Portal | Developer Portal | Service Admin | SDK/API |
|---|---|---|---|---|---|---|---|---|---|
| Platform owner | establish the identity platform | configure global IDP, domains, compliance posture, and default tenant policies | ✅ | ✅ |  |  |  |  |  |
| Platform owner | establish the identity platform | define tenancy model, authority boundaries, and product tiers | ✅ | ✅ |  |  |  |  |  |
| Platform owner | establish the identity platform | view tenant, operator, and security boundaries | ✅ | ✅ |  |  |  |  |  |
| Platform owner | delegate platform authority | appoint platform administrators and operators | ✅ | ✅ |  |  |  |  |  |
| Platform owner | delegate platform authority | require approval rules for privileged changes | ✅ | ✅ |  |  |  |  |  |
| Platform owner | delegate platform authority | separate business administration from runtime operations | ✅ | ✅ |  |  |  |  |  |
| Platform owner | steer platform lifecycle and risk | review adoption, incident, compliance, and tenant-risk reports | ✅ | ✅ |  |  |  |  |  |
| Platform owner | steer platform lifecycle and risk | approve rollout of developer and service product surfaces | ✅ | ✅ |  |  | ✅ | ✅ |  |
| Platform owner | steer platform lifecycle and risk | review certification and evidence summaries | ✅ | ✅ |  |  |  |  |  |
| Platform administrator | onboard tenants | create tenant Beta | ✅ | ✅ |  |  |  |  |  |
| Platform administrator | onboard tenants | assign tenant owner or tenant admin | ✅ | ✅ | ✅ |  |  |  |  |
| Platform administrator | onboard tenants | verify tenant discovery, JWKS, and default branding | ✅ | ✅ | ✅ | ✅ |  |  |  |
| Platform administrator | support tenant lifecycle | inspect tenant status, admins, and configuration | ✅ | ✅ |  |  |  |  |  |
| Platform administrator | support tenant lifecycle | suspend, recover, or retire tenants | ✅ | ✅ |  |  |  |  |  |
| Platform administrator | support tenant lifecycle | transfer tenant ownership safely | ✅ | ✅ | ✅ |  |  |  |  |
| Platform administrator | manage tenant entitlements and templates | assign tenant feature tiers | ✅ | ✅ |  |  |  |  |  |
| Platform administrator | manage tenant entitlements and templates | apply tenant templates for login, registration, developer access, and service identity | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |  |
| Platform administrator | manage tenant entitlements and templates | review tenant usage and entitlement drift | ✅ | ✅ |  |  |  |  |  |
| Platform operators | run the shared platform | deploy and monitor IDP, public UIX, and admin consoles | ✅ | ✅ | ✅ | ✅ |  |  |  |
| Platform operators | run the shared platform | manage scaling, backups, and restore procedures | ✅ |  |  |  |  |  |  |
| Platform operators | run the shared platform | run smoke checks for public, admin, discovery, JWKS, and token surfaces | ✅ | ✅ | ✅ | ✅ |  |  |  |
| Platform operators | maintain security posture | rotate platform infrastructure secrets and runtime configuration | ✅ | ✅ |  |  |  |  |  |
| Platform operators | maintain security posture | use audit-safe break-glass access | ✅ | ✅ |  |  |  |  |  |
| Platform operators | maintain security posture | patch dependencies and runtime images with change evidence | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Platform operators | respond to incidents | triage outages across IDP, UIX, token, and discovery surfaces | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |  |
| Platform operators | respond to incidents | isolate tenant-impacting configuration or key issues | ✅ | ✅ | ✅ |  |  |  |  |
| Platform operators | respond to incidents | produce post-incident evidence and recovery notes | ✅ | ✅ |  |  |  |  |  |
| Tenant owner | accept and configure tenancy | claim Beta's tenant boundary | ✅ |  | ✅ |  |  |  |  |
| Tenant owner | accept and configure tenancy | configure tenant branding, issuer metadata, and login defaults | ✅ |  | ✅ | ✅ |  |  |  |
| Tenant owner | accept and configure tenancy | approve baseline policy and registration defaults | ✅ |  | ✅ |  | ✅ | ✅ |  |
| Tenant owner | delegate tenant authority | appoint tenant admins | ✅ |  | ✅ |  |  |  |  |
| Tenant owner | delegate tenant authority | delegate developer and service-owner permissions | ✅ |  | ✅ |  | ✅ | ✅ |  |
| Tenant owner | delegate tenant authority | review and revoke delegated permissions | ✅ |  | ✅ |  | ✅ | ✅ |  |
| Tenant owner | govern tenant risk and lifecycle | review audit trails, app inventory, and service identities | ✅ |  | ✅ |  | ✅ | ✅ |  |
| Tenant owner | govern tenant risk and lifecycle | approve key rotations, app trust changes, and service identity changes | ✅ |  | ✅ |  | ✅ | ✅ |  |
| Tenant owner | govern tenant risk and lifecycle | manage tenant export, retention, and offboarding controls | ✅ |  | ✅ |  |  |  |  |
| Tenant admin | manage tenant identities | create, update, deactivate, and recover tenant users | ✅ |  | ✅ | ✅ |  |  |  |
| Tenant admin | manage tenant identities | issue credentials and reset access | ✅ |  | ✅ | ✅ |  |  |  |
| Tenant admin | manage tenant identities | manage user status, password-change requirements, and role flags | ✅ |  | ✅ |  |  |  |  |
| Tenant admin | manage tenant auth posture | rotate tenant JWKS and signing keys | ✅ |  | ✅ |  |  |  |  |
| Tenant admin | manage tenant auth posture | review tenant apps, service identities, and policy settings | ✅ |  | ✅ |  | ✅ | ✅ |  |
| Tenant admin | manage tenant auth posture | verify tenant discovery and JWKS publication | ✅ |  | ✅ | ✅ |  |  |  |
| Tenant admin | support tenant users and developers | troubleshoot login, registration, recovery, consent, and logout | ✅ |  | ✅ | ✅ |  |  |  |
| Tenant admin | support tenant users and developers | approve or reject developer app requests | ✅ |  | ✅ |  | ✅ |  |  |
| Tenant admin | support tenant users and developers | grant service or workload access to approved owners | ✅ |  | ✅ |  |  | ✅ |  |
| Tenant user | authenticate into tenant apps | log in through tenant-branded public UIX | ✅ |  |  | ✅ |  |  |  |
| Tenant user | authenticate into tenant apps | consent to app access | ✅ |  |  | ✅ |  |  | ✅ |
| Tenant user | authenticate into tenant apps | use predictable sessions and token refresh | ✅ |  |  | ✅ |  |  | ✅ |
| Tenant user | manage personal account access | register, recover password, reset password, logout, and manage profile | ✅ |  |  | ✅ |  |  |  |
| Tenant user | manage personal account access | route consistently through the correct tenant namespace | ✅ |  |  | ✅ |  |  |  |
| Tenant user | manage personal account access | receive tenant-matched verification and recovery messages | ✅ |  |  | ✅ |  |  |  |
| Tenant user | control personal authorization | view authorized applications | ✅ |  |  | ✅ |  |  |  |
| Tenant user | control personal authorization | revoke or end app sessions where supported | ✅ |  |  | ✅ |  |  | ✅ |
| Tenant user | control personal authorization | log out of the intended tenant session | ✅ |  |  | ✅ |  |  |  |
| Tenant user developer | create tenant-owned applications | register an OIDC app | ✅ |  |  |  | ✅ |  |  |
| Tenant user developer | create tenant-owned applications | configure redirect URIs, grants, client auth method, and metadata | ✅ |  |  |  | ✅ |  |  |
| Tenant user developer | create tenant-owned applications | select public or confidential client posture | ✅ |  |  |  | ✅ |  |  |
| Tenant user developer | operate app integration | rotate client secrets or JWKS metadata | ✅ |  |  |  | ✅ |  |  |
| Tenant user developer | operate app integration | use discovery URLs and SDK examples | ✅ |  |  |  | ✅ |  | ✅ |
| Tenant user developer | operate app integration | manage test and production client records | ✅ |  |  |  | ✅ |  | ✅ |
| Tenant user developer | debug and evolve tenant apps | inspect authorization, callback, token, and logout failures | ✅ |  |  | ✅ | ✅ |  | ✅ |
| Tenant user developer | debug and evolve tenant apps | update scopes and consent metadata | ✅ |  |  | ✅ | ✅ |  |  |
| Tenant user developer | debug and evolve tenant apps | decommission old clients safely | ✅ |  |  |  | ✅ |  |  |
| Tenant's customer | use a tenant-created app | register or log in through tenant-branded auth | ✅ |  |  | ✅ |  |  |  |
| Tenant's customer | use a tenant-created app | recover password, reset password, logout, and verify account | ✅ |  |  | ✅ |  |  |  |
| Tenant's customer | use a tenant-created app | see clear tenant and app identity in login | ✅ |  |  | ✅ |  |  | ✅ |
| Tenant's customer | authorize application access | see consent prompts that name the tenant app | ✅ |  |  | ✅ | ✅ |  |  |
| Tenant's customer | authorize application access | use session and logout across app and IDP | ✅ |  |  | ✅ |  |  | ✅ |
| Tenant's customer | authorize application access | see consent that matches requested scopes | ✅ |  |  | ✅ | ✅ |  |  |
| Tenant's customer | manage customer account lifecycle | update profile and contact data where allowed | ✅ |  | ✅ | ✅ |  |  |  |
| Tenant's customer | manage customer account lifecycle | recover access without support for common issues | ✅ |  |  | ✅ |  |  |  |
| Tenant's customer | manage customer account lifecycle | understand account closure or access-removal behavior | ✅ |  | ✅ | ✅ |  |  |  |
| Tenant's customer developer | integrate with a tenant's developer ecosystem | receive delegated access to developer portal | ✅ |  | ✅ |  | ✅ |  |  |
| Tenant's customer developer | integrate with a tenant's developer ecosystem | manage app credentials, redirect URIs, and discovery metadata | ✅ |  |  |  | ✅ |  | ✅ |
| Tenant's customer developer | integrate with a tenant's developer ecosystem | receive delegated permissions scoped to customer organization or app | ✅ |  | ✅ |  | ✅ |  |  |
| Tenant's customer developer | consume tenant-protected APIs | use token, JWKS, and introspection guidance | ✅ |  |  |  | ✅ |  | ✅ |
| Tenant's customer developer | consume tenant-protected APIs | use sandbox and test clients before production approval | ✅ |  |  |  | ✅ |  | ✅ |
| Tenant's customer developer | consume tenant-protected APIs | follow resource and audience guidance for protected APIs | ✅ |  |  |  | ✅ |  | ✅ |
| Tenant's customer developer | operate third-party integration lifecycle | rotate credentials without tenant support tickets | ✅ |  |  |  | ✅ |  |  |
| Tenant's customer developer | operate third-party integration lifecycle | view relevant integration audit events | ✅ |  | ✅ |  | ✅ |  |  |
| Tenant's customer developer | operate third-party integration lifecycle | request approval for expanded scopes | ✅ |  | ✅ |  | ✅ |  |  |
| Direct customer owner / admin / developer / user | onboard as a direct Acme customer | provision organization as a first-class tenant | ✅ | ✅ | ✅ |  |  |  |  |
| Direct customer owner / admin / developer / user | onboard as a direct Acme customer | use tenant-admin capabilities without Acme operating the tenant | ✅ |  | ✅ |  |  |  |  |
| Direct customer owner / admin / developer / user | onboard as a direct Acme customer | assign admins, developers, and service owners | ✅ |  | ✅ |  | ✅ | ✅ |  |
| Direct customer owner / admin / developer / user | build and use direct customer apps | register apps and implement login with developer UIX and RP SDKs | ✅ |  |  |  | ✅ |  | ✅ |
| Direct customer owner / admin / developer / user | build and use direct customer apps | use public UIX login, registration, recovery, consent, logout, and profile | ✅ |  |  | ✅ |  |  |  |
| Direct customer owner / admin / developer / user | build and use direct customer apps | use tenant discovery and SDK guidance | ✅ |  |  | ✅ | ✅ |  | ✅ |
| Direct customer owner / admin / developer / user | operate direct customer security | rotate tenant keys and review app/service access | ✅ |  | ✅ |  | ✅ | ✅ |  |
| Direct customer owner / admin / developer / user | operate direct customer security | review audit and compliance evidence for the tenant | ✅ | ✅ | ✅ |  |  |  |  |
| Direct customer owner / admin / developer / user | operate direct customer security | trust account recovery, consent, and logout behavior | ✅ |  |  | ✅ |  |  |  |


