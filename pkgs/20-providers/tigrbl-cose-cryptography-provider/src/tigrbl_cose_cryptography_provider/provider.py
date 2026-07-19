import cbor2
from collections.abc import Mapping
from tigrbl_cose_concrete import CoseMessageKind, decode_cose_message, sig_structure
from tigrbl_identity_core import ProtectedEnvelopeKind
from tigrbl_protected_envelope_bases import ProtectedEnvelopeIssuerBase, ProtectedEnvelopeVerifierBase
from tigrbl_protected_envelope_contracts import EnvelopeProtectionRequest, EnvelopeVerificationRequest, EnvelopeVerificationResult, ProtectedEnvelope
from .signatures import verify_detached_signature
from .signing import sign_detached_signature

class CoseSign1CryptographyProvider(ProtectedEnvelopeIssuerBase, ProtectedEnvelopeVerifierBase):
    def __init__(self, private_keys: Mapping[str, object] | None = None, public_keys: Mapping[str, object] | None = None): self._private=dict(private_keys or {}); self._public=dict(public_keys or {})
    def protect(self, request: EnvelopeProtectionRequest, /) -> ProtectedEnvelope:
        headers=dict(request.protected_headers); alg=headers.get(1,headers.get("alg")); kid=headers.get(4,headers.get("kid",request.key_reference))
        if not isinstance(alg,int) or not isinstance(kid,(str,bytes)): raise ValueError("COSE Sign1 requires protected integer alg and kid")
        key_id=kid.decode() if isinstance(kid,bytes) else kid; protected=cbor2.dumps(headers,canonical=True); structure=sig_structure("Signature1",protected,request.external_aad,request.payload)
        try: key=self._private[request.key_reference]
        except KeyError as exc: raise LookupError(f"unknown COSE signing key: {request.key_reference}") from exc
        signature=sign_detached_signature(algorithm=alg,private_key=key,signing_input=structure); encoded=cbor2.dumps(cbor2.CBORTag(18,[protected,{},request.payload,signature]),canonical=True)
        return ProtectedEnvelope(ProtectedEnvelopeKind.COSE_SIGN1,encoded,headers,payload=request.payload)
    def verify(self, request: EnvelopeVerificationRequest, /) -> EnvelopeVerificationResult:
        try:
            message=decode_cose_message(bytes(request.envelope.serialization),expected_kind=CoseMessageKind.SIGN1); alg=message.protected_headers.get(1); kid=message.protected_headers.get(4)
            if not isinstance(alg,int) or not isinstance(kid,(str,bytes)): raise ValueError("COSE Sign1 protected alg and kid are required")
            key_id=kid.decode() if isinstance(kid,bytes) else kid; key=self._public[key_id]; signature=message.remaining[0]
            if not isinstance(signature,bytes) or message.payload_or_ciphertext is None: raise ValueError("invalid COSE Sign1 payload or signature")
            structure=sig_structure("Signature1",message.protected_serialized,request.external_aad,message.payload_or_ciphertext); valid=verify_detached_signature(algorithm=alg,public_key=key,signing_input=structure,signature=signature)
            return EnvelopeVerificationResult(valid,structural_valid=True,cryptographic_valid=valid,key_resolved=True,profile_valid=valid,payload=message.payload_or_ciphertext,key_reference=key_id)
        except Exception as exc: return EnvelopeVerificationResult(False,reason=str(exc))