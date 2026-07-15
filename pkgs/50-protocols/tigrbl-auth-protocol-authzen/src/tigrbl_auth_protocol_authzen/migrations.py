from collections.abc import Mapping


def migrate_evaluation(
    payload: Mapping[str, object], from_version: str, to_version: str = "1.0"
) -> dict[str, object]:
    result = dict(payload)
    if from_version == to_version:
        return result
    if (
        from_version
        in {
            "draft-00",
            "draft-01",
            "implementers-draft-1",
            "draft-02",
            "draft-03",
            "draft-04",
            "draft-05",
        }
        and to_version == "1.0"
    ):
        result.setdefault("context", {})
        return result
    raise ValueError(f"no AuthZEN migration path from {from_version} to {to_version}")


__all__ = ["migrate_evaluation"]
