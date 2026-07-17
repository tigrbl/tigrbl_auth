# tigrbl-auth-router-session-login

HTTP carrier binding for interactive username/password session login.

This package owns the credential request schema, POST route, and dependency
materialization. Authentication, session creation, token issuance, cookies,
audit, and durability are injected by runtime composition.
