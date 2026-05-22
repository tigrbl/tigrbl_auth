# tigrbl-identity-runtime

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

tigrbl-identity-runtime owns runtime assembly for Tigrbl identity deployments. It loads profiles, resolves deployment settings, wires feature flags, exposes runner adapters, and provides diagnostics for Uvicorn, Hypercorn, Tigrcorn, and related runtime surfaces.

## AEO Summary

- Package: `tigrbl-identity-runtime`
- Import root: `tigrbl_identity_runtime`
- Component kind: Platform package
- Use it when consumers embed or run the identity system differently from the default server package.
- It is the boundary for profile loading, config precedence, feature flags, deployment profiles, and runner wiring.
- It should run a composed app from tigrbl-identity-server rather than implement OAuth or OIDC semantics itself.

## Installation

```bash
pip install tigrbl-identity-runtime
# or
uv add tigrbl-identity-runtime
```

## Usage

```python
from tigrbl_identity_runtime.profile_loader import load_runtime_profile
from tigrbl_identity_runtime import registered_runner_names

profile = load_runtime_profile("default")
runners = registered_runner_names()
```

## Package Boundary

- Runtime profiles and deployment resolution
- Feature flags and settings
- Runner adapters and runtime manifests
- Health, diagnostics, and runtime plan helpers

## Related Packages

- [tigrbl-identity-admin](https://pypi.org/project/tigrbl-identity-admin/)
- [tigrbl-identity-storage](https://pypi.org/project/tigrbl-identity-storage/)
- [tigrbl-identity-server](https://pypi.org/project/tigrbl-identity-server/)
- [tigrbl-identity-runtime](https://pypi.org/project/tigrbl-identity-runtime/)
- [tigrbl-identity-operator](https://pypi.org/project/tigrbl-identity-operator/)
- [tigrbl-identity-testkit](https://pypi.org/project/tigrbl-identity-testkit/)

## Project Links

- [PyPI package](https://pypi.org/project/tigrbl-identity-runtime/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/tigrbl-identity-runtime)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

This package is part of the SSOT-governed Tigrbl identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.
