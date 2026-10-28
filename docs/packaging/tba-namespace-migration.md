# TBA package namespace

Active downstream identity packages use the `tba-` distribution prefix, `tba_`
Python import prefix, and `@tba/` npm scope. The short facades `tba` and `tbauth`
retain their names. Both example distributions now also have the `tba-` prefix.

Active package directories have the `tba-` prefix. TypeScript clients in layer 75
use `tba-typescript-` directory names to distinguish them from Python clients.

Implementation packages follow `tba-<role>-<subject>[-<qualifier>...]`, with a
single-token role: `tba-protocol-webauthn`, `tba-storage-token`,
`tba-provider-secret-hashing-bcrypt`, and `tba-profile-fido2-server`.
The role vocabulary and approved package mapping are checked in
`tests/unit/test_tba_namespace.py` and
[`role-first-renaming.json`](role-first-renaming.json). Standard names such as
OAuth and WebAuthn remain intact. Generic suite-level `auth` is omitted from
router, backend app, plugin, and release-certification names. The domain term
`authorization` is spelled out instead of abbreviated as `authz`.

The separately packaged compatibility facade and CLI retain `tba-auth`; merging
that facade into the existing `tba` planning package is not part of this rename.
All four facades (`tba`, `tbauth`, `tba-auth`, and `tba-credentials`) are explicit
public entry-point exceptions to the implementation naming grammar.

Layer `55-profiles` is a separate profile index above layer `50-protocols`.
Profiles may select, constrain, and compose protocol implementations. Protocols
must not depend on the profile index. Nine existing profile packages moved to
this layer; claim subjects containing the word `profile` remain concrete claims.

| Previous package | Current package |
| --- | --- |
| `@tigrbl-auth/rp` | `@tba/client-oidc-relying-party` |
| `@tigrbl-auth/session-client` | `@tba/client-relying-party-session` |
| `tigrbl-rp-session-client` | `tba-client-relying-party-session` |
| `tigrbl-policy-enforcement-asgi` | `tba-middleware-policy-enforcement-asgi` |
| `tigrbl-auth` | `tba-auth` |

The OIDC relying-party client implements browser authorization and callback
flows. The relying-party session clients call server-owned login and session
APIs. The ASGI package provides policy enforcement middleware rather than a
general-purpose API client.

The middleware lives in `pkgs/85-middleware`, above clients and routers and
below backend application composition. Its dependency policy permits primitives,
contracts, clients, and middleware; concrete router and backend app dependencies
are forbidden. Layer 90 may compose all three surfaces.

Update application imports to `tba_*`, the CLI command to `tba-auth`, auth
environment variables to `TBA_AUTH_*`, and the local key directory setting to
`TBA_JOSE_LOCAL_KEY_DIR`. Suite plugin classes use `TbaPlugin` and
`TbaBackendAppPlugin`.
There are no old-name compatibility aliases for the renamed active packages.

Upstream Tigrbl framework dependencies, framework classes such as `TigrblApp`,
the GitHub repository identity, and the checkout directory retain their names.

`pkgs/deprecated` remains unchanged, including its package names, imports,
metadata, and directory names. These legacy snapshots are excluded from the
active development harness and package release discovery. Their old imports
are not compatibility aliases for the newly named suite.

After updating a checkout, run `uv sync --locked --all-extras --dev` and
`npm ci` to refresh editable paths and npm workspace links. Configure new PyPI
publishers for the new distribution names; existing registrations do not move
with the source rename. Package-name and npm-scope availability must be checked
before publishing.

Changes to names in checked-in compliance artifacts are reference updates,
not new certification or signature evidence.
