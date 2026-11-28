"""WIT-bound HTTP request proofs for draft-ietf-wimse-http-signature-08."""

from .request import authenticate_signature, sign_request

__all__ = ["authenticate_signature", "sign_request"]
