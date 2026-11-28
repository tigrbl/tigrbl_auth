"""Opt-in RFC 8037 X448 policy for compact direct-agreement JWE."""

from collections.abc import Mapping
from typing import Any

from tba_bases_encryption import CipherPolicyDomainBase
from tba_contracts_security_trust import CapabilityMap, KeyRefLike, NormalizedDescriptor


class JweCipherPolicy(CipherPolicyDomainBase):
    """Allow ECDH-ES/A256GCM with an OKP/X448 recipient key."""

    def suite_id(self) -> str:
        return "jwe-x448"

    def supports(self) -> CapabilityMap:
        return CapabilityMap(ops={"key_agreement": ("ECDH-ES",)})

    def default_alg(self, op: str, *, for_key: KeyRefLike | None = None) -> str:
        if op != "key_agreement":
            raise ValueError(f"unsupported JWE cipher policy operation: {op}")
        return "ECDH-ES"

    def policy(self) -> Mapping[str, Any]:
        return {"kty": "OKP", "crv": "X448", "enc": "A256GCM"}

    def features(self) -> Mapping[str, Any]:
        return {
            "suite": self.suite_id(),
            "ops": self.supports().ops,
            "constraints": self.policy(),
        }

    def normalize(
        self,
        *,
        op: str,
        alg: str | None = None,
        key: KeyRefLike | None = None,
        params: Mapping[str, Any] | None = None,
        dialect: str | None = None,
    ) -> NormalizedDescriptor:
        default = self.default_alg(op)
        chosen = default if alg is None else alg
        if chosen != default or dialect not in {None, "jwa"}:
            raise ValueError("X448 JWE policy requires ECDH-ES in the JWA dialect")
        if not isinstance(key, Mapping) or (key.get("kty"), key.get("crv")) != (
            "OKP",
            "X448",
        ):
            raise ValueError("ECDH-ES policy requires an OKP/X448 key")
        resolved = dict(params or {})
        if resolved.setdefault("enc", "A256GCM") != "A256GCM":
            raise ValueError("X448 requires A256GCM")
        if resolved.setdefault("crv", "X448") != "X448":
            raise ValueError("ECDH-ES policy requires X448")
        return NormalizedDescriptor(
            op=op,
            alg=chosen,
            dialect="jwa",
            mapped={"jwa": chosen},
            params=resolved,
            policy=self.policy(),
        )
