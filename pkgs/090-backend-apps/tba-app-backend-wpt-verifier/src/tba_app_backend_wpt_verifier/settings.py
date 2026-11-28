"""Deployment-selected WIT trust, recipient identity and required token bindings."""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from tba_profile_workload_proof_wimse_wpt import normalize_wpt_audience


@dataclass(frozen=True, slots=True)
class WptVerifierSettings:
    audience: str
    trust_by_domain: Mapping[str, Sequence[Mapping[str, object]]]
    required_token_headers: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "audience", normalize_wpt_audience(self.audience))
