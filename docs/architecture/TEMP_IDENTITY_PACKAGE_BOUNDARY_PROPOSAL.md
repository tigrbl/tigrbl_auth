# Temporary Identity Package Boundary Proposal

This note captures the current working proposal for splitting `tigrbl_auth`
into smaller Python distributions. It is intentionally temporary and should be
promoted into SSOT ADR/SPEC rows before it becomes binding.

## Core Roles

The suite should distinguish these roles:

| Role | Meaning |
| --- | --- |
| Authorization Server | Issues OAuth access/refresh tokens, handles grants, client authentication, revocation, introspection, device authorization, token exchange, and related OAuth protocol behavior. |
| OIDC Provider / IdP | Authenticates users, issues ID tokens, publishes discovery/JWKS/UserInfo/logout/session behavior. |
| Admin Control Plane | Creates and manages tenants, users, apps, clients, services, credentials, policies, keys, and runtime settings. |
| Operator Surface | CLI/workflow layer over the admin and runtime surfaces. |
| Server Composition | Builds the Tigrbl ASGI app, loads profiles, resolves config precedence, applies feature flags, mounts surfaces, registers routes, and assembles middleware. |
| Runtime Execution | Runs the composed app through supported runner profiles and owns lifecycle, health, diagnostics, and runtime manifests. |
| Resource Server Toolkit | Helps downstream APIs validate tokens and enforce scopes, permissions, resource indicators, proof binding, and tenant trust domains. |
| Relying Party / Client SDK | Helps applications initiate OIDC/OAuth login, handle callbacks, exchange codes, validate ID tokens, refresh tokens, call UserInfo, and log out. |

The current repo aligns most strongly with Authorization Server, OIDC Provider,
Admin Control Plane, Operator Surface, Server Composition, Runtime Execution, contracts, and
testkit. Resource Server Toolkit and Relying Party SDK are important consumer
roles but require more work.

## Proposed First-Wave Packages

| Package | Boundary |
| --- | --- |
| `tigrbl-identity-core` | Shared IDs, errors, value objects, tenant and issuer primitives, base interfaces. |
| `tigrbl-identity-contracts` | OpenAPI, OpenRPC, JSON Schema, discovery schemas, compliance target metadata, generated contract artifacts. |
| `tigrbl-identity-principals` | Actor taxonomy: users, clients, apps, services, devices, workloads, machines, federated subjects. |
| `tigrbl-identity-credentials` | Credential taxonomy and lifecycle: passwords, API keys, service keys, client secrets, JWT assertions, certificate bindings, DPoP keys, passkeys/WebAuthn credentials, recovery codes, sessions. |
| `tigrbl-identity-jose` | JWT, JWK, JWS, JWE, JWA, JWKS, signing, encryption, key material, key selection primitives. |
| `tigrbl-identity-policy` | Tenant isolation, RBAC/ABAC decisions, scope authorization, admin authorization, audit/provenance policy, credential-use policy. |
| `tigrbl-identity-oauth` | OAuth protocol semantics: authorization, token, revocation, introspection, client registration, device authorization, token exchange, PAR, JAR, RAR, DPoP, mTLS, resource indicators. |
| `tigrbl-identity-oidc` | OIDC provider semantics: discovery, ID token, UserInfo, sessions, logout, `acr`/`amr` claim emission. |
| `tigrbl-identity-admin` | Control-plane APIs for tenants, users, apps, clients, services, credentials, policies, key rotation, and governed mutations. |
| `tigrbl-identity-storage-sqlalchemy` | SQLAlchemy/Tigrbl table mappings, migrations, repositories, SQLite/Postgres support, database bootstrap, migration portability. |
| `tigrbl-identity-server` | Default runnable Authorization Server / OIDC Provider / IdP distribution. |
| `tigrbl-identity-runtime` | Process/runtime layer: runner profiles, ASGI runtime adapters, lifecycle hooks, runtime manifests, health and diagnostics wiring. |
| `tigrbl-identity-operator` | CLI/operator workflows over admin, runtime, contracts, and evidence surfaces. |
| `tigrbl-identity-resource-server` | Protected API toolkit: token validation, JWKS cache, introspection, scope/permission enforcement, DPoP/mTLS/resource checks. |
| `tigrbl-identity-rp` | Relying-party/client SDK: discovery, authorization URL, PKCE, callback handling, token exchange, ID-token validation, UserInfo, logout. |
| `tigrbl-identity-testkit` | Conformance fixtures, fake providers, fake clients, fake resource servers, protocol vectors, downstream harnesses. |
| `tigrbl-auth` | Backward-compatible facade/default install. |

## First-Class Objects By Package

The following inventory names the first-class objects each proposed distribution
owns. These are package-boundary objects, not necessarily one class per object
on day one.

| Package | First-class objects |
| --- | --- |
| `tigrbl-identity-core` | `TenantId`, `PrincipalId`, `CredentialId`, `ClientId`, `Issuer`, `Subject`, `Audience`, `Scope`, `Permission`, `GrantType`, `ResponseType`, `TokenType`, `Nonce`, `Clock`, `TimeWindow`, `ErrorCode`, `Result`, `CapabilityName`, `FeatureFlagName`, `RuntimeProfileName`. |
| `tigrbl-identity-contracts` | `AuthorizeRequest`, `AuthorizeResponse`, `TokenRequest`, `TokenResponse`, `IntrospectionRequest`, `IntrospectionResponse`, `RevocationRequest`, `DeviceAuthorizationRequest`, `DeviceAuthorizationResponse`, `OpenIDConfiguration`, `OAuthAuthorizationServerMetadata`, `ProtectedResourceMetadata`, `JwksDocument`, `AdminRequest`, `AdminResponse`, `ErrorResponse`, `CapabilityManifest`, `OpenApiContractInput`, `OpenRpcContractInput`. |
| `tigrbl-identity-principals` | `Principal`, `UserPrincipal`, `ClientPrincipal`, `AppPrincipal`, `ServicePrincipal`, `DevicePrincipal`, `MachinePrincipal`, `WorkloadPrincipal`, `FederatedSubjectPrincipal`, `Group`, `Role`, `Membership`, `PrincipalAlias`, `Tenant`, `TenantMembership`, `Ownership`, `Delegation`, `AdminAuthority`, `OwnerAuthority`, `SuperuserAuthority`. |
| `tigrbl-identity-credentials` | `Credential`, `CredentialBinding`, `CredentialVerificationResult`, `CredentialStatus`, `PasswordCredential`, `ApiKeyCredential`, `ServiceKeyCredential`, `ClientSecretCredential`, `JwtAssertionCredential`, `MtlsCertificateCredential`, `DpopKeyCredential`, `WebAuthnCredential`, `PasskeyCredential`, `RecoveryCodeCredential`, `SessionCookieCredential`, `RefreshTokenCredential`, `DeviceCodeCredential`, `CredentialRotation`, `CredentialRevocation`, `CredentialPosture`. |
| `tigrbl-identity-jose` | `Jwk`, `Jwks`, `Jws`, `Jwe`, `Jwt`, `JoseHeader`, `KeyId`, `SigningKey`, `VerificationKey`, `EncryptionKey`, `KeySet`, `KeyRotationPlan`, `KeySelectionPolicy`, `TokenSigner`, `TokenVerifier`, `JwksPublisher`, `JoseAlgorithmPolicy`. |
| `tigrbl-identity-policy` | `Policy`, `PolicyDecision`, `PolicyRequest`, `PolicyContext`, `RbacPolicy`, `AbacPolicy`, `ScopePolicy`, `TenantIsolationPolicy`, `DelegatedAdminPolicy`, `ClientExposurePolicy`, `CredentialUsePolicy`, `AuthorizationTrace`, `PolicyVersion`, `PolicyRegistry`, `AuditPolicy`. |
| `tigrbl-identity-oauth` | `AuthorizationGrant`, `AuthorizationCode`, `AccessToken`, `RefreshToken`, `ClientRegistration`, `ClientAuthentication`, `TokenExchange`, `DeviceAuthorization`, `DeviceCode`, `UserCode`, `PushedAuthorizationRequest`, `JwtSecuredAuthorizationRequest`, `RichAuthorizationRequest`, `ResourceIndicator`, `DpopProof`, `MtlsClientBinding`, `TokenRevocation`, `TokenIntrospection`, `OAuthError`. |
| `tigrbl-identity-oidc` | `IdToken`, `UserInfo`, `OidcClaims`, `Acr`, `Amr`, `AuthenticationContext`, `OidcProviderMetadata`, `OidcSession`, `SessionState`, `LogoutRequest`, `RpInitiatedLogout`, `FrontChannelLogout`, `BackChannelLogout`, `FederatedLoginResult`. |
| `tigrbl-identity-admin` | `AdminOperation`, `TenantAdminService`, `UserAdminService`, `ClientAdminService`, `AppAdminService`, `ServiceAdminService`, `CredentialAdminService`, `KeyAdminService`, `SessionAdminService`, `TokenAdminService`, `PolicyAdminService`, `DelegatedAdminService`, `SafeMutation`, `AdminAuditEvent`. |
| `tigrbl-identity-storage-sqlalchemy` | `UserTable`, `ClientTable`, `AppTable`, `ServiceTable`, `DeviceTable`, `MachineTable`, `WorkloadTable`, `CredentialTable`, `ApiKeyTable`, `ServiceKeyTable`, `SessionTable`, `TenantTable`, `AuthorizationCodeTable`, `DeviceCodeTable`, `ConsentTable`, `AuditEventTable`, `Repository`, `UnitOfWork`, `Migration`, `DatabaseBootstrap`, `SqliteProfile`, `PostgresProfile`. |
| `tigrbl-identity-server` | `IdentityApp`, `AppFactory`, `GatewayFactory`, `PluginInstaller`, `RouteManifest`, `SurfaceManifest`, `PublicRestSurface`, `AdminRpcSurface`, `DiagnosticsSurface`, `ProtocolPublisher`, `OpenApiPublisher`, `OpenRpcPublisher`, `DiscoveryPublisher`, `ServerSettings`. |
| `tigrbl-identity-runtime` | `RuntimeProfile`, `RuntimeConfig`, `RuntimeManifest`, `RunnerProfile`, `UvicornRuntime`, `HypercornRuntime`, `TigrcornRuntime`, `LifecycleHook`, `HealthCheck`, `DiagnosticsEndpoint`, `RuntimeAdapter`, `ServeCommandPlan`, `RuntimeState`. |
| `tigrbl-identity-operator` | `OperatorCommand`, `BootstrapCommand`, `MigrateCommand`, `ImportCommand`, `ExportCommand`, `KeyRotationCommand`, `ClientCommand`, `ServiceCommand`, `TenantCommand`, `ProfileInspectCommand`, `ClaimsLintCommand`, `ReleaseGateCommand`, `EvidenceBundleCommand`, `CertificationReportCommand`, `OperatorReport`. |
| `tigrbl-identity-resource-server` | `ResourceServer`, `ResourceMetadata`, `Audience`, `ScopeRequirement`, `PermissionRequirement`, `TokenValidator`, `JwksCache`, `IntrospectionClient`, `ProofBindingValidator`, `DpopValidator`, `MtlsBindingValidator`, `ResourceAuthorizationResult`. |
| `tigrbl-identity-rp` | `RelyingParty`, `LoginRequest`, `AuthorizationUrlBuilder`, `CallbackHandler`, `PkceVerifier`, `TokenExchangeClient`, `IdTokenValidator`, `UserInfoClient`, `LogoutClient`, `RpSession`, `RpConfiguration`. |
| `tigrbl-identity-testkit` | `FakeClock`, `FakeKeyStore`, `FakeRepository`, `FakePrincipalFactory`, `FakeCredentialFactory`, `FakeIdp`, `FakeOAuthClient`, `FakeResourceServer`, `ProtocolTestVector`, `ConformanceHarness`, `PeerProfileHarness`, `TestTenantFactory`, `TestAppFactory`, `TokenFixture`, `JoseFixture`. |
| `tigrbl-auth` | `app`, `create_app`, `create_gateway`, `install_plugin`, `IdentityServer`, `DefaultRuntime`, selected public re-exports, install extras, compatibility entrypoints. |

The package-boundary rule is:

```text
principals = actors
credentials = proof material
policy = authorization decisions
oauth/oidc = protocol behavior
jose = token/key cryptography
storage = persistence implementation
server = Tigrbl app composition
runtime = process/runner execution
operator = CLI/evidence/control workflows
```

## Proposed Dependency DAG

Distribution names use hyphens. Import names should use a namespace layout:

```text
dist:   tigrbl-identity-oauth
import: tigrbl_identity.oauth
```

Avoid `tigrbl.identity.*` unless the existing `tigrbl` package is deliberately
converted into a namespace package. The current package depends on `tigrbl`, so
claiming the `tigrbl` import namespace would create unnecessary collision risk.

`A -> B` means package `A` may import package `B`.

```text
tigrbl-identity-contracts
  -> tigrbl-identity-core

tigrbl-identity-principals
  -> tigrbl-identity-core

tigrbl-identity-credentials
  -> tigrbl-identity-core
  -> tigrbl-identity-contracts
  -> tigrbl-identity-principals

tigrbl-identity-jose
  -> tigrbl-identity-core
  -> tigrbl-identity-contracts

tigrbl-identity-policy
  -> tigrbl-identity-core
  -> tigrbl-identity-contracts
  -> tigrbl-identity-principals
  -> tigrbl-identity-credentials

tigrbl-identity-oauth
  -> tigrbl-identity-core
  -> tigrbl-identity-contracts
  -> tigrbl-identity-principals
  -> tigrbl-identity-credentials
  -> tigrbl-identity-jose
  -> tigrbl-identity-policy

tigrbl-identity-oidc
  -> tigrbl-identity-core
  -> tigrbl-identity-contracts
  -> tigrbl-identity-principals
  -> tigrbl-identity-credentials
  -> tigrbl-identity-jose
  -> tigrbl-identity-oauth
  -> tigrbl-identity-policy

tigrbl-identity-admin
  -> tigrbl-identity-core
  -> tigrbl-identity-contracts
  -> tigrbl-identity-principals
  -> tigrbl-identity-credentials
  -> tigrbl-identity-jose
  -> tigrbl-identity-policy
  -> tigrbl-identity-oauth
  -> tigrbl-identity-oidc

tigrbl-identity-storage-sqlalchemy
  -> tigrbl-identity-core
  -> tigrbl-identity-contracts
  -> tigrbl-identity-principals
  -> tigrbl-identity-credentials
  -> tigrbl-identity-policy
  -> tigrbl-identity-oauth
  -> tigrbl-identity-oidc

tigrbl-identity-server
  -> tigrbl-identity-core
  -> tigrbl-identity-contracts
  -> tigrbl-identity-principals
  -> tigrbl-identity-credentials
  -> tigrbl-identity-jose
  -> tigrbl-identity-policy
  -> tigrbl-identity-oauth
  -> tigrbl-identity-oidc
  -> tigrbl-identity-admin
  -> tigrbl-identity-storage-sqlalchemy

tigrbl-identity-runtime
  -> tigrbl-identity-core
  -> tigrbl-identity-contracts
  -> tigrbl-identity-server

tigrbl-identity-operator
  -> tigrbl-identity-core
  -> tigrbl-identity-contracts
  -> tigrbl-identity-admin
  -> tigrbl-identity-storage-sqlalchemy
  -> tigrbl-identity-server
  -> tigrbl-identity-runtime

tigrbl-identity-resource-server
  -> tigrbl-identity-core
  -> tigrbl-identity-contracts
  -> tigrbl-identity-principals
  -> tigrbl-identity-credentials
  -> tigrbl-identity-jose
  -> tigrbl-identity-policy
  -> tigrbl-identity-oauth
  -> tigrbl-identity-oidc

tigrbl-identity-rp
  -> tigrbl-identity-core
  -> tigrbl-identity-contracts
  -> tigrbl-identity-credentials
  -> tigrbl-identity-jose
  -> tigrbl-identity-oauth
  -> tigrbl-identity-oidc

tigrbl-identity-testkit
  -> tigrbl-identity-core
  -> tigrbl-identity-contracts
  -> tigrbl-identity-principals
  -> tigrbl-identity-credentials
  -> tigrbl-identity-jose
  -> tigrbl-identity-policy
  -> tigrbl-identity-oauth
  -> tigrbl-identity-oidc
  -> tigrbl-identity-admin
  -> tigrbl-identity-storage-sqlalchemy
  -> tigrbl-identity-server
  -> tigrbl-identity-resource-server
  -> tigrbl-identity-rp

tigrbl-auth
  -> tigrbl-identity-core
  -> tigrbl-identity-contracts
  -> tigrbl-identity-server
  -> tigrbl-identity-runtime
```

### One-Way Edges

The most important one-way edges are:

```text
contracts -> core
principals -> core
credentials -> principals/core/contracts
jose -> core/contracts
policy -> principals/credentials/contracts/core
oauth -> jose/policy/credentials/principals/contracts/core
oidc -> oauth/jose/policy/credentials/principals/contracts/core
admin -> oauth/oidc/jose/policy/credentials/principals/contracts/core
storage-sqlalchemy -> oauth/oidc/policy/credentials/principals/contracts/core
server -> admin/storage-sqlalchemy/oauth/oidc/jose/policy/credentials/principals/contracts/core
runtime -> server/contracts/core
operator -> runtime/server/storage-sqlalchemy/admin/contracts/core
facade -> server/runtime/contracts/core
```

### Forbidden Edges

These edges are intentionally forbidden:

```text
core              must not import anything above it
contracts         must not import principals/credentials/jose/policy/oauth/oidc/admin/storage/server/runtime/operator/testkit
principals        must not import credentials/jose/policy/oauth/oidc/admin/storage/server/runtime/operator/testkit
credentials       must not import jose/oauth/oidc/admin/storage/server/runtime/operator/testkit
jose              must not import principals/credentials/policy/oauth/oidc/admin/storage/server/runtime/operator/testkit
policy            must not perform credential verification or import oauth/oidc/admin/storage/server/runtime/operator/testkit
oauth             must not import oidc/admin/storage/server/runtime/operator/testkit
oidc              must not import admin/storage/server/runtime/operator/testkit
admin             must not import storage/server/runtime/operator/testkit
storage           must not import server/runtime/operator/testkit
server            must not import runtime/operator/testkit
runtime           must not import operator/testkit
operator          must not import testkit in production code
production code   must not import testkit
```

### DAG Rationale

`core` and `contracts` are foundational and must stay pure. They cannot open a
database session, construct an app, sign a token, or run a server.

`principals` owns actors. `credentials` owns proof material. `policy` consumes
principal and credential facts to make authorization decisions, but it must not
own credential verification implementations.

`jose` owns token and key cryptography. `oauth` consumes JOSE and policy to run
OAuth protocol state machines. `oidc` consumes OAuth and JOSE to add OIDC
identity, discovery, userinfo, session, and logout behavior.

`storage-sqlalchemy` is the default persistence adapter. It may map protocol
and identity objects into tables and repositories, but protocol packages must
not import storage. That keeps OAuth/OIDC portable across SQLite, Postgres,
test fakes, and future storage adapters.

`server` builds the Tigrbl ASGI application and mounts public/admin/diagnostic
surfaces. `runtime` runs the composed app through supported runner profiles.
`operator` controls, inspects, migrates, and verifies the runtime from outside
the request path.

`testkit` is non-production support. Production packages must not depend on it.

## Deferred Or Optional Packages

| Package | Status |
| --- | --- |
| `tigrbl-identity-federation` | Later extension for social/SSO providers, OIDC Federation, external provider trust, account linking, and cross-cloud trust. |
| `tigrbl-identity-provisioning` | Later only if SCIM provisioning comes back into scope. |
| `tigrbl-identity-saml` | Do not create now; SAML IdP/SP is explicitly out of scope. |
| `tigrbl-identity-webauthn` | Do not create now; keep passkeys/WebAuthn under credentials until it is large enough to split. |
| `tigrbl-identity-browser` | Do not create now for Python distributions; browser helpers belong under RP or a future non-Python SDK. |

## Tenant, App, Client, And User Flows

The desired product flow is:

1. A platform owner or superuser bootstraps the deployment.
2. The deployment creates one or more tenants.
3. Each tenant can have tenant admins.
4. Tenant admins can create users, invite users, or allow user self-registration depending on policy.
5. Tenant admins can create apps.
6. Each app can own one or more OAuth/OIDC clients.
7. App clients define redirect URIs, grant types, scopes, consent policy, secret/public-client posture, and allowed login behavior.
8. End users can log into those tenant apps using the `tigrbl-identity-server` as the OAuth/OIDC provider.
9. The app uses `tigrbl-identity-rp` to initiate login and handle callback/token validation.
10. The app's APIs use `tigrbl-identity-resource-server` to validate access tokens and enforce authorization.

This is the Google/GitHub-style platform pattern:

```text
Tenant admin creates app/client in tigrbl identity
User visits tenant app
Tenant app redirects user to tigrbl identity
tigrbl identity authenticates user and issues tokens for that app/client
Tenant app consumes the login result
Tenant app APIs validate access tokens as resource servers
```

The current repo has many of the provider-side pieces: tenants, users, clients,
OAuth/OIDC routes, dynamic client registration, admin/control-plane concepts,
service identities, service keys, API keys, runtime profiles, contracts, and
test coverage. The missing or less normalized pieces are a first-class app
object, tenant-admin self-service flow, consumer-facing RP SDK, and downstream
resource-server toolkit.

## Proposed Object Cardinality

The proposed platform object model uses the following cardinality:

```text
Deployment
  1 -> many Tenants

Tenant
  1 -> many Users / Memberships
  1 -> many Apps
  1 -> many Services
  1 -> many Resource Servers / APIs
  1 -> many Policies
  1 -> many Credentials

App
  belongs to 1 Tenant
  1 -> many OAuth/OIDC Clients
  0 -> many Services
  0 -> many Resource Servers / APIs

OAuth/OIDC Client
  belongs to 1 App, or directly to 1 Tenant for compatibility
  1 -> many redirect URIs
  0 -> many client credentials
  acts as a relying party when doing OIDC login

Resource Server / API
  belongs to 1 Tenant, optionally 1 App
  1 -> many audiences / resources / scopes / permissions
  validates access tokens issued by the server

Service
  belongs to 1 Tenant, optionally 1 App
  0 -> many service credentials
  may use 0 -> many OAuth clients for protocol flows

User
  current repo: belongs to 1 Tenant
  better target: global account 1 -> many TenantMemberships

TenantMembership
  joins User to Tenant
  carries tenant roles: admin, owner, developer, member

Credential
  belongs to 1 Principal
  principal can be user, client, service, device, workload, or machine

Authority / Role / Entitlement
  assigned to 1 Principal
  scoped to deployment, tenant, app, service, client, or resource
```

The current repo's `User` model is tenant-bound. For a Google/GitHub-style
platform, the cleaner target model is a global account plus tenant memberships:

```text
Account / User
  -> TenantMembership
      -> Tenant
      -> roles / entitlements inside that tenant
```

That allows one human to belong to multiple tenants without duplicating the
human identity record.

## Object Ownership By Package

| Object | Package that owns model semantics | Persisted/admin ownership |
| --- | --- | --- |
| `Tenant` | `tigrbl-identity-core` or `tigrbl-identity-principals` | `tigrbl-identity-admin` creates and manages it. |
| `User` / `Account` | `tigrbl-identity-principals` | `tigrbl-identity-admin` and self-registration flows manage lifecycle. |
| `TenantMembership` | `tigrbl-identity-principals` and `tigrbl-identity-policy` | `tigrbl-identity-admin` manages membership and tenant-scoped authority. |
| `Role` / `Entitlement` | `tigrbl-identity-policy` | `tigrbl-identity-admin` governs assignment. |
| `App` | `tigrbl-identity-principals` | `tigrbl-identity-admin` creates and manages app registration. |
| `OAuthClient` | `tigrbl-identity-principals` and `tigrbl-identity-oauth` | `tigrbl-identity-admin` manages persisted client records; dynamic client registration belongs to OAuth protocol behavior. |
| `RelyingParty` | Runtime role of an app/client, not usually persisted separately | `tigrbl-identity-rp` provides the SDK used by consuming apps. |
| `ResourceServer` | `tigrbl-identity-principals` and `tigrbl-identity-resource-server` | `tigrbl-identity-admin` registers resource/audience metadata. |
| `Service` | `tigrbl-identity-principals` | `tigrbl-identity-admin` manages lifecycle. |
| `Machine` | `tigrbl-identity-principals` | `tigrbl-identity-admin` or workload trust integration manages lifecycle. |
| `Workload` | `tigrbl-identity-principals` | `tigrbl-identity-admin` or future workload registry manages lifecycle. |
| `Device` | `tigrbl-identity-principals` | User enrollment and/or admin enrollment manages lifecycle. |
| `Credential` | `tigrbl-identity-credentials` | `tigrbl-identity-admin` manages issue, bind, rotate, revoke, expire. |
| `Policy` | `tigrbl-identity-policy` | `tigrbl-identity-admin` governs policy lifecycle. |
| Runtime profile/config | `tigrbl-identity-runtime` | Operator/runtime config owns deployment selection and overrides. |
| OAuth/OIDC protocol behavior | `tigrbl-identity-oauth`, `tigrbl-identity-oidc`, `tigrbl-identity-jose` | Used by server, RP, and resource-server packages. |

## Service And Machine Identity Flows

Service and machine identities should not be treated as users.

| Identity | Package ownership |
| --- | --- |
| Service principal | `principals` owns the actor type; `admin` creates/manages it. |
| Service key | `credentials` owns credential lifecycle; `admin` rotates/revokes it. |
| OAuth client used by a service | `oauth` owns protocol semantics; `principals` links it to the service/app actor. |
| Machine principal | `principals` owns the actor type when introduced. |
| Workload principal | `principals` owns workload identity shape; `policy` handles tenant/trust-domain authorization. |
| JWT assertion | `credentials` owns credential class; `oauth` owns RFC 7523 use. |
| mTLS certificate binding | `credentials` owns binding metadata; `oauth` owns RFC 8705 semantics. |
| DPoP key binding | `credentials` owns key binding; `oauth` owns RFC 9449 semantics. |

The intended non-human flow is:

1. Tenant admin creates a service or workload identity.
2. Admin issues or binds one or more credentials, such as service key, JWT assertion key, mTLS certificate, or DPoP key.
3. Service/workload authenticates to token endpoint or admin-approved API.
4. Authorization enforces tenant, audience, resource, scope, delegation, and proof-binding constraints.
5. Resource server validates the token and proof binding before accepting the request.

## Current Support Versus Work Needed

| Capability | Current alignment | Work needed |
| --- | --- | --- |
| Tenants | Present | Clarify tenant-admin lifecycle and self-service boundaries. |
| Users | Present | Normalize user principal model and self-registration policy. |
| Admin/superuser | Present as user authority flags | Model tenant admin, owner, and superuser as authorities/entitlements, not separate principal classes unless break-glass rules require it. |
| OAuth/OIDC clients | Present | Add app-to-client ownership model and tenant self-service app/client management. |
| Apps | Not clearly first-class | Add app registration object if tenants should create apps that own multiple clients/services. |
| Tenant-created login apps | Partially possible through clients | Needs first-class app model, admin UX/API, tenant policy, consent, RP examples, and resource-server examples. |
| Service identities | Present/partial | Normalize service principal and service credential lifecycle across principals/credentials/admin/oauth. |
| Machine identities | Not clearly first-class | Add machine principal if needed, likely adjacent to workload identity. |
| Workload identities | Partial advanced-plane model | Promote into normalized principal/credential/policy contracts. |
| Resource servers | Partial adjacent metadata/verifier work | Add reusable verifier toolkit package. |
| OIDC RP/client SDK | Weak/partial | Add login client package for app developers. |
