from tigrbl_auth.uix import SAFE_MUTATION_METHODS, SafeMutationRequest, execute_safe_mutation


def test_safe_mutations_require_confirmation_before_execution():
    for action in SAFE_MUTATION_METHODS:
        result = execute_safe_mutation(SafeMutationRequest(action=action, target_id="target-1"))

        assert result.status == "confirmation_required"
        assert result.audit_event["outcome"] == "blocked"
        assert result.required_method == SAFE_MUTATION_METHODS[action]


def test_safe_mutations_report_failure_and_expose_audit_outcome():
    failed = execute_safe_mutation(
        SafeMutationRequest(
            action="revoke-session",
            target_id="sess-1",
            confirmed=True,
            confirmation_text="revoke-session:sess-1",
        ),
        executor=lambda _request: {"ok": False, "error": "upstream unavailable"},
    )
    succeeded = execute_safe_mutation(
        SafeMutationRequest(
            action="rotate-key",
            target_id="kid-1",
            confirmed=True,
            confirmation_text="rotate-key:kid-1",
        )
    )

    assert failed.status == "failed"
    assert failed.error == "upstream unavailable"
    assert failed.audit_event["outcome"] == "failed"
    assert succeeded.status == "executed"
    assert succeeded.audit_event["outcome"] == "executed"
