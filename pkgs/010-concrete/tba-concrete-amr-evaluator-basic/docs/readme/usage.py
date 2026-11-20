from tba_concrete_amr_evaluator_basic import BasicAmrEvaluator
from tba_contracts_security_trust import AmrEvaluationRequest

result = BasicAmrEvaluator().evaluate_amr(
    AmrEvaluationRequest(required=("pwd", "otp"), achieved=("pwd",))
)
assert result.satisfied is False
assert result.missing == ("otp",)
