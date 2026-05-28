# Competitor Product Surface Research

Research date: 2026-05-27

Scope: five identity-platform competitors with public product/API/SDK/UIX documentation: Auth0, Okta, Keycloak, FusionAuth, and Amazon Cognito. This file treats a "product surface" as any externally documented API, SDK/client library family, hosted UI/console UI, workflow/admin surface, or extension/runtime surface that a customer or integrator can directly use. The feature lists below are grouped from public documentation, not pricing pages.

## Auth0

Auth0 advertises a smaller number of named APIs than it has product capabilities. The main product split is Authentication API, Management API, My Account API, My Organization API, SDKs, Universal Login/Dashboard UI, and extensibility surfaces such as Actions.

### Auth0 API Products

| Product / API surface | Product role | Feature groups | Primary evidence |
|---|---|---|---|
| Authentication API | Public authorization-server and authentication protocol surface. | OAuth/OIDC authorization, token exchange, refresh token use, logout, userinfo, passwordless endpoints, MFA challenge/verify flow, token revocation, M2M/client credentials token issuance, database connection signup/login flows. | [Auth0 Authentication API Reference](https://auth0.com/docs/api/authentication), [Auth0 OAuth 2.0 Authorization Framework](https://auth0.com/docs/authenticate/protocols/oauth), [Auth0 Client Credentials Flow](https://auth0.com/docs/get-started/authentication-and-authorization-flow/client-credentials-flow) |
| Management API v2 | Tenant/application/user/control-plane API. | Users, clients/applications, APIs/resource servers, organizations, roles/RBAC, permissions, connections/IdPs, tenants, email templates, jobs, log streams/logs, custom domains, keys/signing keys, branding/prompts, Guardian/MFA, Actions, grants/device credentials. | [Auth0 Management API v2](https://auth0.com/docs/api/management/v2), [Auth0 Management API Clients](https://auth0.com/docs/api/management/v2/clients), [Auth0 Management API Users](https://auth0.com/docs/api/management/v2/users), [Auth0 Management API Organizations](https://auth0.com/docs/api/management/v2/organizations) |
| My Account API | End-user self-service API for account security and profile-adjacent operations. | Authentication methods, passkeys/WebAuthn credentials, enrolled authenticators, account recovery/credential self-service patterns, end-user scoped access. | [Auth0 My Account API](https://auth0.com/docs/api/myaccount/), [Auth0 Passkeys](https://auth0.com/docs/authenticate/database-connections/passkeys) |
| My Organization API | Delegated organization self-service API. | Organization metadata, organization members, member roles, organization invitations, organization branding/connection context, delegated organization administration. | [Auth0 My Organization API](https://auth0.com/docs/api/myorganization), [Auth0 Organizations](https://auth0.com/docs/manage-users/organizations) |
| Fine-Grained Authorization | Relationship/permission decision product adjacent to authentication. | Authorization model, stores, tuples, checks, list objects/users, writes, assertions, authorization DSL and SDK/client access. | [Auth0 Fine-Grained Authorization Docs](https://auth0.com/docs/authorization), [Auth0 FGA API Explorer](https://docs.fga.dev/api/service) |

### Auth0 SDK Products

| SDK / library family | Target user | Feature groups | Primary evidence |
|---|---|---|---|
| Browser and SPA SDKs | Browser app developers. | Authorization-code with PKCE, redirect login/logout, token caching, silent refresh/session checks, user profile loading, route guards through framework bindings. | [Auth0 Single Page App SDK](https://auth0.com/docs/libraries/auth0-single-page-app-sdk), [Auth0 React SDK](https://auth0.com/docs/libraries/auth0-react), [Auth0 Angular SDK](https://auth0.com/docs/libraries/auth0-angular-spa) |
| Server-side web SDKs | Backend-rendered apps and API servers. | Login/logout routes, callback handling, session cookies, access token retrieval, ID token/profile access, framework middleware. | [Auth0 Next.js SDK](https://auth0.com/docs/libraries/auth0-nextjs), [Auth0 Express OpenID Connect SDK](https://auth0.com/docs/libraries/auth0-express-openid-connect), [Auth0 ASP.NET Core SDK](https://auth0.com/docs/libraries/auth0-aspnet-core) |
| Mobile and native SDKs | Native app developers. | Universal Login handoff, callback handling, credential storage, token renewal, biometric/passkey-adjacent platform integration where supported. | [Auth0 iOS / macOS SDK](https://auth0.com/docs/libraries/auth0-swift), [Auth0 Android SDK](https://auth0.com/docs/libraries/auth0-android) |
| Management/API SDKs | Admin automation and platform integrators. | Management API clients, Authentication API clients, user/client/organization/connection/key/log automation. | [Auth0 Node Management SDK](https://github.com/auth0/node-auth0), [Auth0 Python SDK](https://github.com/auth0/auth0-python), [Auth0 .NET SDK](https://github.com/auth0/auth0.net) |
| FGA SDKs | Authorization system implementers. | Store/model/tuple/check APIs, writes, reads, assertion checks, relationship-based authorization. | [OpenFGA SDKs](https://openfga.dev/docs/getting-started/setup-sdk-client), [Auth0 FGA API Explorer](https://docs.fga.dev/api/service) |

### Auth0 UIX / Hosted UI Products

| UIX product | Primary actor | Feature groups | Primary evidence |
|---|---|---|---|
| Universal Login | End users and app developers. | Hosted login, signup, identifier-first login, MFA prompts, password reset, passwordless prompts, social/enterprise federation prompts, branding/customization. | [Auth0 Universal Login](https://auth0.com/docs/authenticate/login/auth0-universal-login), [Customize Universal Login](https://auth0.com/docs/customize/login-pages/universal-login) |
| Auth0 Dashboard | Tenant admins, operators, developers. | Application/client setup, API/resource server setup, user management, organizations, connections, branding, Actions, logs, tenant settings, signing keys. | [Auth0 Dashboard Overview](https://auth0.com/docs/get-started/auth0-overview/dashboard), [Auth0 Tenant Settings](https://auth0.com/docs/get-started/tenant-settings) |
| Organizations UX | SaaS admins and organization members. | Organization invitations, org membership, org-aware login, member roles, organization branding and connections. | [Auth0 Organizations](https://auth0.com/docs/manage-users/organizations), [Auth0 Organization Login Flow](https://auth0.com/docs/manage-users/organizations/login-flows-for-organizations) |
| Branding and prompts UI | Tenant admins and designers. | Branding colors/logo, custom domains, prompt customization, text customization, page templates. | [Auth0 Customize](https://auth0.com/docs/customize), [Auth0 Branding API](https://auth0.com/docs/api/management/v2/branding) |

### Auth0 Extensibility / Operations Products

| Product surface | Product role | Feature groups | Primary evidence |
|---|---|---|---|
| Actions | Login/runtime extension platform. | Post-login, credentials exchange, pre/post user registration, password reset/post-change hooks, custom JavaScript actions, secrets, versions, deployments. | [Auth0 Actions](https://auth0.com/docs/customize/actions), [Auth0 Management API Actions](https://auth0.com/docs/api/management/v2/actions) |
| Logs and log streams | Observability and audit integration. | Tenant logs, event search, log streams, external SIEM/event destinations. | [Auth0 Logs](https://auth0.com/docs/deploy-monitor/logs), [Auth0 Management API Logs](https://auth0.com/docs/api/management/v2/logs) |
| Security features | Tenant security posture. | MFA, attack protection, breached password detection, bot detection, suspicious IP throttling, token/security settings. | [Auth0 Multi-Factor Authentication](https://auth0.com/docs/secure/multi-factor-authentication), [Auth0 Attack Protection](https://auth0.com/docs/secure/attack-protection) |

## Okta

Okta's surface area is broader than a single API. The public catalog divides API Access Management/OIDC, Management APIs, MyAccount APIs, SCIM APIs, SDKs, Sign-In Widget/UI, Admin Console, Workflows/hooks, and service-app M2M patterns.

### Okta API Products

| Product / API surface | Product role | Feature groups | Primary evidence |
|---|---|---|---|
| OIDC and OAuth 2.0 API | Authorization-server and token protocol surface. | Discovery, authorize, token, userinfo, JWKS, introspection, revocation, device authorization where supported, dynamic client registration references, custom authorization servers. | [Okta OpenID Connect and OAuth 2.0 Reference](https://developer.okta.com/docs/reference/api/oidc/), [Okta OAuth 2.0 API](https://developer.okta.com/docs/api/openapi/okta-oauth/oauth/overview/) |
| Management API | Administrative control plane. | Users, groups, applications, authorization servers, policies, authenticators, factors, identity providers, brands, custom domains, event hooks, inline hooks, templates, system log, zones, API tokens. | [Okta Management API Overview](https://developer.okta.com/docs/api/openapi/okta-management/guides/overview/), [Okta Users API](https://developer.okta.com/docs/api/openapi/okta-management/management/tag/User/), [Okta Applications API](https://developer.okta.com/docs/api/openapi/okta-management/management/tag/Application/) |
| MyAccount API | End-user self-service API. | Profile access, password operations, email/phone/authenticator enrollment and lifecycle, self-service account security operations. | [Okta MyAccount API Overview](https://developer.okta.com/docs/api/openapi/okta-myaccount/myaccount/overview/), [Okta MyAccount Authenticators](https://developer.okta.com/docs/api/openapi/okta-myaccount/myaccount/tag/Authenticator/) |
| API Access Management | API authorization product. | Custom authorization servers, access policies/rules, scopes/claims, resource server concepts, token customization, token validation/introspection. | [Okta API Access Management](https://developer.okta.com/docs/concepts/api-access-management/), [Okta Authorization Servers API](https://developer.okta.com/docs/reference/api/authorization-servers/) |
| OAuth for service apps | M2M/service-account authorization. | Private key JWT client authentication, client credentials, Okta service app setup, scoped OAuth access to Okta management APIs. | [Okta OAuth for Service Apps](https://developer.okta.com/docs/guides/implement-oauth-for-okta-serviceapp/), [Okta Client Credentials Flow](https://developer.okta.com/docs/guides/implement-grant-type/clientcreds/main/) |
| SCIM protocol surface | Inbound/outbound provisioning integration. | SCIM 2.0 user/group provisioning, schemas, create/read/update/delete, enterprise provisioning integration. | [Okta SCIM 2.0 Guide](https://developer.okta.com/docs/api/openapi/okta-scim/guides/scim-20/), [Okta SCIM Concepts](https://developer.okta.com/docs/concepts/scim/) |

### Okta SDK Products

| SDK / library family | Target user | Feature groups | Primary evidence |
|---|---|---|---|
| Okta Auth JS | Browser and JavaScript app developers. | Token acquisition, token manager, session operations, IDX/Identity Engine flows, PKCE helpers, sign-in integration. | [Okta Auth JS](https://github.com/okta/okta-auth-js), [Okta JavaScript SDKs](https://developer.okta.com/code/javascript/) |
| Framework SDKs | SPA and web framework developers. | React/Angular/Vue route protection, callback components, auth state providers, token handling. | [Okta React SDK](https://github.com/okta/okta-react), [Okta Angular SDK](https://github.com/okta/okta-angular), [Okta Vue SDK](https://github.com/okta/okta-vue) |
| Server-side SDKs | Backend service developers. | OIDC middleware, JWT validation, session/callback integration, user/group/app management helpers in management SDKs. | [Okta .NET SDKs](https://developer.okta.com/code/dotnet/), [Okta Java SDKs](https://developer.okta.com/code/java/), [Okta Node.js SDK](https://github.com/okta/okta-sdk-nodejs) |
| Mobile SDKs | Native app developers. | OIDC login, browser handoff, token storage, native callback handling, Identity Engine flows. | [Okta Mobile SDKs](https://developer.okta.com/code/mobile/) |
| JWT verifier libraries | Resource-server developers. | Local JWT validation, issuer/audience checks, JWKS fetching/caching, access token validation. | [Okta JWT Verifier for Node.js](https://github.com/okta/okta-jwt-verifier-js), [Validate Access Tokens](https://developer.okta.com/docs/guides/validate-access-tokens/) |

### Okta UIX / Hosted UI Products

| UIX product | Primary actor | Feature groups | Primary evidence |
|---|---|---|---|
| Okta-hosted sign-in | End users and app developers. | Hosted login, redirect authentication, branding/theme integration, Identity Engine remediation, MFA/authenticator prompts. | [Okta Sign-In Experience](https://help.okta.com/oie/en-us/content/topics/identity-engine/identity-engine-sign-in.htm), [Okta Brands API](https://developer.okta.com/docs/api/openapi/okta-management/management/tag/Brand/) |
| Sign-In Widget | App developers embedding Okta UX. | Embedded login component, IDX flow handling, MFA/authenticator enrollment, password recovery, social/IdP routing, custom branding. | [Okta Sign-In Widget Concept](https://developer.okta.com/docs/concepts/sign-in-widget/), [Okta Sign-In Widget GitHub](https://github.com/okta/okta-signin-widget) |
| Admin Console | Org admins and operators. | Users/groups/apps/policies/authenticators/admin roles/branding/security/logs configuration. | [Okta Admin Console Overview](https://help.okta.com/oie/en-us/content/topics/settings/settings-admin-console.htm), [Okta Management API Overview](https://developer.okta.com/docs/api/openapi/okta-management/guides/overview/) |
| End-User Dashboard | End users. | App launchpad, self-service app access, profile/password/security settings, dashboard personalization. | [Okta End-User Dashboard](https://help.okta.com/oie/en-us/content/topics/end-user/dashboard-overview.htm), [Okta MyAccount API Overview](https://developer.okta.com/docs/api/openapi/okta-myaccount/myaccount/overview/) |

### Okta Extensibility / Operations Products

| Product surface | Product role | Feature groups | Primary evidence |
|---|---|---|---|
| Event Hooks and Inline Hooks | Event-driven and inline runtime extension. | Event subscriptions, external HTTP delivery, token/password/import/registration inline hooks, hook verification and lifecycle APIs. | [Okta Event Hooks](https://developer.okta.com/docs/concepts/event-hooks/), [Okta Inline Hooks](https://developer.okta.com/docs/concepts/inline-hooks/) |
| System Log | Audit and compliance observability. | Event search, correlation, actor/client/target metadata, security event history. | [Okta System Log](https://developer.okta.com/docs/concepts/system-log/), [Okta System Log API](https://developer.okta.com/docs/api/openapi/okta-management/management/tag/SystemLog/) |
| Workflows | Low-code identity automation. | Event-triggered automations, connectors, scheduled flows, app lifecycle and identity operations. | [Okta Workflows](https://help.okta.com/wf/en-us/content/topics/workflows/workflows-main.htm), [Okta Workflows Connector Builder](https://help.okta.com/wf/en-us/content/topics/workflows/connector-builder/connector-builder.htm) |

## Keycloak

Keycloak is packaged as an identity server rather than a hosted SaaS, but its documented product surfaces still split into protocol endpoints, Admin REST API, Client Registration, Account/Admin/Login consoles, adapters/SDKs, and provider SPIs.

### Keycloak API Products

| Product / API surface | Product role | Feature groups | Primary evidence |
|---|---|---|---|
| Realm OIDC/OAuth endpoints | Public authorization-server protocol surface. | Discovery, authorize, token, userinfo, JWKS/certs, logout, introspection, token revocation, client credentials/service-account token issuance. | [Keycloak OIDC Endpoint Layers](https://www.keycloak.org/securing-apps/oidc-layers), [Keycloak Securing Applications](https://www.keycloak.org/docs/latest/securing_apps/) |
| SAML protocol endpoints | Federation/protocol surface for SAML clients. | SAML clients, IdP/SP metadata, SSO/SLO, assertions, client configuration. | [Keycloak SAML Galleon / SAML Client Docs](https://www.keycloak.org/docs/latest/securing_apps/#saml), [Keycloak Server Administration Guide](https://www.keycloak.org/docs/latest/server_admin/) |
| Admin REST API | Administrative control plane. | Realms, clients, users, groups, roles, client scopes, identity providers, authentication flows, components, keys, sessions, events, organizations where available. | [Keycloak Admin REST API](https://www.keycloak.org/docs-api/26.5.2/rest-api/), [Keycloak Server Administration Guide](https://www.keycloak.org/docs/latest/server_admin/) |
| Client Registration Service | Dynamic client/application registration surface. | Anonymous/authenticated client registration, registration access tokens, initial access tokens, client update/delete, registration policies. | [Keycloak Client Registration](https://www.keycloak.org/securing-apps/client-registration) |
| Authorization Services / Protection API | Resource-server authorization product. | Resources, scopes, policies, permissions, UMA protection API, entitlement/permission checks, policy enforcement. | [Keycloak Authorization Services](https://www.keycloak.org/docs/latest/authorization_services/), [Keycloak Authorization Services REST](https://www.keycloak.org/docs/latest/authorization_services/#_service_overview) |

### Keycloak SDK / Adapter Products

| SDK / adapter family | Target user | Feature groups | Primary evidence |
|---|---|---|---|
| JavaScript adapter | Browser app developers. | Login/logout, token acquisition, token refresh, session status iframe, authorization-code flow, implicit/hybrid legacy support notes. | [Keycloak JavaScript Adapter](https://www.keycloak.org/securing-apps/javascript-adapter) |
| Server/application adapters | Backend and framework developers. | OIDC integration patterns, bearer token protection, adapter migration guidance, generic OIDC/RP integration. | [Keycloak Securing Applications](https://www.keycloak.org/docs/latest/securing_apps/) |
| Java Admin Client | Admin automation developers. | Typed Admin REST client for realms, users, clients, roles, groups, sessions, events, components. | [Keycloak Java Admin Client](https://www.keycloak.org/securing-apps/admin-client) |
| Policy enforcer adapters | Resource-server developers. | Authorization Services policy enforcement, resource/scope permissions, entitlement checks, path/resource mapping. | [Keycloak Policy Enforcer](https://www.keycloak.org/docs/latest/authorization_services/#_enforcer_overview) |

### Keycloak UIX / Hosted UI Products

| UIX product | Primary actor | Feature groups | Primary evidence |
|---|---|---|---|
| Admin Console | Realm admins and operators. | Realm settings, clients, users, groups, roles, identity providers, authentication flows, sessions, events, realm keys, organizations where enabled. | [Keycloak Admin Console](https://www.keycloak.org/docs/latest/server_admin/#admin-console), [Keycloak Server Administration Guide](https://www.keycloak.org/docs/latest/server_admin/) |
| Account Console | End users. | Profile update, password update, account security, active sessions, linked accounts, applications/consents, device activity depending on configuration. | [Keycloak Account Console](https://www.keycloak.org/docs/latest/server_admin/#account-console) |
| Login pages and themes | End users, admins, designers. | Login, registration, reset credentials, OTP/WebAuthn/MFA pages, email templates, custom themes, theme inheritance. | [Keycloak Themes](https://www.keycloak.org/docs/latest/server_admin/#_themes), [Keycloak Server Development Themes](https://www.keycloak.org/docs/latest/server_development/#_themes) |

### Keycloak Extensibility / Operations Products

| Product surface | Product role | Feature groups | Primary evidence |
|---|---|---|---|
| SPIs and provider extensions | Server extension model. | Authentication SPI, user storage SPI, event listener SPI, required actions, identity-provider mappers, protocol mappers, custom REST resources. | [Keycloak Server Development Guide](https://www.keycloak.org/docs/latest/server_development/), [Keycloak Event Listener SPI](https://www.keycloak.org/docs/latest/server_development/#_events) |
| Authentication flows | Policy/runtime orchestration. | Browser/direct grant/client auth flows, executions, authenticators, required actions, OTP, WebAuthn, conditional flows. | [Keycloak Authentication Flows](https://www.keycloak.org/docs/latest/server_admin/#_authentication-flows) |
| Events and auditing | Audit and operational observability. | Login/admin events, event listeners, event storage, event details, admin event tracking. | [Keycloak Events](https://www.keycloak.org/docs/latest/server_admin/#_events), [Keycloak Event Listener SPI](https://www.keycloak.org/docs/latest/server_development/#_events) |

## FusionAuth

FusionAuth exposes a large, granular API catalog. Its shape is closer to "one platform API catalog with many resources" plus SDKs, hosted login/theme UI, Admin UI, Lambdas/Webhooks, and Tenant Manager.

### FusionAuth API Products

| Product / API surface | Product role | Feature groups | Primary evidence |
|---|---|---|---|
| OAuth/OIDC and Login APIs | Public authentication and token surface. | Authorization endpoint, token endpoint, userinfo, logout, refresh tokens, client credentials, device code where documented, login API, registration login, passwordless login. | [FusionAuth OAuth Endpoints](https://fusionauth.io/docs/lifecycle/authenticate-users/oauth/endpoints), [FusionAuth Login API](https://fusionauth.io/docs/apis/login), [FusionAuth JWT API](https://fusionauth.io/docs/apis/jwt) |
| User and Registration APIs | Identity and app-membership administration. | Users, registrations, consent, families, actioning users, comments, password lifecycle, user search, bulk import, identity verification. | [FusionAuth User API](https://fusionauth.io/docs/apis/users), [FusionAuth User Registration API](https://fusionauth.io/docs/apis/registrations), [FusionAuth Actioning Users API](https://fusionauth.io/docs/apis/actioning-users) |
| Application / Tenant / Group APIs | Product control plane. | Applications, OAuth scopes, tenants, tenant manager, groups, roles, app configuration, tenant isolation. | [FusionAuth Application API](https://fusionauth.io/docs/apis/applications), [FusionAuth Tenants API](https://fusionauth.io/docs/apis/tenants), [FusionAuth Group API](https://fusionauth.io/docs/apis/groups) |
| Credential and security APIs | Credential lifecycle and security controls. | API keys, keys, JWT signing/validation, MFA, WebAuthn/passkeys, passwordless, refresh tokens, breach/security controls where documented. | [FusionAuth API Keys API](https://fusionauth.io/docs/apis/api-keys), [FusionAuth Key API](https://fusionauth.io/docs/apis/keys), [FusionAuth Multi-Factor API](https://fusionauth.io/docs/apis/multi-factor), [FusionAuth WebAuthn API](https://fusionauth.io/docs/apis/webauthn) |
| Federation and provisioning APIs | External identity and lifecycle integration. | Identity providers, SAML, SCIM, connectors, entity/entity grant APIs. | [FusionAuth Identity Provider APIs](https://fusionauth.io/docs/apis/identity-providers), [FusionAuth SCIM API](https://fusionauth.io/docs/apis/scim), [FusionAuth Connectors API](https://fusionauth.io/docs/apis/connectors) |
| Observability and messaging APIs | Operational and lifecycle messaging. | Audit logs, event logs, webhooks, email templates, messenger templates, reports, system APIs. | [FusionAuth Audit Log API](https://fusionauth.io/docs/apis/audit-logs), [FusionAuth Event Log API](https://fusionauth.io/docs/apis/event-logs), [FusionAuth Webhooks API](https://fusionauth.io/docs/apis/webhooks) |

### FusionAuth SDK Products

| SDK / library family | Target user | Feature groups | Primary evidence |
|---|---|---|---|
| Server/client SDKs | Backend and automation developers. | API client wrappers for user, application, tenant, key, login, registration, group, webhook, lambda, and other platform APIs. | [FusionAuth Client Libraries](https://fusionauth.io/docs/sdks/), [FusionAuth TypeScript Client](https://github.com/FusionAuth/fusionauth-typescript-client), [FusionAuth Python Client](https://github.com/FusionAuth/fusionauth-python-client) |
| Frontend framework SDKs | SPA developers. | Login/logout helpers, React/Vue/Angular integration, token/session helpers, route protection and hosted-login integration patterns. | [FusionAuth React SDK](https://fusionauth.io/docs/sdks/react-sdk), [FusionAuth Angular SDK](https://fusionauth.io/docs/sdks/angular-sdk), [FusionAuth Vue SDK](https://fusionauth.io/docs/sdks/vue-sdk) |
| Native/mobile examples and guides | Native and mobile developers. | OAuth/OIDC login integration, PKCE/native app guidance, token storage patterns, platform framework examples. | [FusionAuth SDKs](https://fusionauth.io/docs/sdks/), [FusionAuth OAuth Guide](https://fusionauth.io/docs/lifecycle/authenticate-users/oauth/) |

### FusionAuth UIX / Hosted UI Products

| UIX product | Primary actor | Feature groups | Primary evidence |
|---|---|---|---|
| Hosted Login Pages | End users and app developers. | Hosted login, registration, password reset, email verification, MFA, passwordless/WebAuthn prompts, OAuth consent, theme customization. | [FusionAuth Hosted Login Pages](https://fusionauth.io/docs/lifecycle/authenticate-users/hosted-login-page), [FusionAuth OAuth Guide](https://fusionauth.io/docs/lifecycle/authenticate-users/oauth/) |
| Admin UI | Tenant/platform admins and operators. | User/app/tenant/group/role configuration, identity providers, API keys, keys, themes, webhooks, lambdas, logs, reports. | [FusionAuth Admin UI](https://fusionauth.io/docs/get-started/core-concepts/admin-ui), [FusionAuth APIs](https://fusionauth.io/docs/apis/) |
| Theme editor and Theme API | Designers and tenant admins. | Hosted-login template editing, theme inheritance, localized messages, email/template styling, custom page templates. | [FusionAuth Themes](https://fusionauth.io/docs/customize/look-and-feel/themes), [FusionAuth Theme API](https://fusionauth.io/docs/apis/themes) |

### FusionAuth Extensibility / Operations Products

| Product surface | Product role | Feature groups | Primary evidence |
|---|---|---|---|
| Lambdas | Runtime customization. | Login, registration, JWT populate, SAML populate, reconcile, self-service registration validation, custom scripts. | [FusionAuth Lambda API](https://fusionauth.io/docs/apis/lambdas), [FusionAuth Lambdas](https://fusionauth.io/docs/customize/lambdas/) |
| Webhooks | Event integration. | Event configuration, transaction settings, event subscriptions, external delivery for auth/user/app events. | [FusionAuth Webhooks API](https://fusionauth.io/docs/apis/webhooks), [FusionAuth Webhooks](https://fusionauth.io/docs/extend/events-and-webhooks) |
| Tenant Manager | Delegated tenant administration. | Tenant-scoped admin access, tenant manager APIs, tenant isolation, delegated control. | [FusionAuth Tenant Manager API](https://fusionauth.io/docs/apis/tenant-manager), [FusionAuth Tenants API](https://fusionauth.io/docs/apis/tenants) |

## Amazon Cognito

Amazon Cognito is split into User Pools, Identity Pools, managed/hosted UI, OAuth endpoints, AWS SDK/API operations, Amplify SDK/UI, Lambda triggers, and AWS observability/security integrations.

### Amazon Cognito API / Service Products

| Product / API surface | Product role | Feature groups | Primary evidence |
|---|---|---|---|
| Cognito User Pools | CIAM user directory and authorization-server product. | User pools, app clients, hosted/managed login, OAuth 2.0 endpoints, OIDC federation, SAML federation, groups, MFA, passkeys/WebAuthn, password policies, user import, custom attributes, resource servers/scopes, M2M/client credentials. | [Amazon Cognito User Pools](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools.html), [User Pool Features](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-features.html), [OAuth 2.0 Endpoints](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-userpools-server-contract-reference.html) |
| Cognito User Pools API | Programmatic user-pool control and runtime auth API. | SignUp, ConfirmSignUp, InitiateAuth, RespondToAuthChallenge, AdminCreateUser, AdminSetUserPassword, AdminAddUserToGroup, app-client/user-pool/domain/resource-server CRUD, identity-provider CRUD. | [Amazon Cognito Identity Provider API Reference](https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/Welcome.html), [Amazon Cognito User Pool API Operations](https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_Operations_Amazon_Cognito_Identity_Provider.html) |
| Cognito Identity Pools | Federated identity to AWS credentials. | Identity pools, unauthenticated/authenticated identities, provider federation, role mapping, credential vending for AWS services. | [Amazon Cognito Identity Pools](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-identity.html), [Identity Pools API Reference](https://docs.aws.amazon.com/cognitoidentity/latest/APIReference/Welcome.html) |
| Managed Login / Hosted UI endpoints | Hosted OAuth/OIDC login surface. | Authorize, token, userinfo, logout, JWKS, managed login pages, social/enterprise federation, custom domains, branding, OAuth scopes. | [Managed Login](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-managed-login.html), [Cognito User Pools OIDC Endpoints](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-userpools-server-contract-reference.html) |
| M2M and resource servers | Service-to-service/API authorization lane. | Client credentials grant, app-client confidential secret, OAuth scopes, resource servers, API authorization with JWT access tokens. | [Cognito M2M Authorization](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-define-resource-servers.html), [Client Credentials Grant](https://docs.aws.amazon.com/cognito/latest/developerguide/federation-endpoints-oauth-grants.html) |

### Amazon Cognito SDK Products

| SDK / library family | Target user | Feature groups | Primary evidence |
|---|---|---|---|
| AWS SDKs | Backend/app automation developers. | Cognito Identity Provider and Identity Pools API clients across AWS SDK languages, user-pool and identity-pool CRUD/auth operations. | [AWS SDKs and Tools](https://aws.amazon.com/developer/tools/), [Cognito Identity Provider API Reference](https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/Welcome.html) |
| AWS Amplify Auth | Frontend/mobile app developers. | Sign-up/sign-in/sign-out, session/token access, MFA, password reset, social login, user attributes, custom auth flows, Hosted UI integration. | [Amplify Auth for React](https://docs.amplify.aws/react/build-a-backend/auth/), [Amplify JavaScript Auth](https://docs.amplify.aws/gen1/javascript/build-a-backend/auth/) |
| Amplify client libraries by platform | Web/mobile developers. | Auth category integrations for JavaScript, React, React Native, Swift, Android/Kotlin, Flutter depending on generation/platform support. | [Amplify Documentation](https://docs.amplify.aws/), [Amplify UI Authenticator](https://ui.docs.amplify.aws/react/connected-components/authenticator) |
| OIDC/JWT validation libraries | Resource-server developers. | JWT validation via issuer/JWKS/audience/scope checks using AWS examples and generic OIDC/JWT libraries. | [Verify a JWT in Amazon Cognito](https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-using-the-access-token.html), [Cognito JWKS and OIDC Endpoints](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-userpools-server-contract-reference.html) |

### Amazon Cognito UIX / Hosted UI Products

| UIX product | Primary actor | Feature groups | Primary evidence |
|---|---|---|---|
| Managed Login | End users and app developers. | Hosted sign-in/sign-up, password recovery, MFA/passkey prompts, federation chooser, OAuth consent, branding, custom domains. | [Amazon Cognito Managed Login](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-managed-login.html), [Managed Login Branding](https://docs.aws.amazon.com/cognito/latest/developerguide/managed-login-branding.html) |
| Classic Hosted UI | End users and app developers using older UI. | Hosted OAuth UI, sign-in/sign-up, IdP selection, custom CSS/logo, OAuth redirect flow. | [Classic Hosted UI](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-app-integration.html), [Hosted UI Customization](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-app-ui-customization.html) |
| AWS Console for Cognito | AWS operators and admins. | User-pool/identity-pool configuration, app clients, domains, IdPs, groups, triggers, security settings, branding. | [Getting Started with User Pools](https://docs.aws.amazon.com/cognito/latest/developerguide/getting-started-with-cognito-user-pools.html), [Amazon Cognito Console Guide](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-console.html) |
| Amplify UI Authenticator | App developers embedding auth UI. | Prebuilt sign-in/sign-up/reset/MFA components, theming, social login integration, route protection through app composition. | [Amplify UI Authenticator](https://ui.docs.amplify.aws/react/connected-components/authenticator), [Amplify UI Theming](https://ui.docs.amplify.aws/react/theming) |

### Amazon Cognito Extensibility / Operations Products

| Product surface | Product role | Feature groups | Primary evidence |
|---|---|---|---|
| Lambda triggers | Runtime customization. | Pre sign-up, post confirmation, pre authentication, post authentication, pre token generation, custom authentication challenges, custom messages, user migration. | [Amazon Cognito Lambda Triggers](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-working-with-lambda-triggers.html), [Pre Token Generation Trigger](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-pre-token-generation.html) |
| Security integrations | Threat protection and account security. | Advanced security features, threat protection/adaptive auth, MFA, compromised credentials, AWS WAF integration, account recovery. | [Cognito Threat Protection](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-settings-threat-protection.html), [AWS WAF with Cognito](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-waf.html) |
| Observability and audit | AWS account operations. | CloudTrail API audit, CloudWatch metrics/logs through Lambda and AWS services, service quotas and operational monitoring. | [Logging Cognito API Calls with CloudTrail](https://docs.aws.amazon.com/cognito/latest/developerguide/logging-using-cloudtrail.html), [Amazon Cognito Metrics](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-metrics.html) |

## Cross-Competitor Surface Implications

| Segment | Auth0 | Okta | Keycloak | FusionAuth | Amazon Cognito | Implication for `tigrbl_auth` |
|---|---|---|---|---|---|---|
| Public issuer / authentication API | Authentication API | OIDC/OAuth API | Realm OIDC endpoints | OAuth/Login/JWT APIs | User-pool OAuth endpoints | Keep `tigrbl-auth-api-public` as a distinct public issuer. |
| Management control plane | Management API v2 | Management API | Admin REST API | API catalog / Admin APIs | Cognito IdP API / AWS Console | A single "Management API product" can contain multiple deployable slices. |
| Delegated org/tenant admin | My Organization API | Org/admin-role patterns in Management API | Realm/org admin delegation | Tenant Manager | AWS account/IAM plus user-pool scoped admin | `tenant-admin` should be framed as delegated management, not a generic admin clone. |
| End-user self-service | My Account API | MyAccount API / End-User Dashboard | Account Console | Hosted account/user flows and User APIs | Managed Login / Amplify Authenticator | `tigrbl_auth` has a visible gap around first-class account self-service. |
| M2M/workload identity | M2M applications + client credentials | OAuth for service apps | Service accounts + client credentials | Applications/API keys/client credentials | Client credentials/resource servers | M2M needs first-class product framing, not only "service admin." |
| API access security / resource validation | Token/JWKS/Auth0 FGA adjacency | API Access Management | Authorization Services / policy enforcer | JWT/introspection/key APIs | JWT validation/resource servers | `resource-validation` maps to a real competitor lane, but API access management should be specified more clearly. |
| SDK/platform integration | SPA/server/mobile + Management SDKs | Auth JS/framework/mobile/JWT verifier SDKs | JS adapter/admin client/policy enforcer | Client libraries + React/Angular/Vue SDKs | AWS SDKs + Amplify Auth/UI | SDKs are product surfaces, not just examples. |
| UIX | Universal Login/Dashboard | Sign-In Widget/Admin/End-User Dashboard | Admin/Account/Login themes | Hosted Login/Admin UI/Themes | Managed Login/Amplify UI/AWS Console | UIX apps should be explicit first-class product surfaces with API ownership links. |
| Extensibility | Actions/log streams | Hooks/Workflows/System Log | SPIs/events/auth flows | Lambdas/webhooks | Lambda triggers/CloudTrail | Runtime extension/event surfaces are a separate product lane from CRUD admin. |

## Bibliography

### Auth0

- Auth0. [Authentication API Reference](https://auth0.com/docs/api/authentication). Accessed 2026-05-27.
- Auth0. [Management API v2](https://auth0.com/docs/api/management/v2). Accessed 2026-05-27.
- Auth0. [My Account API](https://auth0.com/docs/api/myaccount/). Accessed 2026-05-27.
- Auth0. [My Organization API](https://auth0.com/docs/api/myorganization). Accessed 2026-05-27.
- Auth0. [Universal Login](https://auth0.com/docs/authenticate/login/auth0-universal-login). Accessed 2026-05-27.
- Auth0. [Organizations](https://auth0.com/docs/manage-users/organizations). Accessed 2026-05-27.
- Auth0. [Actions](https://auth0.com/docs/customize/actions). Accessed 2026-05-27.
- Auth0. [Dashboard Overview](https://auth0.com/docs/get-started/auth0-overview/dashboard). Accessed 2026-05-27.
- Auth0. [Client Credentials Flow](https://auth0.com/docs/get-started/authentication-and-authorization-flow/client-credentials-flow). Accessed 2026-05-27.
- Auth0. [Fine-Grained Authorization](https://auth0.com/docs/authorization). Accessed 2026-05-27.
- OpenFGA / Auth0 FGA. [FGA API Explorer](https://docs.fga.dev/api/service). Accessed 2026-05-27.

### Okta

- Okta. [OpenID Connect and OAuth 2.0 Reference](https://developer.okta.com/docs/reference/api/oidc/). Accessed 2026-05-27.
- Okta. [OAuth 2.0 API Overview](https://developer.okta.com/docs/api/openapi/okta-oauth/oauth/overview/). Accessed 2026-05-27.
- Okta. [Management API Overview](https://developer.okta.com/docs/api/openapi/okta-management/guides/overview/). Accessed 2026-05-27.
- Okta. [MyAccount API Overview](https://developer.okta.com/docs/api/openapi/okta-myaccount/myaccount/overview/). Accessed 2026-05-27.
- Okta. [API Access Management](https://developer.okta.com/docs/concepts/api-access-management/). Accessed 2026-05-27.
- Okta. [OAuth for Okta Service Apps](https://developer.okta.com/docs/guides/implement-oauth-for-okta-serviceapp/). Accessed 2026-05-27.
- Okta. [Sign-In Widget Concept](https://developer.okta.com/docs/concepts/sign-in-widget/). Accessed 2026-05-27.
- Okta. [Event Hooks](https://developer.okta.com/docs/concepts/event-hooks/). Accessed 2026-05-27.
- Okta. [Inline Hooks](https://developer.okta.com/docs/concepts/inline-hooks/). Accessed 2026-05-27.
- Okta. [System Log](https://developer.okta.com/docs/concepts/system-log/). Accessed 2026-05-27.
- Okta. [Workflows](https://help.okta.com/wf/en-us/content/topics/workflows/workflows-main.htm). Accessed 2026-05-27.

### Keycloak

- Keycloak. [Securing Applications and Services Guide](https://www.keycloak.org/docs/latest/securing_apps/). Accessed 2026-05-27.
- Keycloak. [OIDC Endpoint Layers](https://www.keycloak.org/securing-apps/oidc-layers). Accessed 2026-05-27.
- Keycloak. [Admin REST API](https://www.keycloak.org/docs-api/26.5.2/rest-api/). Accessed 2026-05-27.
- Keycloak. [Server Administration Guide](https://www.keycloak.org/docs/latest/server_admin/). Accessed 2026-05-27.
- Keycloak. [Client Registration](https://www.keycloak.org/securing-apps/client-registration). Accessed 2026-05-27.
- Keycloak. [Authorization Services Guide](https://www.keycloak.org/docs/latest/authorization_services/). Accessed 2026-05-27.
- Keycloak. [JavaScript Adapter](https://www.keycloak.org/securing-apps/javascript-adapter). Accessed 2026-05-27.
- Keycloak. [Java Admin Client](https://www.keycloak.org/securing-apps/admin-client). Accessed 2026-05-27.
- Keycloak. [Server Development Guide](https://www.keycloak.org/docs/latest/server_development/). Accessed 2026-05-27.

### FusionAuth

- FusionAuth. [API Reference](https://fusionauth.io/docs/apis/). Accessed 2026-05-27.
- FusionAuth. [OAuth Endpoints](https://fusionauth.io/docs/lifecycle/authenticate-users/oauth/endpoints). Accessed 2026-05-27.
- FusionAuth. [Login API](https://fusionauth.io/docs/apis/login). Accessed 2026-05-27.
- FusionAuth. [User API](https://fusionauth.io/docs/apis/users). Accessed 2026-05-27.
- FusionAuth. [Application API](https://fusionauth.io/docs/apis/applications). Accessed 2026-05-27.
- FusionAuth. [Tenants API](https://fusionauth.io/docs/apis/tenants). Accessed 2026-05-27.
- FusionAuth. [API Keys API](https://fusionauth.io/docs/apis/api-keys). Accessed 2026-05-27.
- FusionAuth. [Hosted Login Pages](https://fusionauth.io/docs/lifecycle/authenticate-users/hosted-login-page). Accessed 2026-05-27.
- FusionAuth. [Client Libraries and SDKs](https://fusionauth.io/docs/sdks/). Accessed 2026-05-27.
- FusionAuth. [Lambdas](https://fusionauth.io/docs/customize/lambdas/). Accessed 2026-05-27.
- FusionAuth. [Webhooks](https://fusionauth.io/docs/extend/events-and-webhooks). Accessed 2026-05-27.

### Amazon Cognito

- AWS. [Amazon Cognito User Pools](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools.html). Accessed 2026-05-27.
- AWS. [Amazon Cognito User Pool Features](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-features.html). Accessed 2026-05-27.
- AWS. [Amazon Cognito User Pools API Reference](https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/Welcome.html). Accessed 2026-05-27.
- AWS. [Amazon Cognito Identity Pools](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-identity.html). Accessed 2026-05-27.
- AWS. [Amazon Cognito Identity Pools API Reference](https://docs.aws.amazon.com/cognitoidentity/latest/APIReference/Welcome.html). Accessed 2026-05-27.
- AWS. [Managed Login](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-managed-login.html). Accessed 2026-05-27.
- AWS. [OAuth 2.0 Endpoints and Server Contract](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-userpools-server-contract-reference.html). Accessed 2026-05-27.
- AWS. [Resource Servers and Custom Scopes](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-define-resource-servers.html). Accessed 2026-05-27.
- AWS. [Lambda Triggers](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-working-with-lambda-triggers.html). Accessed 2026-05-27.
- AWS. [Amplify Auth for React](https://docs.amplify.aws/react/build-a-backend/auth/). Accessed 2026-05-27.
- AWS Amplify UI. [Authenticator](https://ui.docs.amplify.aws/react/connected-components/authenticator). Accessed 2026-05-27.
