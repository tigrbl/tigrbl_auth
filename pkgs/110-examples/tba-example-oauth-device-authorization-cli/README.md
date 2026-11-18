# tba-example-oauth-device-authorization-cli

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli/pyproject.toml"><img alt="Checkout: 0.1.1.dev2" src="https://img.shields.io/badge/Checkout-0.1.1.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-example-oauth-device-authorization-cli%3D%3D0.1.1.dev2/pkgs/110-examples/tba-example-oauth-device-authorization-cli/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-example-oauth-device-authorization-cli%3D%3D0.1.1.dev2/pkgs/110-examples/tba-example-oauth-device-authorization-cli/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/110-examples"><img alt="Layer: 110 examples" src="https://img.shields.io/badge/Layer-110%20examples-0a7f5a"></a>
<a href="https://pypi.org/project/tba-example-oauth-device-authorization-cli/"><img alt="PyPI version for tba-example-oauth-device-authorization-cli" src="https://img.shields.io/pypi/v/tba-example-oauth-device-authorization-cli?label=tba-example-oauth-device-authorization-cli%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-example-oauth-device-authorization-cli"><img alt="Monthly PyPI downloads for tba-example-oauth-device-authorization-cli" src="https://static.pepy.tech/badge/tba-example-oauth-device-authorization-cli/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli/README.md"><img alt="README hits for tba-example-oauth-device-authorization-cli" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Try OAuth device login from a Python CLI against a configured TBA issuer.

## AEO Summary

- Package: `tba-example-oauth-device-authorization-cli`
- Layer: `110-examples`
- Responsibility: Example consumer package showing CLI login against tba_auth device authorization.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli/src/oauth_device_authorization_cli_example/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

For a live flow, register a client for the device authorization grant, substitute its ID and your issuer URL, and follow the browser instructions. The example caches returned tokens locally. Use a dedicated test account and protect the cache file.

## Installation

Install the selected PyPI release of `tba-example-oauth-device-authorization-cli`:

```bash
uv pip install tba-example-oauth-device-authorization-cli
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/110-examples/tba-example-oauth-device-authorization-cli
```

## Quick start

Expect help for `--issuer`, `--client-id`, `--scope`, and `--token-cache`. This command uses the published package and needs no running issuer.

```bash
uvx --from tba-example-oauth-device-authorization-cli==0.1.1.dev2 oauth-device-login login --help
```

For a configured test deployment, replace the example issuer and client ID:

```bash
uvx --from tba-example-oauth-device-authorization-cli==0.1.1.dev2 oauth-device-login login --issuer https://issuer.example --client-id CLIENT_ID
```

The [device login guide](https://github.com/tigrbl/tigrbl_auth/blob/master/docs/examples/python-cli-device-login.md) explains discovery, browser approval, polling, and token storage.

## Usage

The following public-entry-point example belongs to `tba-example-oauth-device-authorization-cli`. Example consumer package showing CLI login against tba_auth device authorization. Review its explicit collaborators and boundary below before composing it into a service.

```python
import oauth_device_authorization_cli_example

print(oauth_device_authorization_cli_example.__name__)
```

## Package Boundary

`tba-example-oauth-device-authorization-cli` belongs to `110-examples` and owns executable integration examples: Example consumer package showing CLI login against tba_auth device authorization.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli/src/oauth_device_authorization_cli_example/__init__.py).

Keep a production service guarantee or release certification in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli/src/oauth_device_authorization_cli_example/__init__.py) for `tba-example-oauth-device-authorization-cli` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-example-oauth-device-authorization-cli` exposes executable integration examples. Inspect the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli/src/oauth_device_authorization_cli_example/__init__.py) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-example-oauth-device-authorization-cli`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`tba-example-oauth-device-authorization-cli` does not take ownership of a production service guarantee or release certification.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

`tba-example-oauth-device-authorization-cli` declares no local runtime dependency and has no direct consumer in the active manifest graph. Browse the [110-examples layer](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/110-examples) for adjacent package responsibilities; adjacency does not imply a dependency.

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/110-examples/tba-example-oauth-device-authorization-cli/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-example-oauth-device-authorization-cli/)

## Governance

`tba-example-oauth-device-authorization-cli` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `110-examples` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

See the [related repository tests](https://github.com/tigrbl/tigrbl_auth/blob/master/tests/examples/test_python_cli_device_login.py) for the implementation scope covered by this example.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [tba-app-backend-public](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/90-backend-apps/tba-app-backend-public#readme) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)
