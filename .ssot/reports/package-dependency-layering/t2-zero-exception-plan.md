# Package Dependency Layering T2 Pytest Evidence

Commands:

```text
uv run pytest tests/unit/test_package_dependency_layering.py
uv run pytest tests/unit/test_package_dependency_layering.py tests/unit/test_auth_package_taxonomy_boundary.py tests/unit/test_identity_package_split_imports.py tests/unit/test_principals_model_boundary.py tests/unit/test_tigrbl_auth_facade_ownership.py tests/unit/test_monorepo_release.py
uv run pytest tests/unit/test_credentials_lifecycle_boundary.py tests/unit/test_jose_policy_boundary.py tests/unit/test_oauth_oidc_protocol_boundary.py tests/unit/test_provider_white_label_login_boundary.py tests/unit/test_resource_server_consumer_boundary.py tests/unit/test_rp_consumer_boundary.py
uv run pytest tests/packages/tigrbl-auth-backend-app-public tests/packages/tigrbl-auth-backend-app-resource-validation tests/packages/tigrbl-auth-backend-app-platform-admin tests/packages/tigrbl-auth-backend-app-tenant-admin tests/packages/tigrbl-auth-backend-app-developer tests/packages/tigrbl-auth-backend-app-my-account
```

Observed result:

```text
4 passed
28 passed
34 passed
44 passed, 6 skipped
```

T2 result:

- remove every foundational import of `tigrbl_auth`;
- remove the T1 exception ledger from `tests/unit/test_package_dependency_layering.py`;
- keep `tigrbl-auth` as the only facade package and `tigrbl-auth-router-*` as the backend consumers of that facade;
- keep frontend UIX workspaces free of Python facade module imports.
