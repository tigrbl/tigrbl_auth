from collections.abc import Mapping, Sequence
from .formats import select_format


def _validate_vcdm(payload: Mapping[object, object], artifact_kind: str) -> None:
    if "vc" in payload or "vp" in payload:
        raise ValueError("VC-JOSE-COSE prohibits legacy vc and vp JWT claims")
    context = payload.get("@context")
    types = payload.get("type")
    if not isinstance(context, Sequence) or isinstance(context, (str, bytes)):
        raise ValueError("VCDM @context is required")
    type_values = (types,) if isinstance(types, str) else tuple(types or ())
    expected = (
        "VerifiableCredential"
        if artifact_kind == "credential"
        else "VerifiablePresentation"
    )
    if expected not in type_values:
        raise ValueError(f"VCDM type must include {expected}")
    if artifact_kind == "credential":
        if "issuer" not in payload or "credentialSubject" not in payload:
            raise ValueError("secured VC requires issuer and credentialSubject")
    elif "verifiableCredential" not in payload:
        raise ValueError("secured VP requires verifiableCredential")


def validate_jose_vc(
    headers: Mapping[str, object],
    claims: Mapping[str, object],
    *,
    media_type: str = "application/vc+jwt",
) -> None:
    selected = select_format(media_type)
    if selected.envelope_family != "JOSE":
        raise ValueError("JOSE artifact requires a JOSE VC/VP media type")
    if headers.get("alg") in {None, "none"}:
        raise ValueError("JOSE VC/VP must be signed")
    expected_typ = "vc+jwt" if selected.artifact_kind == "credential" else "vp+jwt"
    if headers.get("typ") not in {None, expected_typ}:
        raise ValueError(f"unexpected JOSE typ; expected {expected_typ}")
    _validate_vcdm(claims, selected.artifact_kind)


def validate_cose_vc(
    protected_headers: Mapping[object, object],
    claims: Mapping[object, object],
    *,
    media_type: str = "application/vc+cose",
) -> None:
    selected = select_format(media_type)
    if selected.envelope_family != "COSE":
        raise ValueError("COSE artifact requires a COSE VC/VP media type")
    if 1 not in protected_headers and "alg" not in protected_headers:
        raise ValueError("COSE VC/VP protected alg is required")
    _validate_vcdm(claims, selected.artifact_kind)
