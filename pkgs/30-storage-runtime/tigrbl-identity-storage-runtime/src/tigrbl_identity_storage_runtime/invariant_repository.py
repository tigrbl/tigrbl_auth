"""Storage-runtime authorization invariant repository composition."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any, Callable

from tigrbl_identity_contracts.invariants import (
    AuthorizationInvariant as AuthorizationInvariantContract,
    InvariantEvaluation as InvariantEvaluationContract,
    InvariantViolation as InvariantViolationContract,
    InvariantSeverity,
    VerificationMethod,
)
from tigrbl_identity_core.clock import utc_now_iso
from tigrbl_identity_storage.tables import (
    AuthorizationInvariant,
    InvariantEvaluation,
    InvariantViolation,
)


def _items(result: Any) -> tuple[Any, ...]:
    if isinstance(result, Mapping) and isinstance(result.get("items"), list):
        result = result["items"]
    elif hasattr(result, "items") and isinstance(getattr(result, "items"), list):
        result = result.items
    if isinstance(result, tuple):
        return result
    if isinstance(result, list):
        return tuple(result)
    if result is None:
        return ()
    return (result,)


def _row_value(row: Any, key: str, default: Any = None) -> Any:
    if isinstance(row, Mapping):
        return row.get(key, default)
    return getattr(row, key, default)


def _list_payload(values: Iterable[str]) -> dict[str, list[str]]:
    return {"items": sorted({str(value).strip() for value in values if str(value).strip()})}


def _list_from_payload(value: Any) -> tuple[str, ...]:
    if isinstance(value, Mapping):
        value = value.get("items", ())
    return tuple(str(item) for item in (value or ()))


def _invariant_contract(row: Any) -> AuthorizationInvariantContract:
    return AuthorizationInvariantContract(
        invariant_id=str(_row_value(row, "invariant_id")),
        title=str(_row_value(row, "title")),
        property_family=str(_row_value(row, "property_family")),
        statement=str(_row_value(row, "statement")),
        verification_method=VerificationMethod(str(_row_value(row, "verification_method"))),
        severity=InvariantSeverity(str(_row_value(row, "severity", "error"))),
        enabled=bool(_row_value(row, "enabled", True)),
        feature_ids=_list_from_payload(_row_value(row, "feature_ids", {})),
        spec_ids=_list_from_payload(_row_value(row, "spec_ids", {})),
        tags=_list_from_payload(_row_value(row, "tags", {})),
    )


def _evaluation_contract(row: Any) -> InvariantEvaluationContract:
    return InvariantEvaluationContract(
        invariant_id=str(_row_value(row, "invariant_id")),
        passed=bool(_row_value(row, "passed")),
        message=str(_row_value(row, "message")),
        evaluated_at=str(_row_value(row, "evaluated_at")),
        evidence=dict(_row_value(row, "evidence", {}) or {}),
    )


class StorageInvariantRepository:
    """Invariant registry behavior backed by identity storage table handlers."""

    def __init__(self, db: Any) -> None:
        self.db = db

    async def invariants(self) -> Mapping[str, AuthorizationInvariantContract]:
        rows = _items(await AuthorizationInvariant.handlers.list.core({"payload": {}, "db": self.db}))
        return {row.invariant_id: row for row in (_invariant_contract(item) for item in rows)}

    async def register(self, invariant: AuthorizationInvariantContract) -> AuthorizationInvariantContract:
        if invariant.invariant_id in await self.invariants():
            raise ValueError(f"duplicate invariant {invariant.invariant_id!r}")
        row = await AuthorizationInvariant.handlers.create.core(
            {
                "payload": {
                    "invariant_id": invariant.invariant_id,
                    "title": invariant.title,
                    "property_family": invariant.property_family,
                    "statement": invariant.statement,
                    "verification_method": invariant.verification_method.value,
                    "severity": invariant.severity.value,
                    "enabled": invariant.enabled,
                    "feature_ids": _list_payload(invariant.feature_ids),
                    "spec_ids": _list_payload(invariant.spec_ids),
                    "tags": _list_payload(invariant.tags),
                },
                "db": self.db,
            }
        )
        return _invariant_contract(row)

    async def get(self, invariant_id: str) -> AuthorizationInvariantContract:
        row = (await self.invariants()).get(invariant_id)
        if row is None:
            raise KeyError(f"unknown invariant {invariant_id!r}")
        return row

    async def list(
        self,
        *,
        property_family: str | None = None,
        enabled_only: bool = False,
        tags: Iterable[str] = (),
    ) -> tuple[AuthorizationInvariantContract, ...]:
        rows = []
        required_tags = set(tags)
        for invariant in (await self.invariants()).values():
            if property_family is not None and invariant.property_family != property_family:
                continue
            if enabled_only and not invariant.enabled:
                continue
            if required_tags and not required_tags.issubset(set(invariant.tags)):
                continue
            rows.append(invariant)
        return tuple(sorted(rows, key=lambda item: item.invariant_id))

    async def evaluate(
        self,
        invariant_id: str,
        evaluator: Callable[[AuthorizationInvariantContract], bool | InvariantEvaluationContract],
    ) -> InvariantEvaluationContract:
        invariant = await self.get(invariant_id)
        result = evaluator(invariant)
        if isinstance(result, InvariantEvaluationContract):
            if result.invariant_id != invariant_id:
                raise ValueError("evaluation invariant_id mismatch")
            evaluation = result
        else:
            passed = bool(result)
            evaluation = InvariantEvaluationContract(
                invariant_id=invariant_id,
                passed=passed,
                message="passed" if passed else "failed",
                evaluated_at=utc_now_iso(),
            )
        row = await InvariantEvaluation.handlers.create.core(
            {
                "payload": {
                    "invariant_id": evaluation.invariant_id,
                    "passed": evaluation.passed,
                    "message": evaluation.message,
                    "evaluated_at": evaluation.evaluated_at,
                    "evidence": dict(evaluation.evidence),
                },
                "db": self.db,
            }
        )
        return _evaluation_contract(row)

    async def violations(
        self, evaluations: Iterable[InvariantEvaluationContract]
    ) -> tuple[InvariantViolationContract, ...]:
        rows: list[InvariantViolationContract] = []
        invariants = await self.invariants()
        for evaluation in evaluations:
            if evaluation.passed:
                continue
            invariant = invariants.get(evaluation.invariant_id)
            severity = invariant.severity if invariant is not None else InvariantSeverity.ERROR
            violation = InvariantViolationContract(
                invariant_id=evaluation.invariant_id,
                severity=severity,
                message=evaluation.message,
                evidence=evaluation.evidence,
            )
            await InvariantViolation.handlers.create.core(
                {
                    "payload": {
                        "invariant_id": violation.invariant_id,
                        "severity": violation.severity.value,
                        "message": violation.message,
                        "evidence": dict(violation.evidence),
                    },
                    "db": self.db,
                }
            )
            rows.append(violation)
        return tuple(rows)


def create_storage_invariant_repository(db: Any) -> StorageInvariantRepository:
    return StorageInvariantRepository(db)


__all__ = ["StorageInvariantRepository", "create_storage_invariant_repository"]
