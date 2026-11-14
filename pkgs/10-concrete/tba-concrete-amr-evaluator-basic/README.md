# tba-concrete-amr-evaluator-basic

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-amr-evaluator-basic/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-amr-evaluator-basic/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-amr-evaluator-basic/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/10-concrete"><img alt="Layer: 10 concrete" src="https://img.shields.io/badge/Layer-10%20concrete-0a7f5a"></a>
<a href="https://pypi.org/project/tba-concrete-amr-evaluator-basic/"><img alt="PyPI version for tba-concrete-amr-evaluator-basic" src="https://img.shields.io/pypi/v/tba-concrete-amr-evaluator-basic?label=tba-concrete-amr-evaluator-basic%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-concrete-amr-evaluator-basic"><img alt="Monthly PyPI downloads for tba-concrete-amr-evaluator-basic" src="https://static.pepy.tech/badge/tba-concrete-amr-evaluator-basic/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-amr-evaluator-basic/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Compare required authentication methods with achieved AMR evidence.

## Quick start

Install the version used by this example.

```bash
python -m pip install "tba-concrete-amr-evaluator-basic==0.4.0.dev2"
```

Save the following as `quickstart.py` and run `python quickstart.py`. The assertions should pass.

```python
from tba_concrete_amr_evaluator_basic import BasicAmrEvaluator
from tba_contracts_security_trust import AmrEvaluationRequest

result = BasicAmrEvaluator().evaluate_amr(
    AmrEvaluationRequest(required=("pwd", "otp"), achieved=("pwd",))
)
assert result.satisfied is False
assert result.missing == ("otp",)
```

## When to use it

Use `BasicAmrEvaluator` when the rule is simple set inclusion. It reports missing methods in sorted order. The caller supplies the evidence and decides how to handle a missing factor.

## Verification

Run the example above to check the public API against the installed package. Its assertions describe the expected behavior.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [tba-bases-authenticator](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/05-bases/tba-bases-authenticator#readme) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)
