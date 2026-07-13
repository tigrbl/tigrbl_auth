from collections.abc import Mapping


def migrate_document(
    document: Mapping[str, object], *, from_version: str, to_version: str
) -> dict[str, object]:
    if from_version == to_version:
        return dict(document)
    if (from_version, to_version) == (
        "draft-ietf-rats-corim-10",
        "draft-ietf-rats-corim-11",
    ):
        migrated = dict(document)
        migrated.setdefault("profile", "tag:ietf.org,2025:corim")
        return migrated
    raise ValueError(f"unsupported CoRIM migration: {from_version} -> {to_version}")


__all__ = ["migrate_document"]
