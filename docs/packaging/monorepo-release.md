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
