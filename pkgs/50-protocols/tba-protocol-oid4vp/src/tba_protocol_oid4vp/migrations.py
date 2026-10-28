from collections.abc import Mapping


def migrate_request(
    payload: Mapping[str, object], from_version: str, to_version: str = "1.0"
) -> dict[str, object]:
    result = dict(payload)
    if from_version == to_version:
        return result
    if from_version == "draft-25" and to_version == "1.0":
        return result
    if from_version == "draft-20" and to_version == "1.0":
        if "presentation_definition" in result:
            raise ValueError(
                "Presentation Exchange cannot be losslessly migrated to DCQL without an ecosystem mapping"
            )
        return result
    raise ValueError(f"no OID4VP migration path from {from_version} to {to_version}")


__all__ = ["migrate_request"]
