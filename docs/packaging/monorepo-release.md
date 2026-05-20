# Monorepo Package Release

The split package release lane is package-scoped. A release tag must match:

```text
<package-name>==<package-version>
```

Examples:

```text
tigrbl-auth==0.3.5
tigrbl-identity-core==0.3.5
tigrbl-identity-oauth==0.3.5
```

The authoritative package version is the package-local `pyproject.toml` under
`pkgs/<package>/pyproject.toml`. The release workflow rejects tags whose
version does not match that file.

## Workflow

`.github/workflows/monorepo-package-release.yml` provides the split package
release lane.

On `workflow_dispatch`, it creates package tags:

```text
package=all
package=tigrbl-identity-core
```

On a pushed package tag, it:

1. discovers `pkgs/*` with `cobycloud/actions/actions/monorepo-discover`;
2. validates package metadata with `cobycloud/actions/actions/package-metadata`;
3. validates the tag with `scripts/monorepo_release.py resolve-tag`;
4. builds the package with `cobycloud/actions/actions/python-package-build`;
5. attests the wheel and sdist;
6. publishes the package with `cobycloud/actions/actions/pypi-publish`;
7. creates a GitHub Release with `cobycloud/actions/actions/github-release`.

## PyPI Trusted Publishing

Each PyPI project should configure GitHub Trusted Publishing with:

```text
owner: tigrbl
repository: tigrbl_auth
workflow: monorepo-package-release.yml
environment: pypi
```

The legacy root release workflow remains separate from this package-scoped
monorepo release lane.

## Package Python Matrix

`.github/workflows/package-python-matrix.yml` provides the split package
test lane.

It expands every package under `pkgs/*` across the supported interpreter range:

```text
3.10
3.11
3.12
3.13
3.14
```

Each matrix cell:

1. discovers `pkgs/*` with `cobycloud/actions/actions/monorepo-discover`;
2. validates package metadata with `cobycloud/actions/actions/package-metadata`;
3. builds the target package with `cobycloud/actions/actions/python-package-build`
   on that cell's Python version;
4. creates a clean virtual environment;
5. exposes sibling workspace package members from source through a `.pth` file;
6. installs the target package from the built wheel with `--no-deps`;
7. runs `pip check`;
8. imports the package's declared import root and verifies installed package
   metadata.

Package-specific pytest suites can be added under either:

```text
tests/packages/<package-name>/
tests/packages/<import-root>/
```

When either path exists for a package, the isolated cell installs `pytest` in
the clean environment and runs those tests with:

```text
PACKAGE_UNDER_TEST
IMPORT_ROOT_UNDER_TEST
PACKAGE_VERSION_UNDER_TEST
```

The `tigrbl-identity-testkit` package is the cross-cutting package-test owner.
Its package matrix cells additionally include:

```text
tests/integration
tests/interop
```

Those cells pass `--certification-lane all` through the cobycloud isolated
package test action so the repo lane filter collects integration and interop
tests instead of the default core-only lane.

Before running those cross-cutting tests, the isolated cell installs the local
workspace facade with test/runtime extras into the isolated venv:

```text
$VENV_PYTHON -m pip install -e ".[test,sqlite,postgres,servers]"
```

Manual dispatch supports narrowing the matrix:

```text
package=tigrbl-identity-oauth
python-version=3.12
```
