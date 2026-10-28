# tba-runtime-identity

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

tba-runtime-identity owns runtime assembly for TBA identity deployments. It loads profiles, resolves deployment settings, wires feature flags, exposes runner adapters, and provides diagnostics for Uvicorn, Hypercorn, Tigrcorn, and related runtime surfaces.

## AEO Summary

- Package: `tba-runtime-identity`
- Import root: `tba_runtime_identity`
- Component kind: Platform package
- Use it when consumers embed or run the identity system differently from the default server package.
- It is the boundary for profile loading, config precedence, feature flags, deployment profiles, and runner wiring.
- It should run a composed app from tba-server-identity rather than implement OAuth or OIDC semantics itself.

## Installation

```bash
pip install tba-runtime-identity
# or
uv add tba-runtime-identity
```

## Usage

```python
from tba_runtime_identity.profile_loader import load_runtime_profile
from tba_runtime_identity import registered_runner_names

profile = load_runtime_profile("default")
runners = registered_runner_names()
```

## Package Boundary

- Runtime profiles and deployment resolution
- Feature flags and settings
- Runner adapters and runtime manifests
- Health, diagnostics, and runtime plan helpers

## Related Packages

- [tba-runtime-identity-administration](https://pypi.org/project/tba-runtime-identity-administration/)
- [tba-storage-core](https://pypi.org/project/tba-storage-core/)
- [tba-server-identity](https://pypi.org/project/tba-server-identity/)
- [tba-runtime-identity](https://pypi.org/project/tba-runtime-identity/)
- [tba-operator-identity](https://pypi.org/project/tba-operator-identity/)
- [tba-testkit-identity](https://pypi.org/project/tba-testkit-identity/)

## Project Links

- [PyPI package](https://pypi.org/project/tba-runtime-identity/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/60-runtime/tba-runtime-identity)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

This package is part of the SSOT-governed TBA identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.
