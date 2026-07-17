# Router/backend-app migration completion plan

Status: planned.

The layer-80 router boundary is enforced, but the migration is not complete while
`tigrbl-identity-server` retains explicit layer-60 to layer-80 dependency
exceptions in `pkgs/layers.toml`.

Completion requires moving deployable router composition into layer-90 backend
apps, retaining carrier-neutral runtime handlers below layer 80, removing all 16
transitional exceptions, and passing the package dependency and router/backend-app
boundary suites with an empty exception set for this migration.
