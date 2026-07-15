"""Composable digital-credential issuance over injected durable operations."""

from __future__ import annotations

import inspect
from collections.abc import Callable
from typing import TypeAlias

from tigrbl_capability import Capability
from tigrbl_identity_contracts.capabilities import (
    CapabilityDefinition,
    CapabilityOperation,
)
from tigrbl_identity_contracts.digital_credentials import (
    CredentialConfiguration,
    CredentialIssuanceRequest,
    CredentialIssuanceResult,
    CredentialIssuerPort,
    CredentialOffer,
    WalletAttestationVerifierPort,
)


ConfigurationWriter: TypeAlias = Callable[[CredentialConfiguration], object]
ConfigurationReader: TypeAlias = Callable[[str], CredentialConfiguration | None]
OfferRecorder: TypeAlias = Callable[[CredentialOffer], object]
IssuanceRecorder: TypeAlias = Callable[
    [CredentialIssuanceRequest, CredentialIssuanceResult], object
]


async def _resolve(value):
    return await value if inspect.isawaitable(value) else value


class DigitalCredentialIssuanceCapability(Capability):
    def __init__(
        self,
        issuer: CredentialIssuerPort,
        configuration_writer: ConfigurationWriter,
        configuration_reader: ConfigurationReader,
        offer_recorder: OfferRecorder,
        issuance_recorder: IssuanceRecorder,
        wallet_verifier: WalletAttestationVerifierPort | None = None,
    ):
        self._issuer = issuer
        self._configuration_writer = configuration_writer
        self._configuration_reader = configuration_reader
        self._offer_recorder = offer_recorder
        self._issuance_recorder = issuance_recorder
        self._wallet_verifier = wallet_verifier
        super().__init__(
            CapabilityDefinition(
                capability_id="digital-credential.issuance",
                version="1.0",
            ),
            operations={
                "register_configuration": CapabilityOperation(
                    target=self.register_configuration,
                    delegated=True,
                ),
                "create_offer": CapabilityOperation(
                    target=self.offer,
                    delegated=True,
                ),
                "issue": CapabilityOperation(target=self.issue, delegated=True),
                "verify_wallet_attestation": CapabilityOperation(
                    target=(
                        self.verify_wallet_attestation
                        if wallet_verifier is not None
                        else None
                    ),
                    required=False,
                    delegated=True,
                ),
                "record_issuance": CapabilityOperation(
                    target=self.record_issuance,
                    delegated=True,
                ),
            },
        )

    async def register_configuration(
        self,
        configuration: CredentialConfiguration,
    ) -> object:
        if await _resolve(self._configuration_reader(configuration.identifier)):
            raise ValueError("duplicate credential configuration")
        return await _resolve(self._configuration_writer(configuration))

    async def offer(
        self,
        issuer: str,
        configuration_ids: tuple[str, ...],
    ) -> CredentialOffer:
        if not configuration_ids:
            raise ValueError("credential offer requires configurations")
        configurations = [
            await _resolve(self._configuration_reader(identifier))
            for identifier in configuration_ids
        ]
        if any(configuration is None for configuration in configurations):
            raise ValueError("credential offer references unknown configurations")
        offer = CredentialOffer(issuer, configuration_ids)
        await _resolve(self._offer_recorder(offer))
        return offer

    async def verify_wallet_attestation(self, value: str | bytes) -> bool:
        if self._wallet_verifier is None:
            raise LookupError("wallet attestation verifier is not configured")
        return bool(
            await _resolve(
                self._wallet_verifier.verify_wallet_attestation(value)
            )
        )

    async def record_issuance(
        self,
        request: CredentialIssuanceRequest,
        result: CredentialIssuanceResult,
    ) -> object:
        return await _resolve(self._issuance_recorder(request, result))

    async def issue(
        self,
        request: CredentialIssuanceRequest,
        *,
        wallet_attestation: str | bytes | None = None,
        require_wallet_attestation: bool = False,
    ) -> CredentialIssuanceResult:
        configuration = await _resolve(
            self._configuration_reader(request.configuration_id)
        )
        if configuration is None:
            raise LookupError(request.configuration_id)
        if require_wallet_attestation:
            if wallet_attestation is None:
                raise PermissionError("wallet attestation is required")
            if not await self.verify_wallet_attestation(wallet_attestation):
                raise PermissionError("wallet attestation verification failed")
        result = await _resolve(self._issuer.issue(request))
        await self.record_issuance(request, result)
        return result


__all__ = [
    "ConfigurationReader",
    "ConfigurationWriter",
    "DigitalCredentialIssuanceCapability",
    "IssuanceRecorder",
    "OfferRecorder",
]
