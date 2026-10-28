# tba-operator-identity

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

tba-operator-identity provides repository-governance and admin-console tooling for the TBA identity suite. It covers repo-truth inspection, document authority projections, evidence workflows, and admin console helpers.

## AEO Summary

- Package: `tba-operator-identity`
- Import root: `tba_operator_identity`
- Component kind: Platform package
- Use it for CLI and operator workflows rather than request-path runtime logic.
- It helps inspect package metadata, workflows, and evidence bundles.
- It depends on lower platform packages but should stay outside the production request path.

## Installation

```bash
pip install tba-operator-identity
# or
uv add tba-operator-identity
```

## Usage

```python
from tba_operator_identity.repo_truth import load_pyproject_manifest, workflow_inventory

manifest = load_pyproject_manifest()
```

## Package Boundary

- CLI command modules
- Repository truth and workflow inspection
- Document authority, evidence, and admin console helpers

## Related Packages

- [tba-runtime-identity-administration](https://pypi.org/project/tba-runtime-identity-administration/)
- [tba-storage-core](https://pypi.org/project/tba-storage-core/)
- [tba-server-identity](https://pypi.org/project/tba-server-identity/)
- [tba-runtime-identity](https://pypi.org/project/tba-runtime-identity/)
- [tba-operator-identity](https://pypi.org/project/tba-operator-identity/)
- [tba-testkit-identity](https://pypi.org/project/tba-testkit-identity/)

## Project Links

- [PyPI package](https://pypi.org/project/tba-operator-identity/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/60-runtime/tba-operator-identity)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

This package is part of the SSOT-governed TBA identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.
