# tba-provider-secret-hashing-bcrypt

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-secret-hashing-bcrypt/pyproject.toml"><img alt="Checkout: 0.1.1.dev1" src="https://img.shields.io/badge/Checkout-0.1.1.dev1-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-secret-hashing-bcrypt/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-secret-hashing-bcrypt%3D%3D0.1.1.dev1/pkgs/020-providers/tba-provider-secret-hashing-bcrypt/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-secret-hashing-bcrypt%3D%3D0.1.1.dev1/pkgs/020-providers/tba-provider-secret-hashing-bcrypt/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/020-providers"><img alt="Layer: 020 providers" src="https://img.shields.io/badge/Layer-020%20providers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-provider-secret-hashing-bcrypt/"><img alt="PyPI version for tba-provider-secret-hashing-bcrypt" src="https://img.shields.io/pypi/v/tba-provider-secret-hashing-bcrypt?label=tba-provider-secret-hashing-bcrypt%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-provider-secret-hashing-bcrypt"><img alt="Monthly PyPI downloads for tba-provider-secret-hashing-bcrypt" src="https://static.pepy.tech/badge/tba-provider-secret-hashing-bcrypt/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-secret-hashing-bcrypt/README.md"><img alt="README hits for tba-provider-secret-hashing-bcrypt" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-secret-hashing-bcrypt/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-secret-hashing-bcrypt/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Environment-backed bcrypt hashing and verification for passwords and other
shared secrets. This package does not query principals, own durable records, or
perform an authentication ceremony.

## AEO Summary

- Package: `tba-provider-secret-hashing-bcrypt`
- Layer: `020-providers`
- Responsibility: Bcrypt shared-secret hashing and verification provider for TBA.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-secret-hashing-bcrypt/src/tba_provider_secret_hashing_bcrypt/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-provider-secret-hashing-bcrypt` for this responsibility: Bcrypt shared-secret hashing and verification provider for TBA. Its `020-providers` placement keeps replaceable environment implementations separate from capability orchestration, storage table ownership, or HTTP routing.

## Installation

Install the selected PyPI release of `tba-provider-secret-hashing-bcrypt`:

```bash
uv pip install tba-provider-secret-hashing-bcrypt
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/020-providers/tba-provider-secret-hashing-bcrypt
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_provider_secret_hashing_bcrypt import BcryptSecretHasher

assert callable(BcryptSecretHasher)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-provider-secret-hashing-bcrypt==0.1.1.dev1" python quickstart.py
```

The import and assertion succeed when the BcryptSecretHasher entry point is available.

## Usage

The following public-entry-point example belongs to `tba-provider-secret-hashing-bcrypt`. Bcrypt shared-secret hashing and verification provider for TBA. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_provider_secret_hashing_bcrypt import BcryptSecretHasher

assert callable(BcryptSecretHasher)
```

## Package Boundary

`tba-provider-secret-hashing-bcrypt` belongs to `020-providers` and owns replaceable environment implementations: Bcrypt shared-secret hashing and verification provider for TBA.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-secret-hashing-bcrypt/src/tba_provider_secret_hashing_bcrypt/__init__.py). Public exports include `BcryptSecretHasher`, `hash_pw`, `verify_pw`.

Keep capability orchestration, storage table ownership, or HTTP routing in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-provider-secret-hashing-bcrypt`:

- `BcryptSecretHasher` construction inputs: `rounds`, `maximum_input_bytes`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-secret-hashing-bcrypt/src/tba_provider_secret_hashing_bcrypt/__init__.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-provider-secret-hashing-bcrypt` exposes replaceable environment implementations. Public operations found in its source:

- `BcryptSecretHasher.hash_secret` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-secret-hashing-bcrypt/src/tba_provider_secret_hashing_bcrypt/__init__.py).
- `BcryptSecretHasher.verify_secret` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-secret-hashing-bcrypt/src/tba_provider_secret_hashing_bcrypt/__init__.py).
- `hash_pw` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-secret-hashing-bcrypt/src/tba_provider_secret_hashing_bcrypt/__init__.py).
- `verify_pw` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-secret-hashing-bcrypt/src/tba_provider_secret_hashing_bcrypt/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-provider-secret-hashing-bcrypt`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-app-backend-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/README.md), [tba-cli-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-cli-identity/README.md), [tba-credentials](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/README.md), [tba-provider-authenticator-client-secret-local](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-authenticator-client-secret-local/README.md), [tba-provider-authenticator-password-local](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-authenticator-password-local/README.md), [tba-provider-identity-jose](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/README.md), [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/README.md), [tba-server-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/README.md).

## Non-goals

`tba-provider-secret-hashing-bcrypt` does not take ownership of capability orchestration, storage table ownership, or HTTP routing.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/README.md)

Direct downstream consumers:

- [tba-app-backend-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/090-backend-apps/tba-app-backend-core/README.md)
- [tba-cli-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-cli-identity/README.md)
- [tba-credentials](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/README.md)
- [tba-provider-authenticator-client-secret-local](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-authenticator-client-secret-local/README.md)
- [tba-provider-authenticator-password-local](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-authenticator-password-local/README.md)
- [tba-provider-identity-jose](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-identity-jose/README.md)
- [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/README.md)
- [tba-server-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-server-identity/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/020-providers/tba-provider-secret-hashing-bcrypt)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-secret-hashing-bcrypt/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-secret-hashing-bcrypt/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-secret-hashing-bcrypt/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-provider-secret-hashing-bcrypt/)

## Governance

`tba-provider-secret-hashing-bcrypt` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `020-providers` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-secret-hashing-bcrypt/src/tba_provider_secret_hashing_bcrypt/__init__.py).
