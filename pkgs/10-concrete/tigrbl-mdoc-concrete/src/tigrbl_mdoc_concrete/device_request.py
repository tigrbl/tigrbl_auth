from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True, slots=True)
class ItemsRequest:
    doc_type: str
    name_spaces: Mapping[str, Mapping[str, bool]]
    request_info: Mapping[str, object] | None = None


@dataclass(frozen=True, slots=True)
class DocRequest:
    items_request: ItemsRequest
    reader_auth: bytes | None = None


@dataclass(frozen=True, slots=True)
class DeviceRequest:
    version: str
    doc_requests: tuple[DocRequest, ...]


def parse_device_request(value: Mapping[str, object]) -> DeviceRequest:
    version, requests = value.get("version"), value.get("docRequests")
    if not isinstance(version, str) or not isinstance(requests, list):
        raise ValueError("DeviceRequest requires version and docRequests")
    parsed = []
    for request in requests:
        if not isinstance(request, Mapping) or not isinstance(
            request.get("itemsRequest"), Mapping
        ):
            raise ValueError("DocRequest requires itemsRequest")
        items = request["itemsRequest"]
        doc_type, namespaces = items.get("docType"), items.get("nameSpaces")
        if not isinstance(doc_type, str) or not isinstance(namespaces, Mapping):
            raise ValueError("ItemsRequest requires docType and nameSpaces")
        for namespace, elements in namespaces.items():
            if (
                not isinstance(namespace, str)
                or not isinstance(elements, Mapping)
                or any(
                    not isinstance(name, str) or not isinstance(intent, bool)
                    for name, intent in elements.items()
                )
            ):
                raise ValueError(
                    "ItemsRequest namespace entries must map element names to intent-to-retain booleans"
                )
        request_info = items.get("requestInfo")
        if request_info is not None and not isinstance(request_info, Mapping):
            raise ValueError("requestInfo must be an object")
        reader_auth = request.get("readerAuth")
        if reader_auth is not None and not isinstance(reader_auth, bytes):
            raise ValueError("readerAuth must be encoded COSE bytes")
        parsed.append(
            DocRequest(ItemsRequest(doc_type, namespaces, request_info), reader_auth)
        )
    return DeviceRequest(version, tuple(parsed))


__all__ = ["DeviceRequest", "DocRequest", "ItemsRequest", "parse_device_request"]
