def validate_endpoint(address: str) -> None:
    if not (address.startswith("unix://") or address.startswith("npipe://")):
        raise ValueError(
            "Workload API endpoint must use an explicitly configured local transport"
        )
