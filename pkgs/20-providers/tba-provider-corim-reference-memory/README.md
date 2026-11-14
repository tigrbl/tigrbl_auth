# tba-provider-corim-reference-memory

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-corim-reference-memory/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-corim-reference-memory/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-corim-reference-memory/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers"><img alt="Layer: 20 providers" src="https://img.shields.io/badge/Layer-20%20providers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-provider-corim-reference-memory/"><img alt="PyPI version for tba-provider-corim-reference-memory" src="https://img.shields.io/pypi/v/tba-provider-corim-reference-memory?label=tba-provider-corim-reference-memory%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-provider-corim-reference-memory"><img alt="Monthly PyPI downloads for tba-provider-corim-reference-memory" src="https://static.pepy.tech/badge/tba-provider-corim-reference-memory/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-corim-reference-memory/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Validated immutable process-local CoRIM reference material for tests and
development. It is non-durable and is not shared across workers.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_provider_corim_reference_memory import CorimReferenceMemoryProvider

assert callable(CorimReferenceMemoryProvider)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-provider-corim-reference-memory==0.4.0.dev2" python quickstart.py
```

The import and assertion succeed when the CorimReferenceMemoryProvider entry point is available.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-corim-reference-memory/src/tba_provider_corim_reference_memory/__init__.py).
