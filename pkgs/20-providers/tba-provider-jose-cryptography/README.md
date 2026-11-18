# tba-provider-jose-cryptography

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-jose-cryptography/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-jose-cryptography/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-jose-cryptography%3D%3D0.4.0.dev4/pkgs/20-providers/tba-provider-jose-cryptography/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-jose-cryptography%3D%3D0.4.0.dev4/pkgs/20-providers/tba-provider-jose-cryptography/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers"><img alt="Layer: 20 providers" src="https://img.shields.io/badge/Layer-20%20providers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-provider-jose-cryptography/"><img alt="PyPI version for tba-provider-jose-cryptography" src="https://img.shields.io/pypi/v/tba-provider-jose-cryptography?label=tba-provider-jose-cryptography%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-provider-jose-cryptography"><img alt="Monthly PyPI downloads for tba-provider-jose-cryptography" src="https://static.pepy.tech/badge/tba-provider-jose-cryptography/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-jose-cryptography/README.md"><img alt="README hits for tba-provider-jose-cryptography" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-jose-cryptography/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-jose-cryptography/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Neutral cryptography-backed JWS and JWE provider. Protocol profiles and trust policy remain layer-50 concerns.

## AEO Summary

- Package: `tba-provider-jose-cryptography`
- Layer: `20-providers`
- Responsibility: Neutral cryptography-backed JWS and JWE provider.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-jose-cryptography/src/tba_provider_jose_cryptography/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-provider-jose-cryptography` for this responsibility: Neutral cryptography-backed JWS and JWE provider. Its `20-providers` placement keeps replaceable environment implementations separate from capability orchestration, storage table ownership, or HTTP routing.

## Installation

Install the selected PyPI release of `tba-provider-jose-cryptography`:

```bash
uv pip install tba-provider-jose-cryptography
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/20-providers/tba-provider-jose-cryptography
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_provider_jose_cryptography import JweCryptographyProvider

assert callable(JweCryptographyProvider)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-provider-jose-cryptography==0.4.0.dev4" python quickstart.py
```

The import and assertion succeed when the JweCryptographyProvider entry point is available.

## Usage

The following public-entry-point example belongs to `tba-provider-jose-cryptography`. Neutral cryptography-backed JWS and JWE provider. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_provider_jose_cryptography import JweCryptographyProvider

assert callable(JweCryptographyProvider)
```

### Opt-in X448 JWE

Inject `JweCipherPolicy` from `tba-concrete-jose` to enable compact
`ECDH-ES` with `A256GCM`. Configure the sender with the recipient's
`X448PublicKey` and the recipient with its `X448PrivateKey`. Both key
maps are indexed by the protected `kid`.

```python
from cryptography.hazmat.primitives.asymmetric.x448 import X448PrivateKey
from tba_concrete_jose import JweCipherPolicy
from tba_provider_jose_cryptography import JweCryptographyProvider

recipient = X448PrivateKey.generate()
policy = JweCipherPolicy()
issuer = JweCryptographyProvider(
    cipher_policy=policy, x448_public_keys={"recipient": recipient.public_key()}
)
verifier = JweCryptographyProvider(
    cipher_policy=policy, x448_private_keys={"recipient": recipient}
)
```

## Package Boundary

`tba-provider-jose-cryptography` belongs to `20-providers` and owns replaceable environment implementations: Neutral cryptography-backed JWS and JWE provider.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-jose-cryptography/src/tba_provider_jose_cryptography/__init__.py). Public exports include `JweCryptographyProvider`, `JwsCryptographyProvider`.

Keep capability orchestration, storage table ownership, or HTTP routing in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-provider-jose-cryptography`:

- `JweCryptographyProvider` accepts `keys`, `cipher_policy`, `x448_public_keys`, and `x448_private_keys`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-jose-cryptography/src/tba_provider_jose_cryptography/jwe.py).
- `JwsCryptographyProvider` construction inputs: `keys`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-jose-cryptography/src/tba_provider_jose_cryptography/jws.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-provider-jose-cryptography` exposes replaceable environment implementations. Public operations found in its source:

- `JweCryptographyProvider.protect` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-jose-cryptography/src/tba_provider_jose_cryptography/jwe.py).
- `JweCryptographyProvider.verify` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-jose-cryptography/src/tba_provider_jose_cryptography/jwe.py).
- `JwsCryptographyProvider.protect` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-jose-cryptography/src/tba_provider_jose_cryptography/jws.py).
- `JwsCryptographyProvider.verify` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-jose-cryptography/src/tba_provider_jose_cryptography/jws.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

The following layer-50 manifests directly depend on `tba-provider-jose-cryptography`:

- [tba-protocol-workload-spiffe-svid](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-workload-spiffe-svid/README.md)

Other direct consumers include [tba-app-backend-wit-issuance](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wit-issuance/README.md), [tba-profile-workload-credential-spiffe-wit-svid](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-credential-spiffe-wit-svid/README.md), [tba-profile-workload-credential-wimse-wit](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-credential-wimse-wit/README.md), [tba-profile-workload-proof-wimse-http-signature](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-proof-wimse-http-signature/README.md), [tba-profile-workload-proof-wimse-wpt](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-proof-wimse-wpt/README.md), [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/README.md).

## Non-goals

`tba-provider-jose-cryptography` does not take ownership of capability orchestration, storage table ownership, or HTTP routing.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-bases-protected-envelope](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-protected-envelope/README.md)
- [tba-concrete-jwe](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-jwe/README.md)
- [tba-concrete-jws](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-jws/README.md)
- [tba-contracts-protected-envelope](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-protected-envelope/README.md)
- [tba-contracts-security-trust](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-security-trust/README.md)
- [tba-primitives-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/00-primitives/tba-primitives-identity/README.md)

Direct downstream consumers:

- [tba-app-backend-wit-issuance](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wit-issuance/README.md)
- [tba-profile-workload-credential-spiffe-wit-svid](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-credential-spiffe-wit-svid/README.md)
- [tba-profile-workload-credential-wimse-wit](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-credential-wimse-wit/README.md)
- [tba-profile-workload-proof-wimse-http-signature](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-proof-wimse-http-signature/README.md)
- [tba-profile-workload-proof-wimse-wpt](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-proof-wimse-wpt/README.md)
- [tba-protocol-workload-spiffe-svid](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-workload-spiffe-svid/README.md)
- [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers/tba-provider-jose-cryptography)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-jose-cryptography/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-jose-cryptography/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-jose-cryptography/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-provider-jose-cryptography/)

## Governance

`tba-provider-jose-cryptography` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `20-providers` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-jose-cryptography/src/tba_provider_jose_cryptography/__init__.py).

Set `SWARMAURI_SDK_ROOT` to the Swarmauri SDK checkout containing X448
support and run `python -m pytest tests/unit/test_x448_jwe_swarmauri_interop.py`
from the TbA checkout to test compact JWE in both directions.
