"""Default server provider, durable-runtime, capability, and protocol assembly."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_contracts.capabilities import CapabilityDefinition
from tigrbl_identity_contracts.replay import (
    ReplayReservationRequest,
    ReplayReservationResult,
)
from tigrbl_identity_jose.jwt_coder import JWTCoder
from tigrbl_identity_runtime import (
    CapabilityFactory,
    CapabilityRegistry,
    RuntimeCapabilityAssembly,
    build_runtime_capability_assembly,
)
from tigrbl_identity_storage_runtime.ops.replay import check_and_reserve
from tigrbl_protocol_artifact_processing import ProtocolArtifactProcessingCapability
from tigrbl_replay_protection_capability import ReplayProtectionCapability


class DatabaseReplayProvider:
    provider_id = "replay:sql"
    persistence = "durable"

    def __init__(self, db: Any) -> None:
        self._db = db

    async def check_and_reserve(
        self,
        request: ReplayReservationRequest,
        /,
    ) -> ReplayReservationResult:
        return await check_and_reserve({"payload": request, "db": self._db})


def build_server_runtime_assembly(
    settings_obj: object,
) -> RuntimeCapabilityAssembly:
    def providers() -> dict[str, object]:
        return {"token-coder": JWTCoder.default()}

    def storage_runtime(provider_set: dict[str, object]) -> dict[str, object]:
        from tigrbl_identity_server.security.client_registration import (
            build_client_registration_capability,
        )
        from tigrbl_identity_server.security.pushed_authorization import (
            build_pushed_authorization_capability,
        )
        from tigrbl_identity_server.security.token_issuance import (
            build_token_issuance_capability,
        )
        from tigrbl_identity_server.platform_tenant_administration import (
            build_tenant_administration_capability,
        )

        token_coder = provider_set["token-coder"]
        return {
            "client-registration": build_client_registration_capability,
            "pushed-authorization": build_pushed_authorization_capability,
            "replay-provider": DatabaseReplayProvider,
            "tenant-administration": build_tenant_administration_capability,
            "token-issuance": lambda db: build_token_issuance_capability(
                db=db,
                token_coder=token_coder,
            ),
        }

    def capabilities(
        provider_set: dict[str, object],
        storage_set: dict[str, object],
    ) -> CapabilityRegistry:
        from tigrbl_identity_server.security.token_introspection import (
            token_introspection,
        )
        from tigrbl_identity_server.security.token_revocation import token_revocation
        from tigrbl_identity_server.token_exchange_runtime import (
            token_exchange_capability,
        )

        registry = CapabilityRegistry(
            (token_introspection, token_revocation, token_exchange_capability)
        )
        registry.register_factory(
            CapabilityFactory(
                CapabilityDefinition("identity-admin.tenants", "1.0"),
                (
                    "create_tenant",
                    "delete_tenant",
                    "list_tenants",
                    "read_tenant",
                    "update_tenant",
                ),
                storage_set["tenant-administration"],
            )
        )
        registry.register_factory(
            CapabilityFactory(
                CapabilityDefinition("token.issuance", "1.0"),
                ("issue_token_pair", "redeem_refresh_token"),
                storage_set["token-issuance"],
            )
        )
        registry.register_factory(
            CapabilityFactory(
                CapabilityDefinition("oauth.pushed-authorization", "1.0"),
                ("push_authorization_request",),
                storage_set["pushed-authorization"],
            )
        )
        registry.register_factory(
            CapabilityFactory(
                CapabilityDefinition("client.registration", "1.0"),
                (
                    "disable_registration",
                    "get_registration",
                    "register_client",
                    "update_registration",
                ),
                storage_set["client-registration"],
            )
        )
        registry.register_factory(
            CapabilityFactory(
                CapabilityDefinition("security.replay-protection", "1.0"),
                ("check_and_reserve",),
                lambda db: ReplayProtectionCapability(
                    storage_set["replay-provider"](db)
                ),
            )
        )
        registry.register_factory(
            CapabilityFactory(
                CapabilityDefinition("artifact.processing", "1.0"),
                ("decode", "encode", "map_error", "validate"),
                lambda processor: ProtocolArtifactProcessingCapability(processor),
            )
        )
        return registry

    def protocols(registry: CapabilityRegistry):
        from tigrbl_auth_protocol_oauth import capability_report as oauth_report
        from tigrbl_auth_protocol_oidc import capability_report as oidc_report

        return (oauth_report(), oidc_report())

    return build_runtime_capability_assembly(
        build_providers=providers,
        build_storage_runtime=storage_runtime,
        build_capabilities=capabilities,
        build_protocols=protocols,
    )


__all__ = ["DatabaseReplayProvider", "build_server_runtime_assembly"]
