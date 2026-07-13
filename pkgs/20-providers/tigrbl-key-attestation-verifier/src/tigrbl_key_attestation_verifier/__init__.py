from collections.abc import Callable, Mapping

from tigrbl_identity_contracts.digital_credentials import KeyAttestationVerifierPort

KeyAttestationBackend = Callable[[bytes | str, str], Mapping[str, object]]


class ProfiledKeyAttestationVerifier(KeyAttestationVerifierPort):
    def __init__(
        self,
        backend: KeyAttestationBackend,
        profile: str,
        expected_key_id: str,
        expected_challenge: str,
        allowed_protections: set[str] | None = None,
    ):
        self._backend = backend
        self._profile = profile
        self._key_id = expected_key_id
        self._challenge = expected_challenge
        self._protections = set(
            allowed_protections or {"hardware", "tee", "secure-element"}
        )

    def verify_key_attestation(self, attestation: bytes | str, /) -> bool:
        try:
            claims = self._backend(attestation, self._profile)
        except (TypeError, ValueError):
            return False
        return (
            claims.get("profile") == self._profile
            and claims.get("key_id") == self._key_id
            and claims.get("challenge") == self._challenge
            and claims.get("key_protection") in self._protections
            and claims.get("verified_boot") is not False
        )


__all__ = ["KeyAttestationBackend", "ProfiledKeyAttestationVerifier"]
