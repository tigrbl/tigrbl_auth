from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping

from tigrbl_user_plane_contracts.authz.replay import (
    DecisionStabilityChange,
    DecisionStabilityReport,
    PolicyDeterminismReport,
    PolicyEvaluator,
    PolicyReplayCase,
    PolicyReplayResult,
)


def _normalize(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _normalize(val) for key, val in sorted(value.items(), key=lambda item: str(item[0]))}
    if isinstance(value, tuple):
        return [_normalize(item) for item in value]
    if isinstance(value, list):
        return [_normalize(item) for item in value]
    if isinstance(value, set):
        return [_normalize(item) for item in sorted(value, key=lambda item: repr(item))]
    return value


def canonical_json(value: Any) -> str:
    return json.dumps(_normalize(value), sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def canonical_hash(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def replay_policy_determinism(
    *,
    policy_version: str,
    cases: tuple[PolicyReplayCase, ...],
    evaluator: PolicyEvaluator,
    runs: int = 2,
    schema_version: str = "",
) -> PolicyDeterminismReport:
    if runs < 2:
        raise ValueError("runs must be at least 2")
    results: list[PolicyReplayResult] = []
    failures: list[str] = []
    for case in cases:
        decisions = tuple(dict(evaluator(case.request)) for _ in range(runs))
        decision_hashes = tuple(canonical_hash(decision) for decision in decisions)
        stable = len(set(decision_hashes)) == 1
        if not stable:
            failures.append(f"case {case.case_id!r} produced non-deterministic decisions")
        results.append(
            PolicyReplayResult(
                case_id=case.case_id,
                request_hash=canonical_hash(case.request),
                decision_hashes=decision_hashes,
                stable=stable,
                decisions=decisions,
            )
        )
    return PolicyDeterminismReport(
        passed=not failures,
        policy_version=policy_version,
        schema_version=schema_version,
        results=tuple(results),
        failures=tuple(failures),
    )


def compare_policy_version_decisions(
    *,
    baseline_version: str,
    candidate_version: str,
    cases: tuple[PolicyReplayCase, ...],
    baseline_evaluator: PolicyEvaluator,
    candidate_evaluator: PolicyEvaluator,
    allowed_change_reasons: Mapping[str, str] = {},
    baseline_schema_version: str = "",
    candidate_schema_version: str = "",
) -> DecisionStabilityReport:
    changes: list[DecisionStabilityChange] = []
    failures: list[str] = []
    for case in cases:
        baseline_hash = canonical_hash(baseline_evaluator(case.request))
        candidate_hash = canonical_hash(candidate_evaluator(case.request))
        if baseline_hash == candidate_hash:
            continue
        reason = allowed_change_reasons.get(case.case_id, "")
        attributed = bool(reason and baseline_version != candidate_version)
        if not attributed:
            failures.append(f"case {case.case_id!r} changed without policy-version attribution")
        changes.append(
            DecisionStabilityChange(
                case_id=case.case_id,
                baseline_hash=baseline_hash,
                candidate_hash=candidate_hash,
                attributed=attributed,
                reason=reason,
            )
        )
    return DecisionStabilityReport(
        passed=not failures,
        baseline_version=baseline_version,
        candidate_version=candidate_version,
        baseline_schema_version=baseline_schema_version,
        candidate_schema_version=candidate_schema_version,
        changes=tuple(changes),
        failures=tuple(failures),
    )


__all__ = [
    "DecisionStabilityChange",
    "DecisionStabilityReport",
    "PolicyDeterminismReport",
    "PolicyReplayCase",
    "PolicyReplayResult",
    "canonical_hash",
    "canonical_json",
    "compare_policy_version_decisions",
    "replay_policy_determinism",
]
