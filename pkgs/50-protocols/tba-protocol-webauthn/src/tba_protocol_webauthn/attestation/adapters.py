"""Normalize provider-specific attestation verifier call signatures."""

from __future__ import annotations

from collections.abc import Callable

from .registry import AttestationVerifierRegistry


def build_attestation_registry(
    *,
    packed: Callable[..., object] | None = None,
    u2f: Callable[..., object] | None = None,
    tpm: Callable[..., object] | None = None,
) -> AttestationVerifierRegistry:
    registry = AttestationVerifierRegistry()
    if packed:
        registry.register(
            "packed",
            lambda value: packed(
                statement=value.statement,
                authenticator_data=value.authenticator_data,
                client_data_hash=value.client_data_hash,
                credential_public_key=value.credential_public_key,
            ),
        )
    if u2f:
        registry.register(
            "fido-u2f",
            lambda value: u2f(
                statement=value.statement,
                rp_id_hash=value.rp_id_hash,
                client_data_hash=value.client_data_hash,
                credential_id=value.credential_id,
                credential_public_key=value.credential_public_key,
            ),
        )
    if tpm:
        registry.register(
            "tpm",
            lambda value: tpm(
                statement=value.statement,
                authenticator_data=value.authenticator_data,
                client_data_hash=value.client_data_hash,
                credential_public_key=value.credential_public_key,
            ),
        )
    return registry


__all__ = ["build_attestation_registry"]
