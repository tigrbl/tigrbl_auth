# tba-durability-replay-protection

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-durability-replay-protection/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-durability-replay-protection/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-durability-replay-protection/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/30-storage-runtime"><img alt="Layer: 30 storage runtime" src="https://img.shields.io/badge/Layer-30%20storage%20runtime-0a7f5a"></a>
<a href="https://pypi.org/project/tba-durability-replay-protection/"><img alt="PyPI version for tba-durability-replay-protection" src="https://img.shields.io/pypi/v/tba-durability-replay-protection?label=tba-durability-replay-protection%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-durability-replay-protection"><img alt="Monthly PyPI downloads for tba-durability-replay-protection" src="https://static.pepy.tech/badge/tba-durability-replay-protection/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/30-storage-runtime/tba-durability-replay-protection/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Compose replay protection persistence operations into an identity runtime.

## Quick start

Install the version used by this example.

```bash
python -m pip install "tba-durability-replay-protection==0.4.0.dev2"
```

Save the following as `quickstart.py` and run `python quickstart.py`. The assertions should pass.

```python
from tba_durability_replay_protection import RUNTIME_OPERATION_BY_ALIAS

aliases = sorted(RUNTIME_OPERATION_BY_ALIAS)
assert aliases
print(*aliases, sep="\n")
```

## When to use it

Use the exported operation inventory when wiring a runtime. This package owns durable replay operations and derived table specs. The runtime supplies a session and protocol layers decide when a replay check is required.

## Verification

See the [related repository tests](https://github.com/tigrbl/tigrbl_auth/blob/master/tests/unit/test_replay_layer_ownership.py) for the implementation scope covered by this example.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [tba-storage-core](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/01-storage/tba-storage-core#readme) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)
