# tba-capability-workload-identity

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-workload-identity/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-workload-identity/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-workload-identity/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities"><img alt="Layer: 40 capabilities" src="https://img.shields.io/badge/Layer-40%20capabilities-0a7f5a"></a>
<a href="https://pypi.org/project/tba-capability-workload-identity/"><img alt="PyPI version for tba-capability-workload-identity" src="https://img.shields.io/pypi/v/tba-capability-workload-identity?label=tba-capability-workload-identity%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-capability-workload-identity"><img alt="Monthly PyPI downloads for tba-capability-workload-identity" src="https://static.pepy.tech/badge/tba-capability-workload-identity/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-workload-identity/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Protocol-neutral workload credential acquisition, verification, trust resolution, and refresh capability. SPIFFE and WIMSE mappings belong in layer 50.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_capability_workload_identity import WorkloadIdentityCapability

assert callable(WorkloadIdentityCapability)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-capability-workload-identity==0.4.0.dev2" python quickstart.py
```

The import and assertion succeed when the WorkloadIdentityCapability entry point is available.

## Injected dependencies

- No package-mandated runtime dependency; callables are constructor-injected.

## Operations and readiness

- `obtain_workload_credential`
- `refresh_workload_credentials`
- `resolve_workload_trust`
- `verify_workload_credential`

## Protocol consumers

- Protocol-neutral; layer-50 packages may bind these operations.

## Non-goals

- No HTTP or protocol wire schemas.
- No direct layer-01 table access.
- No hidden mutable persistence or provider selection.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-workload-identity/src/tba_capability_workload_identity/__init__.py).
