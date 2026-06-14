# Package Dependency Layering T2 Plan Evidence

T2 target:

- remove every foundational import of `tigrbl_auth`;
- remove the T1 exception ledger from `tests/unit/test_package_dependency_layering.py`;
- keep `tigrbl-auth` as the only facade package and `tigrbl-auth-api-*` as the backend consumers of that facade;
- keep frontend UIX workspaces free of Python facade module imports.

The T2 claim remains proposed until the strict zero-exception unit guard passes.
