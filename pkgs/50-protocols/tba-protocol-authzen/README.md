# tba-protocol-authzen

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-authzen/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-authzen/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-authzen/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/50-protocols"><img alt="Layer: 50 protocols" src="https://img.shields.io/badge/Layer-50%20protocols-0a7f5a"></a>
<a href="https://pypi.org/project/tba-protocol-authzen/"><img alt="PyPI version for tba-protocol-authzen" src="https://img.shields.io/pypi/v/tba-protocol-authzen?label=tba-protocol-authzen%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-protocol-authzen"><img alt="Monthly PyPI downloads for tba-protocol-authzen" src="https://static.pepy.tech/badge/tba-protocol-authzen/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-authzen/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Layer-50 owner for OpenID AuthZEN Authorization API 1.0 and its superseded
draft/Implementer’s Draft history.

The package owns version selection, feature gates, lossless configuration
migrations, AuthZEN entity/message schemas, protocol errors, and the explicit
mapping from wire operations to `policy.evaluation` and
`artifact.processing` capabilities.

It intentionally declares an empty protocol claim class set: AuthZEN exchanges
policy entities and decisions rather than a registered token claim set. Signed
PDP metadata uses the separately owned JWT artifact processing capability.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_protocol_authzen import capability_report

report = capability_report()
assert report
print(sorted(report))
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-protocol-authzen==0.4.0.dev2" python quickstart.py
```

The command prints the keys in the package's capability report.

## Non-goals

This package does not implement policy decisions, own policy data, construct
providers, authenticate API callers, open sessions, or mount HTTP routes.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-authzen/src/tba_protocol_authzen/__init__.py).
