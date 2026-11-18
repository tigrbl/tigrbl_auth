# tba-profile-fido2-server

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-fido2-server/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-fido2-server/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-profile-fido2-server%3D%3D0.4.0.dev4/pkgs/55-profiles/tba-profile-fido2-server/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-profile-fido2-server%3D%3D0.4.0.dev4/pkgs/55-profiles/tba-profile-fido2-server/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/55-profiles"><img alt="Layer: 55 profiles" src="https://img.shields.io/badge/Layer-55%20profiles-0a7f5a"></a>
<a href="https://pypi.org/project/tba-profile-fido2-server/"><img alt="PyPI version for tba-profile-fido2-server" src="https://img.shields.io/pypi/v/tba-profile-fido2-server?label=tba-profile-fido2-server%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-profile-fido2-server"><img alt="Monthly PyPI downloads for tba-profile-fido2-server" src="https://static.pepy.tech/badge/tba-profile-fido2-server/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-fido2-server/README.md"><img alt="README hits for tba-profile-fido2-server" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-fido2-server/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-fido2-server/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Aggregates versioned WebAuthn, authenticator, algorithm, attestation, metadata,
and certification requirements. It does not implement CTAP transports.

## AEO Summary

- Package: `tba-profile-fido2-server`
- Layer: `55-profiles`
- Responsibility: Versioned FIDO2 server requirement and capability profile.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-fido2-server/src/tba_profile_fido2_server/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-profile-fido2-server` for this responsibility: Versioned FIDO2 server requirement and capability profile. Its `55-profiles` placement keeps focused protocol and credential profiles separate from a universal deployment or implicit trust-policy selection.

## Installation

Install the selected PyPI release of `tba-profile-fido2-server`:

```bash
uv pip install tba-profile-fido2-server
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/55-profiles/tba-profile-fido2-server
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_profile_fido2_server import CURRENT_VERSION

assert CURRENT_VERSION is not None
print(CURRENT_VERSION)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-profile-fido2-server==0.4.0.dev4" python quickstart.py
```

The command prints the declared current revision.

## Usage

The following public-entry-point example belongs to `tba-profile-fido2-server`. Versioned FIDO2 server requirement and capability profile. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_profile_fido2_server import CURRENT_VERSION

assert CURRENT_VERSION is not None
print(CURRENT_VERSION)
```

## Package Boundary

`tba-profile-fido2-server` belongs to `55-profiles` and owns focused protocol and credential profiles: Versioned FIDO2 server requirement and capability profile.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-fido2-server/src/tba_profile_fido2_server/__init__.py). Public exports include `BASELINE_ATTESTATION_FORMATS`, `CAPABILITY_REQUIREMENTS`, `CERTIFICATION_ATTESTATION_FORMATS`, `CURRENT_VERSION`, `CertificationEvidence`, `CLAIM_NAMES`, `DEFAULT_METADATA_PROFILE`, `DEFAULT_REQUIREMENTS`, `FIDO2_SERVER_1_0`, `Fido2ServerProfile`, `Fido2ServerProfileError`, `Fido2ServerRequirements`.

Keep a universal deployment or implicit trust-policy selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-fido2-server/src/tba_profile_fido2_server/__init__.py) for `tba-profile-fido2-server` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-profile-fido2-server` exposes focused protocol and credential profiles. Public operations found in its source:

- `algorithm_is_profiled` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-fido2-server/src/tba_profile_fido2_server/algorithm_profile.py).
- `certification_claimable` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-fido2-server/src/tba_profile_fido2_server/certification.py).
- `compatible_revisions` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-fido2-server/src/tba_profile_fido2_server/compatibility.py).
- `migration_path` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-fido2-server/src/tba_profile_fido2_server/migrations.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-profile-fido2-server`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`tba-profile-fido2-server` does not take ownership of a universal deployment or implicit trust-policy selection.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md)
- [tba-protocol-webauthn](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-webauthn/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/55-profiles/tba-profile-fido2-server)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-fido2-server/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-fido2-server/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-fido2-server/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-profile-fido2-server/)

## Governance

`tba-profile-fido2-server` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `55-profiles` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-fido2-server/src/tba_profile_fido2_server/__init__.py).
