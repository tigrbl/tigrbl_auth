# Platform RP and BFF contract

## Normative requirements

The RP validates discovery issuer identity, authorization callback state and
issuer, PKCE, ID-token signature, issuer, audience, authorized party, nonce,
expiration, issued-at, not-before, authentication time, and maximum age. UserInfo
is accepted only when its subject matches the verified ID token. Unknown signing
keys trigger a bounded JWKS refresh; algorithms and keys remain policy constrained.

Login transactions are durable, expiring, and atomically consumed once. Upstream
refresh tokens are encrypted at rest. Refresh rotation uses compare-and-swap or a
lease so concurrent refresh cannot fork token state. Tokens, secrets, and cookie
values never enter logs or audit evidence.

The RP/BFF exposes login, callback, current session, refresh, step-up, logout, and
health routes. It uses secure HttpOnly cookies, mutation CSRF protection, trusted
proxy policy, and redirect allowlists. Customer and internal deployments have
separate client ids, audiences, cookies, redirect allowlists, assurance policy,
and application-session bindings.

The RP produces a verified external identity and calls an injected application
identity-binding/session-exchange port. It does not create application-specific
roles, permissions, tenants, or resource scopes.
