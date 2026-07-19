def validate_endpoint(address: str) -> None:
    if not (address.startswith("unix://") or address.startswith("npipe://")): raise ValueError("Broker API requires a local Broker Endpoint")