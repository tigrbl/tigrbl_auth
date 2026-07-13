# tigrbl-replay-memory-provider

Atomic process-local replay reservations for tests, development, and explicit
single-process deployments. State is lost on restart and is not shared across
workers, so this provider is not suitable for horizontally scaled production.
