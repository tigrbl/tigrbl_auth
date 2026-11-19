from __future__ import annotations

from dataclasses import replace
from typing import Any, Mapping
from uuid import uuid4

from tigrbl_identity_core.clock import utc_now_iso
from tigrbl_identity_core.entity_keys import tenant_key

from .models import DeviceIdentity, WorkloadIdentity


class DeviceWorkloadIdentityRegistry:
    def __init__(self) -> None:
        self._devices: dict[str, DeviceIdentity] = {}
        self._workloads: dict[str, WorkloadIdentity] = {}

    @property
    def devices(self) -> Mapping[str, DeviceIdentity]:
        return dict(self._devices)

    @property
    def workloads(self) -> Mapping[str, WorkloadIdentity]:
        return dict(self._workloads)

    def register_device(
        self,
        *,
        device_id: str,
        subject_id: str,
        tenant_id: str,
        credential_posture: str,
        last_ip_country: str | None = None,
    ) -> DeviceIdentity:
        identity = DeviceIdentity(
            device_id=device_id,
            subject_id=subject_id,
            tenant_id=tenant_id,
            credential_posture=credential_posture,
            last_ip_country=last_ip_country,
            created_at=utc_now_iso(),
        )
        self._devices[tenant_key(tenant_id, device_id)] = identity
        return identity

    def revoke_device(self, *, device_id: str, tenant_id: str) -> DeviceIdentity:
        key = tenant_key(tenant_id, device_id)
        identity = self._devices[key]
        updated = replace(identity, revoked=True)
        self._devices[key] = updated
        return updated

    def register_workload(
        self,
        *,
        workload_id: str,
        tenant_id: str,
        trust_domain: str,
        cloud: str,
        namespace: str,
        attestor: str,
    ) -> WorkloadIdentity:
        identity = WorkloadIdentity(
            workload_id=workload_id,
            tenant_id=tenant_id,
            trust_domain=trust_domain,
            cloud=cloud,
            namespace=namespace,
            attestor=attestor,
            credential_id=f"spire://{trust_domain}/{workload_id}/{uuid4().hex}",
            created_at=utc_now_iso(),
        )
        self._workloads[tenant_key(tenant_id, workload_id)] = identity
        return identity

    def rotate_workload_credential(
        self, *, workload_id: str, tenant_id: str
    ) -> WorkloadIdentity:
        key = tenant_key(tenant_id, workload_id)
        identity = self._workloads[key]
        updated = replace(
            identity,
            credential_id=f"spire://{identity.trust_domain}/{workload_id}/{uuid4().hex}",
        )
        self._workloads[key] = updated
        return updated

    def revoke_workload(self, *, workload_id: str, tenant_id: str) -> WorkloadIdentity:
        key = tenant_key(tenant_id, workload_id)
        identity = self._workloads[key]
        updated = replace(identity, revoked=True)
        self._workloads[key] = updated
        return updated

    def summary(self) -> dict[str, Any]:
        return {
            "device_count": len(self._devices),
            "active_device_count": sum(
                not device.revoked for device in self._devices.values()
            ),
            "workload_count": len(self._workloads),
            "active_workload_count": sum(
                not workload.revoked for workload in self._workloads.values()
            ),
            "trust_domains": sorted(
                {workload.trust_domain for workload in self._workloads.values()}
            ),
        }
