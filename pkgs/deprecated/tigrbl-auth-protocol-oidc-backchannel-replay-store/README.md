# tigrbl-auth-protocol-oidc-backchannel-replay-store

Deprecated compatibility package for the former OIDC back-channel logout replay
store.

Canonical replay tracking is now table-owned by `tigrbl-identity-storage` through
the `BackchannelLogoutReplay` table. New OIDC composition should depend on that
table surface rather than this compatibility package.
