from .versions import VERSION_HISTORY


def require_version(identifier: str) -> None:
    if identifier not in {version.identifier for version in VERSION_HISTORY}:
        raise ValueError(f"unsupported WPT draft: {identifier}")
