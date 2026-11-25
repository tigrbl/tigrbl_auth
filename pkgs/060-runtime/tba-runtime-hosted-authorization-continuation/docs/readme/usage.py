from tba_runtime_hosted_authorization_continuation import ContinuationRequirements

requirements = ContinuationRequirements(required_methods=frozenset({'otp'}))
assert requirements.required_methods == {'otp'}
