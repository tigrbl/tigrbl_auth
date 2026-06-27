# tigrbl-identity-admin-advanced-authenticator-registry

Deprecated compatibility package for `AdvancedAuthenticatorRegistry`.

Canonical advanced-authentication state is owned by storage tables in
`tigrbl-identity-storage`, including credential subtype tables and the
`AuthenticationChallenge` table. New code should import the admin capability
surface from `tigrbl_identity_admin` instead of this package.
