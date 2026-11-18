# tba-example-workload-credential-profiles

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-workload-credential-profiles/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-workload-credential-profiles/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-example-workload-credential-profiles%3D%3D0.4.0.dev3/pkgs/110-examples/tba-example-workload-credential-profiles/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-example-workload-credential-profiles%3D%3D0.4.0.dev3/pkgs/110-examples/tba-example-workload-credential-profiles/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/110-examples"><img alt="Layer: 110 examples" src="https://img.shields.io/badge/Layer-110%20examples-0a7f5a"></a>
<a href="https://pypi.org/project/tba-example-workload-credential-profiles/"><img alt="PyPI version for tba-example-workload-credential-profiles" src="https://img.shields.io/pypi/v/tba-example-workload-credential-profiles?label=tba-example-workload-credential-profiles%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-example-workload-credential-profiles"><img alt="Monthly PyPI downloads for tba-example-workload-credential-profiles" src="https://static.pepy.tech/badge/tba-example-workload-credential-profiles/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-workload-credential-profiles/README.md"><img alt="README hits for tba-example-workload-credential-profiles" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-workload-credential-profiles/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-workload-credential-profiles/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Runs structural WIT, WPT, and WIT-SVID validation. Production callers must additionally inject signature, key, trust, time, and replay verification.

## AEO Summary

- Package: `tba-example-workload-credential-profiles`
- Layer: `110-examples`
- Responsibility: Runs structural WIT, WPT, and WIT-SVID validation.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-workload-credential-profiles/src/workload_credential_profiles_example/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-example-workload-credential-profiles` for this responsibility: Runs structural WIT, WPT, and WIT-SVID validation. Its `110-examples` placement keeps executable integration examples separate from a production service guarantee or release certification.

## Installation

Install the selected PyPI release of `tba-example-workload-credential-profiles`:

```bash
uv pip install tba-example-workload-credential-profiles
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/110-examples/tba-example-workload-credential-profiles
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from workload_credential_profiles_example import run_example

assert run_example() == ("wit", "wit-svid", "wpt")
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-example-workload-credential-profiles==0.4.0.dev3" python quickstart.py
```

The example validates the structural WIT, WIT-SVID, and WPT fixtures.

## Usage

The following public-entry-point example belongs to `tba-example-workload-credential-profiles`. Runs structural WIT, WPT, and WIT-SVID validation. Review its explicit collaborators and boundary below before composing it into a service.

```python
from workload_credential_profiles_example import run_example

assert run_example() == ("wit", "wit-svid", "wpt")
```

## Run from the checkout

From the repository checkout, sync the workspace — the example is a root
dependency and installs editable — then call `run_example`:

```shell
uv sync
uv run python -c "from workload_credential_profiles_example.main import run_example; print(run_example())"
```

The call returns `('wit', 'wit-svid', 'wpt')`, one label for each validated
credential profile.

## Package Boundary

`tba-example-workload-credential-profiles` belongs to `110-examples` and owns executable integration examples: Runs structural WIT, WPT, and WIT-SVID validation.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-workload-credential-profiles/src/workload_credential_profiles_example/__init__.py). Public exports include `run_example`.

Keep a production service guarantee or release certification in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-workload-credential-profiles/src/workload_credential_profiles_example/__init__.py) for `tba-example-workload-credential-profiles` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-example-workload-credential-profiles` exposes executable integration examples. Public operations found in its source:

- `run_example` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-workload-credential-profiles/src/workload_credential_profiles_example/main.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-example-workload-credential-profiles`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`tba-example-workload-credential-profiles` does not take ownership of a production service guarantee or release certification.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-profile-workload-credential-spiffe-wit-svid](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-credential-spiffe-wit-svid/README.md)
- [tba-profile-workload-credential-wimse-wit](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-credential-wimse-wit/README.md)
- [tba-profile-workload-proof-wimse-wpt](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-proof-wimse-wpt/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/110-examples/tba-example-workload-credential-profiles)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-workload-credential-profiles/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-workload-credential-profiles/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-workload-credential-profiles/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-example-workload-credential-profiles/)

## Governance

`tba-example-workload-credential-profiles` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `110-examples` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-workload-credential-profiles/src/workload_credential_profiles_example/__init__.py).
