# tba-client-policy-decision

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/75-clients/tba-client-policy-decision/pyproject.toml"><img alt="Checkout: 0.4.0.dev5" src="https://img.shields.io/badge/Checkout-0.4.0.dev5-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/75-clients/tba-client-policy-decision/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-client-policy-decision%3D%3D0.4.0.dev5/pkgs/75-clients/tba-client-policy-decision/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-client-policy-decision%3D%3D0.4.0.dev5/pkgs/75-clients/tba-client-policy-decision/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/75-clients"><img alt="Layer: 75 clients" src="https://img.shields.io/badge/Layer-75%20clients-0a7f5a"></a>
<a href="https://pypi.org/project/tba-client-policy-decision/"><img alt="PyPI version for tba-client-policy-decision" src="https://img.shields.io/pypi/v/tba-client-policy-decision?label=tba-client-policy-decision%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-client-policy-decision"><img alt="Monthly PyPI downloads for tba-client-policy-decision" src="https://static.pepy.tech/badge/tba-client-policy-decision/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/75-clients/tba-client-policy-decision/README.md"><img alt="README hits for tba-client-policy-decision" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/75-clients/tba-client-policy-decision/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/75-clients/tba-client-policy-decision/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Call a policy decision point through a transport you supply.

## AEO Summary

- Package: `tba-client-policy-decision`
- Layer: `75-clients`
- Responsibility: Typed client for platform authorization decisions.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/75-clients/tba-client-policy-decision/src/tba_client_policy_decision/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Inject a callable that accepts a decision request mapping and returns a result mapping. The adapter owns network authentication, serialization, retries, and error handling. This example uses an in-process stub for one decision.

## Installation

Install the selected PyPI release of `tba-client-policy-decision`:

```bash
uv pip install tba-client-policy-decision
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/75-clients/tba-client-policy-decision
```

## Quick start

Install the version used by this example.

```bash
python -m pip install "tba-client-policy-decision==0.4.0.dev5"
```

Save the following as `quickstart.py` and run `python quickstart.py`. The assertions should pass.

```python
from tba_client_policy_decision import PolicyDecisionClient

client = PolicyDecisionClient(request=lambda payload: {"allowed": payload["action"] == "read"})
assert client.decide({"action": "read"}) == {"allowed": True}
assert client.decide({"action": "write"}) == {"allowed": False}
```

## Usage

The following public-entry-point example belongs to `tba-client-policy-decision`. Typed client for platform authorization decisions. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_client_policy_decision import PolicyDecisionClient

client = PolicyDecisionClient(request=lambda payload: {"allowed": payload["action"] == "read"})
assert client.decide({"action": "read"}) == {"allowed": True}
assert client.decide({"action": "write"}) == {"allowed": False}
```

## Package Boundary

`tba-client-policy-decision` belongs to `75-clients` and owns relying-party and client integration: Typed client for platform authorization decisions.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/75-clients/tba-client-policy-decision/src/tba_client_policy_decision/__init__.py). Public exports include `PolicyDecisionClient`.

Keep authority-side policy decisions or server-owned persistence in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/75-clients/tba-client-policy-decision/src/tba_client_policy_decision/__init__.py) for `tba-client-policy-decision` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-client-policy-decision` exposes relying-party and client integration. Public operations found in its source:

- `PolicyDecisionClient.decide` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/75-clients/tba-client-policy-decision/src/tba_client_policy_decision/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-client-policy-decision`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-middleware-policy-enforcement-asgi](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/85-middleware/tba-middleware-policy-enforcement-asgi/README.md).

## Non-goals

`tba-client-policy-decision` does not take ownership of authority-side policy decisions or server-owned persistence.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-contracts-authorization](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-authorization/README.md)

Direct downstream consumers:

- [tba-middleware-policy-enforcement-asgi](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/85-middleware/tba-middleware-policy-enforcement-asgi/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/75-clients/tba-client-policy-decision)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/75-clients/tba-client-policy-decision/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/75-clients/tba-client-policy-decision/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/75-clients/tba-client-policy-decision/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-client-policy-decision/)

## Governance

`tba-client-policy-decision` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `75-clients` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

Run the example above to check the public API against the installed package. Its assertions describe the expected behavior.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [tba-middleware-policy-enforcement-asgi](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/85-middleware/tba-middleware-policy-enforcement-asgi#readme) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)
