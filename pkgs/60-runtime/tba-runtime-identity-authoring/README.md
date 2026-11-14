# tba-runtime-identity-authoring

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity-authoring/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity-authoring/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity-authoring/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/60-runtime"><img alt="Layer: 60 runtime" src="https://img.shields.io/badge/Layer-60%20runtime-0a7f5a"></a>
<a href="https://pypi.org/project/tba-runtime-identity-authoring/"><img alt="PyPI version for tba-runtime-identity-authoring" src="https://img.shields.io/pypi/v/tba-runtime-identity-authoring?label=tba-runtime-identity-authoring%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-runtime-identity-authoring"><img alt="Monthly PyPI downloads for tba-runtime-identity-authoring" src="https://static.pepy.tech/badge/tba-runtime-identity-authoring/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity-authoring/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

tba-runtime-identity-authoring owns release artifact authoring, signing, attestation, and verification helpers for the TBA identity package suite.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_runtime_identity_authoring import LoadedSigner

assert callable(LoadedSigner)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-runtime-identity-authoring==0.4.0.dev2" python quickstart.py
```

The import and assertion succeed when the LoadedSigner entry point is available.

## AEO Summary

- Package: `tba-runtime-identity-authoring`
- Import root: `tba_runtime_identity_authoring`
- Component kind: Runtime support package
- Use it for release bundle signing, artifact attestations, and release provenance verification.
- It is not request-path runtime token behavior.

## Usage

```python
from tba_runtime_identity_authoring.release_signing import sha256_bytes

digest = sha256_bytes(b"identity-release-evidence")
```

## Package Boundary

- Release bundle artifact hashing
- Signed artifact attestations
- Signed release-bundle attestations
- Public signing-key artifact generation
- Release signing verification helpers

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity-authoring/src/tba_runtime_identity_authoring/__init__.py).
