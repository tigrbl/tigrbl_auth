# tba-protocol-gnap

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-gnap/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-gnap/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-gnap/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/50-protocols"><img alt="Layer: 50 protocols" src="https://img.shields.io/badge/Layer-50%20protocols-0a7f5a"></a>
<a href="https://pypi.org/project/tba-protocol-gnap/"><img alt="PyPI version for tba-protocol-gnap" src="https://img.shields.io/pypi/v/tba-protocol-gnap?label=tba-protocol-gnap%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-protocol-gnap"><img alt="Monthly PyPI downloads for tba-protocol-gnap" src="https://static.pepy.tech/badge/tba-protocol-gnap/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-gnap/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Layer-50 owner for RFC 9635, the Grant Negotiation and Authorization Protocol,
and the supported superseded draft migration paths.

The package owns RFC version/feature selection, compatibility, wire schemas,
subject-information claim composition, protocol errors, response envelopes,
and explicit mappings to grant negotiation, artifact verification, and replay
protection capabilities.

`sub_ids`, `assertions`, and RFC 3339 `updated_at` are imported from separate
layer-10 claim packages. The OIDC integer `updated_at` claim is intentionally
not reused because its value semantics differ.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_protocol_gnap import capability_report

report = capability_report()
assert report
print(sorted(report))
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-protocol-gnap==0.4.0.dev2" python quickstart.py
```

The command prints the keys in the package's capability report.

## Non-goals

This package does not persist grants, generate continuation secrets, mint or
verify tokens, authenticate resource owners, choose keys, open sessions, or
mount the GNAP HTTP endpoints.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-gnap/src/tba_protocol_gnap/__init__.py).
