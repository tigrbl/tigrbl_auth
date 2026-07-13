"""Provider-neutral key contracts for security/trust components."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Sequence

from .types import Alg, Artifact, ArtifactFormat, KeyRefLike


class KeyKind(str, Enum):
    """Structural key family."""

    SYMMETRIC = "symmetric"
    ASYMMETRIC = "asymmetric"
    KEM = "kem"
    HMAC = "hmac"
    PASSWORD_DERIVED = "password_derived"
    EXTERNAL = "external"


class KeyUsage(str, Enum):
    """Named usage recipe for default and maximum permitted operations."""

    KEK = "kek"
    DEK = "dek"
    SIGNING = "signing"
    VERIFICATION = "verification"
    KEM_PUBLIC = "kem_public"
    KEM_PRIVATE = "kem_private"
    TRANSPORT = "transport"
    ATTESTATION = "attestation"
    IDENTITY = "identity"


class KeyOperation(str, Enum):
    """Permitted cryptographic operation names."""

    SIGN = "sign"
    VERIFY = "verify"
    ENCRYPT = "encrypt"
    DECRYPT = "decrypt"
    WRAP_KEY = "wrap_key"
    UNWRAP_KEY = "unwrap_key"
    DERIVE_KEY = "derive_key"
    DERIVE_BITS = "derive_bits"
    ENCAPSULATE = "encapsulate"
    DECAPSULATE = "decapsulate"
    ATTEST = "attest"
    VERIFY_ATTESTATION = "verify_attestation"
    CERTIFY_KEY = "certify_key"
    EXPORT_PUBLIC = "export_public"
    IMPORT_PUBLIC = "import_public"
    ROTATE = "rotate"
    RETIRE = "retire"
    DESTROY = "destroy"


@dataclass(frozen=True)
class KeyUsageSpec:
    """Concrete usage recipe for durable keys."""

    usage: KeyUsage
    allowed_kinds: tuple[KeyKind, ...]
    default_ops: tuple[KeyOperation, ...]
    max_ops: tuple[KeyOperation, ...]


def _unique_ops(values: Sequence[KeyOperation]) -> tuple[KeyOperation, ...]:
    seen: set[KeyOperation] = set()
    result: list[KeyOperation] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return tuple(result)


def coerce_key_kind(value: KeyKind | str) -> KeyKind:
    """Normalize a key kind enum or value string."""

    if isinstance(value, KeyKind):
        return value
    return KeyKind(str(value))


def coerce_key_usage(value: KeyUsage | str) -> KeyUsage:
    """Normalize a key usage enum or value string."""

    if isinstance(value, KeyUsage):
        return value
    return KeyUsage(str(value))


def coerce_key_operation(value: KeyOperation | str) -> KeyOperation:
    """Normalize a key operation enum or value string."""

    if isinstance(value, KeyOperation):
        return value
    return KeyOperation(str(value))


def normalize_key_usages(
    values: Sequence[KeyUsage | str] | KeyUsage | str | None,
) -> tuple[KeyUsage, ...]:
    """Normalize usage values while preserving first-seen order."""

    if values is None or values == "" or values is False:
        return ()
    if isinstance(values, (KeyUsage, str)):
        items: Sequence[KeyUsage | str] = (values,)
    else:
        items = values
    seen: set[KeyUsage] = set()
    result: list[KeyUsage] = []
    for item in items:
        if item in {None, ""}:  # type: ignore[comparison-overlap]
            continue
        usage = coerce_key_usage(item)
        if usage not in seen:
            seen.add(usage)
            result.append(usage)
    return tuple(result)


def normalize_key_operations(
    values: Sequence[KeyOperation | str] | KeyOperation | str | None,
) -> tuple[KeyOperation, ...]:
    """Normalize operation values while preserving first-seen order."""

    if values is None or values == "" or values is False:
        return ()
    if isinstance(values, (KeyOperation, str)):
        items: Sequence[KeyOperation | str] = (values,)
    else:
        items = values
    result: list[KeyOperation] = []
    for item in items:
        if item in {None, ""}:  # type: ignore[comparison-overlap]
            continue
        result.append(coerce_key_operation(item))
    return _unique_ops(result)


KEY_USAGE_SPECS: Mapping[KeyUsage, KeyUsageSpec] = {
    KeyUsage.DEK: KeyUsageSpec(
        usage=KeyUsage.DEK,
        allowed_kinds=(KeyKind.SYMMETRIC, KeyKind.EXTERNAL),
        default_ops=(KeyOperation.ENCRYPT, KeyOperation.DECRYPT),
        max_ops=(KeyOperation.ENCRYPT, KeyOperation.DECRYPT),
    ),
    KeyUsage.KEK: KeyUsageSpec(
        usage=KeyUsage.KEK,
        allowed_kinds=(KeyKind.SYMMETRIC, KeyKind.EXTERNAL),
        default_ops=(KeyOperation.WRAP_KEY, KeyOperation.UNWRAP_KEY),
        max_ops=(KeyOperation.WRAP_KEY, KeyOperation.UNWRAP_KEY),
    ),
    KeyUsage.SIGNING: KeyUsageSpec(
        usage=KeyUsage.SIGNING,
        allowed_kinds=(KeyKind.ASYMMETRIC, KeyKind.HMAC, KeyKind.EXTERNAL),
        default_ops=(KeyOperation.SIGN, KeyOperation.EXPORT_PUBLIC),
        max_ops=(KeyOperation.SIGN, KeyOperation.EXPORT_PUBLIC),
    ),
    KeyUsage.VERIFICATION: KeyUsageSpec(
        usage=KeyUsage.VERIFICATION,
        allowed_kinds=(KeyKind.ASYMMETRIC, KeyKind.HMAC, KeyKind.EXTERNAL),
        default_ops=(KeyOperation.VERIFY, KeyOperation.EXPORT_PUBLIC),
        max_ops=(KeyOperation.VERIFY, KeyOperation.EXPORT_PUBLIC),
    ),
    KeyUsage.KEM_PUBLIC: KeyUsageSpec(
        usage=KeyUsage.KEM_PUBLIC,
        allowed_kinds=(KeyKind.KEM, KeyKind.EXTERNAL),
        default_ops=(KeyOperation.ENCAPSULATE, KeyOperation.EXPORT_PUBLIC),
        max_ops=(KeyOperation.ENCAPSULATE, KeyOperation.EXPORT_PUBLIC),
    ),
    KeyUsage.KEM_PRIVATE: KeyUsageSpec(
        usage=KeyUsage.KEM_PRIVATE,
        allowed_kinds=(KeyKind.KEM, KeyKind.EXTERNAL),
        default_ops=(KeyOperation.DECAPSULATE, KeyOperation.EXPORT_PUBLIC),
        max_ops=(KeyOperation.DECAPSULATE, KeyOperation.EXPORT_PUBLIC),
    ),
    KeyUsage.TRANSPORT: KeyUsageSpec(
        usage=KeyUsage.TRANSPORT,
        allowed_kinds=(
            KeyKind.SYMMETRIC,
            KeyKind.ASYMMETRIC,
            KeyKind.KEM,
            KeyKind.EXTERNAL,
        ),
        default_ops=(KeyOperation.ENCRYPT, KeyOperation.DECRYPT),
        max_ops=(
            KeyOperation.ENCRYPT,
            KeyOperation.DECRYPT,
            KeyOperation.ENCAPSULATE,
            KeyOperation.DECAPSULATE,
        ),
    ),
    KeyUsage.ATTESTATION: KeyUsageSpec(
        usage=KeyUsage.ATTESTATION,
        allowed_kinds=(KeyKind.ASYMMETRIC, KeyKind.EXTERNAL),
        default_ops=(
            KeyOperation.ATTEST,
            KeyOperation.VERIFY_ATTESTATION,
            KeyOperation.EXPORT_PUBLIC,
        ),
        max_ops=(
            KeyOperation.ATTEST,
            KeyOperation.VERIFY_ATTESTATION,
            KeyOperation.EXPORT_PUBLIC,
        ),
    ),
    KeyUsage.IDENTITY: KeyUsageSpec(
        usage=KeyUsage.IDENTITY,
        allowed_kinds=(KeyKind.ASYMMETRIC, KeyKind.EXTERNAL),
        default_ops=(
            KeyOperation.SIGN,
            KeyOperation.VERIFY,
            KeyOperation.EXPORT_PUBLIC,
        ),
        max_ops=(KeyOperation.SIGN, KeyOperation.VERIFY, KeyOperation.EXPORT_PUBLIC),
    ),
}


def key_usage_spec(usage: KeyUsage | str) -> KeyUsageSpec:
    """Return the concrete usage recipe for a usage enum or value."""

    return KEY_USAGE_SPECS[coerce_key_usage(usage)]


def default_key_operations(
    usages: Sequence[KeyUsage | str] | KeyUsage | str | None,
) -> tuple[KeyOperation, ...]:
    """Return the union of default operations for the supplied usages."""

    operations: list[KeyOperation] = []
    for usage in normalize_key_usages(usages):
        operations.extend(key_usage_spec(usage).default_ops)
    return _unique_ops(operations)


def maximum_key_operations(
    usages: Sequence[KeyUsage | str] | KeyUsage | str | None,
) -> tuple[KeyOperation, ...]:
    """Return the union of maximum operations for the supplied usages."""

    operations: list[KeyOperation] = []
    for usage in normalize_key_usages(usages):
        operations.extend(key_usage_spec(usage).max_ops)
    return _unique_ops(operations)


def resolve_key_allowed_operations(
    *,
    kind: KeyKind | str,
    usages: Sequence[KeyUsage | str] | KeyUsage | str | None,
    allowed_ops: Sequence[KeyOperation | str] | KeyOperation | str | None = None,
) -> tuple[KeyOperation, ...]:
    """Default or validate permitted operations for a key kind and usage set."""

    normalized_kind = coerce_key_kind(kind)
    normalized_usages = normalize_key_usages(usages)
    for usage in normalized_usages:
        spec = key_usage_spec(usage)
        if normalized_kind not in spec.allowed_kinds:
            allowed = ", ".join(kind.value for kind in spec.allowed_kinds)
            raise ValueError(
                f"key usage {usage.value!r} does not allow key kind {normalized_kind.value!r}; allowed: {allowed}"
            )

    if allowed_ops is None:
        return default_key_operations(normalized_usages)

    normalized_ops = normalize_key_operations(allowed_ops)
    if not normalized_usages:
        return normalized_ops

    max_ops = set(maximum_key_operations(normalized_usages))
    illegal = [
        operation.value for operation in normalized_ops if operation not in max_ops
    ]
    if illegal:
        allowed = ", ".join(
            operation.value for operation in maximum_key_operations(normalized_usages)
        )
        raise ValueError(
            f"key operations exceed usage maximum: {', '.join(illegal)}; allowed: {allowed}"
        )
    return normalized_ops



from . import _key_requests
from ._key_requests import *  # noqa: F401,F403

__all__ = _key_requests.__all__

