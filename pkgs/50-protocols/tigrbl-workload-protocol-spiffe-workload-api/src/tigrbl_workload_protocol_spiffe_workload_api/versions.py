from dataclasses import dataclass
@dataclass(frozen=True, slots=True)
class WorkloadApiVersion:
    identifier: str
    status: str
    specification_uri: str
CURRENT_VERSION = WorkloadApiVersion("SPIFFE-Workload-API-1.0", "stable", "https://github.com/spiffe/spiffe/blob/main/standards/SPIFFE_Workload_API.md")
VERSION_HISTORY = (CURRENT_VERSION,)