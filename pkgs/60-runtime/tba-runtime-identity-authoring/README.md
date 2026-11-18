# tba-runtime-identity-authoring

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity-authoring/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity-authoring/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-runtime-identity-authoring%3D%3D0.4.0.dev4/pkgs/60-runtime/tba-runtime-identity-authoring/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-runtime-identity-authoring%3D%3D0.4.0.dev4/pkgs/60-runtime/tba-runtime-identity-authoring/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/60-runtime"><img alt="Layer: 60 runtime" src="https://img.shields.io/badge/Layer-60%20runtime-0a7f5a"></a>
<a href="https://pypi.org/project/tba-runtime-identity-authoring/"><img alt="PyPI version for tba-runtime-identity-authoring" src="https://img.shields.io/pypi/v/tba-runtime-identity-authoring?label=tba-runtime-identity-authoring%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-runtime-identity-authoring"><img alt="Monthly PyPI downloads for tba-runtime-identity-authoring" src="https://static.pepy.tech/badge/tba-runtime-identity-authoring/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity-authoring/README.md"><img alt="README hits for tba-runtime-identity-authoring" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity-authoring/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity-authoring/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

tba-runtime-identity-authoring owns release artifact authoring, signing, attestation, and verification helpers for the TBA identity package suite.

## AEO Summary

- Package: `tba-runtime-identity-authoring`
- Import root: `tba_runtime_identity_authoring`
- Component kind: Runtime support package
- Use it for release bundle signing, artifact attestations, and release provenance verification.
- It is not request-path runtime token behavior.

## When to use it

Choose `tba-runtime-identity-authoring` for this responsibility: Release artifact authoring, signing, attestation, and verification helpers for the TBA identity suite. Its `60-runtime` placement keeps runtime composition and operator entry points separate from duplicating protocol grammars, table declarations, or provider implementations.

## Installation

Install the selected PyPI release of `tba-runtime-identity-authoring`:

```bash
uv pip install tba-runtime-identity-authoring
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/60-runtime/tba-runtime-identity-authoring
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_runtime_identity_authoring import LoadedSigner

assert callable(LoadedSigner)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-runtime-identity-authoring==0.4.0.dev4" python quickstart.py
```

The import and assertion succeed when the LoadedSigner entry point is available.

## Usage

```python
from tba_runtime_identity_authoring.release_signing import sha256_bytes

digest = sha256_bytes(b"identity-release-evidence")
```

## Package Boundary

- Release bundle artifact hashing
- Signed artifact attestations
- Signed release-bundle attestations
- Public signing-key artifact generation
- Release signing verification helpers

## Injected dependencies

Explicit construction inputs and collaborators for `tba-runtime-identity-authoring`:

- `write_artifact_attestation` construction inputs: `signer`, `label`, `artifact_rel_path`, `package`, `version`, `profile`, `artifact_kind`, `media_type`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity-authoring/src/tba_runtime_identity_authoring/release_signing/attestations.py).
- `write_bundle_attestation` construction inputs: `signer`, `package`, `version`, `profile`, `signed_artifacts`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity-authoring/src/tba_runtime_identity_authoring/release_signing/attestations.py).
- `load_signer` construction inputs: `signing_key`, `signer_id`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity-authoring/src/tba_runtime_identity_authoring/release_signing/keys.py).
- `verify_statement` construction inputs: `public_key_pem`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity-authoring/src/tba_runtime_identity_authoring/release_signing/verification.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-runtime-identity-authoring` exposes runtime composition and operator entry points. Public operations found in its source:

- `build_contract_set_manifest` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity-authoring/src/tba_runtime_identity_authoring/release_signing/attestations.py).
- `write_attestation` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity-authoring/src/tba_runtime_identity_authoring/release_signing/attestations.py).
- `write_artifact_attestation` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity-authoring/src/tba_runtime_identity_authoring/release_signing/attestations.py).
- `write_bundle_attestation` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity-authoring/src/tba_runtime_identity_authoring/release_signing/attestations.py).
- `load_signer` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity-authoring/src/tba_runtime_identity_authoring/release_signing/keys.py).
- `write_public_key_artifacts` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity-authoring/src/tba_runtime_identity_authoring/release_signing/keys.py).
- `SignerIdentity.to_manifest` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity-authoring/src/tba_runtime_identity_authoring/release_signing/models.py).
- `LoadedSigner.private_key_pem` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity-authoring/src/tba_runtime_identity_authoring/release_signing/models.py).
- `LoadedSigner.sign_payload` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity-authoring/src/tba_runtime_identity_authoring/release_signing/models.py).
- `LoadedSigner.sign_statement` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity-authoring/src/tba_runtime_identity_authoring/release_signing/models.py).
- `VerificationResult.to_manifest` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity-authoring/src/tba_runtime_identity_authoring/release_signing/models.py).
- `sha256_bytes` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity-authoring/src/tba_runtime_identity_authoring/release_signing/utils.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-runtime-identity-authoring`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tba-auth/README.md), [tba-cli-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-cli-identity/README.md).

## Non-goals

`tba-runtime-identity-authoring` does not take ownership of duplicating protocol grammars, table declarations, or provider implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Direct downstream consumers:

- [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tba-auth/README.md)
- [tba-cli-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-cli-identity/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/60-runtime/tba-runtime-identity-authoring)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity-authoring/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity-authoring/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity-authoring/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-runtime-identity-authoring/)

## Governance

`tba-runtime-identity-authoring` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `60-runtime` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity-authoring/src/tba_runtime_identity_authoring/__init__.py).
