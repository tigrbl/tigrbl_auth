def require_version(identifier: str) -> None:
    if identifier != "draft-ietf-wimse-wpt-01": raise ValueError(f"unsupported WPT draft: {identifier}")
