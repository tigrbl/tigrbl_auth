from __future__ import annotations

from tigrbl_identity_runtime import runner_registry_manifest

from .models import TRANSPORT_REQUIREMENTS, TransportPosture


def build_transport_postures() -> dict[str, TransportPosture]:
    runners = runner_registry_manifest()
    postures: dict[str, TransportPosture] = {}
    for protocol, requirement in TRANSPORT_REQUIREMENTS.items():
        capabilities = set(requirement["capabilities"])
        supported_runners = tuple(
            sorted(
                runner["name"]
                for runner in runners
                if capabilities
                and capabilities
                <= {item["name"] for item in runner.get("capabilities", [])}
            )
        )
        implemented = bool(supported_runners) if capabilities else False
        postures[protocol] = TransportPosture(
            protocol=protocol,
            backend_runtime_support="implemented" if implemented else "absent",
            runtime_enablement=str(requirement["runtime_enablement"]),
            contract_visibility=str(requirement["contract_visibility"]),
            uix_dependency=str(requirement["uix_dependency"]),
            certification_claimable=implemented,
            supported_runners=supported_runners,
            enablement_flags=tuple(requirement["flag_names"]),
        )
    return postures
