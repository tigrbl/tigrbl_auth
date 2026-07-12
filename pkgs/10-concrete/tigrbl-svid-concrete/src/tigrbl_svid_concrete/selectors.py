from collections.abc import Iterable

from tigrbl_identity_contracts.workloads import WorkloadSelector


def normalize_selectors(
    selectors: Iterable[WorkloadSelector],
) -> tuple[WorkloadSelector, ...]:
    normalized = tuple(
        sorted(set(selectors), key=lambda item: (item.selector_type, item.value))
    )
    if not normalized or any(
        not item.selector_type or not item.value for item in normalized
    ):
        raise ValueError("workload selectors must be non-empty")
    return normalized


__all__ = ["normalize_selectors"]
