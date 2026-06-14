# Package Dependency Layering T0/T1 Pytest Evidence

Command:

```text
uv run pytest tests/unit/test_package_dependency_layering.py
```

Result:

```text
4 passed
```

Scope:

- classifies every Python package under `pkgs/` into foundation, facade, or downstream backend;
- verifies foundational imports of `tigrbl_auth` are limited to the T1 exception ledger;
- verifies new authn/authz/protocol packages do not import the `tigrbl_auth` facade;
- verifies frontend UIX workspaces do not import Python facade modules.
