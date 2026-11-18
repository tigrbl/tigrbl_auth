# tba-concrete-authorization-scope-set-matcher

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-scope-set-matcher/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-scope-set-matcher/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-authorization-scope-set-matcher%3D%3D0.4.0.dev3/pkgs/10-concrete/tba-concrete-authorization-scope-set-matcher/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-authorization-scope-set-matcher%3D%3D0.4.0.dev3/pkgs/10-concrete/tba-concrete-authorization-scope-set-matcher/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/10-concrete"><img alt="Layer: 10 concrete" src="https://img.shields.io/badge/Layer-10%20concrete-0a7f5a"></a>
<a href="https://pypi.org/project/tba-concrete-authorization-scope-set-matcher/"><img alt="PyPI version for tba-concrete-authorization-scope-set-matcher" src="https://img.shields.io/pypi/v/tba-concrete-authorization-scope-set-matcher?label=tba-concrete-authorization-scope-set-matcher%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-concrete-authorization-scope-set-matcher"><img alt="Monthly PyPI downloads for tba-concrete-authorization-scope-set-matcher" src="https://static.pepy.tech/badge/tba-concrete-authorization-scope-set-matcher/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-scope-set-matcher/README.md"><img alt="README hits for tba-concrete-authorization-scope-set-matcher" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-scope-set-matcher/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-scope-set-matcher/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Owns deterministic concrete value semantics.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_concrete_authorization_scope_set_matcher import ScopeSetMatcher

assert callable(ScopeSetMatcher)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-concrete-authorization-scope-set-matcher==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the ScopeSetMatcher entry point is available.

## Non-goals

Higher-layer orchestration, lower-layer persistence, and protocol behavior outside this package's declared layer are not owned here.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-authorization-scope-set-matcher/src/tba_concrete_authorization_scope_set_matcher/__init__.py).
