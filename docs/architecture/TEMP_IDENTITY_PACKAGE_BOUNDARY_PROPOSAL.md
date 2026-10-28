# Temporary Identity Package Boundary Proposal

This note captures the current working proposal for splitting `tba_auth`
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
| `tba-primitives-identity` | Shared IDs, errors, value objects, tenant and issuer primitives, base interfaces. |
| `tba-contracts-identity` | OpenAPI, OpenRPC, JSON Schema, discovery schemas, compliance target metadata, generated contract artifacts. |
| `tba-concrete-identity-principals` | Actor taxonomy: users, clients, apps, services, devices, workloads, machines, federated subjects. |
| `tba-credentials` | Credential taxonomy and lifecycle: passwords, API keys, service keys, client secrets, JWT assertions, certificate bindings, DPoP keys, passkeys/WebAuthn credentials, recovery codes, sessions. |
| `tba-provider-identity-jose` | JWT, JWK, JWS, JWE, JWA, JWKS, signing, encryption, key material, key selection primitives. |
| `tba-runtime-authorization-policy` | Tenant isolation, RBAC/ABAC decisions, scope authorization, admin authorization, audit/provenance policy, credential-use policy. |
| `tba-protocol-oauth` | OAuth protocol semantics: authorization, token, revocation, introspection, client registration, device authorization, token exchange, PAR, JAR, RAR, DPoP, mTLS, resource indicators. |
| `tba-protocol-oidc` | OIDC provider semantics: discovery, ID token, UserInfo, sessions, logout, `acr`/`amr` claim emission. |
| `tba-runtime-identity-administration` | Control-plane APIs for tenants, users, apps, clients, services, credentials, policies, key rotation, and governed mutations. |
| `tba-storage-core` | Tigrbl/SQLAlchemy table mappings, migrations, repositories, SQLite/Postgres support, database bootstrap, migration portability. SQLAlchemy is the default implementation substrate, not part of the package boundary name. |
| `tba-server-identity` | Default runnable Authorization Server / OIDC Provider / IdP distribution. |
| `tba-runtime-identity` | Process/runtime layer: runner profiles, ASGI runtime adapters, lifecycle hooks, runtime manifests, health and diagnostics wiring. |
| `tba-operator-identity` | CLI/operator workflows over admin, runtime, contracts, and evidence surfaces. |
| `tba-protocol-oauth-protected-resource` | Protected API toolkit: token validation, JWKS cache, introspection, scope/permission enforcement, DPoP/mTLS/resource checks. |
| `tba-protocol-oidc-relying-party` | Relying-party/client SDK: discovery, authorization URL, PKCE, callback handling, token exchange, ID-token validation, UserInfo, logout. |
| `tba-testkit-identity` | Conformance fixtures, fake providers, fake clients, fake resource servers, protocol vectors, downstream harnesses. |
| `tba-auth` | Backward-compatible facade/default install. |

## First-Class Objects By Package

The following inventory names the first-class objects each proposed distribution
owns. These are package-boundary objects, not necessarily one class per object
on day one.

| Package | First-class objects |
| --- | --- |
| `tba-primitives-identity` | `TenantId`, `PrincipalId`, `CredentialId`, `ClientId`, `Issuer`, `Subject`, `Audience`, `Scope`, `Permission`, `GrantType`, `ResponseType`, `TokenType`, `Nonce`, `Clock`, `TimeWindow`, `ErrorCode`, `Result`, `CapabilityName`, `FeatureFlagName`, `RuntimeProfileName`. |
| `tba-contracts-identity` | `AuthorizeRequest`, `AuthorizeResponse`, `TokenRequest`, `TokenResponse`, `IntrospectionRequest`, `IntrospectionResponse`, `RevocationRequest`, `DeviceAuthorizationRequest`, `DeviceAuthorizationResponse`, `OpenIDConfiguration`, `OAuthAuthorizationServerMetadata`, `ProtectedResourceMetadata`, `JwksDocument`, `AdminRequest`, `AdminResponse`, `ErrorResponse`, `CapabilityManifest`, `OpenApiContractInput`, `OpenRpcContractInput`. |
| `tba-concrete-identity-principals` | `Principal`, `UserPrincipal`, `ClientPrincipal`, `AppPrincipal`, `ServicePrincipal`, `DevicePrincipal`, `MachinePrincipal`, `WorkloadPrincipal`, `FederatedSubjectPrincipal`, `Group`, `Role`, `Membership`, `PrincipalAlias`, `Tenant`, `TenantMembership`, `Ownership`, `Delegation`, `AdminAuthority`, `OwnerAuthority`, `SuperuserAuthority`. |
| `tba-credentials` | `Credential`, `CredentialBinding`, `CredentialVerificationResult`, `CredentialStatus`, `PasswordCredential`, `ApiKeyCredential`, `ServiceKeyCredential`, `ClientSecretCredential`, `JwtAssertionCredential`, `MtlsCertificateCredential`, `DpopKeyCredential`, `WebAuthnCredential`, `PasskeyCredential`, `RecoveryCodeCredential`, `SessionCookieCredential`, `RefreshTokenCredential`, `DeviceCodeCredential`, `CredentialRotation`, `CredentialRevocation`, `CredentialPosture`. |
| `tba-provider-identity-jose` | `Jwk`, `Jwks`, `Jws`, `Jwe`, `Jwt`, `JoseHeader`, `KeyId`, `SigningKey`, `VerificationKey`, `EncryptionKey`, `KeySet`, `KeyRotationPlan`, `KeySelectionPolicy`, `TokenSigner`, `TokenVerifier`, `JwksPublisher`, `JoseAlgorithmPolicy`. |
| `tba-runtime-authorization-policy` | `Policy`, `PolicyDecision`, `PolicyRequest`, `PolicyContext`, `RbacPolicy`, `AbacPolicy`, `ScopePolicy`, `TenantIsolationPolicy`, `DelegatedAdminPolicy`, `ClientExposurePolicy`, `CredentialUsePolicy`, `AuthorizationTrace`, `PolicyVersion`, `PolicyRegistry`, `AuditPolicy`. |
| `tba-protocol-oauth` | `AuthorizationGrant`, `AuthorizationCode`, `AccessToken`, `RefreshToken`, `ClientRegistration`, `ClientAuthentication`, `TokenExchange`, `DeviceAuthorization`, `DeviceCode`, `UserCode`, `PushedAuthorizationRequest`, `JwtSecuredAuthorizationRequest`, `RichAuthorizationRequest`, `ResourceIndicator`, `DpopProof`, `MtlsClientBinding`, `TokenRevocation`, `TokenIntrospection`, `OAuthError`. |
| `tba-protocol-oidc` | `IdToken`, `UserInfo`, `OidcClaims`, `Acr`, `Amr`, `AuthenticationContext`, `OidcProviderMetadata`, `OidcSession`, `SessionState`, `LogoutRequest`, `RpInitiatedLogout`, `FrontChannelLogout`, `BackChannelLogout`, `FederatedLoginResult`. |
| `tba-runtime-identity-administration` | `AdminOperation`, `TenantAdminService`, `UserAdminService`, `ClientAdminService`, `AppAdminService`, `ServiceAdminService`, `CredentialAdminService`, `KeyAdminService`, `SessionAdminService`, `TokenAdminService`, `PolicyAdminService`, `DelegatedAdminService`, `SafeMutation`, `AdminAuditEvent`. |
| `tba-storage-core` | `UserTable`, `ClientTable`, `AppTable`, `ServiceTable`, `DeviceTable`, `MachineTable`, `WorkloadTable`, `CredentialTable`, `ApiKeyTable`, `ServiceKeyTable`, `SessionTable`, `TenantTable`, `AuthorizationCodeTable`, `DeviceCodeTable`, `ConsentTable`, `AuditEventTable`, `Repository`, `UnitOfWork`, `Migration`, `DatabaseBootstrap`, `SqliteProfile`, `PostgresProfile`. |
| `tba-server-identity` | `IdentityApp`, `AppFactory`, `GatewayFactory`, `PluginInstaller`, `RouteManifest`, `SurfaceManifest`, `PublicRestSurface`, `AdminRpcSurface`, `DiagnosticsSurface`, `ProtocolPublisher`, `OpenApiPublisher`, `OpenRpcPublisher`, `DiscoveryPublisher`, `ServerSettings`. |
| `tba-runtime-identity` | `RuntimeProfile`, `RuntimeConfig`, `RuntimeManifest`, `RunnerProfile`, `UvicornRuntime`, `HypercornRuntime`, `TigrcornRuntime`, `LifecycleHook`, `HealthCheck`, `DiagnosticsEndpoint`, `RuntimeAdapter`, `ServeCommandPlan`, `RuntimeState`. |
| `tba-operator-identity` | `OperatorCommand`, `BootstrapCommand`, `MigrateCommand`, `ImportCommand`, `ExportCommand`, `KeyRotationCommand`, `ClientCommand`, `ServiceCommand`, `TenantCommand`, `ProfileInspectCommand`, `ClaimsLintCommand`, `ReleaseGateCommand`, `EvidenceBundleCommand`, `CertificationReportCommand`, `OperatorReport`. |
| `tba-protocol-oauth-protected-resource` | `ResourceServer`, `ResourceMetadata`, `Audience`, `ScopeRequirement`, `PermissionRequirement`, `TokenValidator`, `JwksCache`, `IntrospectionClient`, `SenderConstraintValidator`, `DpopCnfBindingValidator`, `MtlsCnfBindingValidator`, `ResourceAuthorizationResult`. |
| `tba-protocol-oidc-relying-party` | `RelyingParty`, `LoginRequest`, `AuthorizationUrlBuilder`, `CallbackHandler`, `PkceVerifier`, `TokenExchangeClient`, `IdTokenValidator`, `UserInfoClient`, `LogoutClient`, `RpSession`, `RpConfiguration`. |
| `tba-testkit-identity` | `FakeClock`, `FakeKeyStore`, `FakeRepository`, `FakePrincipalFactory`, `FakeCredentialFactory`, `FakeIdp`, `FakeOAuthClient`, `FakeResourceServer`, `ProtocolTestVector`, `ConformanceHarness`, `PeerProfileHarness`, `TestTenantFactory`, `TestAppFactory`, `TokenFixture`, `JoseFixture`. |
| `tba-auth` | `app`, `create_app`, `create_gateway`, `install_plugin`, `IdentityServer`, `DefaultRuntime`, selected public re-exports, install extras, compatibility entrypoints. |

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

Distribution names use hyphens. Import names should use independent top-level
packages with underscores:

```text
dist:   tba-protocol-oauth
import: tba_protocol_oauth
```

Do not use a shared `tba_identity.*` namespace package. Each distribution
owns its own import root, such as `tba_primitives_identity`,
`tba_protocol_oauth`, and `tba_storage_core`. Also avoid
`tigrbl.identity.*` unless the existing `tigrbl` package is deliberately
converted into a namespace package.

`A -> B` means package `A` may import package `B`.

```text
tba-contracts-identity
  -> tba-primitives-identity

tba-concrete-identity-principals
  -> tba-primitives-identity

tba-credentials
  -> tba-primitives-identity
  -> tba-contracts-identity
  -> tba-concrete-identity-principals

tba-provider-identity-jose
  -> tba-primitives-identity
  -> tba-contracts-identity

tba-runtime-authorization-policy
  -> tba-primitives-identity
  -> tba-contracts-identity
  -> tba-concrete-identity-principals
  -> tba-credentials

tba-protocol-oauth
  -> tba-primitives-identity
  -> tba-contracts-identity
  -> tba-concrete-identity-principals
  -> tba-credentials
  -> tba-provider-identity-jose
  -> tba-runtime-authorization-policy

tba-protocol-oidc
  -> tba-primitives-identity
  -> tba-contracts-identity
  -> tba-concrete-identity-principals
  -> tba-credentials
  -> tba-provider-identity-jose
  -> tba-protocol-oauth
  -> tba-runtime-authorization-policy

tba-runtime-identity-administration
  -> tba-primitives-identity
  -> tba-contracts-identity
  -> tba-concrete-identity-principals
  -> tba-credentials
  -> tba-provider-identity-jose
  -> tba-runtime-authorization-policy
  -> tba-protocol-oauth
  -> tba-protocol-oidc

tba-storage-core
  -> tba-primitives-identity
  -> tba-contracts-identity
  -> tba-concrete-identity-principals
  -> tba-credentials
  -> tba-runtime-authorization-policy
  -> tba-protocol-oauth
  -> tba-protocol-oidc

tba-server-identity
  -> tba-primitives-identity
  -> tba-contracts-identity
  -> tba-concrete-identity-principals
  -> tba-credentials
  -> tba-provider-identity-jose
  -> tba-runtime-authorization-policy
  -> tba-protocol-oauth
  -> tba-protocol-oidc
  -> tba-runtime-identity-administration
  -> tba-storage-core

tba-runtime-identity
  -> tba-primitives-identity
  -> tba-contracts-identity
  -> tba-server-identity

tba-operator-identity
  -> tba-primitives-identity
  -> tba-contracts-identity
  -> tba-runtime-identity-administration
  -> tba-storage-core
  -> tba-server-identity
  -> tba-runtime-identity

tba-protocol-oauth-protected-resource
  -> tba-primitives-identity
  -> tba-contracts-identity
  -> tba-concrete-identity-principals
  -> tba-credentials
  -> tba-provider-identity-jose
  -> tba-runtime-authorization-policy
  -> tba-protocol-oauth
  -> tba-protocol-oidc

tba-protocol-oidc-relying-party
  -> tba-primitives-identity
  -> tba-contracts-identity
  -> tba-credentials
  -> tba-provider-identity-jose
  -> tba-protocol-oauth
  -> tba-protocol-oidc

tba-testkit-identity
  -> tba-primitives-identity
  -> tba-contracts-identity
  -> tba-concrete-identity-principals
  -> tba-credentials
  -> tba-provider-identity-jose
  -> tba-runtime-authorization-policy
  -> tba-protocol-oauth
  -> tba-protocol-oidc
  -> tba-runtime-identity-administration
  -> tba-storage-core
  -> tba-server-identity
  -> tba-protocol-oauth-protected-resource
  -> tba-protocol-oidc-relying-party

tba-auth
  -> tba-primitives-identity
  -> tba-contracts-identity
  -> tba-server-identity
  -> tba-runtime-identity
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
storage -> oauth/oidc/policy/credentials/principals/contracts/core
server -> admin/storage/oauth/oidc/jose/policy/credentials/principals/contracts/core
runtime -> server/contracts/core
operator -> runtime/server/storage/admin/contracts/core
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

`storage` is the default persistence adapter. It may map protocol
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
| `tba-identity-federation` | Later extension for social/SSO providers, OIDC Federation, external provider trust, account linking, and cross-cloud trust. |
| `tba-identity-provisioning` | Later only if SCIM provisioning comes back into scope. |
| `tba-identity-saml` | Do not create now; SAML IdP/SP is explicitly out of scope. |
| `tba-identity-webauthn` | Do not create now; keep passkeys/WebAuthn under credentials until it is large enough to split. |
| `tba-identity-browser` | Do not create now for Python distributions; browser helpers belong under RP or a future non-Python SDK. |

## Tenant, App, Client, And User Flows

The desired product flow is:

1. A platform owner or superuser bootstraps the deployment.
2. The deployment creates one or more tenants.
3. Each tenant can have tenant admins.
4. Tenant admins can create users, invite users, or allow user self-registration depending on policy.
5. Tenant admins can create apps.
6. Each app can own one or more OAuth/OIDC clients.
7. App clients define redirect URIs, grant types, scopes, consent policy, secret/public-client posture, and allowed login behavior.
8. End users can log into those tenant apps using the `tba-server-identity` as the OAuth/OIDC provider.
9. The app uses `tba-protocol-oidc-relying-party` to initiate login and handle callback/token validation.
10. The app's APIs use `tba-protocol-oauth-protected-resource` to validate access tokens and enforce authorization.

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
| `Tenant` | `tba-primitives-identity` or `tba-concrete-identity-principals` | `tba-runtime-identity-administration` creates and manages it. |
| `User` / `Account` | `tba-concrete-identity-principals` | `tba-runtime-identity-administration` and self-registration flows manage lifecycle. |
| `TenantMembership` | `tba-concrete-identity-principals` and `tba-runtime-authorization-policy` | `tba-runtime-identity-administration` manages membership and tenant-scoped authority. |
| `Role` / `Entitlement` | `tba-runtime-authorization-policy` | `tba-runtime-identity-administration` governs assignment. |
| `App` | `tba-concrete-identity-principals` | `tba-runtime-identity-administration` creates and manages app registration. |
| `OAuthClient` | `tba-concrete-identity-principals` and `tba-protocol-oauth` | `tba-runtime-identity-administration` manages persisted client records; dynamic client registration belongs to OAuth protocol behavior. |
| `RelyingParty` | Runtime role of an app/client, not usually persisted separately | `tba-protocol-oidc-relying-party` provides the SDK used by consuming apps. |
| `ResourceServer` | `tba-concrete-identity-principals` and `tba-protocol-oauth-protected-resource` | `tba-runtime-identity-administration` registers resource/audience metadata. |
| `Service` | `tba-concrete-identity-principals` | `tba-runtime-identity-administration` manages lifecycle. |
| `Machine` | `tba-concrete-identity-principals` | `tba-runtime-identity-administration` or workload trust integration manages lifecycle. |
| `Workload` | `tba-concrete-identity-principals` | `tba-runtime-identity-administration` or future workload registry manages lifecycle. |
| `Device` | `tba-concrete-identity-principals` | User enrollment and/or admin enrollment manages lifecycle. |
| `Credential` | `tba-credentials` | `tba-runtime-identity-administration` manages issue, bind, rotate, revoke, expire. |
| `Policy` | `tba-runtime-authorization-policy` | `tba-runtime-identity-administration` governs policy lifecycle. |
| Runtime profile/config | `tba-runtime-identity` | Operator/runtime config owns deployment selection and overrides. |
| OAuth/OIDC protocol behavior | `tba-protocol-oauth`, `tba-protocol-oidc`, `tba-provider-identity-jose` | Used by server, RP, and resource-server packages. |

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
