from tigrbl_identity_contracts.workloads import SpiffeId


def normalize_spiffe_id(value: str | SpiffeId) -> SpiffeId:
    parsed = SpiffeId.parse(value) if isinstance(value, str) else value
    if parsed.path == "/" or "//" in parsed.path or parsed.path.endswith("/"):
        raise ValueError(
            "SPIFFE workload path must identify a non-root normalized workload"
        )
    return parsed


__all__ = ["normalize_spiffe_id"]
