"""Resolve workload credentials from authenticated enrollment principals."""

from collections.abc import Awaitable, Callable
from typing import TypeAlias

from tba_protocol_workload_wimse_identifier import WorkloadIdentifier

ResolveWorkloadIdentity: TypeAlias = Callable[[str], Awaitable[str | None]]


async def resolve_enrolled_identity(
    principal: str, trust_domain: str, resolver: ResolveWorkloadIdentity
) -> WorkloadIdentifier:
    if not principal:
        raise PermissionError("workload authentication is required")
    value = await resolver(principal)
    if not value:
        raise PermissionError("workload is not enrolled")
    identity = WorkloadIdentifier.parse(value)
    if identity.trust_domain != trust_domain:
        raise PermissionError("workload belongs to another trust domain")
    return identity
