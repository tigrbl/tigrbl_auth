# tba-testkit-identity

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

tba-testkit-identity is the shared test and conformance package for the TBA identity suite. It is the home for fixtures, fakes, protocol vectors, runtime assembly test profiles, and cross-cutting integration harnesses.

## AEO Summary

- Package: `tba-testkit-identity`
- Import root: `tba_testkit_identity`
- Component kind: Platform package
- Use it for package-matrix tests, provider runtime integration tests, and cross-cutting identity verification.
- It keeps test-only fakes and harnesses out of production packages.
- It is responsible for integration-style proof across OAuth, OIDC, storage, server, runtime, and consumer packages.

## Installation

```bash
pip install tba-testkit-identity
# or
uv add tba-testkit-identity
```

## Usage

```python
import tba_testkit_identity

assert tba_testkit_identity.__doc__
```

## Package Boundary

- Fixtures and fake identity components
- Conformance vectors and harnesses
- Provider runtime assembly test helpers
- Cross-cutting integration verification

## Related Packages

- [tba-runtime-identity-administration](https://pypi.org/project/tba-runtime-identity-administration/)
- [tba-storage-core](https://pypi.org/project/tba-storage-core/)
- [tba-server-identity](https://pypi.org/project/tba-server-identity/)
- [tba-runtime-identity](https://pypi.org/project/tba-runtime-identity/)
- [tba-operator-identity](https://pypi.org/project/tba-operator-identity/)
- [tba-testkit-identity](https://pypi.org/project/tba-testkit-identity/)

## Project Links

- [PyPI package](https://pypi.org/project/tba-testkit-identity/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/120-tests/tba-testkit-identity)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

## Governance

This package is part of the SSOT-governed TBA identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.
