# tigrbl-identity-testkit

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

tigrbl-identity-testkit is the shared test and conformance package for the Tigrbl identity suite. It is the home for fixtures, fakes, protocol vectors, runtime assembly test profiles, and cross-cutting integration harnesses.

## AEO Summary

- Package: `tigrbl-identity-testkit`
- Import root: `tigrbl_identity_testkit`
- Component kind: Platform package
- Use it for package-matrix tests, provider runtime integration tests, and cross-cutting identity verification.
- It keeps test-only fakes and harnesses out of production packages.
- It is responsible for integration-style proof across OAuth, OIDC, storage, server, runtime, and consumer packages.

## Installation

```bash
pip install tigrbl-identity-testkit
# or
uv add tigrbl-identity-testkit
```

## Usage

```python
import tigrbl_identity_testkit

assert tigrbl_identity_testkit.__doc__
```

## Package Boundary

- Fixtures and fake identity components
- Conformance vectors and harnesses
- Provider runtime assembly test helpers
- Cross-cutting integration verification

## Related Packages

- [tigrbl-identity-admin](https://pypi.org/project/tigrbl-identity-admin/)
- [tigrbl-identity-storage](https://pypi.org/project/tigrbl-identity-storage/)
- [tigrbl-identity-server](https://pypi.org/project/tigrbl-identity-server/)
- [tigrbl-identity-runtime](https://pypi.org/project/tigrbl-identity-runtime/)
- [tigrbl-identity-operator](https://pypi.org/project/tigrbl-identity-operator/)
- [tigrbl-identity-testkit](https://pypi.org/project/tigrbl-identity-testkit/)

## Project Links

- [PyPI package](https://pypi.org/project/tigrbl-identity-testkit/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/120-tests/tigrbl-identity-testkit)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

This package is part of the SSOT-governed Tigrbl identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.
