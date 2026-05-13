## Request-Scoped Runtime Authority Phase 1

This checkpoint captures the first runtime implementation slice for `feat:request-scoped-resolved-deployment-authority`.

Implemented paths:

- `tigrbl_auth/ops/authorize.py`
- `tigrbl_auth/ops/device_authorization.py`
- `tigrbl_auth/ops/logout.py`
- `tigrbl_auth/ops/par.py`
- `tigrbl_auth/ops/register.py`
- `tigrbl_auth/standards/oidc/rp_initiated_logout.py`
- `tigrbl_auth/standards/oidc/session_mgmt.py`

Coverage added:

- `tests/unit/test_request_scoped_runtime_authority.py`

Validated commands:

```text
uv run pytest tests/unit/test_request_scoped_runtime_authority.py
uv run pytest tests/unit/test_request_scoped_runtime_authority.py tests/unit/test_session_logout_cluster_b.py tests/negative/test_cookie_and_logout_abuse_cases.py tests/conformance/production/test_oidc_session_management.py tests/conformance/production/test_oidc_rp_initiated_logout.py
uv run pytest tests/integration/test_auth_flows.py -k "register_client_success or logout_post_clears_session_cookie"
```

Observed result:

- request-scoped deployment issuer now drives session-state hashing, logout hint validation, logout fanout issuer fields, registration management URI generation, device verification URI generation, and PAR request-object audience validation in the covered paths.
- feature remains partial because other current-horizon trust-domain and verifier-contract work is still open.
