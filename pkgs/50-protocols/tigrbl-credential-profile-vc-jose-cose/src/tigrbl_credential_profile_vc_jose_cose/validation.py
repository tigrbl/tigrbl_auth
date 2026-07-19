from collections.abc import Mapping
from .formats import select_format

def validate_jose_vc(headers: Mapping[str, object], claims: Mapping[str, object], *, media_type: str = "application/vc+jwt") -> None:
    selected = select_format(media_type)
    if selected.envelope_family != "JOSE": raise ValueError("JOSE artifact requires a JOSE VC/VP media type")
    if headers.get("alg") in {None, "none"}: raise ValueError("JOSE VC/VP must be signed")
    if selected.artifact_kind == "credential" and not ({"vc", "credentialSubject"} & claims.keys()): raise ValueError("secured VC payload is missing credential semantics")
    if selected.artifact_kind == "presentation" and not ({"vp", "verifiableCredential"} & claims.keys()): raise ValueError("secured VP payload is missing presentation semantics")

def validate_cose_vc(protected_headers: Mapping[object, object], claims: Mapping[object, object], *, media_type: str = "application/vc+cose") -> None:
    selected = select_format(media_type)
    if selected.envelope_family != "COSE": raise ValueError("COSE artifact requires a COSE VC/VP media type")
    if 1 not in protected_headers and "alg" not in protected_headers: raise ValueError("COSE VC/VP protected alg is required")
    if selected.artifact_kind == "credential" and not claims: raise ValueError("secured VC payload is empty")