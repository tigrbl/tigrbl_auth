from typing import Protocol


class WalletAttestationVerifierPort(Protocol):
    def verify_wallet_attestation(self, attestation: bytes | str, /) -> bool: ...


class KeyAttestationVerifierPort(Protocol):
    def verify_key_attestation(self, attestation: bytes | str, /) -> bool: ...


__all__ = ["KeyAttestationVerifierPort", "WalletAttestationVerifierPort"]
