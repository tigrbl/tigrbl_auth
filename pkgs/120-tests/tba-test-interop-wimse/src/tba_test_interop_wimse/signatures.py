"""Compatibility imports for the relocated WIMSE request signature profile."""

from tba_profile_workload_proof_wimse_http_signature import authenticate_signature, sign_request
from tba_profile_workload_proof_wimse_http_signature.request import ATTRIBUTE, PARAMS, normalize

__all__ = ["ATTRIBUTE", "PARAMS", "authenticate_signature", "normalize", "sign_request"]
