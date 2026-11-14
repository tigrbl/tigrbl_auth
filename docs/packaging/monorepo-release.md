# Monorepo Package Release

The split package release lane is package-scoped. A release tag must match:

```text
<package-name>==<package-version>
```

Examples:

```text
tba-auth==0.3.5
tba-primitives-identity==0.3.5
tba-protocol-oauth==0.3.5
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
package=tba-primitives-identity
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
repository: tba_auth
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
3. builds the target package with `uv build` on that cell's Python version;
4. creates a clean virtual environment;
5. builds wheels for the target package's local dependencies;
6. installs those wheels and the target wheel;
7. runs `pip check`;
8. imports the package's declared import root and verifies installed package
   metadata.

Backend application suites live under
`pkgs/120-tests/tba-tests-backend-apps/tests/packages/<distribution-name>/`.

When a backend suite exists for a package, the isolated cell installs the pinned
pytest, HTTP client, and SQLite test dependencies in
the clean environment and runs those tests with:

```text
PACKAGE_UNDER_TEST
IMPORT_ROOT_UNDER_TEST
PACKAGE_VERSION_UNDER_TEST
```

The `tba-testkit-identity` package is the cross-cutting package-test owner.
Its package matrix cells additionally include:

```text
pkgs/120-tests/tba-testkit-identity/tests
pkgs/120-tests/tba-tests-certification/tests/interop
```

Those cells pass `--certification-lane all` through the isolated runner so pytest collects the testkit's interop checks.

Before running those cross-cutting tests, the isolated cell installs the local
workspace facade with test/runtime extras into the isolated venv:

```text
$VENV_PYTHON -m pip install -e ".[test,sqlite,postgres,servers]"
```

Manual dispatch supports narrowing the matrix:

```text
package=tba-protocol-oauth
python-version=3.12
```
