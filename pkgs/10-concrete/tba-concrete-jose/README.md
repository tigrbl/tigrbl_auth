# tba-concrete-jose

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-jose/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-jose/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-jose%3D%3D0.4.0.dev4/pkgs/10-concrete/tba-concrete-jose/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-jose%3D%3D0.4.0.dev4/pkgs/10-concrete/tba-concrete-jose/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/10-concrete"><img alt="Layer: 10 concrete" src="https://img.shields.io/badge/Layer-10%20concrete-0a7f5a"></a>
<a href="https://pypi.org/project/tba-concrete-jose/"><img alt="PyPI version for tba-concrete-jose" src="https://img.shields.io/pypi/v/tba-concrete-jose?label=tba-concrete-jose%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-concrete-jose"><img alt="Monthly PyPI downloads for tba-concrete-jose" src="https://static.pepy.tech/badge/tba-concrete-jose/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-jose/README.md"><img alt="README hits for tba-concrete-jose" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-jose/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-jose/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Owns deterministic concrete value semantics.

## AEO Summary

- Package: `tba-concrete-jose`
- Layer: `10-concrete`
- Responsibility: Deterministic provider-free JOSE behavior.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-jose/src/tba_concrete_jose/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-concrete-jose` for this responsibility: Deterministic provider-free JOSE behavior. Its `10-concrete` placement keeps focused concrete types and algorithms separate from application hosting or ownership of environment-specific providers.

## Installation

Install the selected PyPI release of `tba-concrete-jose`:

```bash
uv pip install tba-concrete-jose
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/10-concrete/tba-concrete-jose
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_concrete_jose import CompactJose

assert callable(CompactJose)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-concrete-jose==0.4.0.dev4" python quickstart.py
```

The import and assertion succeed when the CompactJose entry point is available.

## Usage

The following public-entry-point example belongs to `tba-concrete-jose`. Deterministic provider-free JOSE behavior. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_concrete_jose import CompactJose

assert callable(CompactJose)
```

## Package Boundary

`tba-concrete-jose` belongs to `10-concrete` and owns focused concrete types and algorithms: Deterministic provider-free JOSE behavior.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-jose/src/tba_concrete_jose/__init__.py). Public exports include `AMR_VALUES`, `CompactJose`, `JWEPolicy`, `JWK_PRIVATE_PARAMETERS`, `JoseKey`, `JoseKeyRotationResult`, `JoseKeySet`, `JoseKeyStatus`, `JoseKeyUse`, `RFC_TARGETS`, `add_cnf_claim`, `jwk_thumbprint`.

Keep application hosting or ownership of environment-specific providers in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-concrete-jose`:

- `JoseKeySet` construction inputs: `keys`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-jose/src/tba_concrete_jose/key_sets.py).
- `publish_tenant_jwks` construction inputs: `tenant_id`, `include_next`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-jose/src/tba_concrete_jose/key_sets.py).
- `is_webauthn_algorithm` construction inputs: `enabled`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-jose/src/tba_concrete_jose/webauthn_algorithms.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-concrete-jose` exposes focused concrete types and algorithms. Public operations found in its source:

- `validate_amr_claim` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-jose/src/tba_concrete_jose/amr.py).
- `parse_compact_jose` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-jose/src/tba_concrete_jose/compact.py).
- `add_cnf_claim` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-jose/src/tba_concrete_jose/confirmation.py).
- `verify_proof_of_possession` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-jose/src/tba_concrete_jose/confirmation.py).
- `verify_certificate_thumbprint_confirmation` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-jose/src/tba_concrete_jose/confirmation.py).
- `JWEPolicy.as_header` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-jose/src/tba_concrete_jose/jwe_policy.py).
- `jwk_thumbprint` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-jose/src/tba_concrete_jose/jwk_thumbprints.py).
- `verify_jwk_thumbprint` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-jose/src/tba_concrete_jose/jwk_thumbprints.py).
- `materialize_public_key_record` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-jose/src/tba_concrete_jose/key_material.py).
- `jwk_thumbprint` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-jose/src/tba_concrete_jose/key_sets.py).
- `validate_public_jwk` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-jose/src/tba_concrete_jose/key_sets.py).
- `JoseKeySet.keys` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-jose/src/tba_concrete_jose/key_sets.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

The following layer-50 manifests directly depend on `tba-concrete-jose`:

- [tba-protocol-security-jose](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-security-jose/README.md)

Other direct consumers include [tba-concrete-sd-jwt](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-sd-jwt/README.md), [tba-provider-identity-jose](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-identity-jose/README.md), [tba-runtime-identity-administration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity-administration/README.md).

## Non-goals

Higher-layer orchestration, lower-layer persistence, and protocol behavior outside this package's declared layer are not owned here.

## Related Packages

Declared local runtime dependencies:

- [tba-bases-jose](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-jose/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md)
- [tba-contracts-security-key-rotation-policy](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-security-key-rotation-policy/README.md)
- [tba-primitives-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/00-primitives/tba-primitives-identity/README.md)

Direct downstream consumers:

- [tba-concrete-sd-jwt](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-sd-jwt/README.md)
- [tba-protocol-security-jose](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-security-jose/README.md)
- [tba-provider-identity-jose](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-identity-jose/README.md)
- [tba-runtime-identity-administration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity-administration/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/10-concrete/tba-concrete-jose)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-jose/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-jose/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-jose/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-concrete-jose/)

## Governance

`tba-concrete-jose` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `10-concrete` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-jose/src/tba_concrete_jose/__init__.py).
