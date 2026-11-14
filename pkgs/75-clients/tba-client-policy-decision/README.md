# tba-client-policy-decision

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/75-clients/tba-client-policy-decision/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/75-clients/tba-client-policy-decision/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/75-clients/tba-client-policy-decision/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/75-clients"><img alt="Layer: 75 clients" src="https://img.shields.io/badge/Layer-75%20clients-0a7f5a"></a>
<a href="https://pypi.org/project/tba-client-policy-decision/"><img alt="PyPI version for tba-client-policy-decision" src="https://img.shields.io/pypi/v/tba-client-policy-decision?label=tba-client-policy-decision%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-client-policy-decision"><img alt="Monthly PyPI downloads for tba-client-policy-decision" src="https://static.pepy.tech/badge/tba-client-policy-decision/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/75-clients/tba-client-policy-decision/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Call a policy decision point through a transport you supply.

## Quick start

Install the version used by this example.

```bash
python -m pip install "tba-client-policy-decision==0.4.0.dev3"
```

Save the following as `quickstart.py` and run `python quickstart.py`. The assertions should pass.

```python
from tba_client_policy_decision import PolicyDecisionClient

client = PolicyDecisionClient(request=lambda payload: {"allowed": payload["action"] == "read"})
assert client.decide({"action": "read"}) == {"allowed": True}
assert client.decide({"action": "write"}) == {"allowed": False}
```

## When to use it

Inject a callable that accepts a decision request mapping and returns a result mapping. The adapter owns network authentication, serialization, retries, and error handling. This example uses an in-process stub for one decision.

## Verification

Run the example above to check the public API against the installed package. Its assertions describe the expected behavior.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [tba-middleware-policy-enforcement-asgi](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/85-middleware/tba-middleware-policy-enforcement-asgi#readme) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)
