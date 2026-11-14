# tba-capability-account-self-service

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-account-self-service/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-account-self-service/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-account-self-service/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities"><img alt="Layer: 40 capabilities" src="https://img.shields.io/badge/Layer-40%20capabilities-0a7f5a"></a>
<a href="https://pypi.org/project/tba-capability-account-self-service/"><img alt="PyPI version for tba-capability-account-self-service" src="https://img.shields.io/pypi/v/tba-capability-account-self-service?label=tba-capability-account-self-service%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-capability-account-self-service"><img alt="Monthly PyPI downloads for tba-capability-account-self-service" src="https://static.pepy.tech/badge/tba-capability-account-self-service/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-account-self-service/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Compose current-account profile, password, session, and consent operations over injected delegates.

## Quick start

Install the version used by this example.

```bash
python -m pip install "tba-capability-account-self-service==0.4.0.dev2"
```

Save the following as `quickstart.py` and run `python quickstart.py`. The assertions should pass.

```python
import asyncio

from tba_capability_account_self_service import AccountSelfServiceCapability
from tba_contracts_identity.account_self_service import AccountPrincipal, AccountProfile

def read_profile(principal):
    return AccountProfile(principal.identity_id, "tenant", "alice", "alice@example.test")

def unbound(*args):
    raise NotImplementedError("profile-only demo")

account = AccountSelfServiceCapability(
    profile_reader=read_profile,
    profile_updater=unbound,
    password_changer=unbound,
    session_lister=unbound,
    session_revoker=unbound,
    consent_lister=unbound,
    consent_revoker=unbound,
    authorized_app_revoker=unbound,
)
profile = asyncio.run(account.get_profile(AccountPrincipal("identity", "tenant")))
assert profile.username == "alice"
```

## When to use it

Pass eight callables to bind nine operations. Consent listing also supplies the authorized-app list. Calls take an authenticated `AccountPrincipal`. The My Account backend supplies authentication and persistence delegates. The example implements the profile reader and raises if another operation is called.

## Verification

See the [related repository tests](https://github.com/tigrbl/tigrbl_auth/blob/master/tests/unit/test_account_self_service_capability.py) for the implementation scope covered by this example.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [@tba/ui-my-account](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/105-ui/tba-ui-my-account#readme) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)
