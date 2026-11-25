from datetime import timedelta

from tba_runtime_mfa_lifecycle import AssuranceRequirement

requirement = AssuranceRequirement(frozenset({'pwd', 'otp'}), timedelta(minutes=5))
assert requirement.required_methods == {'pwd', 'otp'}
