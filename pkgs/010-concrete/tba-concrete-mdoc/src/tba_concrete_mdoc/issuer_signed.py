from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True, slots=True)
class IssuerSignedItem:
    digest_id: int
    random: bytes
    element_identifier: str
    element_value: object


@dataclass(frozen=True, slots=True)
class IssuerSigned:
    name_spaces: Mapping[str, tuple[IssuerSignedItem, ...]]
    issuer_auth: bytes


def parse_issuer_signed(value: Mapping[str, object]) -> IssuerSigned:
    namespaces, issuer_auth = value.get("nameSpaces", {}), value.get("issuerAuth")
    if not isinstance(namespaces, Mapping) or not isinstance(issuer_auth, bytes):
        raise ValueError("IssuerSigned requires nameSpaces and byte-valued issuerAuth")
    parsed = {}
    for namespace, items in namespaces.items():
        if not isinstance(namespace, str) or not isinstance(items, (list, tuple)):
            raise ValueError("mdoc namespaces must map strings to arrays")
        parsed_items = []
        for item in items:
            if not isinstance(item, Mapping):
                raise ValueError("IssuerSignedItem must be an object")
            digest_id, random, identifier = (
                item.get("digestID"),
                item.get("random"),
                item.get("elementIdentifier"),
            )
            if (
                not isinstance(digest_id, int)
                or isinstance(digest_id, bool)
                or digest_id < 0
            ):
                raise ValueError("IssuerSignedItem digestID must be non-negative")
            if (
                not isinstance(random, bytes)
                or not random
                or not isinstance(identifier, str)
                or not identifier
            ):
                raise ValueError(
                    "IssuerSignedItem requires random and elementIdentifier"
                )
            if "elementValue" not in item:
                raise ValueError("IssuerSignedItem requires elementValue")
            parsed_items.append(
                IssuerSignedItem(digest_id, random, identifier, item["elementValue"])
            )
        if len({item.digest_id for item in parsed_items}) != len(parsed_items):
            raise ValueError("digestID values must be unique within a namespace")
        parsed[namespace] = tuple(parsed_items)
    return IssuerSigned(parsed, issuer_auth)


__all__ = ["IssuerSigned", "IssuerSignedItem", "parse_issuer_signed"]
