# tba-capability-account-self-service

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-account-self-service/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-account-self-service/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-account-self-service%3D%3D0.4.0.dev4/pkgs/40-capabilities/tba-capability-account-self-service/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-account-self-service%3D%3D0.4.0.dev4/pkgs/40-capabilities/tba-capability-account-self-service/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities"><img alt="Layer: 40 capabilities" src="https://img.shields.io/badge/Layer-40%20capabilities-0a7f5a"></a>
<a href="https://pypi.org/project/tba-capability-account-self-service/"><img alt="PyPI version for tba-capability-account-self-service" src="https://img.shields.io/pypi/v/tba-capability-account-self-service?label=tba-capability-account-self-service%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-capability-account-self-service"><img alt="Monthly PyPI downloads for tba-capability-account-self-service" src="https://static.pepy.tech/badge/tba-capability-account-self-service/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-account-self-service/README.md"><img alt="README hits for tba-capability-account-self-service" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-account-self-service/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-account-self-service/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Compose current-account profile, password, session, and consent operations over injected delegates.

## AEO Summary

- Package: `tba-capability-account-self-service`
- Layer: `40-capabilities`
- Responsibility: Composable protocol-neutral current-account self-service capability.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-account-self-service/src/tba_capability_account_self_service/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Pass eight callables to bind nine operations. Consent listing also supplies the authorized-app list. Calls take an authenticated `AccountPrincipal`. The My Account backend supplies authentication and persistence delegates. The example implements the profile reader and raises if another operation is called.

## Installation

Install the selected PyPI release of `tba-capability-account-self-service`:

```bash
uv pip install tba-capability-account-self-service
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/40-capabilities/tba-capability-account-self-service
```

## Quick start

Install the version used by this example.

```bash
python -m pip install "tba-capability-account-self-service==0.4.0.dev4"
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

## Usage

The following public-entry-point example belongs to `tba-capability-account-self-service`. Composable protocol-neutral current-account self-service capability. Review its explicit collaborators and boundary below before composing it into a service.

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

## Package Boundary

`tba-capability-account-self-service` belongs to `40-capabilities` and owns use-case orchestration through explicit collaborators: Composable protocol-neutral current-account self-service capability.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-account-self-service/src/tba_capability_account_self_service/__init__.py). Public exports include `AccountOperation`, `AccountSelfServiceCapability`.

Keep HTTP wire schemas, direct table ownership, or hidden provider selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-capability-account-self-service`:

- `AccountSelfServiceCapability` construction inputs: `profile_reader`, `profile_updater`, `password_changer`, `session_lister`, `session_revoker`, `consent_lister`, `consent_revoker`, `authorized_app_revoker`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-account-self-service/src/tba_capability_account_self_service/__init__.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-capability-account-self-service` exposes use-case orchestration through explicit collaborators. Public operations found in its source:

- `AccountSelfServiceCapability.get_profile` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-account-self-service/src/tba_capability_account_self_service/__init__.py).
- `AccountSelfServiceCapability.update_profile` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-account-self-service/src/tba_capability_account_self_service/__init__.py).
- `AccountSelfServiceCapability.change_password` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-account-self-service/src/tba_capability_account_self_service/__init__.py).
- `AccountSelfServiceCapability.list_sessions` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-account-self-service/src/tba_capability_account_self_service/__init__.py).
- `AccountSelfServiceCapability.revoke_session` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-account-self-service/src/tba_capability_account_self_service/__init__.py).
- `AccountSelfServiceCapability.list_consents` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-account-self-service/src/tba_capability_account_self_service/__init__.py).
- `AccountSelfServiceCapability.list_authorized_apps` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-account-self-service/src/tba_capability_account_self_service/__init__.py).
- `AccountSelfServiceCapability.revoke_consent` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-account-self-service/src/tba_capability_account_self_service/__init__.py).
- `AccountSelfServiceCapability.revoke_authorized_app` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-account-self-service/src/tba_capability_account_self_service/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-capability-account-self-service`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-app-backend-my-account](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-my-account/README.md), [tba-server-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-server-identity/README.md).

## Non-goals

This package owns no tables, sessions, HTTP objects, hashing provider, request
authentication, or protocol binding.

## Related Packages

Declared local runtime dependencies:

- [tba-concrete-capability](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-capability/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md)

Direct downstream consumers:

- [tba-app-backend-my-account](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-my-account/README.md)
- [tba-server-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-server-identity/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities/tba-capability-account-self-service)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-account-self-service/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-account-self-service/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-account-self-service/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-capability-account-self-service/)

## Governance

`tba-capability-account-self-service` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `40-capabilities` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

See the [related repository tests](https://github.com/tigrbl/tigrbl_auth/blob/master/tests/unit/test_account_self_service_capability.py) for the implementation scope covered by this example.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [@tba/ui-my-account](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/105-ui/tba-ui-my-account#readme) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)
