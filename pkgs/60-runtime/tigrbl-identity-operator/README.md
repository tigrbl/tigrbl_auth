# tigrbl-identity-operator

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

tigrbl-identity-operator provides repository-governance and admin-console tooling for the Tigrbl identity suite. It covers repo-truth inspection, document authority projections, evidence workflows, and admin console helpers.

## AEO Summary

- Package: `tigrbl-identity-operator`
- Import root: `tigrbl_identity_operator`
- Component kind: Platform package
- Use it for CLI and operator workflows rather than request-path runtime logic.
- It helps inspect package metadata, workflows, and evidence bundles.
- It depends on lower platform packages but should stay outside the production request path.

## Installation

```bash
pip install tigrbl-identity-operator
# or
uv add tigrbl-identity-operator
```

## Usage

```python
from tigrbl_identity_operator.repo_truth import load_pyproject_manifest, workflow_inventory

manifest = load_pyproject_manifest()
```

## Package Boundary

- CLI command modules
- Repository truth and workflow inspection
- Document authority, evidence, and admin console helpers

## Related Packages

- [tigrbl-identity-admin](https://pypi.org/project/tigrbl-identity-admin/)
- [tigrbl-identity-storage](https://pypi.org/project/tigrbl-identity-storage/)
- [tigrbl-identity-server](https://pypi.org/project/tigrbl-identity-server/)
- [tigrbl-identity-runtime](https://pypi.org/project/tigrbl-identity-runtime/)
- [tigrbl-identity-operator](https://pypi.org/project/tigrbl-identity-operator/)
- [tigrbl-identity-testkit](https://pypi.org/project/tigrbl-identity-testkit/)

## Project Links

- [PyPI package](https://pypi.org/project/tigrbl-identity-operator/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/60-runtime/tigrbl-identity-operator)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

This package is part of the SSOT-governed Tigrbl identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.
