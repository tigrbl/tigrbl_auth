from abc import ABC

from tigrbl_public_key_authentication_contracts import (
    PublicKeyCredentialSource,
)


class PublicKeyCredentialResolverBase(ABC):
    async def find_by_external_id(
        self, tenant_id: str, rp_id: str, external_id: bytes, /
    ) -> PublicKeyCredentialSource | None:
        raise NotImplementedError


__all__ = ["PublicKeyCredentialResolverBase"]
