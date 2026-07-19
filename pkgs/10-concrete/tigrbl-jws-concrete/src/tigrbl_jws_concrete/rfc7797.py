from typing import Mapping

def validate_unencoded_payload_headers(headers: Mapping[str, object]) -> None:
    if headers.get("b64", True) is False:
        critical = headers.get("crit")
        if not isinstance(critical, list) or "b64" not in critical:
            raise ValueError("RFC 7797 b64=false requires protected crit containing b64")