from tba_runtime_hosted_sign_in_continuation import HostedSignInContinuationRuntime, Resume


def existing_authorization_request(
    runtime: HostedSignInContinuationRuntime[frozenset[str]],
    flow_id: str,
    verified_methods: frozenset[str],
):
    outcome = runtime.resolve(
        flow_id,
        issuer="https://tenant.example.test",
        tenant_id="tenant",
        browser_binding="host-validated-binding",
        assurance=verified_methods,
    )
    if isinstance(outcome, Resume):
        return outcome.request
    return None


assert callable(existing_authorization_request)
