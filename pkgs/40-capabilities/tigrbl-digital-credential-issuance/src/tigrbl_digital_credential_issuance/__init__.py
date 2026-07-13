from tigrbl_capability import Capability
from tigrbl_identity_contracts.capabilities import CapabilityMetadata
from tigrbl_identity_contracts.digital_credentials import (
    CredentialConfiguration,
    CredentialIssuanceRequest,
    CredentialIssuanceResult,
    CredentialIssuerPort,
    CredentialOffer,
    WalletAttestationVerifierPort,
)


class DigitalCredentialIssuanceCapability(Capability):
    def __init__(
        self,
        issuer: CredentialIssuerPort,
        wallet_verifier: WalletAttestationVerifierPort | None = None,
    ):
        dependencies = [type(issuer).__name__]
        if wallet_verifier is not None:
            dependencies.append(type(wallet_verifier).__name__)
        super().__init__(
            CapabilityMetadata(
                capability_id="digital-credential.issuance",
                version="1.0",
                operations=("register_configuration", "offer", "issue"),
                guarantees=("known-configuration-only", "wallet-policy-before-issuance"),
                optional_features=("wallet-attestation",),
                dependencies=tuple(dependencies),
            )
        )
        self._issuer = issuer
        self._wallet_verifier = wallet_verifier
        self._configurations: dict[str, CredentialConfiguration] = {}
        self.bind("register_configuration", self.register_configuration)
        self.bind("offer", self.offer)
        self.bind("issue", self.issue, delegated=True)

    def register_configuration(self, configuration: CredentialConfiguration) -> None:
        if configuration.identifier in self._configurations:
            raise ValueError("duplicate credential configuration")
        self._configurations[configuration.identifier] = configuration

    def offer(self, issuer: str, configuration_ids: tuple[str, ...]) -> CredentialOffer:
        if not configuration_ids or any(
            identifier not in self._configurations for identifier in configuration_ids
        ):
            raise ValueError("credential offer references unknown configurations")
        return CredentialOffer(issuer, configuration_ids)

    def issue(
        self,
        request: CredentialIssuanceRequest,
        *,
        wallet_attestation: str | bytes | None = None,
        require_wallet_attestation: bool = False,
    ) -> CredentialIssuanceResult:
        if request.configuration_id not in self._configurations:
            raise LookupError(request.configuration_id)
        if require_wallet_attestation:
            if self._wallet_verifier is None or wallet_attestation is None:
                raise PermissionError("wallet attestation is required")
            if not self._wallet_verifier.verify_wallet_attestation(wallet_attestation):
                raise PermissionError("wallet attestation verification failed")
        return self._issuer.issue(request)


__all__ = ["DigitalCredentialIssuanceCapability"]
