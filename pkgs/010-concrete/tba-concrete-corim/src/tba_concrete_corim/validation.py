from .corim import CorimTag


def validate_corim_tag(tag: CorimTag) -> None:
    identities = [
        item.tag_identity if hasattr(item, "tag_identity") else item.tag_id
        for item in tag.tags
    ]
    if len(identities) != len(set(identities)):
        raise ValueError("embedded CoRIM tag identities must be unique")


__all__ = ["validate_corim_tag"]
