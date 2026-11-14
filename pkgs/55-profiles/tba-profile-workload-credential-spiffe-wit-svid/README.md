# tba-profile-workload-credential-spiffe-wit-svid

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-credential-spiffe-wit-svid/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-credential-spiffe-wit-svid/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/55-profiles"><img alt="Layer: 55 profiles" src="https://img.shields.io/badge/Layer-55%20profiles-0a7f5a"></a>
<a href="https://pypi.org/project/tba-profile-workload-credential-spiffe-wit-svid/"><img alt="PyPI version for tba-profile-workload-credential-spiffe-wit-svid" src="https://img.shields.io/pypi/v/tba-profile-workload-credential-spiffe-wit-svid?label=tba-profile-workload-credential-spiffe-wit-svid%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-profile-workload-credential-spiffe-wit-svid"><img alt="Monthly PyPI downloads for tba-profile-workload-credential-spiffe-wit-svid" src="https://static.pepy.tech/badge/tba-profile-workload-credential-spiffe-wit-svid/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-credential-spiffe-wit-svid/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Incubating SPIFFE WIT-SVID profile pinned to the SPIFFE v1.15.1 publication. Disabled by default.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

```python
from tba_profile_workload_credential_spiffe_wit_svid import CURRENT_VERSION

assert CURRENT_VERSION is not None
print(CURRENT_VERSION)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-profile-workload-credential-spiffe-wit-svid==0.4.0.dev2" python quickstart.py
```

The command prints the declared current revision.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-credential-spiffe-wit-svid/src/tba_profile_workload_credential_spiffe_wit_svid/__init__.py).
