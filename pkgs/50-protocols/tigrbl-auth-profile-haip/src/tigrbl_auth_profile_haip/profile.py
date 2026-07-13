from dataclasses import dataclass

from tigrbl_auth_protocol_oid4vci import select_version as select_oid4vci_version
from tigrbl_auth_protocol_oid4vp import select_version as select_oid4vp_version

HAIP_CREDENTIAL_FORMATS = frozenset({"dc+sd-jwt", "mso_mdoc"})


@dataclass(frozen=True, slots=True)
class HaipConfiguration:
    credential_formats: frozenset[str]
    oid4vci_version: str = "1.0"
    oid4vp_version: str = "1.0"
    wallet_attestation: bool = True
    key_attestation: bool = True

    def validate(self) -> None:
        select_oid4vci_version(self.oid4vci_version)
        select_oid4vp_version(self.oid4vp_version)
        unsupported = self.credential_formats - HAIP_CREDENTIAL_FORMATS
        if unsupported:
            raise ValueError(
                f"unsupported HAIP credential formats: {sorted(unsupported)}"
            )
        if not self.credential_formats:
            raise ValueError("HAIP requires at least one credential format")


def configure_haip(*, credential_formats: frozenset[str]) -> HaipConfiguration:
    configuration = HaipConfiguration(credential_formats)
    configuration.validate()
    return configuration


__all__ = ["HAIP_CREDENTIAL_FORMATS", "HaipConfiguration", "configure_haip"]
