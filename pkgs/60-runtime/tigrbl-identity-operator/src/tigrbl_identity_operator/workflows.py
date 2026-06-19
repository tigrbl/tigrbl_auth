from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping


def _utc_now() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


@dataclass(frozen=True, slots=True)
class BootstrapTenant:
    tenant_id: str
    issuer: str
    display_name: str


@dataclass(frozen=True, slots=True)
class BootstrapJwks:
    tenant_id: str
    kids: tuple[str, ...]
    published: bool = True


@dataclass(frozen=True, slots=True)
class BootstrapServiceIdentity:
    tenant_id: str
    service_id: str
    scopes: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class OperatorState:
    tenants: Mapping[str, BootstrapTenant] = field(default_factory=dict)
    jwks: Mapping[str, BootstrapJwks] = field(default_factory=dict)
    services: Mapping[str, BootstrapServiceIdentity] = field(default_factory=dict)

    def to_json(self) -> str:
        return json.dumps(
            {
                "tenants": {key: asdict(value) for key, value in self.tenants.items()},
                "jwks": {key: asdict(value) for key, value in self.jwks.items()},
                "services": {key: asdict(value) for key, value in self.services.items()},
            },
            separators=(",", ":"),
            sort_keys=True,
        )

    @staticmethod
    def from_json(value: str) -> "OperatorState":
        raw = json.loads(value)
        return OperatorState(
            tenants={key: BootstrapTenant(**item) for key, item in raw.get("tenants", {}).items()},
            jwks={key: BootstrapJwks(tenant_id=item["tenant_id"], kids=tuple(item["kids"]), published=item["published"]) for key, item in raw.get("jwks", {}).items()},
            services={key: BootstrapServiceIdentity(tenant_id=item["tenant_id"], service_id=item["service_id"], scopes=tuple(item["scopes"])) for key, item in raw.get("services", {}).items()},
        )


@dataclass(frozen=True, slots=True)
class ReleaseEvidence:
    package: str
    version: str
    artifact_paths: tuple[str, ...]
    generated_at: str = field(default_factory=_utc_now)


class OperatorWorkflow:
    def __init__(self, state: OperatorState | None = None) -> None:
        self.state = state or OperatorState()

    def bootstrap_tenant(self, *, tenant_id: str, issuer: str, display_name: str) -> BootstrapTenant:
        tenant = BootstrapTenant(tenant_id=tenant_id, issuer=issuer, display_name=display_name)
        self.state = OperatorState(
            tenants={**self.state.tenants, tenant_id: tenant},
            jwks=self.state.jwks,
            services=self.state.services,
        )
        return tenant

    def bootstrap_jwks(self, *, tenant_id: str, kids: tuple[str, ...]) -> BootstrapJwks:
        if tenant_id not in self.state.tenants:
            raise ValueError("JWKS bootstrap requires tenant bootstrap first")
        jwks = BootstrapJwks(tenant_id=tenant_id, kids=tuple(sorted(set(kids))))
        self.state = OperatorState(
            tenants=self.state.tenants,
            jwks={**self.state.jwks, tenant_id: jwks},
            services=self.state.services,
        )
        return jwks

    def bootstrap_service_identity(self, *, tenant_id: str, service_id: str, scopes: tuple[str, ...]) -> BootstrapServiceIdentity:
        if tenant_id not in self.state.tenants:
            raise ValueError("service identity bootstrap requires tenant bootstrap first")
        service = BootstrapServiceIdentity(tenant_id=tenant_id, service_id=service_id, scopes=tuple(sorted(set(scopes))))
        self.state = OperatorState(
            tenants=self.state.tenants,
            jwks=self.state.jwks,
            services={**self.state.services, service_id: service},
        )
        return service

    def package_release_evidence(self, *, package: str, version: str, artifact_paths: tuple[str, ...]) -> ReleaseEvidence:
        if not package or not version or not artifact_paths:
            raise ValueError("package release evidence requires package, version, and artifacts")
        return ReleaseEvidence(package=package, version=version, artifact_paths=tuple(artifact_paths))

    def export_state(self) -> str:
        return self.state.to_json()

    @staticmethod
    def import_state(value: str) -> "OperatorWorkflow":
        return OperatorWorkflow(OperatorState.from_json(value))


__all__ = [
    "BootstrapJwks",
    "BootstrapServiceIdentity",
    "BootstrapTenant",
    "OperatorState",
    "OperatorWorkflow",
    "ReleaseEvidence",
]
