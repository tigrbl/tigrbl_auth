from dataclasses import dataclass
from enum import IntEnum
from typing import Mapping

from .mdoc import Mdoc, parse_mdoc


class DeviceResponseStatus(IntEnum):
    OK = 0
    GENERAL_ERROR = 10
    CBOR_DECODING_ERROR = 11
    CBOR_VALIDATION_ERROR = 12


@dataclass(frozen=True, slots=True)
class DeviceResponse:
    version: str
    documents: tuple[Mdoc, ...]
    status: int
    document_errors: tuple[Mapping[str, int], ...] = ()


def parse_device_response(value: Mapping[str, object]) -> DeviceResponse:
    version, status = value.get("version"), value.get("status")
    if (
        not isinstance(version, str)
        or not isinstance(status, int)
        or isinstance(status, bool)
    ):
        raise ValueError("DeviceResponse requires version and integer status")
    documents = value.get("documents", ())
    if not isinstance(documents, (list, tuple)) or not all(
        isinstance(document, Mapping) for document in documents
    ):
        raise ValueError("documents must be an array of mdocs")
    errors = value.get("documentErrors", ())
    if not isinstance(errors, (list, tuple)) or not all(
        isinstance(error, Mapping) for error in errors
    ):
        raise ValueError("documentErrors must be an array")
    if status == DeviceResponseStatus.OK and not documents:
        raise ValueError("successful DeviceResponse requires at least one document")
    return DeviceResponse(
        version,
        tuple(parse_mdoc(document) for document in documents),
        status,
        tuple(errors),
    )


__all__ = ["DeviceResponse", "DeviceResponseStatus", "parse_device_response"]
